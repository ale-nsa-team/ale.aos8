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

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.argspec.port_security.port_security import (
    Port_securityArgs,
)


class Port_securityFacts(object):
    """The AOS8 Port Security fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Port_securityArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_port_security_data(self, connection):
        cmd = 'show configuration snapshot | grep "port-security"'
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
            data = self.get_port_security_data(connection)
            objs = self.parse_port_security(data)

        facts = {}
        if objs:
            facts["port_security"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})

            for cfg in params["config"]:
                facts["port_security"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def parse_port_security(self, data):
        ports = []
        ports_obj = []
        objs = []


        # operate on a collection of resource x
        config = data.split("\n")

        for conf in config:
            isport = re.match("^port-security\sport\s(?P<port_number>[a-zA-Z0-9\/]+)\s", conf)
            if isport:
                port_number = isport.group('port_number')
                if port_number not in ports: # catch unique port_number
                    ports.append(port_number)
                    port_obj = {
                        'port_number' : port_number
                    }                    
                    reg_exp = port_number.replace("/", "\/")
                    for eachline in config:
                        mac = re.match("^port-security\sport\s(" + reg_exp + ")\smac\s(?P<address>[a-fA-F0-9:]+)\svlan\s(?P<vlan_id>(\d+))", eachline)
                        max_filtering = re.match("^port-security\sport\s(" + reg_exp + ")\smax-filtering\s(?P<filtering>(\w)+)",eachline)
                        violation = re.match("^port-security\sport\s(" + reg_exp + ")\sviolation\s(?P<violation>(\w)+)",eachline)
                        state = re.match("^port-security\sport\s(" + reg_exp + ")\sadmin-state\s(?P<state>(\w)+)",eachline)
                        if mac:
                            mac_address = {
                                "address" : mac.group('address'),
                                "vlan" : mac.group('vlan_id'),
                            }
                            port_obj['mac'] = mac_address                        
                        if max_filtering:
                            port_obj['max-filtering'] = max_filtering.group('filtering')                        
                        if violation:
                            port_obj['violation'] = violation.group('violation')
                        if state:
                            port_obj['state'] = state.group('state')                            

                    ports_obj.append(port_obj)    

        members_obj = {
            'port'          :   ports_obj,
        }
        objs.append(members_obj)      
        return objs