#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_hostname
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_hostname
short_description: Resource module to configure the system name
description:
  - This module manages the system name of Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
  - AOS has no command to remove the system name, so this module has no C(deleted) state.
  - The system name is one value, so C(merged), C(replaced) and C(overridden) do the same thing.
version_added: 1.0.0
author:
  - Samuel Yip Kah Yean (@samuelyip74)
  - Mathias Guillemot (@mathias-gt)
notes:
  - Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
  - This module works with connection C(ansible.netcommon.network_cli).
  - After a change, the configuration is saved to flash with C(write memory flash-synchro), unless C(ansible_aos_write_memory_flash)
    is set to C(false). Saving needs C(ansible_command_timeout) to be 60 seconds or more.
options:
  config:
    description:
      - The system name configuration.
    type: dict
    suboptions:
      hostname:
        description:
          - System name of the switch.
        type: str
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show configuration snapshot | grep '^system name') from the switch.
    type: str
  state:
    description:
      - What the module does with the given configuration.
      - C(merged) adds the given configuration to the switch and changes only the attributes that are
        given.
      - C(replaced) makes each given entry match the task exactly. Attributes that are left out go back
        to their default value.
      - C(overridden) makes the whole resource match the task. Entries found on the switch that are not
        in the task are removed.
      - C(gathered) reads the configuration from the switch and returns it as RV(gathered). Nothing is
        changed.
      - C(rendered) returns the commands for the given configuration as RV(rendered), without connecting
        to the switch.
      - C(parsed) converts the text given in O(running_config) into structured data, returned as RV(parsed),
        without connecting to the switch.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - gathered
      - rendered
      - parsed
    default: merged
"""

EXAMPLES = r"""
- name: Set the system name
  ale.aos8.aos8_hostname:
    config:
      hostname: core-sw-1
    state: merged

# Commands sent to the switch
# ---------------------------
# system name "core-sw-1"

- name: Read the system name from the switch
  ale.aos8.aos8_hostname:
    state: gathered

- name: Replace the system name
  ale.aos8.aos8_hostname:
    config:
      hostname: edge-sw-1
    state: replaced

# Commands sent to the switch
# ---------------------------
# system name "edge-sw-1"

- name: Override the system name
  ale.aos8.aos8_hostname:
    config:
      hostname: val-os1
    state: overridden

# Commands sent to the switch
# ---------------------------
# system name "val-os1"

- name: Show the command for a system name without connecting to the switch
  ale.aos8.aos8_hostname:
    config:
      hostname: core-sw-1
    state: rendered

# Value returned as rendered
# --------------------------
# - system name "core-sw-1"

- name: Convert a configuration line into structured data
  ale.aos8.aos8_hostname:
    running_config: system name "core-sw-1"
    state: parsed

# Value returned as parsed
# ------------------------
# hostname: core-sw-1
"""

RETURN = r"""
---
before:
  description: The configuration found on the switch before the module ran.
  returned: when O(state) is C(merged) or C(replaced) or C(overridden)
  type: dict
  sample: The configuration in the format of the O(config) option.
after:
  description: The configuration found on the switch after the module ran.
  returned: when the module changed the switch
  type: dict
  sample: The configuration in the format of the O(config) option.
commands:
  description: The commands sent to the switch. In check mode, the commands that would be sent.
  returned: when O(state) is C(merged) or C(replaced) or C(overridden)
  type: list
  elements: str
  sample:
    - system name "core-sw-1"
gathered:
  description: The configuration read from the switch.
  returned: when O(state) is C(gathered)
  type: dict
  sample: The configuration in the format of the O(config) option.
parsed:
  description: The structured data built from O(running_config).
  returned: when O(state) is C(parsed)
  type: dict
  sample:
    hostname: core-sw-1
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - system name "core-sw-1"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.hostname.hostname import (
    HostnameArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.hostname.hostname import (
    Hostname,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=HostnameArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Hostname(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
