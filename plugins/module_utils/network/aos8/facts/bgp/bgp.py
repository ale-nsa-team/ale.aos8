# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The aos8 bgp fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.bgp.bgp import Bgp_Args
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.rm_templates.Bgp_Template import Bgp_Template


class Bgp_Facts(object):
    """The aos8 bgp facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Bgp_Args.argument_spec

    def get_config(self, connection):
        """Wrapper method for `connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return connection.get("show configuration snapshot bgp ")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Bgp network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []
        if not data:
            data = self.get_config(connection)

        bgp_config = []
        for bgp_line in data.splitlines():
            bgp_config.append(bgp_line)

        # parse native config using the Bgp template
        bgp_parser = Bgp_Template(
            lines=bgp_config,
            module=self._module,
        )
        objs = bgp_parser.parse()

        if objs:
            global_vals = objs.pop("global", {})
            for key, value in iteritems(global_vals):
                objs[key] = value

            if "neighbor" in objs:
                objs["neighbor"] = list(objs["neighbor"].values())

        ansible_facts["ansible_network_resources"].pop("bgp", None)

        params = utils.remove_empties(
            bgp_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["bgp"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
