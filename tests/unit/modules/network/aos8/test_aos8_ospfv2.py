# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_ospfv2

from .aos8_module import TestAos8ResourceModule


class TestAos8Ospfv2Module(TestAos8ResourceModule):
    module = aos8_ospfv2
    fixture = "aos8_ospfv2.txt"

    def test_gathered(self):
        result = self.run_module(state="gathered")
        self.assertEqual(
            result["gathered"],
            {
                "admin_state": "enable",
                "areas": [{"area_id": "0.0.0.0", "interfaces": [{"interface": "int_10", "admin_state": "enable"}]}],
            },
        )

    def test_merged_idempotent(self):
        self.run_module(
            config=dict(
                admin_state="enable",
                areas=[dict(area_id="0.0.0.0", interfaces=[dict(interface="int_10", admin_state="enable")])],
            ),
            commands=[],
        )

    def test_merged_new_interface_and_area(self):
        self.run_module(
            changed=True,
            config=dict(areas=[dict(area_id="0.0.0.1", interfaces=[dict(interface="int_20", admin_state="enable")])]),
            commands=[
                "ip ospf area 0.0.0.1",
                'ip ospf interface "int_20"',
                'ip ospf interface "int_20" area 0.0.0.1',
                'ip ospf interface "int_20" admin-state enable',
            ],
        )

    def test_merged_on_switch_without_ospf_loads_it_first(self):
        self._data = "! OSPF:"
        self.run_module(
            changed=True,
            config=dict(admin_state="enable", areas=[dict(area_id="0.0.0.0")]),
            commands=["ip load ospf", "ip ospf area 0.0.0.0", "ip ospf admin-state enable"],
        )

    def test_merged_admin_state(self):
        self.run_module(changed=True, config=dict(admin_state="disable"), commands=["ip ospf admin-state disable"])

    def test_replaced_removes_what_is_not_listed(self):
        self.run_module(
            changed=True,
            state="replaced",
            config=dict(admin_state="enable", areas=[dict(area_id="0.0.0.0")]),
            commands=['no ip ospf interface "int_10"'],
        )

    def test_overridden_moves_interface_to_another_area(self):
        self.run_module(
            changed=True,
            state="overridden",
            config=dict(
                admin_state="enable",
                areas=[dict(area_id="0.0.0.1", interfaces=[dict(interface="int_10", admin_state="enable")])],
            ),
            commands=["ip ospf area 0.0.0.1", 'ip ospf interface "int_10" area 0.0.0.1', "no ip ospf area 0.0.0.0"],
        )

    def test_deleted_all(self):
        self.run_module(
            changed=True,
            state="deleted",
            commands=["ip ospf admin-state disable", 'no ip ospf interface "int_10"', "no ip ospf area 0.0.0.0"],
        )

    def test_rendered(self):
        result = self.run_module(
            state="rendered",
            config=dict(admin_state="enable", areas=[dict(area_id="0.0.0.0", interfaces=[dict(interface="int_10")])]),
        )
        self.assertEqual(
            result["rendered"],
            [
                "ip load ospf",
                "ip ospf area 0.0.0.0",
                'ip ospf interface "int_10"',
                'ip ospf interface "int_10" area 0.0.0.0',
                "ip ospf admin-state enable",
            ],
        )
