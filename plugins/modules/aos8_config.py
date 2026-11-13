#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_config
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_config
short_description: Send configuration lines to AOS 8 devices
description:
  - Sends configuration lines to an Alcatel-Lucent Enterprise OmniSwitch running AOS 8.
  - Each line is compared with the output of C(show configuration snapshot). Only the lines that are not
    found there are sent.
  - Write the lines the way the switch shows them in C(show configuration snapshot), otherwise they are
    sent again at every run.
version_added: 1.0.0
author:
  - Mathias Guillemot (@mathias-gt)
notes:
  - Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
  - This module works with connection C(ansible.netcommon.network_cli).
  - The AOS configuration has no sections, so this module has no C(parents) option.
  - After lines are sent, the configuration is also saved to flash when C(ansible_aos_write_memory_flash)
    is C(true), which is the default of the connection. Set it to C(false) to let O(save_when) decide.
options:
  lines:
    description:
      - The configuration lines to send, in the order given.
    type: list
    elements: str
    aliases:
      - commands
  src:
    description:
      - Path of a file on the Ansible controller that holds the configuration lines. The file can be a
        Jinja2 template.
      - A relative path is looked up in the C(templates) folder of the role or next to the playbook.
      - C(ansible.netcommon) deprecates reading templates through this option. Prefer O(lines) with the
        C(ansible.builtin.template) lookup, as shown in the examples.
      - Mutually exclusive with O(lines).
    type: str
  before:
    description:
      - Commands to send before the configuration lines, when at least one line has to be sent.
    type: list
    elements: str
  after:
    description:
      - Commands to send after the configuration lines, when at least one line has to be sent.
    type: list
    elements: str
  match:
    description:
      - V(line) only sends the lines that are not in the configuration of the switch.
      - V(none) sends every line without comparing.
    type: str
    choices:
      - line
      - none
    default: line
  backup:
    description:
      - Saves the output of C(show configuration snapshot), taken before any change, to a file on the
        Ansible controller.
      - Without O(backup_options), the file is written to the C(backup) folder next to the playbook.
    type: bool
    default: false
  backup_options:
    description:
      - Where the backup file is written. Only used when O(backup=true).
    type: dict
    suboptions:
      filename:
        description:
          - Name of the backup file. The default is C(<hostname>_config.<date>@<time>).
        type: str
      dir_path:
        description:
          - Folder the backup file is written to. It is created when it does not exist.
        type: path
  running_config:
    description:
      - Configuration to compare the lines with, instead of reading it from the switch.
    type: str
    aliases:
      - config
  save_when:
    description:
      - When the configuration is saved to flash with C(write memory flash-synchro).
      - V(always) saves at every run.
      - V(never) does not save.
      - V(modified) saves when the switch reports that the running configuration is not saved.
      - V(changed) saves when the task changed the configuration.
    type: str
    choices:
      - always
      - never
      - modified
      - changed
    default: never
  diff_against:
    description:
      - What the configuration is compared with when the task runs with C(--diff).
      - V(running) shows the changes made by the task.
      - V(intended) compares the configuration of the switch with O(intended_config).
    type: str
    choices:
      - running
      - intended
    default: running
  diff_ignore_lines:
    description:
      - Lines to leave out of the comparison. Each entry is a line or a regular expression.
    type: list
    elements: str
  intended_config:
    description:
      - The configuration the switch is expected to have. Required with O(diff_against=intended).
    type: str
"""

EXAMPLES = r"""
- name: Send configuration lines
  ale.aos8.aos8_config:
    lines:
      - vlan 41 admin-state enable
      - vlan 41 name "Printers"

- name: Send every line without comparing, with a command before and after
  ale.aos8.aos8_config:
    commands:
      - vlan 41 admin-state enable
    match: none
    before:
      - vlan 42 admin-state enable
    after:
      - vlan 43 admin-state enable

- name: Send the lines of a template with a lookup, and back up the configuration first
  ale.aos8.aos8_config:
    lines: '{{ lookup(''ansible.builtin.template'', ''aos8_config_lines.j2'').splitlines() }}'
    backup: true
    backup_options:
      filename: aos8_config_example.cfg
      dir_path: /tmp/aos8_backup

- name: Send the lines of a template file
  ale.aos8.aos8_config:
    src: aos8_config_example.j2

- name: Compare the lines with a configuration given in the task
  ale.aos8.aos8_config:
    lines:
      - vlan 42 admin-state enable
      - vlan 44 admin-state enable
    running_config: |
      vlan 44 admin-state enable

- name: Show what a change would do, in check mode with a diff
  ale.aos8.aos8_config:
    lines:
      - vlan 43 name "Lab"
    diff_ignore_lines:
      - ^! .*
  check_mode: true
  diff: true

- name: Compare the switch with an intended configuration
  ale.aos8.aos8_config:
    diff_against: intended
    intended_config: |
      vlan 43 admin-state enable
      vlan 43 name "Intended"
  diff: true

- name: Save the configuration when the task changes it
  ale.aos8.aos8_config:
    lines:
      - vlan 43 name "Lab"
    save_when: changed

