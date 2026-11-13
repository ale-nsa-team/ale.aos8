#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_trap_managers
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_trap_managers
short_description: Resource module to configure SNMP trap stations
description:
  - This module manages the SNMP stations that receive traps from Alcatel-Lucent Enterprise OmniSwitch
    devices running AOS 8.
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
      - A list of SNMP trap stations.
    type: list
    elements: dict
    suboptions:
      host:
        description:
          - IP address of the station that receives the traps.
        type: str
        required: true
      port:
        description:
          - UDP port the traps are sent to.
        type: int
        default: 162
      string:
        description:
          - Name of the switch user account used to send the traps. The user must exist on the switch.
        type: str
        default: public
      version:
        description:
          - SNMP version of the traps. V(v3) needs a user created with SNMP authentication and privacy,
            for example C(user <name> password <password> read-only all sha+aes priv-password <password>).
        type: str
        choices:
          - v1
          - v2
          - v3
        default: v2
      state:
        description:
          - Whether traps are sent to the station.
        type: str
        choices:
          - enable
          - disable
        default: enable
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show configuration snapshot | grep "snmp station") from the switch.
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
- name: Add SNMP trap stations
  ale.aos8.aos8_trap_managers:
    config:
      - host: 192.168.121.250
        string: snmpuser
        version: v2
        state: enable
      - host: 192.168.121.249
        port: 1162
        string: snmpuser
        version: v1
        state: disable
      - host: 192.168.121.248
        string: snmpv3user
        version: v3
    state: merged

# Commands sent to the switch
# ---------------------------
# snmp station 192.168.121.250 162 "snmpuser" v2 enable
# snmp station 192.168.121.249 1162 "snmpuser" v1 disable
# snmp station 192.168.121.248 162 "snmpv3user" v3 enable

- name: Enable a station
  ale.aos8.aos8_trap_managers:
    config:
      - host: 192.168.121.249
        port: 1162
        string: snmpuser
        version: v1
        state: enable
    state: merged

# Commands sent to the switch
# ---------------------------
# snmp station 192.168.121.249 1162 "snmpuser" v1 enable

- name: Replace a station (port and version go back to their defaults)
  ale.aos8.aos8_trap_managers:
    config:
      - host: 192.168.121.249
        string: snmpuser
    state: replaced

# Commands sent to the switch
# ---------------------------
# snmp station 192.168.121.249 162 "snmpuser" v2 enable

- name: Read the SNMP trap stations from the switch
  ale.aos8.aos8_trap_managers:
    state: gathered

- name: Keep only one station (every other station is removed)
  ale.aos8.aos8_trap_managers:
    config:
      - host: 192.168.121.250
        string: snmpuser
    state: overridden

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# no snmp station 192.168.121.249
# no snmp station 192.168.121.248

- name: Show the commands for a station without connecting to the switch
  ale.aos8.aos8_trap_managers:
    config:
      - host: 10.0.0.9
        port: 1162
        string: ops
        version: v3
    state: rendered

# Value returned as rendered
# --------------------------
# - snmp station 10.0.0.9 1162 "ops" v3 enable

- name: Convert configuration lines into structured data
  ale.aos8.aos8_trap_managers:
    running_config: |
      snmp station 192.168.121.250 162 "valtest" v2 enable
      snmp station 192.168.121.249 162 "valtest" v1 disable
    state: parsed

# Value returned as parsed
# ------------------------
# - host: 192.168.121.250
#   port: 162
#   string: valtest
#   version: v2
#   state: enable
# - host: 192.168.121.249
#   port: 162
#   string: valtest
#   version: v1
#   state: disable

- name: Remove a station
  ale.aos8.aos8_trap_managers:
    config:
      - host: 192.168.121.250
    state: deleted

# Commands sent to the switch
# ---------------------------
# no snmp station 192.168.121.250

- name: Remove every station
  ale.aos8.aos8_trap_managers:
    state: deleted

# Commands sent to the switch
# ---------------------------
# no snmp station 192.168.121.249
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
    - snmp station 192.168.121.250 162 "snmpuser" v2 enable
    - snmp station 192.168.121.249 1162 "snmpuser" v1 disable
    - snmp station 192.168.121.248 162 "snmpv3user" v3 enable
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
    - host: 192.168.121.250
      port: 162
      string: valtest
      version: v2
      state: enable
    - host: 192.168.121.249
      port: 162
      string: valtest
      version: v1
      state: disable
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - snmp station 10.0.0.9 1162 "ops" v3 enable
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.trap_managers.trap_managers import (
    Trap_managersArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.trap_managers.trap_managers import (
    Trap_managers,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Trap_managersArgs.argument_spec,
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

    result = Trap_managers(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
