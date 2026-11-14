==================================
ALE AOS8 Collection Release Notes
==================================

.. contents:: Topics

v1.1.0
======

Release Summary
---------------

This release prepares the collection for Ansible Galaxy. Every module is now
documented, unit tested, and tested against an OmniSwitch running AOS
8.11.162.R01. The resource modules share one engine and are idempotent.

Major Changes
-------------

- All resource modules were rewritten on a shared engine. They now support the
  states ``merged``, ``replaced``, ``overridden``, ``deleted``, ``gathered``,
  ``rendered`` and ``parsed``, report ``changed`` only when the switch
  configuration differs, and honour check mode.
- Added unit tests, lab (integration) tests and a GitHub Actions workflow.
- Added documentation for every module, in the module and in ``docs/``.

Minor Changes
-------------

- aos8_facts - added the basic facts ``ansible_net_model``,
  ``ansible_net_version``, ``ansible_net_hostname`` and ``ansible_net_system``.
- aos8_facts - added the ``bgp``, ``ntp``, ``ospfv2`` and ``static_routes``
  resources to ``gather_network_resources``.
- aos8_l3_interfaces - interfaces in a VRF are now read from the switch.
- aos8_ntp - added the ``prefer``, ``burst``, ``iburst``, ``minpoll``,
  ``maxpoll`` and ``version`` options of a server.
- aos8_ospfv2 - added the ``gathered`` and ``deleted`` states.
- aos8_static_routes - added routes through an IP interface.
- terminal - every ``ERROR:`` answer of the switch now fails the task.

Breaking Changes / Porting Guide
--------------------------------

- aos8_bgp - removed the ``purged`` state, which had no AOS equivalent.
- aos8_command - removed the ``output`` option, which had no effect.
- aos8_config - removed the ``parents``, ``replace`` and ``defaults`` options,
  the ``strict`` and ``exact`` values of ``match``, the ``startup``,
  ``session`` and ``validate_config`` values of ``diff_against``. They came
  from another platform and did not work on AOS.
- aos8_facts - ``gather_subset`` now defaults to ``min``. The ``port_security``
  resource was removed because it had no module.
- aos8_hostname - removed the ``deleted`` state. It set the system name to
  ``changeme``.
- aos8_l3_interfaces - ``type`` only accepts ``vlan``. The ``rtr-port`` and
  ``tunnel`` values produced commands the switch rejected.
- aos8_ntp - removed the options that were accepted but ignored
  (``authenticate``, ``authentication_keys``, ``local_interface``,
  ``qos_dscp``, ``serve``, ``trusted_key`` and the per-server ``vrf``,
  ``source``, ``local_interface`` and ``key_id``).
- aos8_ospfv2 - removed the ``area`` option of an interface. The area is the
  one the interface is listed under.
- aos8_static_routes - removed the options that were accepted but ignored
  (``vrf``, ``nexthop_grp``, ``mpls_label``, ``track``).
- aos8_trap_managers - ``port`` now defaults to 162, the SNMP trap port,
  instead of 161.
- aos8_vlans - ``admin`` and ``mtu`` have no default any more, so ``merged``
  no longer resets them. ``replaced`` and ``overridden`` reset them to
  ``enable`` and 1500.

Bugfixes
--------

- cliconf - ``ansible_aos_flash_synchro_flag`` ran ``copy flash-synchro``, which
  AOS 8.11 does not support, and the task then failed with "Certified
  directory not synchronized". It now certifies with ``copy running
  certified``, after the configuration is saved.
- aos8_config - check mode no longer changes the switch.
- aos8_config - with ``backup_options``, the task reported ``changed=false``
  after changing the switch when the backup file already held the same
  content (``ansible.netcommon`` replaced the result of the module with the
  status of the backup file).
- aos8_config - ``save_when`` and ``--diff`` no longer fail.
- aos8_l2_interfaces - link aggregates are recognized in the output of the
  switch, so their VLAN membership is idempotent.
- aos8_ntp - the module no longer writes a ``whatInObjs.txt`` file.
- aos8_radius_servers, aos8_static_routes, aos8_trap_managers, aos8_ospfv2 -
  the modules no longer report ``changed`` at every run.
- aos8_radius_servers - the shared secret is no longer shown in the task
  output.
- All resource modules - the ``parsed`` state now returns the parsed data.
- Removed the broken ``hostname`` action plugin.
- Fix the ``SyntaxWarning: invalid escape sequence`` raised by Python 3.12 in
  the fact parsers (https://github.com/ale-nsa-team/ale.aos8/pull/6).
  Thanks to lukeod.
- Fix the ansible-core deprecation warnings about ``ansible.module_utils._text``,
  ``_collections_compat`` and ``warnings`` in ``exit_json``
  (https://github.com/ale-nsa-team/ale.aos8/issues/7). Thanks to mksbv for the report.

v1.0.2
======

Release Summary
---------------

This patch release adds the missing ``meta/runtime.yml`` so the aos8 action
plugin is invoked correctly. This fixes fact-module discovery for the
``ale.aos8.aos8`` network OS and ensures ``aos8_config`` sends file contents
when using the ``src`` option.

Bugfixes
--------

- collection - Add ``meta/runtime.yml`` with action plugin routing and
  action groups. Fixes "No fact modules available" for the ``ale.aos8.aos8``
  network OS and ensures the action plugin runs so ``aos8_config`` ``src``
  sends file contents instead of the filename
  (https://github.com/ale-nsa-team/ale.aos8/issues/1).

v1.0.1
======

Release Summary
---------------

This patch release fixes the radius-server fact parser, which failed to
return any facts due to an invalid regular expression.

Bugfixes
--------

- radius_servers - Close the unbalanced ``host`` named capture group in the
  radius-server fact parser. The group was never terminated, making the
  regular expression invalid and causing fact gathering to fail at runtime
  (https://github.com/ale-nsa-team/ale.aos8/issues/3).

v1.0.0
======

Release Summary
---------------

Initial release of the ale.aos8 collection.
