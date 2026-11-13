# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the aos8_hostname module
"""


class HostnameArgs(object):  # pylint: disable=R0903
    """The arg spec for the aos8_hostname module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {"hostname": {"type": "str"}},
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": ["merged", "replaced", "overridden", "gathered", "rendered", "parsed"],
            "default": "merged",
        },
    }
