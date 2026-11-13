# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_switch_security config class
"""

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import (
    Aos8ResourceBase,
    quote,
)


class Switch_security(Aos8ResourceBase):
    """The aos8_switch_security config class"""

    RESOURCE = "switch_security"

    def item_key(self, item):
        return item["access_method"]

    def is_protected(self, item):
        # the default access method cannot be reset to itself
        return item["access_method"] == "default"

    def validate(self, item):
        if not item.get("aaa_servers_name"):
            self._module.fail_json(
                msg="aaa_servers_name is required for access method %s" % item["access_method"],
            )

    def set_commands(self, want, have):
        return [
            "aaa authentication %s %s" % (want["access_method"], quote(want["aaa_servers_name"])),
        ]

    def delete_commands(self, have):
        # back to the servers of the default access method
        return ["aaa authentication %s default" % have["access_method"]]
