.. _ale.aos8.aos8_command_module:

ale.aos8.aos8_command
*********************

**Run commands on AOS 8 devices**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- Sends commands to an Alcatel-Lucent Enterprise OmniSwitch running AOS 8 and returns the output.
- The module always reports ``changed=false``, also when a command changes the configuration. Use ``ale.aos8.aos8_config`` or the resource modules to configure the switch.
- In check mode, only commands that start with ``show`` are sent.

Parameters
----------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Parameter
     - Type
     - Choices / default
     - Comments
   * - ``commands``
     - list / elements=raw / **required**
     -
     - List of commands to send to the switch. The output of each command is returned. A command that asks for a confirmation is given as a dictionary with the keys ``command``, ``prompt`` (a regular expression that matches the question) and ``answer``.

Notes
-----

- Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
- This module works with connection ``ansible.netcommon.network_cli``.
- The task fails when the switch answers a command with an error.

Examples
--------

.. code-block:: yaml

    - name: Run a show command
      ale.aos8.aos8_command:
        commands: show system

    - name: Run several commands
      ale.aos8.aos8_command:
        commands:
          - show vlan
          - show ip interface

    - name: Run a command that changes the switch
      ale.aos8.aos8_command:
        commands:
          - interfaces port 1/1/20 admin-state disable

    - name: Answer a confirmation question
      ale.aos8.aos8_command:
        commands:
          - command: no vlan 40
            prompt: '[Yy]/[Nn]'
            answer: y

    - name: In check mode only show commands are sent
      ale.aos8.aos8_command:
        commands:
          - show vlan
          - vlan 41 admin-state enable
      check_mode: true

Return values
-------------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Key
     - Type
     - Returned
     - Description
   * - ``stdout``
     - list
     - always
     - The output of each command. Sample: ``["System:\n  Description:  Alcatel-Lucent Enterprise OS687024-SIM 8.11.162.R01 GA"]``
   * - ``stdout_lines``
     - list
     - always
     - The output of each command, split into lines. Sample: ``[["System:", "  Description:  Alcatel-Lucent Enterprise OS687024-SIM 8.11.162.R01 GA"]]``

Authors
-------

- Samuel Yip Kah Yean (@samuelyip74)
- Mathias Guillemot (@mathias-gt)
