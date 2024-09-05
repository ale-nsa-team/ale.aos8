# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The aos8_bgp config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.facts import Facts
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.rm_templates.Bgp_Template import (
    Bgp_Template,
)

class Bgp(ResourceModule):
    """
    The aos8_bgp config class
    """

    def __init__(self, module):
        super(Bgp, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bgp",
            tmplt=Bgp_Template(),
        )
        self.parsers = [
            "as_number",
            "bgp_admin_state",
            "neighbor_address",
            "neighbor_remote_as",
            "neighbor_admin_state",
        ]

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on want, have and desired state."""
        wantd = {}
        haved = {}

        if self.want.get("as_number") == self.have.get("as_number") or not self.have:
            if self.want:
                wantd = {self.want["as_number"]: self.want}
            if self.have:
                haved = {self.have["as_number"]: self.have}
        else:
            self._module.fail_json(
                msg="Only one BGP instance is allowed per device",
            )

        # Convert all lists of dicts into dicts prior to merge
        for entry in wantd, haved:
            self._bgp_list_to_dict(entry)

        # If state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # If state is deleted, empty out wantd and set haved to wantd
        if self.state in ["deleted", "purged"]:
            h_del = {}
            for k, v in iteritems(haved):
                if k in wantd or not wantd:
                    h_del.update({k: v})
            wantd = {}
            haved = h_del

        if self.state == "deleted":
            self._compare(want={}, have=self.have)

        if self.state == "purged":
            for num, entry in iteritems(haved):
                self.commands.append(
                    self._tmplt.setval({"as_number": num}, "bgp_autonomous_system"),
                )

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Bgp network resource.
        """
        self._compare_neighbor(want, have)
        self._compare_bgp_params(want, have)
        for name, entry in iteritems(want):
            if name != "as_number":
                self.compare(
                    parsers=self.parsers,
                    want={name: entry},
                    have={name: have.pop(name, {})},
                )
        for name, entry in iteritems(have):
            if name != "as_number":
                self.compare(
                    parsers=self.parsers,
                    want={},
                    have={name: have.get(name)},
                )

        if self.commands and "router bgp" not in self.commands[0]:
            self.commands.insert(
                0,
                self._tmplt.render(want or have, "router", False),
            )

    def _compare_bgp_params(self, want, have):
        """Compare BGP parameters."""
        parsers = [
            "bgp_admin_state",
            "as_number",
        ]
        wbgp = want.pop("bgp_params", {})
        hbgp = have.pop("bgp_params", {})
        for name, entry in iteritems(wbgp):
            self.compare(
                parsers=parsers,
                want={"bgp_params": {name: entry}},
                have={"bgp_params": {name: hbgp.pop(name, {})}},
            )
        for name, entry in iteritems(hbgp):
            self.compare(
                parsers=parsers,
                want={},
                have={"bgp_params": {name: entry}},
            )

    def _compare_neighbor(self, want, have):
        parsers = [
            "neighbor_address",
            "neighbor_remote_as",
            "neighbor_admin_state",
        ]
        wneigh = want.pop("neighbor", {})
        hneigh = have.pop("neighbor", {})
        for name, entry in iteritems(wneigh):
            peer = entry.get("neighbor_address")
            for k, v in entry.items():
                if k == "neighbor_address":
                    continue
                if hneigh.get(name):
                    h = {"neighbor_address": peer, k: hneigh[name].pop(k, {})}
                else:
                    h = {}
                self.compare(
                    parsers=parsers,
                    want={"neighbor": {"neighbor_address": peer, k: v}},
                    have={"neighbor": h},
                )
        for name, entry in iteritems(hneigh):
            if name not in wneigh.keys():
                self.commands.append("no ip bgp neighbor " + name)
                continue
            for k, v in entry.items():
                self.compare(
                    parsers=parsers,
                    want={},
                    have={"neighbor": {"neighbor_address": name, k: v}},
                )

    def _bgp_list_to_dict(self, entry):
        for name, proc in iteritems(entry):
            if "neighbor" in proc:
                neigh_dict = {}
                for entry in proc.get("neighbor", []):
                    peer = entry.get("neighbor_address")
                    neigh_dict.update({peer: entry})
                proc["neighbor"] = neigh_dict
