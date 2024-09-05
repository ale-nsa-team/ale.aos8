#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ale_ospf class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base import ConfigBase
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import dict_diff, remove_empties, to_list
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.facts import Facts

class Ospfv2(ConfigBase):
    """
    The ale_aos8_ospv2 class
    """

    gather_subset = ["!all", "!min"]
    gather_network_resources = ["ospfv2"]

    def __init__(self, module):
        super(Ospfv2, self).__init__(module)

    def get_ospfv2_facts(self, data=None):
        """Get the 'facts' (the current configuration)

        :rtype: A dictionary
        :returns: The current configuration as a dictionary
        """
        facts, _warnings = Facts(self._module).get_facts(
            self.gather_subset,
            self.gather_network_resources,
            data=data,
        )

        ospfv2_facts = facts["ansible_network_resources"].get("ospfv2")
        if not ospfv2_facts:
            return []
        return ospfv2_facts

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        result = {"changed": False}
        warnings = list()
        commands = list()

        if self.state in self.ACTION_STATES:
            existing_ospfv2_facts = self.get_ospfv2_facts()
        else:
            existing_ospfv2_facts = []
        if self.state in self.ACTION_STATES or self.state == "rendered":
            commands.extend(self.set_config(existing_ospfv2_facts))
        if commands and self.state in self.ACTION_STATES:
            if not self._module.check_mode:
                self._connection.edit_config(commands)
            result["changed"] = True
        if self.state in self.ACTION_STATES:
            result["commands"] = commands
        if self.state in self.ACTION_STATES or self.state == "gathered":
            changed_ospfv2_facts = self.get_ospfv2_facts()
        elif self.state == "rendered":
            result["rendered"] = commands
        elif self.state == "parsed":
            if not self._module.params["running_config"]:
                self._module.fail_json(
                    msg="value of running_config parameter must not be empty for state parsed",
                )
            result["parsed"] = self.get_ospfv2_facts(
                data=self._module.params["running_config"],
            )
        else:
            changed_ospfv2_facts = self.get_ospfv2_facts()
        if self.state in self.ACTION_STATES:
            result["before"] = existing_ospfv2_facts
            if result["changed"]:
                result["after"] = changed_ospfv2_facts
        elif self.state == "gathered":
            result["gathered"] = changed_ospfv2_facts

        result["warnings"] = warnings
        return result

    def set_config(self, existing_ospfv2_facts):
        """Collect the configuration from the args passed to the module,
            collect the current configuration (as a dict from facts)

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        want = self._module.params["config"]
        have = existing_ospfv2_facts
        return self.set_state(want, have)

    def set_state(self, want, have):
        """Select the appropriate function based on the state provided

        :param want: the desired configuration as a dictionary
        :param have: the current configuration as a dictionary
        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        if self.state in ("merged", "replaced", "overridden", "rendered") and not want:
            self._module.fail_json(
                msg="value of config parameter must not be empty for state {0}".format(
                    self.state,
                ),
            )
        if self.state == "overridden":
            return self._state_overridden(want, have)
        elif self.state == "deleted":
            return self._state_deleted(want, have)
        elif self.state == "merged" or self.state == "rendered":
            return self._state_merged(want, have)
        elif self.state == "replaced":
            return self._state_replaced(want, have)
        return []

    def _state_replaced(self, want, have):
        """The command generator when state is replaced

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        commands = self.del_commands(have, want)
        commands.extend(self.add_commands(want, have))
        return commands

    def _state_overridden(self, want, have):
        """The command generator when state is overridden

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        return self._state_replaced(want, have)

    def _state_merged(self, want, have):
        """The command generator when state is merged

        :rtype: A list
        :returns: the commands necessary to merge the provided into
                  the current configuration
        """
        return self.set_commands(want, have)

    def _state_deleted(self, want, have):
        """The command generator when state is deleted

        :rtype: A list
        :returns: the commands necessary to remove the current configuration
                  of the provided objects
        """
        return self.del_commands(want, have)

    def set_commands(self, want, have):
        commands = []
        if have:
            diff = self.compare_dicts(want, have)
            commands.extend(self.add_commands(diff, have))
        else:
            commands.extend(self.add_commands(want, have))
        return commands

    def compare_dicts(self, want_inst, have_inst):
        want_dict = remove_empties(want_inst)
        have = have_inst
        diff_dict = {}
        for w_key, w_value in want_dict.items():
            if w_key not in have or have[w_key] != w_value:
                diff_dict[w_key] = w_value
        return diff_dict

    def add_commands(self, want, have):
        commands = []
        if not want:
            return commands
        for ospf_params in to_list(want):
            if "load" in ospf_params:
                commands.append("ip load ospf " + ospf_params["load"])
            if "areas" in ospf_params:
                for area in ospf_params["areas"]:
                    commands.append("ip ospf area " + area["area_id"])
            if "interfaces" in ospf_params:
                for interface in ospf_params["interfaces"]:
                    commands.append("ip ospf interface " + interface["interface"])
                    if "admin_state" in interface:
                        commands.append("ip ospf interface " + interface["interface"] + " admin-state " + interface["admin_state"])
                    if "area" in interface:
                        commands.append("ip ospf interface " + interface["interface"] + " area " + interface["area"])
            if "admin_state" in ospf_params:
                commands.append("ip ospf admin-state " + ospf_params["admin_state"])
        return commands

    def del_commands(self, want, have):
        commands = []
        if not want:
            return commands
        for ospf_params in to_list(want):
            if "load" in ospf_params:
                commands.append("no ip load ospf " + ospf_params["load"])
            if "areas" in ospf_params:
                for area in ospf_params["areas"]:
                    commands.append("no ip ospf area " + area["area_id"])
            if "interfaces" in ospf_params:
                for interface in ospf_params["interfaces"]:
                    commands.append("no ip ospf interface " + interface["interface"])
                    if "admin_state" in interface:
                        commands.append("no ip ospf interface " + interface["interface"] + " admin-state " + interface["admin_state"])
                    if "area" in interface:
                        commands.append("no ip ospf interface " + interface["interface"] + " area " + interface["area"])
            if "admin_state" in ospf_params:
                commands.append("no ip ospf admin-state " + ospf_params["admin_state"])
        return commands
