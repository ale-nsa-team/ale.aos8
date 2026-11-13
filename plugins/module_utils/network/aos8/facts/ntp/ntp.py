# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 ntp fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.ntp.ntp import (
    Ntp_Args,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.facts.base import Aos8FactsBase


class Ntp_Facts(Aos8FactsBase):
    """Reads the NTP servers from the configuration snapshot"""

    RESOURCE = "ntp"
    ARGSPEC = Ntp_Args
    COMMAND = "show configuration snapshot ntp"

    LINE = re.compile(r"^ntp\s+server\s+(?P<server>\S+)(?P<options>.*)$")
    NUMBERS = ("minpoll", "maxpoll", "version")
    FLAGS = ("prefer", "burst", "iburst")

    def parse(self, data):
        servers = []
        for line in data.splitlines():
            match = self.LINE.match(line.strip())
            if not match:
                continue
            obj = {"server": match.group("server")}
            options = match.group("options").split()
            for keyword in self.NUMBERS:
                if keyword in options[:-1]:
                    obj[keyword] = int(options[options.index(keyword) + 1])
            for flag in self.FLAGS:
                if flag in options:
                    obj[flag] = True
            servers.append(obj)
        return {"servers": sorted(servers, key=lambda k: k["server"])} if servers else {}
