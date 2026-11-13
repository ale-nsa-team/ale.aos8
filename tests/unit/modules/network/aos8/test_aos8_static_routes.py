# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_static_routes

from .aos8_module import TestAos8ResourceModule


class TestAos8StaticRoutesModule(TestAos8ResourceModule):
    module = aos8_static_routes
    fixture = "aos8_static_routes.txt"

    GW = "10.10.10.2"

    def test_gathered(self):
        result = self.run_module(state="gathered")
        self.assertEqual(
            result["gathered"],
            [
                {
                    "routes": [
                        {"dest": "172.31.251.0/24", "next_hops": [{"interface": "int_20", "admin_distance": 1}]},
                        {
                            "dest": "172.31.252.0/24",
                            "next_hops": [{"forward_router_address": "10.10.10.2", "admin_distance": 1}],
                        },
                        {
                            "dest": "172.31.253.0/24",
                            "next_hops": [
                                {
                                    "forward_router_address": "10.10.10.2",
                                    "admin_distance": 1,
                                    "tag": 7,
                                    "description": "valroute",
                                },
                            ],
                        },
                        {
                            "dest": "172.31.254.0/24",
                            "next_hops": [{"forward_router_address": "10.10.10.2", "admin_distance": 5}],
                        },
                        {
                            "dest": "172.31.255.0/24",
                            "next_hops": [{"forward_router_address": "10.10.10.2", "admin_distance": 1}],
                        },
                    ],
                },
            ],
        )

    def test_parsed_mask_form(self):
        result = self.run_module(
            state="parsed",
            running_config="ip static-route 10.9.0.0 mask 255.255.0.0 gateway 10.10.10.2 metric 1",
        )
        self.assertEqual(result["parsed"][0]["routes"][0]["dest"], "10.9.0.0/16")

    def _route(self, dest, **hop):
        return [dict(routes=[dict(dest=dest, next_hops=[hop])])]

    def test_merged_new(self):
        self.run_module(
            changed=True,
            config=self._route("2.2.2.0/24", forward_router_address=self.GW),
            commands=["ip static-route 2.2.2.0/24 gateway 10.10.10.2"],
        )

    def test_merged_new_all_options(self):
        self.run_module(
            changed=True,
            config=self._route(
                "2.2.2.0/24",
                forward_router_address=self.GW,
                admin_distance=10,
                tag=5,
                description="My route",
            ),
            commands=['ip static-route 2.2.2.0/24 gateway 10.10.10.2 tag 5 name "My route" metric 10'],
        )

    def test_merged_interface_route(self):
        self.run_module(
            changed=True,
            config=self._route("2.2.2.0/24", interface="int_20"),
            commands=['ip static-route 2.2.2.0/24 interface "int_20"'],
        )

    def test_merged_idempotent(self):
        self.run_module(
            config=[
                dict(
                    routes=[
                        dict(dest="172.31.255.0/24", next_hops=[dict(forward_router_address=self.GW)]),
                        dict(dest="172.31.254.0/24", next_hops=[dict(forward_router_address=self.GW, admin_distance=5)]),
                        dict(
                            dest="172.31.253.0/24",
                            next_hops=[dict(forward_router_address=self.GW, tag=7, description="valroute")],
                        ),
                        dict(dest="172.31.251.0/24", next_hops=[dict(interface="int_20")]),
                    ],
                ),
            ],
            commands=[],
        )

    def test_merged_metric_change(self):
        self.run_module(
            changed=True,
            config=self._route("172.31.254.0/24", forward_router_address=self.GW, admin_distance=7),
            commands=[
                "no ip static-route 172.31.254.0/24 gateway 10.10.10.2",
                "ip static-route 172.31.254.0/24 gateway 10.10.10.2 metric 7",
            ],
        )

    def test_replaced_swaps_the_next_hop(self):
        self.run_module(
            changed=True,
            state="replaced",
            config=self._route("172.31.255.0/24", forward_router_address="10.10.10.3"),
            commands=[
                "no ip static-route 172.31.255.0/24 gateway 10.10.10.2",
                "ip static-route 172.31.255.0/24 gateway 10.10.10.3",
            ],
        )

    def test_overridden(self):
        self.run_module(
            changed=True,
            state="overridden",
            config=self._route("172.31.255.0/24", forward_router_address=self.GW),
            commands=[
                'no ip static-route 172.31.251.0/24 interface "int_20"',
                "no ip static-route 172.31.252.0/24 gateway 10.10.10.2",
                "no ip static-route 172.31.253.0/24 gateway 10.10.10.2",
                "no ip static-route 172.31.254.0/24 gateway 10.10.10.2",
            ],
            sort=True,
        )

    def test_deleted_next_hop(self):
        self.run_module(
            changed=True,
            state="deleted",
            config=self._route("172.31.255.0/24", forward_router_address=self.GW),
            commands=["no ip static-route 172.31.255.0/24 gateway 10.10.10.2"],
        )

    def test_deleted_destination(self):
        self.run_module(
            changed=True,
            state="deleted",
            config=[dict(routes=[dict(dest="172.31.253.0/24")])],
            commands=["no ip static-route 172.31.253.0/24 gateway 10.10.10.2"],
        )

    def test_deleted_absent_is_idempotent(self):
        self.run_module(state="deleted", config=self._route("9.9.9.0/24", forward_router_address=self.GW), commands=[])

    def test_merged_without_next_hop_fails(self):
        self.run_module(failed=True, config=[dict(routes=[dict(dest="2.2.2.0/24")])])
