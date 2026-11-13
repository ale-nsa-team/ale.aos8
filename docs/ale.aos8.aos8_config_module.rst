.. _ale.aos8.aos8_config_module:

ale.aos8.aos8_config
********************

**Send configuration lines to AOS 8 devices**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- Sends configuration lines to an Alcatel-Lucent Enterprise OmniSwitch running AOS 8.
- Each line is compared with the output of ``show configuration snapshot``. Only the lines that are not found there are sent.
- Write the lines the way the switch shows them in ``show configuration snapshot``, otherwise they are sent again at every run.

Parameters
----------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Parameter
     - Type
     - Choices / default
     - Comments
   * - ``after``
     - list / elements=str
     -
     - Commands to send after the configuration lines, when at least one line has to be sent.
   * - ``backup``
     - bool
     - Default: ``false``
     - Saves the output of ``show configuration snapshot``, taken before any change, to a file on the Ansible controller. Without ``backup_options``, the file is written to the ``backup`` folder next to the playbook.
   * - ``backup_options``
     - dict
     -
     - Where the backup file is written. Only used when ``backup=true``.
   * - – ``dir_path``
     - path
     -
     - Folder the backup file is written to. It is created when it does not exist.
   * - – ``filename``
     - str
     -
     - Name of the backup file. The default is ``<hostname>_config.<date>@<time>``.
   * - ``before``
     - list / elements=str
     -
     - Commands to send before the configuration lines, when at least one line has to be sent.
   * - ``diff_against``
     - str
     - ``running`` (default), ``intended``
     - What the configuration is compared with when the task runs with ``--diff``. ``running`` shows the changes made by the task. ``intended`` compares the configuration of the switch with ``intended_config``.
   * - ``diff_ignore_lines``
     - list / elements=str
     -
     - Lines to leave out of the comparison. Each entry is a line or a regular expression.
   * - ``intended_config``
     - str
     -
     - The configuration the switch is expected to have. Required with ``diff_against=intended``.
   * - ``lines``
     - list / elements=str
     -
     - The configuration lines to send, in the order given. Aliases: commands
   * - ``match``
     - str
     - ``line`` (default), ``none``
     - ``line`` only sends the lines that are not in the configuration of the switch. ``none`` sends every line without comparing.
   * - ``running_config``
     - str
     -
     - Configuration to compare the lines with, instead of reading it from the switch. Aliases: config
   * - ``save_when``
     - str
     - ``always``, ``never`` (default), ``modified``, ``changed``
     - When the configuration is saved to flash with ``write memory flash-synchro``. ``always`` saves at every run. ``never`` does not save. ``modified`` saves when the switch reports that the running configuration is not saved. ``changed`` saves when the task changed the configuration.
   * - ``src``
     - str
     -
     - Path of a file on the Ansible controller that holds the configuration lines. The file can be a Jinja2 template. A relative path is looked up in the ``templates`` folder of the role or next to the playbook. ``ansible.netcommon`` deprecates reading templates through this option. Prefer ``lines`` with the ``ansible.builtin.template`` lookup, as shown in the examples. Mutually exclusive with ``lines``.

Notes
-----

- Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
- This module works with connection ``ansible.netcommon.network_cli``.
- The AOS configuration has no sections, so this module has no ``parents`` option.
- After lines are sent, the configuration is also saved to flash when ``ansible_aos_write_memory_flash`` is ``true``, which is the default of the connection. Set it to ``false`` to let ``save_when`` decide.

Examples
--------

.. code-block:: yaml

    - name: Send configuration lines
      ale.aos8.aos8_config:
        lines:
          - vlan 41 admin-state enable
          - vlan 41 name "Printers"

    - name: Send every line without comparing, with a command before and after
      ale.aos8.aos8_config:
        commands:
          - vlan 41 admin-state enable
        match: none
        before:
          - vlan 42 admin-state enable
        after:
          - vlan 43 admin-state enable

    - name: Send the lines of a template with a lookup, and back up the configuration first
      ale.aos8.aos8_config:
        lines: '{{ lookup(''ansible.builtin.template'', ''aos8_config_lines.j2'').splitlines() }}'
        backup: true
        backup_options:
          filename: aos8_config_example.cfg
          dir_path: /tmp/aos8_backup

    - name: Send the lines of a template file
      ale.aos8.aos8_config:
        src: aos8_config_example.j2

    - name: Compare the lines with a configuration given in the task
      ale.aos8.aos8_config:
        lines:
          - vlan 42 admin-state enable
          - vlan 44 admin-state enable
        running_config: |
          vlan 44 admin-state enable

    - name: Show what a change would do, in check mode with a diff
      ale.aos8.aos8_config:
        lines:
          - vlan 43 name "Lab"
        diff_ignore_lines:
          - ^! .*
      check_mode: true
      diff: true

    - name: Compare the switch with an intended configuration
      ale.aos8.aos8_config:
        diff_against: intended
        intended_config: |
          vlan 43 admin-state enable
          vlan 43 name "Intended"
      diff: true

    - name: Save the configuration when the task changes it
      ale.aos8.aos8_config:
        lines:
          - vlan 43 name "Lab"
        save_when: changed

    - name: Save the configuration only when it is not saved yet
      ale.aos8.aos8_config:
        save_when: modified

    - name: Save the configuration at every run
      ale.aos8.aos8_config:
        save_when: always

    - name: Never save the configuration (the default)
      ale.aos8.aos8_config:
        lines:
          - vlan 43 admin-state enable
        config: |
          vlan 43 admin-state enable
        save_when: never
        match: line
        backup: false
        diff_against: running

Return values
-------------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Key
     - Type
     - Returned
     - Description
   * - ``backup_path``
     - str
     - when ``backup=true``
     - Full path of the backup file.
   * - ``commands``
     - list
     - when lines have to be sent
     - The lines sent to the switch. Sample: ``["vlan 41 admin-state enable", "vlan 41 name \"Printers\""]``
   * - ``updates``
     - list
     - when lines have to be sent
     - Same value as ``commands``. Sample: ``["vlan 41 admin-state enable", "vlan 41 name \"Printers\""]``

Authors
-------

- Mathias Guillemot (@mathias-gt)
