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


def make(write_memory=True, certify=False, directory=WORKING, timeout=180):
    cliconf = Cliconf.__new__(Cliconf)
    cliconf._device_info = {}
    cliconf._connection = MagicMock()
    cliconf._connection.get_option.return_value = timeout
    options = {"write_memory_flag": write_memory, "flash_synchro_flag": certify}
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


def test_certify_after_saving():
    cliconf = make(certify=True)
    cliconf.edit_config(["vlan 30 admin-state enable"])
    assert cliconf.sent[-3:] == ["show running-directory", "copy running certified", "show running-directory"]
    assert "copy flash-synchro" not in cliconf.sent


def test_no_certify_without_saving():
    cliconf = make(write_memory=False, certify=True)
    cliconf.edit_config(["vlan 30 admin-state enable"])
    assert "copy running certified" not in cliconf.sent


def test_certify_waits_until_the_copy_is_done(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda seconds: None)
    # the switch reports CERTIFY NEEDED twice, then CERTIFIED
    needed = WORKING.replace("CERTIFIED,", "CERTIFY NEEDED,")
    states = iter([needed, needed])
    cliconf = make(certify=True)
    original = cliconf.send_command

    def send_command(command, **kwargs):
        if command == "show running-directory" and "copy running certified" in cliconf.sent:
            cliconf.sent.append(command)
            return next(states, WORKING)
        return original(command, **kwargs)

    cliconf.send_command = send_command
    cliconf.edit_config(["vlan 30 admin-state enable"])
    assert cliconf.sent.count("show running-directory") == 5


def test_certify_failure_is_reported(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda seconds: None)
    cliconf = make(certify=True, directory=WORKING.replace("CERTIFIED,", "CERTIFY NEEDED,"))
    with pytest.raises(ValueError, match="certified directory after 120 seconds"):
        cliconf.edit_config(["vlan 30 admin-state enable"])


def test_certify_needs_a_long_timeout():
    cliconf = make(certify=True, timeout=90)
    with pytest.raises(ValueError, match="120 seconds"):
        cliconf.edit_config(["vlan 30 admin-state enable"])


def test_refused_when_running_from_certified():
    cliconf = make(directory=WORKING.replace("Running configuration           : WORKING", "Running configuration           : CERTIFIED"))
    with pytest.raises(ValueError, match="certified directory"):
        cliconf.edit_config(["vlan 30 admin-state enable"])
    assert "vlan 30 admin-state enable" not in cliconf.sent
