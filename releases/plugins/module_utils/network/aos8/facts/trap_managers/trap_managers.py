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

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.argspec.trap_managers.trap_managers import (
    Trap_managersArgs,
)


class Trap_managersFacts(object):
    """The AOS8 Trap Managers fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Trap_managersArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_trap_managers_data(self, connection):
        cmd = 'show configuration snapshot | grep "snmp station"'
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
            data = self.get_trap_managers_data(connection)
            objs = self.parse_trap_managers(data)

        facts = {}
        if objs:
            facts["trap_managers"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})

            for cfg in params["config"]:
                facts["trap_managers"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def parse_trap_managers(self, data):
        objs = []

        # operate on a collection of resource x
        config = data.split("\n")

        for conf in config:
            match = re.match("^^snmp\sstation\s(?P<host>[\d.]+)\s(?P<port>[\d]+)\s\"(?P<string>(\w)+)\"\s(?P<version>v1|v2|v3)\s(?P<state>enable|disable)", conf)
            if match:
                members_obj = {
                    'host'          :   match.group('host'),   
                    'port'          :   match.group('port'),
                    'string'        :   match.group('string'),
                    'version'       :   match.group('version'),
                    'state'         :   match.group('state'),
                }
                objs.append(members_obj)                   
                
        return objs