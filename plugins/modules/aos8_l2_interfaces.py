#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_l2_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_l2_interfaces
short_description: Resource module to configure VLAN membership of ports and link aggregates
description:
  - This module manages the VLAN port associations (VPA) of ports and link aggregates on Alcatel-Lucent
    Enterprise OmniSwitch devices running AOS 8.
  - A port or link aggregate is an untagged member of one VLAN (its default VLAN) and can be a tagged
    member of other VLANs.
  - Untagged membership of VLAN 1 is the factory default of every port. The module never removes it.
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
      - A list of VLAN memberships.
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description:
          - ID of the VLAN. The VLAN must exist.
        type: int
        required: true
      port_number:
        description:
          - Port in C(chassis/slot/port) format, for example V(1/1/5), or ID of a link aggregate, for
            example V(5).
        type: str
        required: true
      port_type:
        description:
          - Whether O(config[].port_number) is a port or a link aggregate. The module works this out from
            the format of O(config[].port_number) when it is left out.
        type: str
        choices:
          - port
          - linkagg
      mode:
        description:
          - V(untagged) makes the VLAN the default VLAN of the port.
          - V(tagged) adds the port to the VLAN with 802.1Q tagging.
          - Required unless O(state=deleted).
        type: str
        choices:
          - untagged
          - tagged
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show vlan members) from the switch.
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
- name: Add a port and a link aggregate to VLANs
  ale.aos8.aos8_l2_interfaces:
    config:
      - vlan_id: 30
        port_type: port
        port_number: 1/1/5
        mode: untagged
      - vlan_id: 31
        port_number: 1/1/5
        mode: tagged
      - vlan_id: 30
        port_type: linkagg
        port_number: '5'
        mode: tagged
    state: merged

# Commands sent to the switch
# ---------------------------
# vlan 30 members port 1/1/5 untagged
# vlan 31 members port 1/1/5 tagged
# vlan 30 members linkagg 5 tagged

- name: Change link aggregate 5 from tagged to untagged in VLAN 30
  ale.aos8.aos8_l2_interfaces:
    config:
      - vlan_id: 30
        port_number: '5'
        mode: untagged
    state: merged

# Commands sent to the switch
# ---------------------------
# no vlan 30 members linkagg 5
# vlan 30 members linkagg 5 untagged

- name: Make port 1/1/6 a tagged member of VLAN 31
  ale.aos8.aos8_l2_interfaces:
    config:
      - vlan_id: 31
        port_number: 1/1/6
        mode: tagged
    state: replaced

# Commands sent to the switch
# ---------------------------
# vlan 31 members port 1/1/6 tagged

- name: Read the VLAN memberships from the switch
  ale.aos8.aos8_l2_interfaces:
    state: gathered

- name: Keep only these memberships (every other one is removed, except untagged VLAN 1)
  ale.aos8.aos8_l2_interfaces:
    config:
      - vlan_id: 10
        port_number: 1/1/1
        mode: tagged
      - vlan_id: 30
        port_number: 1/1/5
        mode: untagged
    state: overridden

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# no vlan 31 members port 1/1/5
# no vlan 31 members port 1/1/6
# no vlan 30 members linkagg 5

- name: Show the commands for a membership without connecting to the switch
  ale.aos8.aos8_l2_interfaces:
    config:
      - vlan_id: 30
        port_number: 1/1/7
        mode: untagged
    state: rendered

# Value returned as rendered
# --------------------------
# - vlan 30 members port 1/1/7 untagged

- name: Convert the output of show vlan members into structured data
  ale.aos8.aos8_l2_interfaces:
    running_config: |
      vlan       port         type         status
      --------+------------+------------+--------------
        1         1/1/1        untagged   forwarding
        99        0/5          tagged     inactive
    state: parsed

# Value returned as parsed
# ------------------------
# - vlan_id: 1
#   port_number: 1/1/1
#   port_type: port
#   mode: untagged
# - vlan_id: 99
#   port_number: '5'
#   port_type: linkagg
#   mode: tagged

- name: Remove port 1/1/5 from VLAN 30
  ale.aos8.aos8_l2_interfaces:
    config:
      - vlan_id: 30
        port_number: 1/1/5
    state: deleted

# Commands sent to the switch
# ---------------------------
# no vlan 30 members port 1/1/5

- name: Remove every membership except untagged VLAN 1
  ale.aos8.aos8_l2_interfaces:
    state: deleted

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# no vlan 10 members port 1/1/1
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
    - vlan 30 members port 1/1/5 untagged
    - vlan 31 members port 1/1/5 tagged
    - vlan 30 members linkagg 5 tagged
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
      port_number: 1/1/1
      port_type: port
      mode: untagged
    - vlan_id: 99
      port_number: '5'
      port_type: linkagg
      mode: tagged
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - vlan 30 members port 1/1/7 untagged
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.l2_interfaces.l2_interfaces import (
    L2_interfacesArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.l2_interfaces.l2_interfaces import (
    L2_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=L2_interfacesArgs.argument_spec,
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

    result = L2_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
