#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Alcatel-Lucent Enterprise OSPFv2 fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
import re

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.ospfv2.ospfv2 import (
    OspfV2_Args,
)

class OspfV2_Facts(object):
    """The Alcatel-Lucent Enterprise OSPF fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = OspfV2_Args.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_device_data(self, connection):
        return connection.get("show configuration snapshot ospf")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for OSPFv2
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """

        if not data:
            data = self.get_device_data(connection)

        # split the config into instances of the resource
        resource_delim = "ip ospf"
        find_pattern = r"(?:^|\n)%s.*?(?=(?:^|\n)%s|$)" % (
            resource_delim,
            resource_delim,
        )
        resources = [p.strip() for p in re.findall(find_pattern, data, re.DOTALL)]
        objs_list = []
        for resource in resources:
            if resource:
                obj = self.render_config(self.generated_spec, resource)
                if obj:
                    objs_list.append(obj)
                
        ansible_facts["ansible_network_resources"].pop("ospf", None)

        facts = {}
        if objs_list:
            facts["ospfv2"] = objs_list

        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def render_config(self, spec, conf):
        """
        Render config as dictionary structure and delete keys
          from spec for null values

        :param spec: The facts tree, generated from the argspec
        :param conf: The configuration
        :rtype: dictionary
        :returns: The generated config
        """
        ospf_params_dict = {}
        areas_list = []
        network_list = []
        for dev_config in conf.split("\n"):
            if not dev_config:
                continue
            dev_config = dev_config.strip()
            dev_config = re.sub(r"-", "_", dev_config).strip()
            if dev_config.startswith("ip ospf"):
                config_params = dev_config.split()
                if "load" in dev_config:
                    ospf_params_dict.update({"load": config_params[-1]})
                elif "area" in dev_config:
                    area_dict = {"area_id": config_params[-1]}
                    areas_list.append(area_dict)
                elif "interface" in dev_config:
                    interface_dict = {"interface": config_params[2]}
                    if "admin_state enable" in dev_config:
                        interface_dict.update({"admin_state": "enable"})
                    if "area" in dev_config:
                        interface_dict.update({"area": config_params[-1]})
                    network_list.append(interface_dict)
                elif "admin_state enable" in dev_config:
                    ospf_params_dict.update({"admin_state": "enable"})
        ospf_params_dict.update({"areas": areas_list})
        ospf_params_dict.update({"interfaces": network_list})
        return utils.remove_empties(ospf_params_dict)
