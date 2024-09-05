#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The aos8_hostname config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.facts import (
    Facts,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.rm_templates.hostname import (
    HostnameTemplate,
)


class Hostname(ResourceModule):
    """
    The aos8_hostname config class
    """

    def __init__(self, module):
        super(Hostname, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="hostname",
            tmplt=HostnameTemplate(),
        )
        self.parsers = ["hostname"]

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
            want, have and desired state.
        """
        wantd = self.want
        haved = self.have

        if self.state == "deleted":
            wantd = { 'hostname' : 'changeme'}

        self._compare(want=wantd, have=haved)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Hostname network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)
