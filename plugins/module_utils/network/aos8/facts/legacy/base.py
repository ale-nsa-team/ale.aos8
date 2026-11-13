# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8 legacy fact class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.aos8 import run_commands


class Default(object):
    """Basic facts about the switch, read from ``show system``"""

    COMMAND = "show system"

    def __init__(self, module):
        self.module = module
        self.facts = dict()
        self.warnings = list()

    def populate(self):
        data = run_commands(self.module, [self.COMMAND])[0]
        self.facts.update(self.parse(data))

    @staticmethod
    def parse(data):
        facts = {"network_os": "aos8"}
        match = re.search(r"^\s*Description:\s+(.+?),?\s*$", data, re.M)
        if match:
            facts["system"] = match.group(1)
            detail = re.search(r"(\S+)\s+(\d+\.\d+\.\d+\.R\d+)", match.group(1))
            if detail:
                facts["model"] = detail.group(1)
                facts["version"] = detail.group(2)
        match = re.search(r"^\s*Name:\s+(.*?),?\s*$", data, re.M)
        if match:
            facts["hostname"] = match.group(1)
        return facts
