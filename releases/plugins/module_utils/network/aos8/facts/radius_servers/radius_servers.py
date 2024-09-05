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

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.radius_servers.radius_servers import (
    Radius_serversArgs,
)


class Radius_serversFacts(object):
    """The AOS8 Radius Server fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Radius_serversArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_radius_servers_data(self, connection):
        cmd = 'show configuration snapshot | grep "aaa radius-server"'
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
            data = self.get_radius_servers_data(connection)
            objs = self.parse_radius_servers(data)

        facts = {}
        if objs:
            facts["radius_servers"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})

            for cfg in params["config"]:
                facts["radius_servers"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def parse_radius_servers(self, data):
        objs = []

        # operate on a collection of resource x
        config = data.split("\n")

        for conf in config:
            match = re.match("^aaa\sradius-server\s\"(?P<name>(\w+))\"\shost\s(?P<host> .*retransmit\s(?P<retransmit>[\d]+)\stimeout\s(?P<timeout>[\d]+)\sauth-port\s(?P<auth_port>[\d]+)\sacct-port\s(?P<acct_port>[\d]+)\svrf-name\s(?P<vrfname>(\w+))", conf)
            if match:
                members_obj = {
                    'name'          :   match.group('name'),
                    'host'          :   match.group('host'),   
                    'retransmit'    :   match.group('retransmit'),
                    'timeout'       :   match.group('timeout'),
                    'auth_port'     :   match.group('auth_port'),
                    'acct_port'     :   match.group('acct_port'),
                    'vrf'           :   match.group('vrfname'),
                }
                objs.append(members_obj)                   
                
        return objs