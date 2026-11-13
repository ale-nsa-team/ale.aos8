# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_radius_servers config class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import (
    Aos8ResourceBase,
    quote,
)


class Radius_servers(Aos8ResourceBase):
    """The aos8_radius_servers config class"""

    RESOURCE = "radius_servers"

    def item_key(self, item):
        return item["name"]

    def comparable(self, item):
        # the shared secret is stored hashed on the switch and cannot be compared
        return dict((k, v) for k, v in item.items() if v is not None and k != "key")

    def validate(self, item):
        if not item.get("host"):
            self._module.fail_json(msg="host is required for RADIUS server %s" % item["name"])

    def set_commands(self, want, have):
        if not want.get("key"):
            self._module.fail_json(
                msg="key is required to create or change RADIUS server %s" % want["name"],
            )
        command = (
            "aaa radius-server %s host %s key %s retransmit %s timeout %s auth-port %s acct-port %s"
            % (
                quote(want["name"]),
                want["host"],
                want["key"],
                want["retransmit"],
                want["timeout"],
                want["auth_port"],
                want["acct_port"],
            )
        )
        if want.get("vrf") and want["vrf"] != "default":
            command += " vrf-name %s" % want["vrf"]
        return [command]

    def display(self, commands):
        return [re.sub(r"( key )\S+", r"\1********", command) for command in commands]

    def delete_commands(self, have):
        return ["no aaa radius-server %s" % quote(have["name"])]
