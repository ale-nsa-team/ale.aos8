#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_radius_servers
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_radius_servers
short_description: Resource module to configure RADIUS servers
description:
  - This module manages RADIUS servers on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
  - The switch stores the shared secret hashed, so the module cannot tell whether O(config[].key) changed.
    The secret is only sent when the server is created or when another attribute changes.
  - The shared secret is replaced by C(********) in the RV(commands) and RV(rendered) returned by the
    module.
  - Every RADIUS server of the switch must use the same VRF.
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
      - A list of RADIUS servers.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Name of the RADIUS server on the switch.
        type: str
        required: true
      host:
        description:
          - IP address or DNS name of the RADIUS server. Required unless O(state=deleted).
        type: str
      key:
        description:
          - Shared secret of the RADIUS server. Required when the server is created or changed.
        type: str
      auth_port:
        description:
          - UDP port for authentication requests.
        type: int
        default: 1812
      acct_port:
        description:
          - UDP port for accounting requests.
        type: int
        default: 1813
      retransmit:
        description:
          - Number of retries before the server is considered unreachable.
        type: int
        default: 3
      timeout:
        description:
          - Time in seconds the switch waits for an answer from the server.
        type: int
        default: 2
      vrf:
        description:
          - Name of the VRF used to reach the server. The VRF must exist, and every RADIUS server of the
            switch must use the same VRF.
        type: str
        default: default
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show configuration snapshot | grep "aaa radius-server") from the switch.
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
- name: Create RADIUS servers
  ale.aos8.aos8_radius_servers:
    config:
      - name: rad1
        host: 192.168.121.251
        key: Secret123
      - name: rad2
        host: 192.168.121.252
        key: Secret123
        auth_port: 1645
        acct_port: 1646
        retransmit: 5
        timeout: 10
        vrf: default
    state: merged

# Commands sent to the switch
# ---------------------------
# aaa radius-server "rad1" host 192.168.121.251 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813
# aaa radius-server "rad2" host 192.168.121.252 key ******** retransmit 5 timeout 10 auth-port 1645 acct-port 1646

- name: Change the timeout of a server
  ale.aos8.aos8_radius_servers:
    config:
      - name: rad1
        host: 192.168.121.251
        key: Secret123
        timeout: 5
    state: merged

# Commands sent to the switch
# ---------------------------
# aaa radius-server "rad1" host 192.168.121.251 key ******** retransmit 3 timeout 5 auth-port 1812 acct-port 1813

- name: Replace a server (ports, retries and timeout go back to their defaults)
  ale.aos8.aos8_radius_servers:
    config:
      - name: rad2
        host: 192.168.121.252
        key: Secret123
    state: replaced

# Commands sent to the switch
# ---------------------------
# aaa radius-server "rad2" host 192.168.121.252 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813

- name: Read the RADIUS servers from the switch
  ale.aos8.aos8_radius_servers:
    state: gathered

- name: Keep only rad1 (every other RADIUS server is removed)
  ale.aos8.aos8_radius_servers:
    config:
      - name: rad1
        host: 192.168.121.251
        key: Secret123
        timeout: 5
    state: overridden

# Commands sent to the switch
# ---------------------------
# no aaa radius-server "rad2"

- name: Show the commands for a server without connecting to the switch
  ale.aos8.aos8_radius_servers:
    config:
      - name: rad9
        host: 10.0.0.9
        key: Secret123
    state: rendered

# Value returned as rendered
# --------------------------
# - aaa radius-server "rad9" host 10.0.0.9 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813

- name: Convert configuration lines into structured data
  ale.aos8.aos8_radius_servers:
    running_config: |
      aaa radius-server "rad1" host 192.168.121.251 hash-key "25EA0FBE" retransmit 3 timeout 2 auth-port 1812 acct-port 1813 vrf-name default
    state: parsed

# Value returned as parsed
# ------------------------
# - name: rad1
#   host: 192.168.121.251
#   retransmit: 3
#   timeout: 2
#   auth_port: 1812
#   acct_port: 1813
#   vrf: default

- name: Remove a server
  ale.aos8.aos8_radius_servers:
    config:
      - name: rad1
    state: deleted

# Commands sent to the switch
# ---------------------------
# no aaa radius-server "rad1"

- name: Reach the RADIUS server through another VRF (no other server is configured)
  ale.aos8.aos8_radius_servers:
    config:
      - name: rad4
        host: 192.168.121.254
        key: Secret123
        vrf: vrf-val
    state: merged

# Commands sent to the switch
# ---------------------------
# aaa radius-server "rad4" host 192.168.121.254 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port 1813 vrf-name vrf-val

- name: Remove every RADIUS server
  ale.aos8.aos8_radius_servers:
    state: deleted

# Commands sent to the switch
# ---------------------------
# no aaa radius-server "rad4"
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
    - aaa radius-server "rad1" host 192.168.121.251 key ******** retransmit 3 timeout 2 auth-port 1812
      acct-port 1813
    - aaa radius-server "rad2" host 192.168.121.252 key ******** retransmit 5 timeout 10 auth-port 1645
      acct-port 1646
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
    - name: rad1
      host: 192.168.121.251
      retransmit: 3
      timeout: 2
      auth_port: 1812
      acct_port: 1813
      vrf: default
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - aaa radius-server "rad9" host 10.0.0.9 key ******** retransmit 3 timeout 2 auth-port 1812 acct-port
      1813
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.radius_servers.radius_servers import (
    Radius_serversArgs,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.radius_servers.radius_servers import (
    Radius_servers,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Radius_serversArgs.argument_spec,
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

    result = Radius_servers(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
