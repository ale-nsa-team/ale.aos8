==================================
ALE AOS8 Collection Release Notes
==================================

.. contents:: Topics

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
