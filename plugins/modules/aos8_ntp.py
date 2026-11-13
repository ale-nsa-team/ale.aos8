#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos8_ntp
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
---
module: aos8_ntp
short_description: Resource module to configure NTP servers
description:
  - This module manages the NTP servers on Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
  - The options of an existing server cannot be cleared in place. The module removes the server and creates
    it again when one of its options changes.
  - The NTP configuration is one object, so C(replaced) and C(overridden) do the same thing.
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
      - The NTP configuration.
    type: dict
    suboptions:
      servers:
        description:
          - A list of NTP servers.
        type: list
        elements: dict
        suboptions:
          server:
            description:
              - IP address or DNS name of the NTP server.
            type: str
            required: true
          minpoll:
            description:
              - Minimum poll interval, as a power of 2 in seconds. The switch default is 6 (64 seconds).
            type: int
          maxpoll:
            description:
              - Maximum poll interval, as a power of 2 in seconds. The switch default is 10 (1024 seconds).
            type: int
          version:
            description:
              - NTP version used with this server. The switch default is 4.
            type: int
            choices:
              - 1
              - 2
              - 3
              - 4
          prefer:
            description:
              - Marks the server as the preferred server.
            type: bool
          burst:
            description:
              - Sends a burst of packets at each poll interval when the server is reachable.
            type: bool
          iburst:
            description:
              - Sends a burst of packets when the server is unreachable, to speed up the first synchronization.
            type: bool
  running_config:
    description:
      - Text to convert into structured data. Only used with O(state=parsed).
      - Give the output of C(show configuration snapshot ntp) from the switch.
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
- name: Add NTP servers
  ale.aos8.aos8_ntp:
    config:
      servers:
        - server: 192.168.121.250
        - server: 192.168.121.251
          prefer: true
        - server: 192.168.121.252
          minpoll: 4
          maxpoll: 12
          version: 3
        - server: 192.168.121.253
          burst: true
          iburst: true
    state: merged

# Commands sent to the switch
# ---------------------------
# ntp server 192.168.121.250
# ntp server 192.168.121.251 prefer
# ntp server 192.168.121.252 minpoll 4 maxpoll 12 version 3
# ntp server 192.168.121.253 burst iburst

- name: Set the NTP version of servers
  ale.aos8.aos8_ntp:
    config:
      servers:
        - server: 192.168.121.247
          version: 1
        - server: 192.168.121.248
          version: 2
        - server: 192.168.121.250
          version: 4
    state: merged

# Commands sent to the switch
# ---------------------------
# ntp server 192.168.121.247 version 1
# ntp server 192.168.121.248 version 2

- name: Keep two servers and clear the prefer option
  ale.aos8.aos8_ntp:
    config:
      servers:
        - server: 192.168.121.250
        - server: 192.168.121.251
    state: replaced

# Commands sent to the switch
# ---------------------------
# no ntp server 192.168.121.247
# no ntp server 192.168.121.248
# no ntp server 192.168.121.252
# no ntp server 192.168.121.253
# no ntp server 192.168.121.251
# ntp server 192.168.121.251

- name: Read the NTP servers from the switch
  ale.aos8.aos8_ntp:
    state: gathered

- name: Keep only one server
  ale.aos8.aos8_ntp:
    config:
      servers:
        - server: 192.168.121.250
    state: overridden

# Commands sent to the switch
# ---------------------------
# no ntp server 192.168.121.251

- name: Show the commands for an NTP server without connecting to the switch
  ale.aos8.aos8_ntp:
    config:
      servers:
        - server: 10.0.0.1
          prefer: true
    state: rendered

# Value returned as rendered
# --------------------------
# - ntp server 10.0.0.1 prefer

- name: Convert configuration lines into structured data
  ale.aos8.aos8_ntp:
    running_config: |
      ntp server 192.168.121.250
      ntp server 192.168.121.251 prefer
    state: parsed

# Value returned as parsed
# ------------------------
# servers:
#   - server: 192.168.121.250
#   - server: 192.168.121.251
#     prefer: true

- name: Remove every NTP server
  ale.aos8.aos8_ntp:
    state: deleted

# Commands sent to the switch
# ---------------------------
# no ntp server 192.168.121.250
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
    - ntp server 192.168.121.250
    - ntp server 192.168.121.251 prefer
    - ntp server 192.168.121.252 minpoll 4 maxpoll 12 version 3
    - ntp server 192.168.121.253 burst iburst
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
    servers:
      - server: 192.168.121.250
      - server: 192.168.121.251
        prefer: true
rendered:
  description: The commands for the given configuration.
  returned: when O(state) is C(rendered)
  type: list
  elements: str
  sample:
    - ntp server 10.0.0.1 prefer
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.argspec.ntp.ntp import (
    Ntp_Args,
)
from ansible_collections.ale.aos8.plugins.module_utils.network.aos8.config.ntp.ntp import (
    Ntp,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Ntp_Args.argument_spec,
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

    result = Ntp(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
