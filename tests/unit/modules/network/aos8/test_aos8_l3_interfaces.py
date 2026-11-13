# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_l3_interfaces

from .aos8_module import TestAos8ResourceModule


class TestAos8L3InterfacesModule(TestAos8ResourceModule):
    module = aos8_l3_interfaces
    fixture = "aos8_l3_interfaces.txt"

    def test_gathered(self):
        result = self.run_module(state="gathered")
        self.assertEqual(
            result["gathered"],
            [
                {"name": "Loopback0", "address": "10.255.0.1"},
                {"name": "int_10", "address": "10.10.10.1", "mask": "255.255.255.0", "type": "vlan", "port_id": "10"},
                {"name": "int_20", "address": "10.10.20.1", "mask": "255.255.255.0", "type": "vlan", "port_id": "20"},
                {
                    "name": "int_99",
                    "address": "10.10.99.1",
                    "mask": "255.255.255.0",
                    "type": "vlan",
                    "port_id": "99",
                    "vrf": "vrf-val",
                },
            ],
        )

    def test_parsed(self):
        result = self.run_module(
            state="parsed",
            running_config='ip interface "int_30" address 10.10.30.1 mask 255.255.255.0 vlan 30 ifindex 4',
        )
        self.assertEqual(
            result["parsed"],
            [{"name": "int_30", "address": "10.10.30.1", "mask": "255.255.255.0", "type": "vlan", "port_id": "30"}],
        )

    def test_merged_new(self):
        self.run_module(
            changed=True,
            config=[dict(name="int_30", address="10.10.30.1", mask="255.255.255.0", type="vlan", port_id="30")],
            commands=['ip interface "int_30" address 10.10.30.1 mask 255.255.255.0 vlan 30'],
        )

    def test_merged_idempotent(self):
        self.run_module(
            config=[
                dict(name="int_20", address="10.10.20.1", mask="255.255.255.0", type="vlan", port_id="20"),
                dict(name="Loopback0", address="10.255.0.1"),
                dict(name="int_99", vrf="vrf-val", address="10.10.99.1", mask="255.255.255.0", port_id="99"),
            ],
            commands=[],
        )

    def test_merged_address_change(self):
        self.run_module(
            changed=True,
            config=[dict(name="int_20", address="10.10.20.254")],
            commands=['ip interface "int_20" address 10.10.20.254 mask 255.255.255.0 vlan 20'],
        )

    def test_merged_loopback(self):
        self.run_module(
            changed=True,
            config=[dict(name="Loopback0", address="10.255.0.9")],
            commands=['ip interface "Loopback0" address 10.255.0.9'],
        )

    def test_merged_vrf(self):
        self.run_module(
            changed=True,
            config=[dict(name="int_98", vrf="vrf-val", address="10.10.98.1", mask="255.255.255.0", port_id="98")],
            commands=['vrf vrf-val ip interface "int_98" address 10.10.98.1 mask 255.255.255.0 vlan 98'],
        )

    def test_merged_missing_mask_fails(self):
        self.run_module(failed=True, config=[dict(name="int_30", address="10.10.30.1", port_id="30")])

    def test_deleted(self):
        self.run_module(
            changed=True,
            state="deleted",
            config=[dict(name="int_20"), dict(name="int_99", vrf="vrf-val")],
            commands=['vrf vrf-val no ip interface "int_99"', 'no ip interface "int_20"'],
            sort=True,
        )

    def test_deleted_other_vrf_does_not_match(self):
        self.run_module(state="deleted", config=[dict(name="int_99")], commands=[])

    def test_overridden(self):
        self.run_module(
            changed=True,
            state="overridden",
            config=[
                dict(name="int_10", address="10.10.10.1", mask="255.255.255.0", port_id="10"),
                dict(name="Loopback0", address="10.255.0.1"),
            ],
            commands=['no ip interface "int_20"', 'vrf vrf-val no ip interface "int_99"'],
            sort=True,
        )

    def test_rendered(self):
        result = self.run_module(
            state="rendered",
            config=[dict(name="int_30", address="10.10.30.1", mask="255.255.255.0", port_id="30")],
        )
        self.assertEqual(result["rendered"], ['ip interface "int_30" address 10.10.30.1 mask 255.255.255.0 vlan 30'])
