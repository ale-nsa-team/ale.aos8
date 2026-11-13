# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_static_routes config class
"""

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import (
    Aos8ResourceBase,
    quote,
)


class Static_routes(Aos8ResourceBase):
    """The aos8_static_routes config class"""

    RESOURCE = "static_routes"

    def flatten(self, config):
        items = []
        for entry in config or []:
            for route in entry.get("routes") or []:
                hops = route.get("next_hops") or []
                if not hops:
                    # only used to remove every next hop of a destination
                    items.append({"dest": route["dest"]})
                for hop in hops:
                    item = dict((k, v) for k, v in hop.items() if v is not None)
                    item["dest"] = route["dest"]
                    items.append(item)
        return items

    @staticmethod
    def _target(item):
        if item.get("forward_router_address"):
            return "gateway %s" % item["forward_router_address"]
        if item.get("interface"):
            return "interface %s" % quote(item["interface"])
        return None

    def item_key(self, item):
        return (item["dest"], self._target(item))

    def item_scope(self, item):
        return item["dest"]

    def comparable(self, item):
        result = dict((k, v) for k, v in item.items() if v is not None)
        result.setdefault("admin_distance", 1)
        return result

    def matches_delete(self, want, have):
        if self._target(want) is None:
            return want["dest"] == have["dest"]
        return self.item_key(want) == self.item_key(have)

    def validate(self, item):
        if self._target(item) is None:
            self._module.fail_json(
                msg="forward_router_address or interface is required for route %s" % item["dest"],
            )
        if item.get("interface") and (item.get("tag") or item.get("description")):
            self._module.fail_json(
                msg="tag and description are only supported with forward_router_address",
            )

    def set_commands(self, want, have):
        commands = []
        if have:
            # tag and name cannot be cleared on an existing route: create it again
            commands.extend(self.delete_commands(have))
        command = "ip static-route %s %s" % (want["dest"], self._target(want))
        if want.get("tag"):
            command += " tag %s" % want["tag"]
        if want.get("description"):
            command += " name %s" % quote(want["description"])
        if want.get("admin_distance"):
            command += " metric %s" % want["admin_distance"]
        commands.append(command)
        return commands

    def delete_commands(self, have):
        return ["no ip static-route %s %s" % (have["dest"], self._target(have))]
