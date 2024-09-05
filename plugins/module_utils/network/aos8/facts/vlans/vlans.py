#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios vlans fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


import re

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.vlans.vlans import (
    VlansArgs,
)


class VlansFacts(object):
    """The ios vlans fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = VlansArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def get_vlans_data(self, connection):
        cmd = "show vlan"
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
            data = self.get_vlans_data(connection)
            objs = self.parse_vlan(data)

        facts = {}
        if objs:
            facts["vlans"] = []
            params = utils.validate_config(self.argument_spec, {"config": objs})

            for cfg in params["config"]:
                facts["vlans"].append(utils.remove_empties(cfg))
        ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts

    def render_config(self, spec, conf, vlan_info):
        """
        Render config as dictionary structure and delete keys
          from spec for null values

        :param spec: The facts tree, generated from the argspec
        :param conf: The configuration
        :rtype: dictionary
        :returns: The generated config
        """
        config = deepcopy(spec)

        if vlan_info == "Name" and "VLAN Name" not in conf:
            conf = list(filter(None, conf.split(" ")))
            config["vlan_id"] = int(conf[0])
            config["name"] = conf[1]
            state_idx = 2
            for i in range(2, len(conf)):  # check for index where state starts
                if conf[i] in ["suspended", "active"]:
                    state_idx = i
                    break
                elif conf[i].split("/")[0] in ["sus", "act"]:
                    state_idx = i
                    break
                config["name"] += " " + conf[i]
            try:
                if len(conf[state_idx].split("/")) > 1:
                    _state = conf[state_idx].split("/")[0]
                    if _state == "sus":
                        config["state"] = "suspend"
                    elif _state == "act":
                        config["state"] = "active"
                    config["shutdown"] = "enabled"
                else:
                    if conf[state_idx] == "suspended":
                        config["state"] = "suspend"
                    elif conf[state_idx] == "active":
                        config["state"] = "active"
                    config["shutdown"] = "disabled"
            except IndexError:
                pass
        elif vlan_info == "Type" and "VLAN Type" not in conf:
            conf = list(filter(None, conf.split(" ")))
            config["mtu"] = int(conf[3])
        elif vlan_info == "Remote":
            if len(conf.split(",")) > 1 or conf.isdigit():
                remote_span_vlan = []
                if len(conf.split(",")) > 1:
                    remote_span_vlan = conf.split(",")
                else:
                    remote_span_vlan.append(conf)
                remote_span = []
                for each in remote_span_vlan:
                    split_sp_list = each.split("-")
                    if len(split_sp_list) > 1:  # break range
                        for r_sp in range(int(split_sp_list[0]), int(split_sp_list[1]) + 1):
                            remote_span.append(r_sp)
                    else:
                        remote_span.append(int(each))
                config["remote_span"] = remote_span

        elif vlan_info == "Private" and "Primary Secondary" not in conf:
            conf = list(filter(None, conf.split(" ")))

            pri_idx = 0
            sec_idx = 1
            priv_type_idx = 2

            config["tmp_pvlans"] = {
                "primary": conf[pri_idx],
                "secondary": conf[sec_idx],
                "sec_type": conf[priv_type_idx],
            }
        return utils.remove_empties(config)

    def parse_vlan_config(self, vlan_conf):
        vlan_list = list()

        re1 = re.compile(r"^vlan configuration +(?P<vlan>\d+)$")
        re2 = re.compile(r"^member +(evpn\-instance +(?P<evi>\d+) )?vni (?P<vni>[\d\-]+)$")

        for line in vlan_conf.splitlines():
            line = line.strip()

            m = re1.match(line)
            if m:
                vlan = m.groupdict()["vlan"]
                vlan_dict = {"vlan_id": vlan}
                continue

            m = re2.match(line)
            if m:
                group = m.groupdict()
                vlan_dict.update({"member": {}})
                vlan_dict["member"].update({"vni": group["vni"]})
                if group["evi"]:
                    vlan_dict["member"].update({"evi": group["evi"]})
                vlan_list.append(vlan_dict)

        return vlan_list

    def parse_vlan(self, data):
        objs = []

        # operate on a collection of resource x
        config = data.split("\n")
        # Get individual vlan configs separately
        for conf in config:
            match = re.match("^(?P<vlan_id>[\d]+).*(?P<type>std)\s*(?P<admin>Ena|Dis)\s*(?P<oper>Ena|Dis)\s*(?P<ip>Ena|Dis)\s*(?P<mtu>[\d]+)\s*(?P<name>.*)$", conf)
            if match:
                if match.group('admin') == 'Ena':
                    admin_state = "enable"  
                else:
                    admin_state = "disable"

                if match.group('oper') == 'Ena':
                    operational_state = "enable"
                else:
                    operational_state = "disable"                    
                vlan_obj = {
                        'vlan_id' : match.group('vlan_id'),
                        'name' : match.group('name').strip(), 
                        'mtu' : match.group('mtu'), 
                        'admin': admin_state,
                        'operational_state' : operational_state,
                }
                objs.append(vlan_obj)

        return objs