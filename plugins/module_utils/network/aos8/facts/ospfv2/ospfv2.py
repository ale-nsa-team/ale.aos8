# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 ospfv2 fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.ospfv2.ospfv2 import (
    OspfV2_Args,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class OspfV2_Facts(Aos8FactsBase):
    """Reads the OSPFv2 configuration of the default VRF from the configuration snapshot"""

    RESOURCE = "ospfv2"
    ARGSPEC = OspfV2_Args
    COMMAND = "show configuration snapshot ospf"

    INTERFACE = re.compile(r'^ip\s+ospf\s+interface\s+"?(?P<name>[^"\s]+)"?(?P<options>.*)$')

    def parse(self, data):
        loaded = False
        admin_state = "disable"
        areas = []
        interfaces = {}
        for line in data.splitlines():
            line = line.strip()
            if line.startswith("vrf "):
                break
            if line == "ip load ospf":
                loaded = True
                continue
            match = re.match(r"^ip\s+ospf\s+area\s+(\S+)\s*$", line)
            if match:
                areas.append(match.group(1))
                continue
            match = re.match(r"^ip\s+ospf\s+admin-state\s+(enable|disable)", line)
            if match:
                admin_state = match.group(1)
                continue
            match = self.INTERFACE.match(line)
            if match:
                entry = interfaces.setdefault(match.group("name"), {"admin_state": "disable"})
                options = match.group("options").split()
                if "area" in options[:-1]:
                    entry["area"] = options[options.index("area") + 1]
                if "admin-state" in options[:-1]:
                    entry["admin_state"] = options[options.index("admin-state") + 1]
        if not loaded:
            return {}
        config = {"admin_state": admin_state}
        if areas:
            config["areas"] = []
            for area_id in areas:
                area = {"area_id": area_id}
                members = [
                    {"interface": name, "admin_state": entry["admin_state"]}
                    for name, entry in interfaces.items()
                    if entry.get("area") == area_id
                ]
                if members:
                    area["interfaces"] = members
                config["areas"].append(area)
        return config
