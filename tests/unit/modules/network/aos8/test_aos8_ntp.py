# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_ntp

from .aos8_module import TestAos8ResourceModule


class TestAos8NtpModule(TestAos8ResourceModule):
    module = aos8_ntp
    fixture = "aos8_ntp.txt"

    def test_gathered(self):
        result = self.run_module(state="gathered")
        self.assertEqual(
            result["gathered"],
            {
                "servers": [
                    {"server": "192.168.121.250"},
                    {"server": "192.168.121.251", "prefer": True},
                    {"server": "192.168.121.252"},
                ],
            },
        )

    def test_parsed(self):
        result = self.run_module(
            state="parsed",
            running_config="ntp server 10.0.0.1 minpoll 4 maxpoll 12 version 3 prefer",
        )
        self.assertEqual(
            result["parsed"],
            {"servers": [{"server": "10.0.0.1", "minpoll": 4, "maxpoll": 12, "version": 3, "prefer": True}]},
        )

    def test_merged_new(self):
        self.run_module(
            changed=True,
            config=dict(servers=[dict(server="10.0.0.1"), dict(server="10.0.0.2", prefer=True, minpoll=4)]),
            commands=["ntp server 10.0.0.1", "ntp server 10.0.0.2 minpoll 4 prefer"],
        )

    def test_merged_idempotent(self):
        # default poll intervals and version are not shown by the switch
        self.run_module(
            config=dict(
                servers=[
                    dict(server="192.168.121.250", prefer=False),
                    dict(server="192.168.121.251", prefer=True),
                    dict(server="192.168.121.252", minpoll=6, maxpoll=10, version=4),
                ],
            ),
            commands=[],
        )

    def test_replaced_removes_option_by_recreating_the_server(self):
        self.run_module(
            changed=True,
            state="replaced",
            config=dict(
                servers=[
                    dict(server="192.168.121.250"),
                    dict(server="192.168.121.251"),
                    dict(server="192.168.121.252"),
                ],
            ),
            commands=["no ntp server 192.168.121.251", "ntp server 192.168.121.251"],
        )

    def test_replaced_removes_other_servers(self):
        self.run_module(
            changed=True,
            state="replaced",
            config=dict(servers=[dict(server="192.168.121.250")]),
            commands=["no ntp server 192.168.121.251", "no ntp server 192.168.121.252"],
            sort=True,
        )

    def test_deleted_one(self):
        self.run_module(
            changed=True,
            state="deleted",
            config=dict(servers=[dict(server="192.168.121.252")]),
            commands=["no ntp server 192.168.121.252"],
        )

    def test_deleted_all(self):
        self.run_module(
            changed=True,
            state="deleted",
            commands=[
                "no ntp server 192.168.121.250",
                "no ntp server 192.168.121.251",
                "no ntp server 192.168.121.252",
            ],
            sort=True,
        )

    def test_rendered(self):
        result = self.run_module(state="rendered", config=dict(servers=[dict(server="10.0.0.1", burst=True, iburst=True)]))
        self.assertEqual(result["rendered"], ["ntp server 10.0.0.1 burst iburst"])
