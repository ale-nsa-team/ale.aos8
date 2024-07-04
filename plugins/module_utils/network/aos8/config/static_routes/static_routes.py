# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING ou https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The aos8_static_routes class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import ConfigBase
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import remove_empties
from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.facts.facts import Facts


class Static_routes(ConfigBase):
    """
    The aos8_static_routes class
    """

    gather_subset = ["!all", "!min"]
    gather_network_resources = ["static_routes"]

    def __init__(self, module):
        super(Static_routes, self).__init__(module)
        self.config = module.params['config']

    def get_static_routes_facts(self, data=None):
        """Get the 'facts' (the current configuration)
        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset,
            self.gather_network_resources,
            data=data,
        )
        static_routes_facts = facts["ansible_network_resources"].get(
            "static_routes",
        )
        if not static_routes_facts:
            return []
        return static_routes_facts

    def execute_module(self):
        """Execute the module
        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        warnings = list()
        commands = list()
        if self.state in self.ACTION_STATES:
            existing_static_routes_facts = self.get_static_routes_facts()
        else:
            existing_static_routes_facts = []

        if self.state in self.ACTION_STATES or self.state == "rendered":
            commands.extend(self.set_config(existing_static_routes_facts))

        if commands and self.state in self.ACTION_STATES:
            if not self._module.check_mode:
                self._connection.edit_config(commands)
            result["changed"] = True
        if self.state in self.ACTION_STATES:
            result["commands"] = commands
        if self.state in self.ACTION_STATES or self.state == "gathered":
            changed_static_routes_facts = self.get_static_routes_facts()
        elif self.state == "rendered":
            result["rendered"] = commands
        elif self.state == "parsed":
            if not self._module.params["running_config"]:
                self._module.fail_json(
                    msg="Value of running_config parameter must not be empty for state parsed",
                )
            result["parsed"] = self.get_static_routes_facts(
                data=self._module.params["running_config"],
            )
        else:
            changed_static_routes_facts = []

        if self.state in self.ACTION_STATES:
            result["before"] = existing_static_routes_facts
            if result["changed"]:
                result["after"] = changed_static_routes_facts
        elif self.state == "gathered":
            result["gathered"] = changed_static_routes_facts

        result["warnings"] = warnings
        return result

    def set_config(self, existing_static_routes_facts):
        """Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []
        onbox_configs = []
        for h in existing_static_routes_facts:
            return_command = add_commands(h)
            for command in return_command:
                onbox_configs.append(command)
        config = self._module.params.get("config")
        want = []
        if config:
            for w in config:
                want.append(remove_empties(w))
        have = existing_static_routes_facts
        resp = self.set_state(want, have)
        for want_config in resp:
            if want_config not in onbox_configs:
                commands.append(want_config)
        return commands

    def set_state(self, want, have):
        """Select the appropriate function based on the state provided
        :param want: the desired configuration as a dictionary
        :param have: the current configuration as a dictionary
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []
        if self.state in ("merged", "replaced", "overridden") and not want:
            self._module.fail_json(
                msg="value of config parameter must not be empty for state {0}".format(
                    self.state,
                ),
            )
        state = self._module.params["state"]
        if state == "overridden":
            commands = self._state_overridden(want, have)
        elif state == "deleted":
            commands = self._state_deleted(want, have)
        elif state == "merged" or self.state == "rendered":
            commands = self._state_merged(want, have)
        elif state == "replaced":
            commands = self._state_replaced(want, have)
        return commands

    @staticmethod
    def _state_replaced(want, have):
        """The command generator when state is replaced
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []
        haveconfigs = []
        dest = get_dest(want)
        for h in have:
            return_command = add_commands(h)
            for command in return_command:
                for d in dest:
                    if d in command:
                        haveconfigs.append(command)
        wantconfigs = set_commands(want, have)
        removeconfigs = list(set(haveconfigs) - set(wantconfigs))
        for command in removeconfigs:
            commands.append("no " + command)
        for wantcmd in wantconfigs:
            commands.append(wantcmd)
        return commands

    @staticmethod
    def _state_overridden(want, have):
        """The command generator when state is overridden
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []
        haveconfigs = []
        for h in have:
            return_command = add_commands(h)
            for command in return_command:
                haveconfigs.append(command)
        wantconfigs = set_commands(want, have)
        idempotentconfigs = list(set(haveconfigs) - set(wantconfigs))
        if not idempotentconfigs:
            return idempotentconfigs
        removeconfigs = list(set(haveconfigs) - set(wantconfigs))
        for command in removeconfigs:
            commands.append("no " + command)
        for wantcmd in wantconfigs:
            commands.append(wantcmd)
        return commands

    @staticmethod
    def _state_merged(want, have):
        """The command generator when state is merged
        :rtype: A list
        :returns: the commands necessary to merge the provided into
                  the current configuration
        """
        return set_commands(want, have)

    @staticmethod
    def _state_deleted(want, have):
        """The command generator when state is deleted
        :rtype: A list
        :returns: the commands necessary to remove the current configuration
                  of the provided objects
        """
        commands = []
        if not want:
            for h in have:
                return_command = add_commands(h)
                for command in return_command:
                    command = "no " + command
                    commands.append(command)
        else:
            for w in want:
                return_command = del_commands(w, have)
                for command in return_command:
                    commands.append(command)
        return commands


def set_commands(want, have):
    commands = []
    for w in want:
        return_command = add_commands(w)
        for command in return_command:
            commands.append(command)
    return commands


def add_commands(want):
    commandset = []
    if not want:
        return commandset

    if 'address_families' not in want:
        print("No address_families found in want")
        return commandset

    for af in want["address_families"]:
        if 'routes' not in af:
            print("No routes found in address_families")
            continue

        for route in af["routes"]:
            commands = []
            commands.append("ip static-route " + route["dest"])
            next_hop = route["next_hops"][0]
            commands.append(" gateway " + next_hop["forward_router_address"])
            if "admin_distance" in next_hop:
                commands.append(" metric " + str(next_hop["admin_distance"]))
            if "description" in next_hop:
                commands.append(" name \"" + next_hop["description"] + "\"")
            if "tag" in next_hop:
                commands.append(" tag " + str(next_hop["tag"]))

            config_commands = "".join(commands)
            commandset.append(config_commands)

            # Ajoutez cette ligne pour déboguer les commandes générées
            print("Generated command: ", config_commands)
    
    return commandset



def del_commands(want, have):
    commandset = []
    haveconfigs = []
    for h in have:
        return_command = add_commands(h)
        for command in return_command:
            command = "no " + command
            haveconfigs.append(command)
    if want is None:
        commandset = haveconfigs
    else:
        for w in want:
            for h in have:
                if w["ip_address"] == h["ip_address"]:
                    return_command = add_commands(w)
                    for command in return_command:
                        command = "no " + command
                        commandset.append(command)
    return commandset


def get_dest(config):
    dest = []
    for c in config:
        if 'routes' in c:
            for route in c["routes"]:
                dest.append(route["ip_address"])
    return dest

