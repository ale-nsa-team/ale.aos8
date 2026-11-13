#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_switch_security
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_switch_security
short_description: Resource module to configure Authenticated Switch Access
description:
  - This module sets which AAA server authenticates each management access method (console, Telnet, SSH,
    FTP, HTTP, SNMP) on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
  - C(deleted) sets an access method back to the servers of the C(default) access method. The C(default)
    access method itself is never reset.
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
      - A list of access methods.
    type: list
    elements: dict
    suboptions:
      access_method:
        description:
          - Management access method. V(default) applies to every method that has no setting of its own.
        type: str
        required: true
        choices:
          - default
          - console
          - telnet
          - ssh
          - snmp
          - http
          - ftp
      aaa_servers_name:
        description:
          - Name of the AAA server that authenticates the access method, or V(local) for the local user
            database. Required unless O(state=deleted).
        type: str
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show configuration snapshot | grep "aaa authentication") from the switch.
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
      - C(deleted) removes the given entries. Without O(config), every entry of this resource is removed.
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
      - deleted
      - gathered
      - rendered
      - parsed
    default: merged
"""

EXAMPLES = r"""
- name: Authenticate Telnet, FTP and SNMP access with the local user database
  ale.aos8.aos8_switch_security:
    config:
      - access_method: telnet
        aaa_servers_name: local
      - access_method: ftp
        aaa_servers_name: local
      - access_method: snmp
        aaa_servers_name: local
    state: merged

# Commands sent to the switch
# ---------------------------
# aaa authentication telnet "local"
# aaa authentication ftp "local"
# aaa authentication snmp "local"

- name: Set the server of HTTP access
  ale.aos8.aos8_switch_security:
    config:
      - access_method: http
        aaa_servers_name: local
    state: replaced

# Commands sent to the switch
# ---------------------------
# aaa authentication http "local"

- name: Read the access methods from the switch
  ale.aos8.aos8_switch_security:
    state: gathered

- name: Set FTP access back to the default servers
  ale.aos8.aos8_switch_security:
    config:
      - access_method: ftp
    state: deleted

# Commands sent to the switch
# ---------------------------
# aaa authentication ftp default

- name: Keep only these access methods (every other one goes back to the default servers)
  ale.aos8.aos8_switch_security:
    config:
      - access_method: default
        aaa_servers_name: local
      - access_method: console
        aaa_servers_name: local
      - access_method: ssh
        aaa_servers_name: local
    state: overridden

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# aaa authentication telnet default
# aaa authentication http default
# aaa authentication snmp default

- name: Show the commands for an access method without connecting to the switch
  ale.aos8.aos8_switch_security:
    config:
      - access_method: ssh
        aaa_servers_name: rad1
    state: rendered

# Value returned as rendered
# --------------------------
# - aaa authentication ssh "rad1"

- name: Convert configuration lines into structured data
  ale.aos8.aos8_switch_security:
    running_config: |
      aaa authentication default "local"
      aaa authentication console "local"
    state: parsed

# Value returned as parsed
# ------------------------
# - access_method: default
#   aaa_servers_name: local
# - access_method: console
#   aaa_servers_name: local
"""

RETURN = r"""
---
before:
  description: The configuration found on the switch before the module ran.
  returned: when O(state) is C(merged) or C(replaced) or C(overridden) or C(deleted)
  type: list
  elements: dict
  sample: The configuration in the format of the O(config) option.
after:
  description: The configuration found on the switch after the module ran.
  returned: when the module changed the switch
  type: list
  elements: dict
  sample: The configuration in the format of the O(config) option.
commands:
  description: The commands sent to the switch. In check mode, the commands that would be sent.
  returned: when O(state) is C(merged) or C(replaced) or C(overridden) or C(deleted)
  type: list
  elements: str
  sample:
    - aaa authentication telnet "local"
    - aaa authentication ftp "local"
    - aaa authentication snmp "local"
gathered:
  description: The configuration read from the switch.
  returned: when O(state) is C(gathered)
  type: list
  elements: dict
  sample: The configuration in the format of the O(config) option.
parsed:
  description: The structured data built from O(running_config).
  returned: when O(state) is C(parsed)
  type: list
  elements: dict
  sample:
    - access_method: default
      aaa_servers_name: local
    - access_method: console
      aaa_servers_name: local
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - aaa authentication ssh "rad1"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.switch_security.switch_security import (
    Switch_securityArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.switch_security.switch_security import (
    Switch_security,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Switch_securityArgs.argument_spec,
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

    result = Switch_security(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
