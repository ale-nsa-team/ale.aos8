.. _ale.aos8.aos8_cliconf:

ale.aos8.aos8
*************

**Use aos8 cliconf to run commands on Alcatel-Lucent Enterprise AOS 8 devices**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This aos8 plugin provides low level abstraction APIs for sending and receiving CLI commands from Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- The switch must run from the working directory. Configuration changes are refused when it runs from the certified directory.

Parameters
----------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Parameter
     - Type
     - Choices / default
     - Comments
   * - ``flash_synchro_flag``
     - boolean
     - Default: ``false``
     - Runs ``copy running certified flash-synchro`` after each change, to copy the running directory to the certified directory and synchronize them. ``ansible_command_timeout`` must be 60 seconds or more when this option is enabled.
   * - ``write_memory_flag``
     - boolean
     - Default: ``true``
     - Saves the configuration to flash with ``write memory flash-synchro`` after each change made by a resource module or by ``ale.aos8.aos8_config``. The command can take a long time, so ``ansible_command_timeout`` must be 60 seconds or more when this option is enabled.

Examples
--------

.. code-block:: yaml

    # Inventory variables for a switch managed with this collection
    #
    # ansible_connection: ansible.netcommon.network_cli
    # ansible_network_os: ale.aos8.aos8
    # ansible_command_timeout: 90
    # ansible_aos_write_memory_flash: true
    # ansible_aos_flash_synchro_flag: false

    - name: Change the system name and save the configuration to flash
      ale.aos8.aos8_hostname:
        config:
          hostname: val-os1-saved
        state: merged
      vars:
        ansible_aos_write_memory_flash: true
        ansible_command_timeout: 90

    - name: Change the system name without saving it
      ale.aos8.aos8_hostname:
        config:
          hostname: val-os1
        state: merged
      vars:
        ansible_aos_write_memory_flash: false

    - name: Change the system name, save it and synchronize the certified directory
      ale.aos8.aos8_hostname:
        config:
          hostname: val-os1-synchro
        state: merged
      vars:
        ansible_aos_write_memory_flash: true
        ansible_aos_flash_synchro_flag: true
        ansible_command_timeout: 90

Authors
-------

- Samuel Yip Kah Yean (@samuelyip74)
- Mathias Guillemot (@mathias-gt)
