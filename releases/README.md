# Alcatel-Lucent Enterprise AOS 8 Collection

The Ansible Alcatel-Lucent Enterprise AOS 8 collection includes a variety of Ansible content to help automate the management of Alcatel-Lucent Enterprise AOS network appliances.

This collection has been tested against Alcatel-Lucent Enterprise AOS 8.9R03.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.14.0**.

For collections that support Ansible 2.9, please ensure you update your `network_os` to use the
fully qualified collection name (for example, `ale.aos.aos8`).
Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

### Supported connections
The Alcatel-Lucent Enterprise AOS 8 collection supports ``network_cli`` connection.

## Included content

<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
[ale.aos8](https://github.com/ale-nsa-team/ale.aos8/blob/main/docs/ale.aos8_cliconf.rst)|Use aos8 cliconf to run command on ALE AOS 8 platform

### Modules
Name | Description
--- | ---
[ale.aos8_command](https://github.com/ale-nsa-team/ale.aos8/blob/main/docs/ale.aos8_command_module.rst)|Module to run commands on remote devices.
[ale.aos8_facts](https://github.com/ale-nsa-team/ale.aos8/blob/main/docs/ale.aos8_facts_module.rst)|Module to collect facts from remote devices.
[ale.aos8_hostname](https://github.com/ale-nsa-team/ale.aos8/blob/main/docs/ale.aos8_hostname_module.rst)|Resource module to configure hostname.
[ale.aos8_switch_security](https://github.com/ale-nsa-team/ale.aos8/blob/main/docs/ale.aos8_switch_security.rst)|Resource module to configure switch security.
[ale.aos8_vlans](https://github.com/ale-nsa-team/ale.aos8/blob/main/docs/ale.aos8_vlans_module.rst)|Resource module to configure VLANs.
[ale.aos8_l2_interfaces](https://github.com/ale-nsa-team/ale.aos8/blob/main/docs/ale.aos8_l2_interfaces_module.rst)|Resource module to configure L2 interfaces.
[ale.aos8_l3_interfaces](https://github.com/ale-nsa-team/ale.aos8/blob/main/docs/ale.aos8_l3_interfaces_module.rst)|Resource module to configure L3 interfaces.
[ale.aos8_radius_servers](https://github.com/ale-nsa-team/ale.aos8/blob/main/docs/ale.aos8_radius_servers_module.rst)|Resource module to configure Radius Servers.
[ale.aos8_trap_managers](https://github.com/ale-nsa-team/ale.aos8/blob/main/docs/ale.aos8_trap_managers_module.rst)|Resource module to configure Trap Managers.


<!--end collection content-->

Click the ``Content`` button to see the list of content included in this collection.

## Installing this collection

You can install the Alcatel-Lucent Enterprise AOS 8 collection with the Ansible Galaxy CLI:

    git clone https://github.com/ale-nsa-team/ale.aos8.git
    cd ale.aos8
    ansible-galaxy collection install ./ale-aos8-1.0.0.tar.gz

## Using this collection


This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

### Using modules from the Alcatel-Lucent Enterprise AOS 8 collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `ale.aos8.aos8_command`.
The following example task replaces configuration changes in the existing configuration on a Alcatel-Lucent Enterprise AOS 8 network device, using the FQCN:

```yaml
---
  - name: Disable a port.
    ale.aos8.aos8_command:
      commands:
        - interfaces port 1/1/1 admin-state disable
```

## Release notes

<!--Add a link to a changelog.md file or an external docsite to cover this information. -->

Release notes are available [here](https://github.com/ale-nsa-team/ale.aos8/blob/main/CHANGELOG.rst).

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
