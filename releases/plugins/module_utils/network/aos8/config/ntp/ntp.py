#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos_ntp config file.
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

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.rm_templates.Ntp_Template import Ntp_Template



class Ntp(ResourceModule):
    """
    The aos_ntp config class
    
    """

    def __init__(self, module):
        super(Ntp, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ntp",
            tmplt=Ntp_Template(),
        )
        self.parsers = [
            "authenticate",
            "local_interface",
            "qos_dscp",
            "trusted_key",
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
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = {"ntp": self.want}
        haved = {"ntp": self.have}
        # turn all lists of dicts into dicts prior to merge
        for entry in wantd["ntp"], haved["ntp"]:
            self._ntp_list_to_dict(entry)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            wantd = {}
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the  network resource.
        """
        
        self._servers_compare(want=want, have=have)
        add_cmd = []
        del_cmd = []
        if self.commands:
            for cmd in self.commands:
                if "no ntp" in cmd:
                    del_cmd.append(cmd)
                else:
                    add_cmd.append(cmd)
            self.commands = del_cmd + add_cmd

    def _servers_compare(self, want, have):
        w = want.pop("servers", {})
        h = have.pop("servers", {})
        for name, entry in iteritems(w):
            if h.get(name):
                h_key = {"servers": h.pop(name)}
            self.compare(
                parsers="servers",
                want={"servers": entry},
                have=h_key,
            )
        for name, entry in iteritems(h):
            self.compare(parsers="servers", want={}, have={"servers": entry})


    def _ntp_list_to_dict(self, entry):
        if "servers" in entry:
            server_dict = {}
            for el in entry["servers"]:
                server_dict.update({el["server"]: el})
            entry["servers"] = server_dict

