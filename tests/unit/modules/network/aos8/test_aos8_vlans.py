# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_vlans

from .aos8_module import TestAos8ResourceModule


class TestAos8VlansModule(TestAos8ResourceModule):
    module = aos8_vlans
    fixture = "aos8_vlans.txt"

    def test_gathered(self):
        result = self.run_module(state="gathered")
        self.assertEqual(
            result["gathered"],
            [
                {"vlan_id": 1, "name": "VLAN 1", "admin": "enable", "mtu": 1500, "operational_state": "enable"},
                {"vlan_id": 10, "name": "VAL-ISL", "admin": "enable", "mtu": 1500, "operational_state": "enable"},
                {"vlan_id": 20, "name": "VAL-CLIENT", "admin": "enable", "mtu": 1500, "operational_state": "enable"},
                {
                    "vlan_id": 99,
                    "name": "VAL 99 with spaces",
                    "admin": "enable",
                    "mtu": 1280,
                    "operational_state": "enable",
                },
            ],
        )

    def test_parsed(self):
        result = self.run_module(state="parsed", running_config=self._data)
        self.assertEqual([v["vlan_id"] for v in result["parsed"]], [1, 10, 20, 99])

    def test_merged_new_vlan(self):
        self.run_module(
            changed=True,
            config=[dict(vlan_id=30, name="Voice", mtu=9000)],
            commands=["vlan 30 admin-state enable", 'vlan 30 name "Voice"', "vlan 30 mtu-ip 9000"],
        )

    def test_merged_new_vlan_minimal(self):
        self.run_module(changed=True, config=[dict(vlan_id=30)], commands=["vlan 30 admin-state enable"])

    def test_merged_idempotent(self):
        self.run_module(
            config=[dict(vlan_id=20, name="VAL-CLIENT"), dict(vlan_id=99, name="VAL 99 with spaces", mtu=1280)],
            commands=[],
        )

    def test_merged_keeps_unspecified_attributes(self):
        # merged only touches what is given: the mtu of VLAN 99 stays 1280
        self.run_module(config=[dict(vlan_id=99, admin="enable")], commands=[])

    def test_merged_change(self):
        self.run_module(
            changed=True,
            config=[dict(vlan_id=20, name="Users", admin="disable")],
            commands=["vlan 20 admin-state disable", 'vlan 20 name "Users"'],
        )

    def test_replaced_resets_unspecified_attributes(self):
        self.run_module(
            changed=True,
            state="replaced",
            config=[dict(vlan_id=99, name="VAL 99 with spaces")],
            commands=["vlan 99 mtu-ip 1500"],
        )

    def test_replaced_idempotent(self):
        self.run_module(state="replaced", config=[dict(vlan_id=20, name="VAL-CLIENT")], commands=[])

    def test_overridden(self):
        self.run_module(
            changed=True,
            state="overridden",
            config=[dict(vlan_id=10, name="VAL-ISL"), dict(vlan_id=30, name="Voice")],
            commands=["no vlan 20", "no vlan 99", "vlan 30 admin-state enable", 'vlan 30 name "Voice"'],
        )

    def test_deleted(self):
        self.run_module(changed=True, state="deleted", config=[dict(vlan_id=20)], commands=["no vlan 20"])

    def test_deleted_absent_is_idempotent(self):
        self.run_module(state="deleted", config=[dict(vlan_id=555)], commands=[])

    def test_deleted_all_keeps_default_vlan(self):
        self.run_module(
            changed=True,
            state="deleted",
            commands=["no vlan 10", "no vlan 20", "no vlan 99"],
        )

    def test_rendered(self):
        result = self.run_module(state="rendered", config=[dict(vlan_id=998, name="Vlan 998", admin="disable")])
        self.assertEqual(result["rendered"], ["vlan 998 admin-state disable", 'vlan 998 name "Vlan 998"'])

    def test_check_mode_does_not_configure(self):
        result = self.run_module_check(config=[dict(vlan_id=30)])
        self.assertEqual(result["commands"], ["vlan 30 admin-state enable"])

    def test_merged_without_config_fails(self):
        self.run_module(failed=True, state="merged")
