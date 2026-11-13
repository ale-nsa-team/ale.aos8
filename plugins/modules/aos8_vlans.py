#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_vlans
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_vlans
short_description: Resource module to configure VLANs
description:
  - This module manages standard VLANs on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
  - VLAN 1 is the default VLAN of the switch. It is never removed.
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
      - A list of VLANs.
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description:
          - ID of the VLAN.
        type: int
        required: true
      name:
        description:
          - Description of the VLAN. The switch names a new VLAN C(VLAN <id>) when no name is given.
        type: str
      admin:
        description:
          - Administrative state of the VLAN. A new VLAN is created enabled.
        type: str
        choices:
          - enable
          - disable
      mtu:
        description:
          - Maximum IP packet size of the VLAN, in bytes. The switch default is 1500.
        type: int
      operational_state:
        description:
          - Operational state of the VLAN. This value is read from the switch and returned by the module.
            It is ignored when given in a task.
        type: str
        choices:
          - enable
          - disable
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show vlan) from the switch.
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
- name: Create two VLANs
  ale.aos8.aos8_vlans:
    config:
      - vlan_id: 30
        name: Voice
        admin: enable
        mtu: 9000
      - vlan_id: 31
    state: merged

# Commands sent to the switch
# ---------------------------
# vlan 30 admin-state enable
# vlan 30 name "Voice"
# vlan 30 mtu-ip 9000
# vlan 31 admin-state enable

- name: Rename a VLAN and disable it
  ale.aos8.aos8_vlans:
    config:
      - vlan_id: 31
        name: Guest
        admin: disable
    state: merged

# Commands sent to the switch
# ---------------------------
# vlan 31 admin-state disable
# vlan 31 name "Guest"

- name: Replace the configuration of VLAN 30 (the MTU goes back to 1500)
  ale.aos8.aos8_vlans:
    config:
      - vlan_id: 30
        name: Voice
    state: replaced

# Commands sent to the switch
# ---------------------------
# vlan 30 mtu-ip 1500

- name: Read the VLANs from the switch
  ale.aos8.aos8_vlans:
    state: gathered

- name: Keep only VLAN 10 and VLAN 30 (every other VLAN except VLAN 1 is removed)
  ale.aos8.aos8_vlans:
    config:
      - vlan_id: 10
        name: VAL-ISL
      - vlan_id: 30
        name: Voice
    state: overridden

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# no vlan 31

- name: Show the commands for a VLAN without connecting to the switch
  ale.aos8.aos8_vlans:
    config:
      - vlan_id: 998
        name: Vlan 998
        admin: disable
    state: rendered

# Value returned as rendered
# --------------------------
# - vlan 998 admin-state disable
# - vlan 998 name "Vlan 998"

- name: Convert the output of show vlan into structured data
  ale.aos8.aos8_vlans:
    running_config: |
      vlan    type   admin   oper    ip    mtu          name
      ------+-------+-------+------+------+------+------------------
      1      std       Ena     Ena   Dis    1500    VLAN 1
      20     std       Ena     Dis   Dis    1280    Users
    state: parsed

# Value returned as parsed
# ------------------------
# - vlan_id: 1
#   name: VLAN 1
#   admin: enable
#   mtu: 1500
#   operational_state: enable
# - vlan_id: 20
#   name: Users
#   admin: enable
#   mtu: 1280
#   operational_state: disable

- name: Remove VLAN 30
  ale.aos8.aos8_vlans:
    config:
      - vlan_id: 30
    state: deleted

# Commands sent to the switch
# ---------------------------
# no vlan 30

- name: Remove every VLAN except VLAN 1
  ale.aos8.aos8_vlans:
    state: deleted

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# no vlan 10
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
    - vlan 30 admin-state enable
    - vlan 30 name "Voice"
    - vlan 30 mtu-ip 9000
    - vlan 31 admin-state enable
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
    - vlan_id: 1
      name: VLAN 1
      admin: enable
      mtu: 1500
      operational_state: enable
    - vlan_id: 20
      name: Users
      admin: enable
      mtu: 1280
      operational_state: disable
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - vlan 998 admin-state disable
    - vlan 998 name "Vlan 998"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.vlans.vlans import (
    VlansArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.vlans.vlans import (
    Vlans,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=VlansArgs.argument_spec,
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

    result = Vlans(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
