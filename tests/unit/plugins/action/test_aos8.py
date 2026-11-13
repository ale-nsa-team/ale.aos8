# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.ale.aos8.plugins.action.aos8 import ActionModule


BASE = "ansible_collections.ansible.netcommon.plugins.action.network.ActionModule._handle_backup_option"


def backup(module_changed, backup_written):
    def fake(self, result, task_vars, backup_options):
        result["changed"] = backup_written

    action = ActionModule.__new__(ActionModule)
    result = {"changed": module_changed}
    with patch(BASE, fake):
        action._handle_backup_option(result, {}, None)
    return result["changed"]


def test_a_configuration_change_stays_changed_when_the_backup_file_is_identical():
    assert backup(module_changed=True, backup_written=False) is True


def test_writing_a_new_backup_file_is_a_change():
    assert backup(module_changed=False, backup_written=True) is True


def test_nothing_changed():
    assert backup(module_changed=False, backup_written=False) is False
