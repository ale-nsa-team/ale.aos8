# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING ou https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The aos8 static_routes fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re
from copy import deepcopy
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.static_routes.static_routes import Static_routesArgs

class Static_routesFacts(object):
    """The aos8 static_routes fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Static_routesArgs.argument_spec
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
        return connection.get("show configuration snapshot ip-routing")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for static_routes for Alcatel devices
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """
        if not data:
            data = self.get_device_data(connection)

        # split the config into instances of the resource
        resource_delim = "ip static-route"
        find_pattern = r"(?:^|\n)%s.*?(?=(?:^|\n)%s|$)" % (
            resource_delim,
            resource_delim,
        )

        resources = [p.strip() for p in re.findall(find_pattern, data)]

        # Create configuration objects for the resources
        objs = []
        for resource in resources:
            if resource:
                obj = self.render_config(self.generated_spec, resource)
                if obj:
                    objs.append(obj)

        # Update Ansible facts
        ansible_facts["ansible_network_resources"].pop("static_routes", None)
        facts = {"static_routes": []}
        if objs:
            facts["static_routes"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})
            for cfg in params["config"]:
                facts["static_routes"].append(utils.remove_empties(cfg))
        
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
        config = deepcopy(spec)
        routes = []
        conf_list = conf.split("\n")
        pattern = r"ip static-route ([\d\.]+)(?: mask ([\d\.]+))? gateway ([\d\.]+)(?: tag (\d+))?(?: name (\w+))?(?: metric (\d+))?"
        
        for conf_elem in conf_list:
            match = re.match(pattern, conf_elem)
            if match:
                route = {
                    "ip_address": match.group(1),
                    "mask": match.group(2) if match.group(2) else None,
                    "forward_router_address": match.group(3),  # Remplacez gateway par forward_router_address
                    "tag": match.group(4) if match.group(4) else None,
                    "description": match.group(5) if match.group(5) else None,
                    "admin_distance": match.group(6) if match.group(6) else None,
                }
                # Remove None values
                route = {k: v for k, v in route.items() if v is not None}
                routes.append(route)

        config["routes"] = routes
        return utils.remove_empties(config)
