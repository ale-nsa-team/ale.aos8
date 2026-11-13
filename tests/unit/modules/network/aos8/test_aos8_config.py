# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type


from unittest.mock import patch

from ansible_collections.ale.aos8.plugins.cliconf.aos8 import Cliconf
from ansible_collections.ale.aos8.plugins.modules import aos8_config
from ansible_collections.ale.aos8.tests.unit.modules.utils import set_module_args

from .aos8_module import TestAos8Module


RUNNING = """! VLAN:
vlan 1 admin-state enable
vlan 10 admin-state enable
vlan 10 name "VAL-ISL"
vlan 10 members port 1/1/1 tagged
! IP:
ip interface "int_10" address 10.10.10.1 mask 255.255.255.0 vlan 10 ifindex 1
"""
SAVED = "  Running Configuration           : SYNCHRONIZED\n"
NOT_SAVED = "  Running Configuration           : NOT SYNCHRONIZED\n"


class FakeCliconf(object):
    """Runs the real diff code of the cliconf plugin without a connection."""

    get_device_operations = Cliconf.get_device_operations
    get_option_values = Cliconf.get_option_values
    get_diff = Cliconf.get_diff


class TestAos8ConfigModule(TestAos8Module):
    module = aos8_config

    def setUp(self):
        super(TestAos8ConfigModule, self).setUp()
        path = "ansible_collections.ale.aos8.plugins.modules.aos8_config."
        self.sent = []
        self.directory = SAVED
        self.mocks = {
            "get_connection": patch(path + "get_connection", return_value=FakeCliconf()),
            "get_config": patch(path + "get_config", return_value=RUNNING),
            "load_config": patch(path + "load_config"),
            "run_commands": patch(path + "run_commands", side_effect=self._run_commands),
            "warn": patch("ansible.module_utils.basic.AnsibleModule.warn"),
        }
        self.started = dict((name, item.start()) for name, item in self.mocks.items())

    def tearDown(self):
        super(TestAos8ConfigModule, self).tearDown()
        for item in self.mocks.values():
            item.stop()

    def _run_commands(self, module, commands):
        self.sent.extend(commands)
        if commands == ["show running-directory"]:
            return [self.directory]
        if commands == ["show configuration snapshot"]:
            return [RUNNING + 'vlan 41 name "Printers"\n']
        return [""]

    def run_config(self, changed=False, commands=None, **args):
        set_module_args(args)
        result = self.execute_module(changed=changed, commands=commands, sort=False)
        if commands and not args.get("_ansible_check_mode"):
            self.started["load_config"].assert_called_once()
            self.assertEqual(self.started["load_config"].call_args[0][1], commands)
        else:
            self.started["load_config"].assert_not_called()
        return result

    def test_lines_new(self):
        result = self.run_config(
            changed=True,
            lines=["vlan 41 admin-state enable", 'vlan 41 name "Printers"'],
            commands=["vlan 41 admin-state enable", 'vlan 41 name "Printers"'],
        )
        self.assertEqual(result["updates"], result["commands"])

    def test_lines_only_missing_lines_are_sent(self):
        self.run_config(
            changed=True,
            lines=["vlan 10 admin-state enable", "vlan 41 admin-state enable"],
            commands=["vlan 41 admin-state enable"],
        )

    def test_lines_idempotent(self):
        result = self.run_config(lines=["vlan 10 admin-state enable", 'vlan 10 name "VAL-ISL"'])
        self.assertNotIn("commands", result)

    def test_src(self):
        # the action plugin replaces src with the content of the file
        self.run_config(
            changed=True,
            src='vlan 10 name "VAL-ISL"\nvlan 42 name "Cameras"\n',
            commands=['vlan 42 name "Cameras"'],
        )

    def test_match_none_sends_everything(self):
        self.run_config(
            changed=True,
            lines=["vlan 10 admin-state enable"],
            match="none",
            commands=["vlan 10 admin-state enable"],
        )

    def test_before_and_after(self):
        self.run_config(
            changed=True,
            lines=["vlan 41 admin-state enable"],
            before=["vlan 42 admin-state enable"],
            after=["vlan 43 admin-state enable"],
            commands=["vlan 42 admin-state enable", "vlan 41 admin-state enable", "vlan 43 admin-state enable"],
        )

    def test_before_and_after_are_not_sent_when_nothing_changes(self):
        self.run_config(lines=["vlan 10 admin-state enable"], before=["vlan 42 admin-state enable"])

    def test_running_config_is_used_instead_of_the_switch(self):
        self.run_config(
            changed=True,
            lines=["vlan 10 admin-state enable", "vlan 44 admin-state enable"],
            running_config="vlan 44 admin-state enable\n",
            commands=["vlan 10 admin-state enable"],
        )

    def test_backup(self):
        result = self.run_config(backup=True)
        self.assertEqual(result["__backup__"], RUNNING)

    def test_check_mode_does_not_configure(self):
        result = self.run_config(changed=True, lines=["vlan 41 admin-state enable"], _ansible_check_mode=True)
        self.assertEqual(result["commands"], ["vlan 41 admin-state enable"])

    def test_save_when_always(self):
        self.run_config(changed=True, save_when="always")
        self.assertEqual(self.sent, ["write memory flash-synchro"])

    def test_save_when_never(self):
        self.run_config(changed=True, lines=["vlan 41 admin-state enable"], commands=["vlan 41 admin-state enable"])
        self.assertEqual(self.sent, [])

    def test_save_when_changed(self):
        self.run_config(
            changed=True,
            lines=["vlan 41 admin-state enable"],
            save_when="changed",
            commands=["vlan 41 admin-state enable"],
        )
        self.assertEqual(self.sent, ["write memory flash-synchro"])

    def test_save_when_changed_without_change(self):
        self.run_config(lines=["vlan 10 admin-state enable"], save_when="changed")
        self.assertEqual(self.sent, [])

    def test_save_when_modified_and_already_saved(self):
        self.run_config(save_when="modified")
        self.assertEqual(self.sent, ["show running-directory"])

    def test_save_when_modified_and_not_saved(self):
        self.directory = NOT_SAVED
        self.run_config(changed=True, save_when="modified")
        self.assertEqual(self.sent, ["show running-directory", "write memory flash-synchro"])

    def test_save_in_check_mode_is_skipped(self):
        self.run_config(changed=True, save_when="always", _ansible_check_mode=True)
        self.assertEqual(self.sent, [])

    def test_diff_against_running(self):
        result = self.run_config(
            changed=True,
            lines=['vlan 41 name "Printers"'],
            commands=['vlan 41 name "Printers"'],
            _ansible_diff=True,
        )
        self.assertNotIn("Printers", result["diff"]["before"])
        self.assertIn('vlan 41 name "Printers"', result["diff"]["after"])

    def test_diff_against_intended(self):
        result = self.run_config(diff_against="intended", intended_config="vlan 99 admin-state enable\n", _ansible_diff=True)
        self.assertEqual(result["diff"]["after"].strip(), "vlan 99 admin-state enable")

    def test_diff_ignore_lines(self):
        result = self.run_config(
            diff_against="intended",
            intended_config=RUNNING + 'vlan 41 name "Printers"\n! changed comment\n',
            diff_ignore_lines=["^!.*"],
            _ansible_diff=True,
        )
        self.assertNotIn("diff", result)

    def test_diff_against_intended_requires_intended_config(self):
        set_module_args(dict(diff_against="intended"))
        self.execute_module(failed=True)

    def test_lines_and_src_are_mutually_exclusive(self):
        set_module_args(dict(lines=["vlan 41"], src="vlan 42"))
        self.execute_module(failed=True)
