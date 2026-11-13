# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type


from ansible_collections.ale.aos8.plugins.terminal.aos8 import TerminalModule


def is_error(output):
    return any(regex.search(output) for regex in TerminalModule.terminal_stderr_re)


def is_prompt(output):
    return any(regex.search(output) for regex in TerminalModule.terminal_stdout_re)


def test_errors_reported_by_the_switch_are_detected():
    # real answers captured from AOS 8.11
    assert is_error(b'show vlan\r\n            ^\r\nERROR: Invalid entry: "vlan"\r\n\r\nval-os1-> ')
    assert is_error(b"ERROR: Interface 'int_10' doesn't exist.\r\nval-os1-> ")


def test_normal_output_is_not_an_error():
    assert not is_error(b"vlan    type   admin   oper\r\n1      std       Ena     Ena\r\nval-os1-> ")
    assert not is_error(b"WARNING: Gateway is unreachable, route marked inactive.\r\nval-os1-> ")
    # the word ERROR inside a line (for example in a log) is not a command error
    assert not is_error(b"2026 Nov 13 swlogd ChassisSupervisor ERROR: fan 1\r\nval-os1-> ")


def test_prompts_are_recognized():
    assert is_prompt(b"\r\nval-os1-> ")
    assert is_prompt(b"\r\nvrf-val::val-os1-> ")
    assert is_prompt(b"\r\ncore-sw-1-> ")
