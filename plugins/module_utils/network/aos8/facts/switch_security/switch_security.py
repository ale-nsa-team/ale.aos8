# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 switch_security fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.switch_security.switch_security import (
    Switch_securityArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class Switch_securityFacts(Aos8FactsBase):
    """Reads the authenticated switch access settings from the configuration snapshot"""

    RESOURCE = "switch_security"
    ARGSPEC = Switch_securityArgs
    COMMAND = 'show configuration snapshot | grep "aaa authentication"'

    LINE = re.compile(
        r'^aaa\s+authentication\s+(?P<access_method>default|console|telnet|ssh|snmp|http|ftp)\s+'
        r'"(?P<aaa_servers_name>[^"]+)"',
    )

    def parse(self, data):
        objs = []
        for line in data.splitlines():
            match = self.LINE.match(line.strip())
            if match:
                objs.append(match.groupdict())
        return objs
