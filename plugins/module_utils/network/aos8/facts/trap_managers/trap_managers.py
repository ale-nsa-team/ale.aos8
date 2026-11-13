# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 trap_managers fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.trap_managers.trap_managers import (
    Trap_managersArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class Trap_managersFacts(Aos8FactsBase):
    """Reads the SNMP trap stations from the configuration snapshot"""

    RESOURCE = "trap_managers"
    ARGSPEC = Trap_managersArgs
    COMMAND = 'show configuration snapshot | grep "snmp station"'

    LINE = re.compile(
        r'^snmp\s+station\s+(?P<host>\S+)\s+(?P<port>\d+)\s+"(?P<string>[^"]*)"\s+'
        r"(?P<version>v1|v2|v3)\s+(?P<state>enable|disable)",
    )

    def parse(self, data):
        objs = []
        for line in data.splitlines():
            match = self.LINE.match(line.strip())
            if match:
                obj = match.groupdict()
                obj["port"] = int(obj["port"])
                objs.append(obj)
        return objs
