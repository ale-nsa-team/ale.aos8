#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The aos8 switch security fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.argspec.switch_security.switch_security import (
    Switch_securityArgs,
)


class Switch_securityFacts(object):
    """The AOS8 Switch security fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Switch_securityArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_switch_security_data(self, connection):
        cmd = 'show configuration snapshot | grep "aaa authentication"'
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
            data = self.get_switch_security_data(connection)
            objs = self.parse_switch_security(data)

        facts = {}
        if objs:
            facts["switch_security"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})

            for cfg in params["config"]:
                facts["switch_security"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def parse_switch_security(self, data):
        objs = []

        # operate on a collection of resource x
        config = data.split("\n")

        for conf in config:
            match = re.match("^aaa\sauthentication\s(?P<access_method>(\w)+)\s\"(?P<aaa_servers_name>(\w)+)\"", conf)
            if match:
                members_obj = {
                    'access_method'      :   match.group('access_method'),
                    'aaa_servers_name'   :   match.group('aaa_servers_name'),   
                }
                objs.append(members_obj)                   
                
        return objs