# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos ntp fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.ntp.ntp import (
    Ntp_Args,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.rm_templates.Ntp_Template import (
    Ntp_Template,
)

class Ntp_Facts(object):
    """The aos ntp facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ntp_Args.argument_spec

    def get_config(self, connection):
        """Wrapper method for `connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return connection.get("show configuration snapshot ntp")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Ntp network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = {}

        if not data:
            data = self.get_config(connection)

        # parse native config using the Ntp_global template
        ntp_parser = Ntp_Template(
            lines=data.splitlines(),
            module=self._module,
        )
        objs = ntp_parser.parse()

        ## print ouput to file
        with open("whatInObjs.txt", "a") as f:
            print(objs, file=f)

        if objs:
            if "servers" in objs:
                objs["servers"] = sorted(
                    list(objs["servers"].values()),
                    key=lambda k, sk="server": k[sk],
                )
        else:
            objs = {}
        ansible_facts["ansible_network_resources"].pop("ntp", None)


        params = utils.remove_empties(
            ntp_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["ntp"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

   