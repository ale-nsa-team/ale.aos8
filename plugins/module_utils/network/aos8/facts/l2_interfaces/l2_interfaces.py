#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The aos8 vlans fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.argspec.l2_interfaces.l2_interfaces import (
    L2_interfacesArgs,
)


class L2_interfacesFacts(object):
    """The aos vlans fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = L2_interfacesArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_l2_interface_date(self, connection):
        cmd = "show vlan members"
        return connection.get(cmd)

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for vlans
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        objs = []

        if not data:
            data = self.get_l2_interface_date(connection)
            objs = self.parse_l2_interfaces(data)

        facts = {}
        if objs:
            facts["l2_interfaces"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})

            for cfg in params["config"]:
                facts["l2_interfaces"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def parse_l2_interfaces(self, data):
        objs = []

        # operate on a collection of resource x
        config = data.split("\n")
        # Get individual vlan configs separately
        for conf in config:
            match = re.match("^^\s+(?P<vlan_id>[\d]+)\s+(?P<port_number>(\d+\/\S+))\s+(?P<port_type>untagged|tagged)\s+(?P<status>.*)$", conf)
            if match:
                port_number = match.group('port_number')
                if re.match('(\d)+\/(\d)+\/(\d)+', port_number):
                    port_type = 'port'
                else:
                    port_type = 'linkagg'
                members_obj = {
                    'vlan_id' : match.group('vlan_id'),
                    'port_number' : match.group('port_number'), 
                    'mode' : match.group('port_type'),
                    'port_type' : port_type,
                }
                objs.append(members_obj)

        return objs