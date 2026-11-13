# Alcatel-Lucent Enterprise AOS 8 Collection

[![Collection Tests](https://github.com/ale-nsa-team/ale.aos8/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/ale-nsa-team/ale.aos8/actions/workflows/tests.yml)

The Ansible Alcatel-Lucent Enterprise AOS 8 collection includes a variety of Ansible content to help automate the management of Alcatel-Lucent Enterprise OmniSwitch network appliances running AOS 8.

This collection has been tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.

## Requirements

- Python 3.10 or later.
- The `ansible.netcommon` collection, version 6.1.0 or later.
- The Python package `ansible-pylibssh`, listed in the collection's [requirements.txt](https://github.com/ale-nsa-team/ale.aos8/blob/master/requirements.txt).

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against the following Ansible versions: **>=2.16.0**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

### Supported connections

The Alcatel-Lucent Enterprise AOS 8 collection supports the ``network_cli`` connection.

## Included content

<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
[ale.aos8.aos8](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_cliconf.rst)|Use aos8 cliconf to run commands on Alcatel-Lucent Enterprise AOS 8 devices

### Modules
Name | Description
--- | ---
[ale.aos8.aos8_bgp](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_bgp_module.rst)|Resource module to configure BGP
[ale.aos8.aos8_command](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_command_module.rst)|Run commands on AOS 8 devices
[ale.aos8.aos8_config](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_config_module.rst)|Send configuration lines to AOS 8 devices
[ale.aos8.aos8_facts](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_facts_module.rst)|Collect facts from AOS 8 devices
[ale.aos8.aos8_hostname](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_hostname_module.rst)|Resource module to configure the system name
[ale.aos8.aos8_l2_interfaces](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_l2_interfaces_module.rst)|Resource module to configure VLAN membership of ports and link aggregates
[ale.aos8.aos8_l3_interfaces](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_l3_interfaces_module.rst)|Resource module to configure IP interfaces
[ale.aos8.aos8_ntp](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_ntp_module.rst)|Resource module to configure NTP servers
[ale.aos8.aos8_ospfv2](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_ospfv2_module.rst)|Resource module to configure OSPFv2
[ale.aos8.aos8_radius_servers](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_radius_servers_module.rst)|Resource module to configure RADIUS servers
[ale.aos8.aos8_static_routes](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_static_routes_module.rst)|Resource module to configure IPv4 static routes
[ale.aos8.aos8_switch_security](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_switch_security_module.rst)|Resource module to configure Authenticated Switch Access
[ale.aos8.aos8_trap_managers](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_trap_managers_module.rst)|Resource module to configure SNMP trap stations
[ale.aos8.aos8_vlans](https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/ale.aos8.aos8_vlans_module.rst)|Resource module to configure VLANs

<!--end collection content-->

## Installing this collection

You can install the Alcatel-Lucent Enterprise AOS 8 collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install ale.aos8

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: ale.aos8
```

## Using this collection

### Inventory

```yaml
all:
  hosts:
    switch1:
      ansible_host: 192.0.2.10
  vars:
    ansible_connection: ansible.netcommon.network_cli
    ansible_network_os: ale.aos8.aos8
    ansible_user: admin
    ansible_password: "{{ vault_switch_password }}"
    # saving to flash can take a long time
    ansible_command_timeout: 90
```

### Saving the configuration

After each change, the collection saves the configuration to flash with `write memory flash-synchro`. Two connection variables control this:

Variable | Default | Effect
--- | --- | ---
`ansible_aos_write_memory_flash` | `true` | Saves the configuration to flash after each change.
`ansible_aos_flash_synchro_flag` | `false` | After saving, certifies the configuration with `copy running certified`.

Saving needs `ansible_command_timeout` to be 60 seconds or more, certifying 120 seconds or more. Set `ansible_aos_write_memory_flash: false` to keep changes in the running configuration only.

The switch must run from the working directory. Changes are refused when it runs from the certified directory.

### Using modules from the collection in your playbooks

You can call modules by their Fully Qualified Collection Name (FQCN), such as `ale.aos8.aos8_vlans`.
The following example task creates two VLANs:

```yaml
---
- name: Create two VLANs
  ale.aos8.aos8_vlans:
    config:
      - vlan_id: 30
        name: Voice
      - vlan_id: 31
    state: merged
```

This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html). Each one accepts the states `merged`, `replaced`, `overridden`, `deleted`, `gathered`, `rendered` and `parsed` (`aos8_hostname` has no `deleted` state).

### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Testing

Every example and every option in the module documentation is run against an OmniSwitch by the lab tests in `tests/integration`. A unit test (`tests/unit/test_documentation.py`) fails when the documentation and the lab tests drift apart.

Tests | Command
--- | ---
Sanity | `ansible-test sanity --docker default`
Unit | `ansible-test units --docker default`
Lab | `ansible-playbook -i tests/integration/inventory.yml tests/integration/lab.yml` (see [tests/integration/README.md](https://github.com/ale-nsa-team/ale.aos8/blob/master/tests/integration/README.md))

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Alcatel-Lucent Enterprise AOS 8 collection repository](https://github.com/ale-nsa-team/ale.aos8).

After changing the documentation of a module, run `python tools/build_docs.py` to rebuild `docs/` and the content table above, and add the matching task to `tests/integration`.

## Release notes

Release notes are available [here](https://github.com/ale-nsa-team/ale.aos8/blob/master/CHANGELOG.rst).

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
