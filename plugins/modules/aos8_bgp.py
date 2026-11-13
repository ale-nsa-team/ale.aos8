#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_bgp
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_bgp
short_description: Resource module to configure BGP
description:
  - This module manages the BGP autonomous system number, global state and neighbors of the default VRF
    on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
  - The module loads the BGP software (C(ip load bgp)) when it is not loaded yet.
  - The BGP configuration is one object, so C(replaced) and C(overridden) do the same thing.
  - The autonomous system number cannot be removed. C(deleted) disables BGP and removes the neighbors.
version_added: 1.0.0
author:
  - Maxime Descloux (@MaximeALE)
  - Mathias Guillemot (@mathias-gt)
notes:
  - Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
  - This module works with connection C(ansible.netcommon.network_cli).
  - After a change, the configuration is saved to flash with C(write memory flash-synchro), unless C(ansible_aos_write_memory_flash)
    is set to C(false). Saving needs C(ansible_command_timeout) to be 60 seconds or more.
options:
  config:
    description:
      - The BGP configuration.
    type: dict
    suboptions:
      as_number:
        description:
          - Autonomous system number of the switch.
        type: str
      bgp_admin_state:
        description:
          - Administrative state of BGP on the switch.
        type: str
        choices:
          - enable
          - disable
      neighbor:
        description:
          - A list of BGP neighbors.
        type: list
        elements: dict
        suboptions:
          neighbor_address:
            description:
              - IPv4 address of the neighbor.
            type: str
            required: true
            aliases:
              - peer
          remote_as:
            description:
              - Autonomous system number of the neighbor.
            type: str
          neighbor_admin_state:
            description:
              - Administrative state of the neighbor. A new neighbor is disabled.
            type: str
            choices:
              - enable
              - disable
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show configuration snapshot bgp) from the switch.
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
- name: Configure BGP with one neighbor
  ale.aos8.aos8_bgp:
    config:
      as_number: '65001'
      bgp_admin_state: enable
      neighbor:
        - neighbor_address: 10.10.10.254
          remote_as: '65002'
          neighbor_admin_state: enable
    state: merged

# Commands sent to the switch (other entries found on the switch are removed in the same way)
# -------------------------------------------------------------------------------------------
# ip bgp neighbor 10.10.10.254
# ip bgp neighbor 10.10.10.254 remote-as 65002
# ip bgp neighbor 10.10.10.254 admin-state enable
# ip bgp admin-state enable

- name: Disable a neighbor (peer is an alias of neighbor_address)
  ale.aos8.aos8_bgp:
    config:
      neighbor:
        - peer: 10.10.10.254
          neighbor_admin_state: disable
    state: merged

# Commands sent to the switch
# ---------------------------
# ip bgp neighbor 10.10.10.254 admin-state disable

- name: Replace the neighbors
  ale.aos8.aos8_bgp:
    config:
      as_number: '65001'
      bgp_admin_state: enable
      neighbor:
        - neighbor_address: 10.10.10.253
          remote_as: '65003'
    state: replaced

# Commands sent to the switch
# ---------------------------
# no ip bgp neighbor 10.10.10.254
# ip bgp neighbor 10.10.10.253
# ip bgp neighbor 10.10.10.253 remote-as 65003

- name: Read the BGP configuration from the switch
  ale.aos8.aos8_bgp:
    state: gathered

- name: Disable BGP and keep the neighbor
  ale.aos8.aos8_bgp:
    config:
      as_number: '65001'
      bgp_admin_state: disable
      neighbor:
        - neighbor_address: 10.10.10.253
          remote_as: '65003'
    state: overridden

# Commands sent to the switch
# ---------------------------
# ip bgp admin-state disable

- name: Show the commands for a BGP configuration without connecting to the switch
  ale.aos8.aos8_bgp:
    config:
      as_number: '65010'
      bgp_admin_state: enable
    state: rendered

# Value returned as rendered
# --------------------------
# - ip load bgp
# - ip bgp autonomous-system 65010
# - ip bgp admin-state enable

- name: Convert configuration lines into structured data
  ale.aos8.aos8_bgp:
    running_config: |
      ip load bgp
      ip bgp autonomous-system 65001
      ip bgp neighbor 10.10.10.2
      ip bgp neighbor 10.10.10.2 remote-as 65002
      ip bgp neighbor 10.10.10.2 admin-state enable
      ip bgp admin-state enable
    state: parsed

# Value returned as parsed
# ------------------------
# as_number: '65001'
# bgp_admin_state: enable
# neighbor:
#   - neighbor_address: 10.10.10.2
#     remote_as: '65002'
#     neighbor_admin_state: enable

- name: Remove every neighbor and disable BGP
  ale.aos8.aos8_bgp:
    state: deleted

# Commands sent to the switch
# ---------------------------
# no ip bgp neighbor 10.10.10.253
"""

RETURN = r"""
---
before:
  description: The configuration found on the switch before the module ran.
  returned: when O(state) is C(merged) or C(replaced) or C(overridden) or C(deleted)
  type: dict
  sample: The configuration in the format of the O(config) option.
after:
  description: The configuration found on the switch after the module ran.
  returned: when the module changed the switch
  type: dict
  sample: The configuration in the format of the O(config) option.
commands:
  description: The commands sent to the switch. In check mode, the commands that would be sent.
  returned: when O(state) is C(merged) or C(replaced) or C(overridden) or C(deleted)
  type: list
  elements: str
  sample:
    - ip bgp neighbor 10.10.10.254
    - ip bgp neighbor 10.10.10.254 remote-as 65002
    - ip bgp neighbor 10.10.10.254 admin-state enable
    - ip bgp admin-state enable
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
    as_number: '65001'
    bgp_admin_state: enable
    neighbor:
      - neighbor_address: 10.10.10.2
        remote_as: '65002'
        neighbor_admin_state: enable
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - ip load bgp
    - ip bgp autonomous-system 65010
    - ip bgp admin-state enable
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.bgp.bgp import (
    Bgp_Args,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.bgp.bgp import (
    Bgp,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bgp_Args.argument_spec,
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

    result = Bgp(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
