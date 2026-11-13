# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 bgp fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.bgp.bgp import (
    Bgp_Args,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class Bgp_Facts(Aos8FactsBase):
    """Reads the BGP configuration of the default VRF from the configuration snapshot"""

    RESOURCE = "bgp"
    ARGSPEC = Bgp_Args
    COMMAND = "show configuration snapshot bgp"

    NEIGHBOR = re.compile(r"^ip\s+bgp\s+neighbor\s+(?P<address>\S+)(?P<options>.*)$")

    def parse(self, data):
        loaded = False
        config = {"bgp_admin_state": "disable"}
        neighbors = {}
        for line in data.splitlines():
            line = line.strip()
            if line.startswith("vrf "):
                break
            if line == "ip load bgp":
                loaded = True
                continue
            match = re.match(r"^ip\s+bgp\s+autonomous-system\s+(\S+)", line)
            if match:
                config["as_number"] = match.group(1)
                continue
            match = re.match(r"^ip\s+bgp\s+admin-state\s+(enable|disable)", line)
            if match:
                config["bgp_admin_state"] = match.group(1)
                continue
            match = self.NEIGHBOR.match(line)
            if match:
                entry = neighbors.setdefault(
                    match.group("address"),
                    {"neighbor_address": match.group("address"), "neighbor_admin_state": "disable"},
                )
                options = match.group("options").split()
                if "remote-as" in options[:-1]:
                    entry["remote_as"] = options[options.index("remote-as") + 1]
                if "admin-state" in options[:-1]:
                    entry["neighbor_admin_state"] = options[options.index("admin-state") + 1]
        if not loaded:
            return {}
        if neighbors:
            config["neighbor"] = list(neighbors.values())
        return config
