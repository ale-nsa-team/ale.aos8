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

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.argspec.l3_interfaces.l3_interfaces import (
    L3_interfacesArgs,
)


class L3_interfacesFacts(object):
    """The AOS8 IP interface fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = L3_interfacesArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_l3_interface_date(self, connection):
        cmd = 'show configuration snapshot | grep "ip interface"'
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
            data = self.get_l3_interface_date(connection)
            objs = self.parse_l3_interfaces(data)

        facts = {}
        if objs:
            facts["l3_interfaces"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})

            for cfg in params["config"]:
                facts["l3_interfaces"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def parse_l3_interfaces(self, data):
        objs = []

        # operate on a collection of resource x
        config = data.split("\n")
        # Get individual IP Interface configs separately
        for conf in config:
            # Is VRF IP Interface
            if (re.match("^vrf\s(.*)\sip", conf)):
                match = re.match("^vrf\s(?P<vrfname>(([a-zA-Z]+)(\W)?([a-zA-Z]+)))\sip\sinterface\s\"(?P<name>.*)\"\saddress\s(?P<address>[\d.]+)\smask\s(?P<mask>[\d.]+)\s(?P<type>(vlan|tunnel|rtr-port))\s(?P<port_id>[\d]+)", conf)
                if match:
                    members_obj = {
                        'vrf'       :   match.group('vrfname'),
                        'name'      :   match.group('name'),
                        'address'   :   match.group('address'),   
                        'mask'      :   match.group('mask'),
                        'type'      :   match.group('type'),
                        'port_id'   :   match.group('port_id'),
                    }
                    objs.append(members_obj)                   
                pass
            
            elif (re.match("^ip\sinterface\s",conf)):
                            
                # Loopback interface
                if(re.match("ip\sinterface\s\"Loopback",conf)):
                    match = re.match("^ip\sinterface\s\"(?P<name>(Loopback[\d]+))\"\saddress\s(?P<address>[\d.]+)",conf)
                    if match:
                        members_obj = {
                            'name'      :   match.group('name'),
                            'address'   :   match.group('address'),                             
                        }
                        objs.append(members_obj)          
                else:            
                    match = re.match("^ip\sinterface\s\"(?P<name>.*)\"\saddress\s(?P<address>[\d.]+)\smask\s(?P<mask>[\d.]+)\s(?P<type>(vlan|tunnel|rtr-port))\s(?P<port_id>[\d]+)", conf)
                    if match:
                        members_obj = {
                            'name'      :   match.group('name'),
                            'address'   :   match.group('address'),   
                            'mask'      :   match.group('mask'),
                            'type'      :   match.group('type'),
                            'port_id'   :   match.group('port_id'),
                        }
                        objs.append(members_obj)                     
                
        return objs