# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import json

__metaclass__ = type

"""
The aos8 hostname fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.rm_templates.hostname import (
    HostnameTemplate,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.hostname.hostname import (
    HostnameArgs,
)

class HostnameFacts(object):
    """ The aos8 hostname facts class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = HostnameArgs.argument_spec

    def get_hostname_data(self, connection):
        return connection.get("show configuration snapshot | grep '^system name'")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Hostname network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_hostname_data(connection)
            # x =  data.replace('"', "")
            # data = x

        hostname_parser = HostnameTemplate(lines=data.splitlines(), module=self._module)
       
        objs = json.dumps((hostname_parser.parse()))
        ansible_facts["ansible_network_resources"].pop("hostname", None)

        params = utils.remove_empties(
            hostname_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )


        facts["hostname"] = params["config"]     
        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts
