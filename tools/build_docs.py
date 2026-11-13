#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Alcatel-Lucent Enterprise
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Builds docs/*.rst and the content table of README.md from the plugin documentation.

Run it from an installed copy of the collection after changing the documentation
of a plugin:

    python tools/build_docs.py
"""

from __future__ import absolute_import, division, print_function

import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLLECTION = "ale.aos8"
BASE_URL = "https://github.com/ale-nsa-team/ale.aos8/blob/master/docs/"
KINDS = (("cliconf", "Cliconf plugins", "_cliconf"), ("module", "Modules", "_module"))


def markup(text):
    """Turns the Ansible documentation markup into reStructuredText."""
    text = re.sub(r"\bRV\(([^)]+)\)", r"``\1``", str(text))
    text = re.sub(r"\b[OM]\(([^)]+)\)", r"``\1``", text)
    text = re.sub(r"\b[CV]\(((?:[^()]|\([^()]*\))*)\)", r"``\1``", text)
    text = re.sub(r"[IB]\(([^)]+)\)", r"*\1*", text)
    return text


def lines_of(value):
    return [markup(item) for item in (value if isinstance(value, list) else [value])]


def title(text, char):
    return [text, char * len(text), ""]


def option_rows(options, depth=0):
    rows = []
    for name, opt in (options or {}).items():
        details = [opt.get("type", "str")]
        if opt.get("elements"):
            details.append("elements=%s" % opt["elements"])
        if opt.get("required"):
            details.append("**required**")
        comments = lines_of(opt.get("description", []))
        if opt.get("aliases"):
            comments.append("Aliases: %s" % ", ".join(opt["aliases"]))
        choices = opt.get("choices") or []
        default = opt.get("default")
        values = []
        for choice in choices:
            values.append("``%s`` (default)" % choice if choice == default else "``%s``" % choice)
        if not choices and default is not None:
            values.append("Default: ``%s``" % json.dumps(default).strip('"'))
        rows.append(("\\ " * 0 + "%s``%s``" % ("– " * depth, name), " / ".join(details), ", ".join(values), " ".join(comments)))
        rows.extend(option_rows(opt.get("suboptions"), depth + 1))
    return rows


def table(header, rows):
    out = [".. list-table::", "   :header-rows: 1", "   :widths: 22 14 20 44", ""]
    for row in [header] + rows:
        for index, cell in enumerate(row):
            out.append(("   %s %s" % ("* -" if index == 0 else "  -", cell)).rstrip())
    return out + [""]


def render(name, doc, examples, returns, kind):
    out = [".. _%s.%s%s:" % (COLLECTION, name, "_module" if kind == "module" else "_" + kind), ""]
    out += title("%s.%s" % (COLLECTION, name), "*")
    out += ["**%s**" % markup(doc["short_description"]), ""]
    if doc.get("version_added"):
        out += ["Version added: %s" % doc["version_added"], ""]
    out += [".. contents::", "   :local:", "   :depth: 1", ""]
    out += title("Synopsis", "-")
    out += ["- %s" % line for line in lines_of(doc.get("description", []))] + [""]
    if doc.get("options"):
        out += title("Parameters", "-")
        out += table(("Parameter", "Type", "Choices / default", "Comments"), option_rows(doc["options"]))
    if doc.get("notes"):
        out += title("Notes", "-")
        out += ["- %s" % line for line in lines_of(doc["notes"])] + [""]
    if examples:
        out += title("Examples", "-")
        out += [".. code-block:: yaml", ""] + ["    " + line if line else "" for line in examples.strip("\n").split("\n")] + [""]
    if returns:
        out += title("Return values", "-")
        rows = []
        for key, value in returns.items():
            sample = value.get("sample")
            text = " ".join(lines_of(value.get("description", "")))
            if sample is not None and not isinstance(sample, str):
                text += " Sample: ``%s``" % json.dumps(sample)
            rows.append(("``%s``" % key, value.get("type", ""), markup(value.get("returned", "")), text))
        out += table(("Key", "Type", "Returned", "Description"), rows)
    authors = doc.get("author") or []
    out += title("Authors", "-")
    out += ["- %s" % author for author in (authors if isinstance(authors, list) else [authors])] + [""]
    return "\n".join(out)


def main():
    readme_rows = {}
    docs_dir = os.path.join(ROOT, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    for kind, heading, suffix in KINDS:
        raw = subprocess.check_output(["ansible-doc", "-t", kind, "--json", "-l", COLLECTION])
        names = sorted(json.loads(raw))
        raw = subprocess.check_output(["ansible-doc", "-t", kind, "--json"] + names)
        plugins = json.loads(raw)
        rows = []
        for fqcn in names:
            entry = plugins[fqcn]
            short = fqcn.split(".")[-1]
            filename = "%s.%s%s.rst" % (COLLECTION, short, suffix)
            with open(os.path.join(docs_dir, filename), "w") as handle:
                handle.write(render(short, entry["doc"], entry.get("examples"), entry.get("return"), kind))
            rows.append("[%s](%s%s)|%s" % (fqcn, BASE_URL, filename, entry["doc"]["short_description"]))
        readme_rows[heading] = rows

    content = []
    for kind, heading, suffix in KINDS:
        content += ["### %s" % heading, "Name | Description", "--- | ---"] + readme_rows[heading] + [""]
    path = os.path.join(ROOT, "README.md")
    with open(path) as handle:
        readme = handle.read()
    readme = re.sub(
        r"(<!--start collection content-->\n).*?(<!--end collection content-->)",
        lambda match: match.group(1) + "\n".join(content) + "\n" + match.group(2),
        readme,
        flags=re.S,
    )
    with open(path, "w") as handle:
        handle.write(readme)
    print("wrote %d files to docs/" % sum(len(rows) for rows in readme_rows.values()))


if __name__ == "__main__":
    main()
