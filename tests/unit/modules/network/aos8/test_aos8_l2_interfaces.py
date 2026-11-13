# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_l2_interfaces

from .aos8_module import TestAos8ResourceModule


class TestAos8L2InterfacesModule(TestAos8ResourceModule):
    module = aos8_l2_interfaces
    fixture = "aos8_l2_interfaces.txt"

    def test_gathered(self):
        result = self.run_module(state="gathered")
        gathered = result["gathered"]
        self.assertEqual(len(gathered), 40)
        self.assertIn({"vlan_id": 20, "port_number": "1/1/2", "port_type": "port", "mode": "untagged"}, gathered)
        self.assertIn({"vlan_id": 99, "port_number": "1/1/3", "port_type": "port", "mode": "tagged"}, gathered)
        self.assertIn({"vlan_id": 1, "port_number": "1/1/25A", "port_type": "port", "mode": "untagged"}, gathered)
        # link aggregate 5 is listed as 0/5 by the switch
        self.assertIn({"vlan_id": 99, "port_number": "5", "port_type": "linkagg", "mode": "tagged"}, gathered)

    def test_parsed(self):
        result = self.run_module(state="parsed", running_config=self._data)
        self.assertEqual(len(result["parsed"]), 40)

    def test_merged_port(self):
        self.run_module(
            changed=True,
            config=[dict(vlan_id=20, port_type="port", port_number="1/1/4", mode="tagged")],
            commands=["vlan 20 members port 1/1/4 tagged"],
        )

    def test_merged_linkagg(self):
        self.run_module(
            changed=True,
            config=[dict(vlan_id=20, port_type="linkagg", port_number="5", mode="tagged")],
            commands=["vlan 20 members linkagg 5 tagged"],
        )

    def test_merged_idempotent(self):
        self.run_module(
            config=[
                dict(vlan_id=20, port_type="port", port_number="1/1/2", mode="untagged"),
                dict(vlan_id=99, port_type="linkagg", port_number="5", mode="tagged"),
                dict(vlan_id=99, port_number="0/5", mode="tagged"),
            ],
            commands=[],
        )

    def test_merged_mode_change(self):
        self.run_module(
            changed=True,
            config=[dict(vlan_id=99, port_number="1/1/3", mode="untagged")],
            commands=["no vlan 99 members port 1/1/3", "vlan 99 members port 1/1/3 untagged"],
        )

    def test_merged_without_mode_fails(self):
        self.run_module(failed=True, config=[dict(vlan_id=20, port_number="1/1/4")])

    def test_deleted(self):
        self.run_module(
            changed=True,
            state="deleted",
            config=[dict(vlan_id=20, port_number="1/1/2")],
            commands=["no vlan 20 members port 1/1/2"],
        )

    def test_deleted_all_keeps_default_vlan_membership(self):
        self.run_module(
            changed=True,
            state="deleted",
            commands=[
                "no vlan 10 members port 1/1/1",
                "no vlan 20 members port 1/1/2",
                "no vlan 99 members port 1/1/3",
                "no vlan 99 members linkagg 5",
            ],
            sort=True,
        )

    def test_overridden(self):
        self.run_module(
            changed=True,
            state="overridden",
            config=[
                dict(vlan_id=10, port_number="1/1/1", mode="tagged"),
                dict(vlan_id=20, port_number="1/1/2", mode="untagged"),
            ],
            commands=["no vlan 99 members port 1/1/3", "no vlan 99 members linkagg 5"],
            sort=True,
        )

    def test_rendered(self):
        result = self.run_module(
            state="rendered",
            config=[dict(vlan_id=30, port_number="1/1/7", mode="untagged")],
        )
        self.assertEqual(result["rendered"], ["vlan 30 members port 1/1/7 untagged"])
