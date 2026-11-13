# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_ntp config class
"""

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import Aos8ResourceBase


class Ntp(Aos8ResourceBase):
    """The aos8_ntp config class"""

    RESOURCE = "ntp"
    # values the switch does not show in the configuration snapshot
    DEFAULTS = {"minpoll": 6, "maxpoll": 10, "version": 4}
    FLAGS = ("prefer", "burst", "iburst")

    def flatten(self, config):
        return [dict(item) for item in (config or {}).get("servers", [])]

    def item_key(self, item):
        return item["server"]

    def item_scope(self, item):
        return "ntp"

    def comparable(self, item):
        result = dict(self.DEFAULTS)
        for key, value in item.items():
            if value is None or (key in self.FLAGS and not value):
                continue
            result[key] = value
        return result

    def set_commands(self, want, have):
        commands = []
        if have:
            # options cannot be cleared on an existing server: create it again
            commands.extend(self.delete_commands(have))
        command = "ntp server %s" % want["server"]
        for option in ("minpoll", "maxpoll", "version"):
            if want.get(option) and want[option] != self.DEFAULTS[option]:
                command += " %s %s" % (option, want[option])
        for flag in self.FLAGS:
            if want.get(flag):
                command += " " + flag
        commands.append(command)
        return commands

    def delete_commands(self, have):
        return ["no ntp server %s" % have["server"]]
