# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 vlans fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.vlans.vlans import (
    VlansArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class VlansFacts(Aos8FactsBase):
    """Reads the standard VLANs from the output of ``show vlan``"""

    RESOURCE = "vlans"
    ARGSPEC = VlansArgs
    COMMAND = "show vlan"

    LINE = re.compile(
        r"^\s*(?P<vlan_id>\d+)\s+std\s+(?P<admin>Ena|Dis)\s+(?P<oper>Ena|Dis)\s+"
        r"(?:Ena|Dis)\s+(?P<mtu>\d+)\s+(?P<name>.*?)\s*$",
    )
    STATE = {"Ena": "enable", "Dis": "disable"}

    def parse(self, data):
        objs = []
        for line in data.splitlines():
            match = self.LINE.match(line)
            if match:
                objs.append(
                    {
                        "vlan_id": int(match.group("vlan_id")),
                        "name": match.group("name"),
                        "admin": self.STATE[match.group("admin")],
                        "mtu": int(match.group("mtu")),
                        "operational_state": self.STATE[match.group("oper")],
                    },
                )
        return objs
