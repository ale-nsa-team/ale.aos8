# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_bgp config class
"""

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import Aos8ResourceBase


class Bgp(Aos8ResourceBase):
    """The aos8_bgp config class"""

    RESOURCE = "bgp"

    def flatten(self, config):
        items = []
        config = config or {}
        if config.get("as_number"):
            items.append({"kind": "as", "as_number": str(config["as_number"])})
        for neighbor in config.get("neighbor") or []:
            item = dict((k, v) for k, v in neighbor.items() if v is not None)
            item["kind"] = "neighbor"
            items.append(item)
        if config.get("bgp_admin_state"):
            items.append({"kind": "admin", "bgp_admin_state": config["bgp_admin_state"]})
        return items

    def item_key(self, item):
        return (item["kind"], item.get("neighbor_address"))

    def item_scope(self, item):
        return "bgp"

    def order(self, item):
        return {"as": 1, "neighbor": 2, "admin": 3}[item["kind"]]

    def is_protected(self, item):
        # the autonomous system number cannot be removed
        return item["kind"] == "as"

    def set_commands(self, want, have):
        have = have or {}
        if want["kind"] == "as":
            return ["ip bgp autonomous-system %s" % want["as_number"]]
        if want["kind"] == "admin":
            return ["ip bgp admin-state %s" % want["bgp_admin_state"]]
        commands = []
        base = "ip bgp neighbor %s" % want["neighbor_address"]
        if not have:
            commands.append(base)
        if want.get("remote_as") and str(want["remote_as"]) != str(have.get("remote_as")):
            commands.append("%s remote-as %s" % (base, want["remote_as"]))
        state = want.get("neighbor_admin_state")
        if state and state != have.get("neighbor_admin_state", "disable"):
            commands.append("%s admin-state %s" % (base, state))
        return commands

    def delete_commands(self, have):
        if have["kind"] == "neighbor":
            return ["no ip bgp neighbor %s" % have["neighbor_address"]]
        if have["kind"] == "admin" and have["bgp_admin_state"] == "enable":
            return ["ip bgp admin-state disable"]
        return []

    def finalize(self, commands, want, have):
        if commands and not have and self.state != "deleted":
            commands.insert(0, "ip load bgp")
        return commands
