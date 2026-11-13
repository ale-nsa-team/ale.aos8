# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ale.aos8.plugins.modules import aos8_radius_servers

import re

from .aos8_module import TestAos8ResourceModule


class TestAos8RadiusServersModule(TestAos8ResourceModule):
    module = aos8_radius_servers
    fixture = "aos8_radius_servers.txt"

    def hide_secrets(self, commands):
        return [re.sub(r"( key )\S+", r"\1********", command) for command in commands]

    def test_the_real_secret_is_sent_to_the_switch(self):
        result = self.run_module(changed=True, config=[dict(name="rad3", host="10.0.0.3", key="secret")])
        self.assertIn(" key ******** ", result["commands"][0])
        self.assertIn(" key secret ", self.connection.edit_config.call_args[0][0][0])

    def test_gathered(self):
        result = self.run_module(state="gathered")
        self.assertEqual(
            result["gathered"],
            [
                {
                    "name": "val-radius",
                    "host": "192.168.121.251",
                    "retransmit": 3,
                    "timeout": 2,
                    "auth_port": 1812,
                    "acct_port": 1813,
                    "vrf": "default",
                },
                {
                    "name": "valradius2",
                    "host": "192.168.121.252",
                    "retransmit": 3,
                    "timeout": 2,
                    "auth_port": 1812,
                    "acct_port": 1813,
                    "vrf": "default",
                },
            ],
        )

    def test_merged_new(self):
        self.run_module(
            changed=True,
            config=[dict(name="rad3", host="10.0.0.3", key="secret")],
            commands=[
                'aaa radius-server "rad3" host 10.0.0.3 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813',
            ],
        )

    def test_merged_new_in_vrf(self):
        self.run_module(
            changed=True,
            config=[dict(name="rad3", host="10.0.0.3", key="secret", vrf="vrf-val", timeout=5)],
            commands=[
                'aaa radius-server "rad3" host 10.0.0.3 key ******** retransmit 3 timeout 5 auth-port 1812 '
                "acct-port 1813 vrf-name vrf-val",
            ],
        )

    def test_merged_idempotent(self):
        # the key is stored hashed: an unchanged server is not sent again
        self.run_module(config=[dict(name="val-radius", host="192.168.121.251", key="valtest123")], commands=[])

    def test_merged_change(self):
        self.run_module(
            changed=True,
            config=[dict(name="val-radius", host="192.168.121.251", key="valtest123", timeout=10)],
            commands=[
                'aaa radius-server "val-radius" host 192.168.121.251 key ******** retransmit 3 timeout 10 '
                "auth-port 1812 acct-port 1813",
            ],
        )

    def test_merged_change_without_key_fails(self):
        self.run_module(failed=True, config=[dict(name="val-radius", host="192.168.121.251", timeout=10)])

    def test_deleted(self):
        self.run_module(
            changed=True,
            state="deleted",
            config=[dict(name="val-radius")],
            commands=['no aaa radius-server "val-radius"'],
        )

    def test_overridden(self):
        self.run_module(
            changed=True,
            state="overridden",
            config=[dict(name="val-radius", host="192.168.121.251", key="valtest123")],
            commands=['no aaa radius-server "valradius2"'],
        )

    def test_rendered(self):
        result = self.run_module(state="rendered", config=[dict(name="r", host="10.0.0.1", key="k")])
        self.assertEqual(
            result["rendered"],
            ['aaa radius-server "r" host 10.0.0.1 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813'],
        )
