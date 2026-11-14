# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import MagicMock

import pytest

from ansible_collections.ale.aos8.plugins.cliconf.aos8 import Cliconf


WORKING = """CONFIGURATION STATUS
  Running CMM                     : PRIMARY,
  Running configuration           : WORKING,
  Certify/Restore Status          : CERTIFIED,
SYNCHRONIZATION STATUS
  Running Configuration           : SYNCHRONIZED
"""


def make(write_memory=True, flash_synchro=False, directory=WORKING, timeout=180):
    cliconf = Cliconf.__new__(Cliconf)
    cliconf._device_info = {}
    cliconf._connection = MagicMock()
    cliconf._connection.get_option.return_value = timeout
    options = {"write_memory_flag": write_memory, "flash_synchro_flag": flash_synchro}
    cliconf.get_option = options.get
    cliconf.sent = []

    def send_command(command, **kwargs):
        cliconf.sent.append(command)
        return directory if command == "show running-directory" else ""

    cliconf.send_command = send_command
    return cliconf


def test_lines_are_sent_then_saved():
    cliconf = make()
    cliconf.edit_config(["vlan 30 admin-state enable"])
    assert cliconf.sent == [
        "show running-directory",
        "vlan 30 admin-state enable",
        "write memory flash-synchro",
        "show running-directory",
    ]


def test_save_can_be_disabled():
    cliconf = make(write_memory=False)
    cliconf.edit_config(["vlan 30 admin-state enable"])
    assert cliconf.sent == ["show running-directory", "vlan 30 admin-state enable"]


def test_flash_synchro_after_saving():
    cliconf = make(flash_synchro=True)
    cliconf.edit_config(["vlan 30 admin-state enable"])
    assert cliconf.sent[-4:] == [
        "write memory flash-synchro",
        "show running-directory",
        "copy running certified flash-synchro",
        "show running-directory",
    ]


def test_flash_synchro_without_saving():
    cliconf = make(write_memory=False, flash_synchro=True)
    cliconf.edit_config(["vlan 30 admin-state enable"])
    assert cliconf.sent[-2:] == ["copy running certified flash-synchro", "show running-directory"]
    assert "write memory flash-synchro" not in cliconf.sent


def test_flash_synchro_failure_is_reported():
    cliconf = make(flash_synchro=True, directory=WORKING.replace("CERTIFIED,", "CERTIFY NEEDED,"))
    with pytest.raises(ValueError, match="Certified directory not synchronized"):
        cliconf.edit_config(["vlan 30 admin-state enable"])


def test_flash_synchro_needs_a_long_timeout():
    cliconf = make(flash_synchro=True, timeout=30)
    with pytest.raises(ValueError, match="60 seconds"):
        cliconf.edit_config(["vlan 30 admin-state enable"])


def test_refused_when_running_from_certified():
    cliconf = make(directory=WORKING.replace("Running configuration           : WORKING", "Running configuration           : CERTIFIED"))
    with pytest.raises(ValueError, match="certified directory"):
        cliconf.edit_config(["vlan 30 admin-state enable"])
    assert "vlan 30 admin-state enable" not in cliconf.sent
