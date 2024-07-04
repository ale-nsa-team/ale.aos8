#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for aos_ntp
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.argspec.ntp.ntp import (
    Ntp_Args,
)
from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.config.ntp.ntp import (
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