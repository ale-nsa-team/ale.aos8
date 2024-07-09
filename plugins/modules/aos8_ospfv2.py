from ansible.module_utils.basic import AnsibleModule

from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.argspec.ospfv2.ospfv2 import (
    OspfV2_Args,
)
from ansible_collections.alcatel.aos8.plugins.module_utils.network.aos8.config.ospfv2.ospfv2 import (
    Ospfv2,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """

    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]
    mutually_exclusive = [("config", "running_config")]

    module = AnsibleModule(
        argument_spec=OspfV2_Args.argument_spec,
        required_if=required_if,
        supports_check_mode=True,
        mutually_exclusive=mutually_exclusive,
    )

    result = Ospfv2(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
