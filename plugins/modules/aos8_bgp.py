#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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

    :returns: the result from module invocation
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
