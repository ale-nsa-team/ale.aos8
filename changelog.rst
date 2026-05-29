==================================
ALE AOS8 Collection Release Notes
==================================

.. contents:: Topics

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
