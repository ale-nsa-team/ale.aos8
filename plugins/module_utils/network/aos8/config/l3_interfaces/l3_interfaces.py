# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_l3_interfaces config class
"""

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import (
    Aos8ResourceBase,
    quote,
)


class L3_interfaces(Aos8ResourceBase):
    """The aos8_l3_interfaces config class"""

    RESOURCE = "l3_interfaces"

    @staticmethod
    def _is_loopback(item):
        return item["name"].startswith("Loopback")

    def normalize(self, item):
        item = dict(item)
        if item.get("vrf") == "default":
            item.pop("vrf")
        if item.get("port_id") and not item.get("type"):
            item["type"] = "vlan"
        return item

    def item_key(self, item):
        return (item.get("vrf", "default"), item["name"])

    def validate(self, item):
        if not item.get("address"):
            self._module.fail_json(msg="address is required for interface %s" % item["name"])
        if not self._is_loopback(item):
            missing = [k for k in ("mask", "port_id") if not item.get(k)]
            if missing:
                self._module.fail_json(
                    msg="%s required for interface %s" % (", ".join(missing), item["name"]),
                )

    def _prefix(self, item):
        return "vrf %s " % item["vrf"] if item.get("vrf") else ""

    def set_commands(self, want, have):
        command = "%sip interface %s address %s" % (
            self._prefix(want),
            quote(want["name"]),
            want["address"],
        )
        if not self._is_loopback(want):
            command += " mask %s vlan %s" % (want["mask"], want["port_id"])
        return [command]

    def delete_commands(self, have):
        return ["%sno ip interface %s" % (self._prefix(have), quote(have["name"]))]
