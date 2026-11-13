# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 radius_servers fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.radius_servers.radius_servers import (
    Radius_serversArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class Radius_serversFacts(Aos8FactsBase):
    """Reads the RADIUS servers from the configuration snapshot"""

    RESOURCE = "radius_servers"
    ARGSPEC = Radius_serversArgs
    COMMAND = 'show configuration snapshot | grep "aaa radius-server"'

    LINE = re.compile(r'^aaa\s+radius-server\s+"?(?P<name>[^"\s]+)"?\s+host\s+(?P<host>\S+)')
    FIELDS = (
        ("retransmit", r"\sretransmit\s+(\d+)", int),
        ("timeout", r"\stimeout\s+(\d+)", int),
        ("auth_port", r"\sauth-port\s+(\d+)", int),
        ("acct_port", r"\sacct-port\s+(\d+)", int),
        ("vrf", r"\svrf-name\s+(\S+)", str),
    )

    def parse(self, data):
        objs = []
        for line in data.splitlines():
            line = line.strip()
            match = self.LINE.match(line)
            if not match:
                continue
            obj = {"name": match.group("name"), "host": match.group("host")}
            for field, pattern, convert in self.FIELDS:
                found = re.search(pattern, line)
                if found:
                    obj[field] = convert(found.group(1))
            objs.append(obj)
        return objs
