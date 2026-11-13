# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_ospfv2 config class
"""

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import (
    Aos8ResourceBase,
    quote,
)


class Ospfv2(Aos8ResourceBase):
    """The aos8_ospfv2 config class"""

    RESOURCE = "ospfv2"
    # an area can only be removed once its interfaces have moved to another area
    DELETE_FIRST = False

    def flatten(self, config):
        items = []
        config = config or {}
        for area in config.get("areas") or []:
            items.append({"kind": "area", "area_id": area["area_id"]})
            for interface in area.get("interfaces") or []:
                item = {"kind": "interface", "interface": interface["interface"], "area": area["area_id"]}
                if interface.get("admin_state"):
                    item["admin_state"] = interface["admin_state"]
                items.append(item)
        if config.get("admin_state"):
            items.append({"kind": "admin", "admin_state": config["admin_state"]})
        return items

    def item_key(self, item):
        return (item["kind"], item.get("area_id") or item.get("interface"))

    def item_scope(self, item):
        return "ospfv2"

    def order(self, item):
        return {"area": 1, "interface": 2, "admin": 3}[item["kind"]]

    def set_commands(self, want, have):
        have = have or {}
        if want["kind"] == "area":
            return ["ip ospf area %s" % want["area_id"]]
        if want["kind"] == "admin":
            return ["ip ospf admin-state %s" % want["admin_state"]]
        commands = []
        base = "ip ospf interface %s" % quote(want["interface"])
        if not have:
            commands.append(base)
        if want["area"] != have.get("area"):
            commands.append("%s area %s" % (base, want["area"]))
        if want.get("admin_state") and want["admin_state"] != have.get("admin_state", "disable"):
            commands.append("%s admin-state %s" % (base, want["admin_state"]))
        return commands

    def delete_commands(self, have):
        if have["kind"] == "area":
            return ["no ip ospf area %s" % have["area_id"]]
        if have["kind"] == "interface":
            return ["no ip ospf interface %s" % quote(have["interface"])]
        if have["admin_state"] == "enable":
            return ["ip ospf admin-state disable"]
        return []

    def finalize(self, commands, want, have):
        if commands and not have and self.state != "deleted":
            commands.insert(0, "ip load ospf")
        return commands
