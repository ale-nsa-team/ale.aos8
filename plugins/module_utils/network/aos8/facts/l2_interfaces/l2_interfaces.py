# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 l2_interfaces fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.l2_interfaces.l2_interfaces import (
    L2_interfacesArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class L2_interfacesFacts(Aos8FactsBase):
    """Reads the VLAN port associations from the output of ``show vlan members``"""

    RESOURCE = "l2_interfaces"
    ARGSPEC = L2_interfacesArgs
    COMMAND = "show vlan members"

    LINE = re.compile(
        r"^\s*(?P<vlan_id>\d+)\s+(?P<port>\d+/\S+)\s+(?P<mode>untagged|tagged)\s+\S+",
    )

    def parse(self, data):
        objs = []
        for line in data.splitlines():
            match = self.LINE.match(line)
            if not match:
                continue
            port = match.group("port")
            if port.startswith("0/"):
                # link aggregates are listed as 0/<agg id>
                port_type, port = "linkagg", port[2:]
            else:
                port_type = "port"
            objs.append(
                {
                    "vlan_id": int(match.group("vlan_id")),
                    "port_number": port,
                    "port_type": port_type,
                    "mode": match.group("mode"),
                },
            )
        return objs
