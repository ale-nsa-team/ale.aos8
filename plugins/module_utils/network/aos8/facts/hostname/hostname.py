# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 hostname fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.hostname.hostname import (
    HostnameArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class HostnameFacts(Aos8FactsBase):
    """Reads the system name from the configuration snapshot"""

    RESOURCE = "hostname"
    ARGSPEC = HostnameArgs
    COMMAND = "show configuration snapshot | grep '^system name'"

    LINE = re.compile(r'^system\s+name\s+"?(?P<hostname>[^"]+)"?\s*$')

    def parse(self, data):
        for line in data.splitlines():
            match = self.LINE.match(line.strip())
            if match:
                return {"hostname": match.group("hostname")}
        return {}
