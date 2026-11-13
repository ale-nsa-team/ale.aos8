# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Keeps the documentation honest:

* the documented options are exactly the options the module accepts
* every documented example is a task of the lab tests in tests/integration
* every documented option and choice is used by a task of the lab tests
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import glob
import importlib
import os

from unittest.mock import patch

import pytest
import yaml


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODULES = sorted(
    os.path.basename(path)[:-3] for path in glob.glob(os.path.join(ROOT, "plugins", "modules", "aos8_*.py"))
)
# read-only value: it cannot be set by a task, the lab tests check it in the gathered data
NOT_LAB_TESTED = set(
    ["config.operational_state", "config.operational_state=enable", "config.operational_state=disable"],
)


class _Captured(Exception):
    pass


def load(name):
    return importlib.import_module("ansible_collections.ale.aos8.plugins.modules." + name)


def argument_spec(module):
    def capture(self, argument_spec=None, **kwargs):
        raise _Captured(argument_spec)

    with patch("ansible.module_utils.basic.AnsibleModule.__init__", capture):
        with pytest.raises(_Captured) as info:
            module.main()
    return info.value.args[0]


def compare(documented, spec, path, errors):
    documented = documented or {}
    spec = spec or {}
    for name in sorted(set(documented) | set(spec)):
        where = path + name
        if name not in spec:
            errors.append("%s is documented but not accepted by the module" % where)
            continue
        if name not in documented:
            errors.append("%s is accepted by the module but not documented" % where)
            continue
        doc, opt = documented[name], spec[name]
        if not doc.get("description"):
            errors.append("%s has no description" % where)
        for key, default in (("type", "str"), ("elements", None), ("default", None), ("required", False)):
            if doc.get(key, default) != opt.get(key, default):
                errors.append("%s: %s is %r in the documentation, %r in the module" % (where, key, doc.get(key), opt.get(key)))
        for key in ("choices", "aliases"):
            if sorted(map(str, doc.get(key) or [])) != sorted(map(str, opt.get(key) or [])):
                errors.append("%s: %s differ" % (where, key))
        compare(doc.get("suboptions"), opt.get("options"), where + ".", errors)


def lab_tasks(name):
    tasks = []

    def walk(items):
        for item in items or []:
            if "block" in item:
                walk(item["block"])
                walk(item.get("always"))
            elif "ale.aos8." + name in item:
                tasks.append(item["ale.aos8." + name])

    pattern = os.path.join(ROOT, "tests", "integration", "targets", name, "tasks", "*.yaml")
    for path in glob.glob(pattern):
        with open(path) as handle:
            walk(yaml.safe_load(handle))
    return tasks


def used_values(args, documented, path, used):
    """Records every option, and every choice, a task uses."""
    if isinstance(args, list):
        for item in args:
            used_values(item, documented, path, used)
        return
    if not isinstance(args, dict):
        return
    for key, value in args.items():
        doc = (documented or {}).get(key)
        if doc is None:
            for candidate, entry in (documented or {}).items():
                if key in (entry.get("aliases") or []):
                    used.add(path + candidate + "|alias:" + key)
                    key, doc = candidate, entry
        if doc is None:
            continue
        used.add(path + key)
        if doc.get("choices"):
            for choice in value if isinstance(value, list) else [value]:
                used.add("%s%s=%s" % (path, key, choice))
        used_values(value, doc.get("suboptions"), path + key + ".", used)


def expected_values(documented, path, expected):
    for key, doc in (documented or {}).items():
        expected.add(path + key)
        for choice in doc.get("choices") or []:
            expected.add("%s%s=%s" % (path, key, choice))
        for alias in doc.get("aliases") or []:
            expected.add(path + key + "|alias:" + alias)
        expected_values(doc.get("suboptions"), path + key + ".", expected)


@pytest.mark.parametrize("name", MODULES)
def test_documented_options_match_the_module(name):
    module = load(name)
    documentation = yaml.safe_load(module.DOCUMENTATION)
    assert documentation["module"] == name
    errors = []
    compare(documentation["options"], argument_spec(module), "", errors)
    assert not errors, "\n".join(errors)


@pytest.mark.parametrize("name", MODULES)
def test_every_example_runs_in_the_lab_tests(name):
    module = load(name)
    tasks = lab_tasks(name)
    examples = yaml.safe_load(module.EXAMPLES)
    assert examples, "no examples"
    for example in examples:
        assert example["ale.aos8." + name] in tasks, "example %r is not a lab test" % example["name"]


@pytest.mark.parametrize("name", MODULES)
def test_every_option_and_choice_is_used_in_the_lab_tests(name):
    module = load(name)
    documented = yaml.safe_load(module.DOCUMENTATION)["options"]
    expected, used = set(), set()
    expected_values(documented, "", expected)
    for task in lab_tasks(name):
        used_values(task, documented, "", used)
    missing = sorted(expected - used - NOT_LAB_TESTED)
    assert not missing, "not covered by tests/integration: %s" % ", ".join(missing)


@pytest.mark.parametrize("name", MODULES)
def test_return_values_are_documented(name):
    returns = yaml.safe_load(load(name).RETURN)
    assert returns
    for key, value in returns.items():
        assert value.get("description") and value.get("returned") and value.get("type"), key
