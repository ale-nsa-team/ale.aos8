# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The aos8_l2_interfaces config class
"""

import re

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.base import Aos8ResourceBase


class L2_interfaces(Aos8ResourceBase):
    """The aos8_l2_interfaces config class"""

    RESOURCE = "l2_interfaces"

    def normalize(self, item):
        item = dict(item)
        port = str(item["port_number"])
        if port.startswith("0/"):
            port = port[2:]
        item["port_number"] = port
        item["port_type"] = "port" if re.match(r"^\d+/\d+/\S+$", port) else "linkagg"
        return item

    def item_key(self, item):
        return (item["vlan_id"], item["port_number"])

    def is_protected(self, item):
        # untagged membership of VLAN 1 is the factory default of every port
        return item["vlan_id"] == 1 and item.get("mode") == "untagged"

    def validate(self, item):
        if not item.get("mode"):
            self._module.fail_json(
                msg="mode is required to add port %s to VLAN %s"
                % (item["port_number"], item["vlan_id"]),
            )

    def _member(self, item):
        return "vlan %s members %s %s" % (item["vlan_id"], item["port_type"], item["port_number"])

    def set_commands(self, want, have):
        commands = []
        if have and have.get("mode") != want["mode"]:
            commands.extend(self.delete_commands(have))
        commands.append("%s %s" % (self._member(want), want["mode"]))
        return commands

    def delete_commands(self, have):
        return ["no " + self._member(have)]
