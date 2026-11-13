# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 l3_interfaces fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.l3_interfaces.l3_interfaces import (
    L3_interfacesArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class L3_interfacesFacts(Aos8FactsBase):
    """Reads the IP interfaces from the configuration snapshot"""

    RESOURCE = "l3_interfaces"
    ARGSPEC = L3_interfacesArgs
    COMMAND = 'show configuration snapshot | grep "ip interface"'

    LINE = re.compile(
        r'^(?:vrf\s+(?P<vrf>\S+)\s+)?ip\s+interface\s+"(?P<name>[^"]+)"\s+address\s+(?P<address>[\d.]+)'
        r"(?:\s+mask\s+(?P<mask>[\d.]+))?(?:\s+vlan\s+(?P<vlan>\d+))?",
    )

    def parse(self, data):
        objs = []
        for line in data.splitlines():
            match = self.LINE.match(line.strip())
            if not match:
                continue
            obj = {"name": match.group("name"), "address": match.group("address")}
            if match.group("vrf"):
                obj["vrf"] = match.group("vrf")
            if match.group("mask"):
                obj["mask"] = match.group("mask")
            if match.group("vlan"):
                obj["type"] = "vlan"
                obj["port_id"] = match.group("vlan")
            objs.append(obj)
        return objs
