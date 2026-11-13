# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_bgp

from .aos8_module import TestAos8ResourceModule


class TestAos8BgpModule(TestAos8ResourceModule):
    module = aos8_bgp
    fixture = "aos8_bgp.txt"

    def test_gathered(self):
        result = self.run_module(state="gathered")
        self.assertEqual(
            result["gathered"],
            {
                "as_number": "65001",
                "bgp_admin_state": "enable",
                "neighbor": [{"neighbor_address": "10.10.10.2", "remote_as": "65002", "neighbor_admin_state": "enable"}],
            },
        )

    def test_merged_idempotent(self):
        self.run_module(
            config=dict(
                as_number="65001",
                bgp_admin_state="enable",
                neighbor=[dict(neighbor_address="10.10.10.2", remote_as="65002", neighbor_admin_state="enable")],
            ),
            commands=[],
        )

    def test_merged_new_neighbor(self):
        self.run_module(
            changed=True,
            config=dict(neighbor=[dict(peer="10.10.10.3", remote_as="65003", neighbor_admin_state="enable")]),
            commands=[
                "ip bgp neighbor 10.10.10.3",
                "ip bgp neighbor 10.10.10.3 remote-as 65003",
                "ip bgp neighbor 10.10.10.3 admin-state enable",
            ],
        )

    def test_merged_on_switch_without_bgp_loads_it_first(self):
        self._data = "! BGP:"
        self.run_module(
            changed=True,
            config=dict(as_number="65010", bgp_admin_state="enable"),
            commands=["ip load bgp", "ip bgp autonomous-system 65010", "ip bgp admin-state enable"],
        )

    def test_merged_neighbor_change(self):
        self.run_module(
            changed=True,
            config=dict(neighbor=[dict(neighbor_address="10.10.10.2", remote_as="65009", neighbor_admin_state="disable")]),
            commands=[
                "ip bgp neighbor 10.10.10.2 remote-as 65009",
                "ip bgp neighbor 10.10.10.2 admin-state disable",
            ],
        )

    def test_overridden_removes_other_neighbors(self):
        self.run_module(
            changed=True,
            state="overridden",
            config=dict(
                as_number="65001",
                bgp_admin_state="enable",
                neighbor=[dict(neighbor_address="10.10.10.3", remote_as="65003")],
            ),
            commands=[
                "no ip bgp neighbor 10.10.10.2",
                "ip bgp neighbor 10.10.10.3",
                "ip bgp neighbor 10.10.10.3 remote-as 65003",
            ],
        )

    def test_deleted_all_keeps_the_as_number(self):
        self.run_module(
            changed=True,
            state="deleted",
            commands=["ip bgp admin-state disable", "no ip bgp neighbor 10.10.10.2"],
        )

    def test_deleted_one_neighbor(self):
        self.run_module(
            changed=True,
            state="deleted",
            config=dict(neighbor=[dict(neighbor_address="10.10.10.2")]),
            commands=["no ip bgp neighbor 10.10.10.2"],
        )

    def test_rendered(self):
        result = self.run_module(state="rendered", config=dict(as_number="65010"))
        self.assertEqual(result["rendered"], ["ip load bgp", "ip bgp autonomous-system 65010"])