- name: Save the configuration only when it is not saved yet
  ale.aos8.aos8_config:
    save_when: modified

- name: Save the configuration at every run
  ale.aos8.aos8_config:
    save_when: always

- name: Never save the configuration (the default)
  ale.aos8.aos8_config:
    lines:
      - vlan 43 admin-state enable
    config: |
      vlan 43 admin-state enable
    save_when: never
    match: line
    backup: false
    diff_against: running
"""

RETURN = r"""
---
commands:
  description: The lines sent to the switch.
  returned: when lines have to be sent
  type: list
  elements: str
  sample:
    - vlan 41 admin-state enable
    - vlan 41 name "Printers"
updates:
  description: Same value as RV(commands).
  returned: when lines have to be sent
  type: list
  elements: str
  sample:
    - vlan 41 admin-state enable
    - vlan 41 name "Printers"
backup_path:
  description: Full path of the backup file.
  returned: when O(backup=true)
  type: str
  sample: /playbooks/backup/val-os1_config.2026-11-13@10:15:00
"""

import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.connection import ConnectionError
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import (
    NetworkConfig,
    dumps,
)

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.aos8 import (
    get_config,
    get_connection,
    load_config,
    run_commands,
)


def get_candidate(module):
    if module.params["src"]:
        return module.params["src"]
    candidate_obj = NetworkConfig(indent=3)
    candidate_obj.add(module.params["lines"])
    return dumps(candidate_obj, "raw")


def is_saved(module):
    """True when the running configuration is saved in the running directory."""
    output = run_commands(module, ["show running-directory"])[0]
    match = re.search(r"Running Configuration\s*:\s*(NOT SYNCHRONIZED|SYNCHRONIZED)", to_text(output))
    return bool(match) and match.group(1) == "SYNCHRONIZED"


def save_config(module, result):
    result["changed"] = True
    if module.check_mode:
        module.warn("Skipping command `write memory flash-synchro` due to check_mode.")
        return
    run_commands(module, ["write memory flash-synchro"])


def main():
    """main entry point for module execution"""
    backup_spec = dict(filename=dict(type="str"), dir_path=dict(type="path"))
    argument_spec = dict(
        lines=dict(aliases=["commands"], type="list", elements="str"),
        src=dict(type="str"),
        before=dict(type="list", elements="str"),
        after=dict(type="list", elements="str"),
        match=dict(type="str", default="line", choices=["line", "none"]),
        backup=dict(type="bool", default=False),
        backup_options=dict(type="dict", options=backup_spec),
        running_config=dict(type="str", aliases=["config"]),
        save_when=dict(
            type="str",
            default="never",
            choices=["always", "never", "modified", "changed"],
        ),
        diff_against=dict(type="str", default="running", choices=["running", "intended"]),
        diff_ignore_lines=dict(type="list", elements="str"),
        intended_config=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[("lines", "src")],
        required_if=[("diff_against", "intended", ["intended_config"])],
        supports_check_mode=True,
    )

    result = {"changed": False}
    diff_ignore_lines = module.params["diff_ignore_lines"]
    connection = get_connection(module)
    before_config = None

    if module.params["backup"] or module._diff:
        before_config = get_config(module)
        if module.params["backup"]:
            result["__backup__"] = before_config

    if module.params["src"] or module.params["lines"]:
        running = module.params["running_config"] or before_config or get_config(module)
        try:
            response = connection.get_diff(
                candidate=get_candidate(module),
                running=running,
                diff_match=module.params["match"],
                diff_ignore_lines=diff_ignore_lines,
            )
        except ConnectionError as exc:
            module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))

        config_diff = response["config_diff"]
        if config_diff:
            commands = [line.strip() for line in config_diff.split("\n") if line.strip()]
            if module.params["before"]:
                commands[:0] = module.params["before"]
            if module.params["after"]:
                commands.extend(module.params["after"])
            result["commands"] = commands
            result["updates"] = commands
            if not module.check_mode:
                load_config(module, commands)
            result["changed"] = True

    save_when = module.params["save_when"]
    if save_when == "always":
        save_config(module, result)
    elif save_when == "modified":
        if not is_saved(module):
            save_config(module, result)
    elif save_when == "changed" and result["changed"]:
        save_config(module, result)

    if module._diff:
        after_config = run_commands(module, ["show configuration snapshot"])[0]
        after_obj = NetworkConfig(indent=3, contents=after_config, ignore_lines=diff_ignore_lines)
        if module.params["diff_against"] == "intended":
            base = NetworkConfig(
                indent=3,
                contents=module.params["intended_config"],
                ignore_lines=diff_ignore_lines,
            )
            if after_obj.sha1 != base.sha1:
                result["diff"] = {"before": str(after_obj), "after": str(base)}
        else:
            base = NetworkConfig(indent=3, contents=before_config, ignore_lines=diff_ignore_lines)
            if after_obj.sha1 != base.sha1:
                result["diff"] = {"before": str(base), "after": str(after_obj)}

    module.exit_json(**result)


if __name__ == "__main__":
    main()
