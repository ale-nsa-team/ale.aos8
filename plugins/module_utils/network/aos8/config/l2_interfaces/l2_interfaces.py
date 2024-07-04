#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The aos8_l2_interfaces class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from __future__ import absolute_import, division, print_function

import re

__metaclass__ = type


from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import (
    ConfigBase,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    remove_empties,
    to_list,
)

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.facts.facts import Facts
from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.utils.utils import dict_to_set


class L2_interfaces(ConfigBase):
    """
    The aos8_l2_interfaces class
    """
    gather_subset = ["!all", "!min"]
    gather_network_resources = ["l2_interfaces"]

    def __init__(self, module):
        super(L2_interfaces, self).__init__(module)

    def get_l2_interfaces_facts(self, data=None):
        """Get the 'facts' (the current configuration)
        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset,
            self.gather_network_resources,
            data=data,
        )
        l2_interfaces_facts = facts["ansible_network_resources"].get("l2_interfaces")
        if not l2_interfaces_facts:
            return []
        return l2_interfaces_facts

    def execute_module(self):
        """Execute the module
        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        commands = list()
        warnings = list()
        self.have_now = list()

        # if state in ACTION_STATES, get interface facts from device
        if self.state in self.ACTION_STATES:
            existing_l2_interfaces_facts = self.get_l2_interfaces_facts()
        else:
            existing_l2_interfaces_facts = []

        # if state in ACTION_STATES, generate commands to device or rendered commands
        if self.state in self.ACTION_STATES or self.state == "rendered":
            commands.extend(self.set_config(existing_l2_interfaces_facts))

        # if state in ACTION_STATES, commands generated and check_mode false, send command to device            
        if commands and self.state in self.ACTION_STATES:
            if not self._module.check_mode:              
                self._connection.edit_config(commands)
            result["changed"] = True
        if self.state in self.ACTION_STATES:
            result["commands"] = commands

        if self.state in self.ACTION_STATES or self.state == "gathered":
            changed_l2_interfaces_facts = self.get_l2_interfaces_facts()
        elif self.state == "rendered":
            result["rendered"] = commands
        elif self.state == "parsed":
            running_config = self._module.params["running_config"]
            if not running_config:
                self._module.fail_json(
                    msg="value of running_config parameter must not be empty for state parsed",
                )
            result["parsed"] = self.get_l2_interfaces_facts(data=running_config)
        else:
            changed_l2_interfaces_facts = []

        if self.state in self.ACTION_STATES:
            result["before"] = existing_l2_interfaces_facts
            if result["changed"]:
                result["after"] = changed_l2_interfaces_facts
        elif self.state == "gathered":
            result["gathered"] = changed_l2_interfaces_facts

        result["warnings"] = warnings
        return result

    def set_config(self, existing_l2_interfaces_facts):
        """Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = []
        if self._module.params.get("config"):
            for cfg in self._module.params["config"]:
                want.append(remove_empties(cfg))
        have = existing_l2_interfaces_facts
        resp = self.set_state(want, have)
        return to_list(resp)

    def set_state(self, want, have):
        """Select the appropriate function based on the state provided

        :param want: the desired configuration as a dictionary
        :param have: the current configuration as a dictionary
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """

        if self.state in ("overridden", "merged", "replaced", "rendered") and not want:
            self._module.fail_json(
                msg="value of config parameter must not be empty for state {0}".format(
                    self.state,
                ),
            )

        if self.state == "overridden":
            commands = self._state_overridden(want, have)
        elif self.state == "deleted":
            commands = self._state_deleted(want, have)
        elif self.state in ("merged", "rendered"):
            commands = self._state_merged(want, have)
        elif self.state == "replaced":
            commands = self._state_replaced(want, have)
            pass            
        return commands

    def _state_replaced(self, want, have):
        """The command generator when state is replaced

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []

        check = False
        for each in want:
            for every in have:
                if every == each :
                    check = True
                    break
                continue
            if check:
                commands.extend(self._set_config(each, every))
            else:
                commands.extend(self._set_config(each, dict()))

        return commands

    def _state_overridden(self, want, have):
        """The command generator when state is overridden

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = []

        want_local = want
        self.have_now = have.copy()
        for each in have:
            count = 0
            for every in want_local:
                if each == every:
                    break
                count += 1
            else:
                # We didn't find a matching desired state, which means we can
                # pretend we received an empty desired state.
                commands.extend(self._clear_config(every, each))
                continue
            commands.extend(self._set_config(every, each))
            # as the pre-existing L2 Interface are now configured by
            # above set_config call, deleting the respective
            # L2 Interface entry from the want_local list
            del want_local[count]

        # Iterating through want_local list which now only have new L2 Interfaces to be
        # configured
        for each in want_local:
            commands.extend(self._set_config(each, dict()))

        return commands

    def _state_merged(self, want, have):
        """The command generator when state is merged

        :rtype: A list
        :returns: the commands necessary to merge the provided into
                  the current configuration
        """
        commands = []

        check = False             
        for each in want:
            for every in have:
                if each == every:
                    check = True
                    break
                continue
            if check:
                commands.extend(self._set_config(each, every))
            else:
                commands.extend(self._set_config(each, dict()))

        return commands

    def _state_deleted(self, want, have):
        """The command generator when state is deleted

        :rtype: A list
        :returns: the commands necessary to remove the current configuration
                  of the provided objects
        """
        commands = []

        if want:
            check = False
            for each in want:
                for every in have:
                    if each == every:
                        check = True
                        break
                    check = False
                    continue
                if check:
                    commands.extend(self._clear_config(each, every))
        else:
            for each in have:
                commands.extend(self._clear_config(dict(), each))

        return commands


    def _set_config(self, want, have):
        # Set the L2 Interface config based on the want and have config
        # vlan 10 members port 1/1/1 tagged
        # vlan 10 members port 1/1/1 untagged

        commands = []
        port_number = dict(want).get("port_number")

        # Get the diff b/w want n have
        want_dict = dict_to_set(want, sort_dictionary=True)
        have_dict = dict_to_set(have, sort_dictionary=True)
        diff = want_dict - have_dict

        if diff:
            port_type = dict(want).get("port_type")
            vlan_id = dict(want).get("vlan_id")
            mode = dict(want).get("mode")

            if port_type:
                if re.match('(\d)+\/(\d)+\/(\d)+', port_number):
                    port_type_attr = 'port'
                else:
                    port_type_attr = 'linkagg'
            commands.append("vlan " + str(vlan_id) + " members " + port_type_attr + " " + port_number + " " + mode)

        return commands

    def _clear_config(self, want, have):
        # Delete the L2 Interface config based on the want and have config
        commands = []
        port_number = dict(have).get("port_number")
        port_type = dict(have).get("port_type")
        vlan_id = dict(have).get("vlan_id")
        mode = dict(have).get("mode")        
        if port_type:
            if re.match('(\d)+\/(\d)+\/(\d)+', port_number):
                port_type_attr = 'port'
            else:
                port_type_attr = 'linkagg'        

        if (
            have.get("port_number")
            and (have.get("port_number") != want.get("port_number") 
            or self.state == "deleted")
        ):
            commands.append("no vlan " + str(vlan_id) + " members " + port_type_attr + " " + port_number)
            if self.state == "overridden":
                self.have_now.remove(have)
        return commands
