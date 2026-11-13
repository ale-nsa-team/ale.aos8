# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_vlans config class
"""

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import (
    Aos8ResourceBase,
    quote,
)


class Vlans(Aos8ResourceBase):
    """The aos8_vlans config class"""

    RESOURCE = "vlans"
    REPLACE_DEFAULTS = {"admin": "enable", "mtu": 1500}

    def item_key(self, item):
        return item["vlan_id"]

    def comparable(self, item):
        return dict(
            (k, v) for k, v in item.items() if v is not None and k != "operational_state"
        )

    def is_protected(self, item):
        # VLAN 1 is the default VLAN and cannot be removed
        return item["vlan_id"] == 1

    def set_commands(self, want, have):
        commands = []
        base = "vlan %s" % want["vlan_id"]
        have = have or {}
        admin = want.get("admin")
        if not have:
            commands.append("%s admin-state %s" % (base, admin or "enable"))
        elif admin and admin != have.get("admin"):
            commands.append("%s admin-state %s" % (base, admin))
        if want.get("name") and want["name"] != have.get("name"):
            commands.append("%s name %s" % (base, quote(want["name"])))
        if want.get("mtu") and want["mtu"] != have.get("mtu", 1500):
            commands.append("%s mtu-ip %s" % (base, want["mtu"]))
        return commands

    def delete_commands(self, have):
        return ["no vlan %s" % have["vlan_id"]]
