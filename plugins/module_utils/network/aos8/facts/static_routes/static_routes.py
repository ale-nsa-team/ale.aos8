# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 static_routes fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.static_routes.static_routes import (
    Static_routesArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class Static_routesFacts(Aos8FactsBase):
    """Reads the static routes of the default VRF from the configuration snapshot"""

    RESOURCE = "static_routes"
    ARGSPEC = Static_routesArgs
    COMMAND = "show configuration snapshot ip-routing"

    LINE = re.compile(
        r"^ip\s+static-route\s+(?P<dest>[\d.]+(?:/\d+)?)(?:\s+mask\s+(?P<mask>[\d.]+))?\s+"
        r'(?:gateway\s+(?P<gateway>\S+)|interface\s+"?(?P<interface>[^"\s]+)"?)(?P<options>.*)$',
    )

    @staticmethod
    def _prefix(dest, mask):
        if mask and "/" not in dest:
            bits = sum(bin(int(octet)).count("1") for octet in mask.split("."))
            return "%s/%s" % (dest, bits)
        return dest

    def parse(self, data):
        routes = {}
        order = []
        for line in data.splitlines():
            line = line.strip()
            if line.startswith("vrf "):
                # routes listed after a "vrf create" line belong to another VRF
                break
            match = self.LINE.match(line)
            if not match:
                continue
            hop = {}
            if match.group("gateway"):
                hop["forward_router_address"] = match.group("gateway")
            else:
                hop["interface"] = match.group("interface")
            options = match.group("options")
            for field, pattern in (("admin_distance", r"\smetric\s+(\d+)"), ("tag", r"\stag\s+(\d+)")):
                found = re.search(pattern, options)
                if found:
                    hop[field] = int(found.group(1))
            found = re.search(r'\sname\s+"?([^"]+?)"?\s*(?:$|\smetric\s|\stag\s)', options)
            if found:
                hop["description"] = found.group(1)
            dest = self._prefix(match.group("dest"), match.group("mask"))
            if dest not in routes:
                routes[dest] = []
                order.append(dest)
            routes[dest].append(hop)
        if not routes:
            return []
        return [{"routes": [{"dest": dest, "next_hops": routes[dest]} for dest in order]}]
