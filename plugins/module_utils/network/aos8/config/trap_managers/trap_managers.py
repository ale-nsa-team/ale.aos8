# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_trap_managers config class
"""

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import (
    Aos8ResourceBase,
    quote,
)


class Trap_managers(Aos8ResourceBase):
    """The aos8_trap_managers config class"""

    RESOURCE = "trap_managers"

    def item_key(self, item):
        return item["host"]

    def set_commands(self, want, have):
        return [
            "snmp station %s %s %s %s %s"
            % (want["host"], want["port"], quote(want["string"]), want["version"], want["state"]),
        ]

    def delete_commands(self, have):
        return ["no snmp station %s" % have["host"]]
