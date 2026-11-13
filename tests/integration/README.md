# Lab tests

These tests run every example of the module documentation against an OmniSwitch
(a virtual one is enough) and check the commands sent, the result on the switch
and that a second run changes nothing.

**They create and remove configuration. Never run them against a production switch.**

## State the switch must be in

Setting | Value
--- | ---
System name | `val-os1`
VLAN 10 | name `VAL-ISL`, port 1/1/1 tagged
IP interface | `int_10`, 10.10.10.1/24 on VLAN 10
Authentication | `aaa authentication default`, `console` and `ssh` set to `local`
Nothing else | no other VLAN, IP interface, static route, OSPF, BGP, NTP, RADIUS or SNMP station configuration

`tests/integration/lab/` holds a containerlab topology and start-up configuration that give this state.

## Run

```bash
cp tests/integration/inventory.example.yml tests/integration/inventory.yml   # set the address and password
cd tests/integration
ansible-playbook -i inventory.yml lab.yml                            # every target
ansible-playbook -i inventory.yml lab.yml -e targets=aos8_vlans      # one target
```

The last tasks print one `LABTEST <target>: ok` or `LABTEST <target>: FAILED ...` line for each target.

## Adding a test

Each folder of `targets/` is one module. Add the task to `targets/<module>/tasks/main.yaml`,
then copy the same task to the `EXAMPLES` of the module. `tests/unit/test_documentation.py`
fails when an example or an option of the documentation has no task here.
