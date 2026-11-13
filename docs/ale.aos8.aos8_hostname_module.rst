.. _ale.aos8.aos8_hostname_module:

ale.aos8.aos8_hostname
**********************

**Resource module to configure the system name**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------

- This module manages the system name of Alcatel-Lucent Enterprise OmniSwitch devices running AOS 8.
- AOS has no command to remove the system name, so this module has no ``deleted`` state.
- The system name is one value, so ``merged``, ``replaced`` and ``overridden`` do the same thing.

Parameters
----------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Parameter
     - Type
     - Choices / default
     - Comments
   * - ``config``
     - dict
     -
     - The system name configuration.
   * - – ``hostname``
     - str
     -
     - System name of the switch.
   * - ``running_config``
     - str
     -
     - Text to convert into structured data. Only used with ``state=parsed``. Give the output of ``show configuration snapshot | grep '^system name'`` from the switch.
   * - ``state``
     - str
     - ``merged`` (default), ``replaced``, ``overridden``, ``gathered``, ``rendered``, ``parsed``
     - What the module does with the given configuration. ``merged`` adds the given configuration to the switch and changes only the attributes that are given. ``replaced`` makes each given entry match the task exactly. Attributes that are left out go back to their default value. ``overridden`` makes the whole resource match the task. Entries found on the switch that are not in the task are removed. ``gathered`` reads the configuration from the switch and returns it as ``gathered``. Nothing is changed. ``rendered`` returns the commands for the given configuration as ``rendered``, without connecting to the switch. ``parsed`` converts the text given in ``running_config`` into structured data, returned as ``parsed``, without connecting to the switch.

Notes
-----

- Tested against Alcatel-Lucent Enterprise OmniSwitch AOS 8.11.162.R01.
- This module works with connection ``ansible.netcommon.network_cli``.
- After a change, the configuration is saved to flash with ``write memory flash-synchro``, unless ``ansible_aos_write_memory_flash`` is set to ``false``. Saving needs ``ansible_command_timeout`` to be 60 seconds or more.

Examples
--------

.. code-block:: yaml

    - name: Set the system name
      ale.aos8.aos8_hostname:
        config:
          hostname: core-sw-1
        state: merged

    # Commands sent to the switch
    # ---------------------------
    # system name "core-sw-1"

    - name: Read the system name from the switch
      ale.aos8.aos8_hostname:
        state: gathered

    - name: Replace the system name
      ale.aos8.aos8_hostname:
        config:
          hostname: edge-sw-1
        state: replaced

    # Commands sent to the switch
    # ---------------------------
    # system name "edge-sw-1"

    - name: Override the system name
      ale.aos8.aos8_hostname:
        config:
          hostname: val-os1
        state: overridden

    # Commands sent to the switch
    # ---------------------------
    # system name "val-os1"

    - name: Show the command for a system name without connecting to the switch
      ale.aos8.aos8_hostname:
        config:
          hostname: core-sw-1
        state: rendered

    # Value returned as rendered
    # --------------------------
    # - system name "core-sw-1"

    - name: Convert a configuration line into structured data
      ale.aos8.aos8_hostname:
        running_config: system name "core-sw-1"
        state: parsed

    # Value returned as parsed
    # ------------------------
    # hostname: core-sw-1

Return values
-------------

.. list-table::
   :header-rows: 1
   :widths: 22 14 20 44

   * - Key
     - Type
     - Returned
     - Description
   * - ``after``
     - dict
     - when the module changed the switch
     - The configuration found on the switch after the module ran.
   * - ``before``
     - dict
     - when ``state`` is ``merged`` or ``replaced`` or ``overridden``
     - The configuration found on the switch before the module ran.
   * - ``commands``
     - list
     - when ``state`` is ``merged`` or ``replaced`` or ``overridden``
     - The commands sent to the switch. In check mode, the commands that would be sent. Sample: ``["system name \"core-sw-1\""]``
   * - ``gathered``
     - dict
     - when ``state`` is ``gathered``
     - The configuration read from the switch.
   * - ``parsed``
     - dict
     - when ``state`` is ``parsed``
     - The structured data built from ``running_config``. Sample: ``{"hostname": "core-sw-1"}``
   * - ``rendered``
     - list
     - when ``state`` is ``rendered``
     - The commands for the given configuration. Sample: ``["system name \"core-sw-1\""]``

Authors
-------

- Samuel Yip Kah Yean (@samuelyip74)
- Mathias Guillemot (@mathias-gt)
