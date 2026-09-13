# -*- coding: utf-8 -*-
"""
check-i18n.py — sanity check for the translation files.

Run it after editing anything in /i18n/ or after adding a new data-i18n
attribute to a page:

    python tools/check-i18n.py

It reports:
  * invalid JSON
  * keys used in the HTML but missing from a language file
  * keys present in a language file but never used in the HTML
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, "i18n")
LANGS = ["en", "sr", "ru", "de", "zh"]

RE_TEXT = re.compile(r'data-i18n(?:-html)?="([^"]+)"')
RE_ATTR = re.compile(r'data-i18n-attr="([^"]+)"')


def keys_in_html():
    """Every translation key referenced by the .html files."""
    found = set()
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".html"):
            continue
        with open(os.path.join(ROOT, name), encoding="utf-8") as handle:
            html = handle.read()
        for match in RE_TEXT.findall(html):
            found.add(match)
        for match in RE_ATTR.findall(html):
            for pair in match.split(","):
                bits = pair.split(":")
                if len(bits) == 2:
                    found.add(bits[1].strip())
    # data-i18n-attr values are also matched by RE_TEXT, so drop the leftovers
    return {k for k in found if not k.startswith("data-i18n")}


def flatten(obj, prefix=""):
    """Turn {"a": {"b": "x"}} into {"a.b": "x"}."""
    flat = {}
    for key, value in obj.items():
        path = prefix + key
        if isinstance(value, dict):
            flat.update(flatten(value, path + "."))
        else:
            flat[path] = value
    return flat


def main():
    html_keys = keys_in_html()
    # Keys like "alt" / "aria-label" are attribute names, not translation keys
    html_keys = {k for k in html_keys if "." in k}

    print("Keys referenced in HTML: %d\n" % len(html_keys))
    problems = 0

    for lang in LANGS:
        path = os.path.join(I18N, lang + ".json")
        try:
            with open(path, encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception as error:  # noqa: BLE001 - report anything and move on
            print("%s.json  INVALID JSON: %s" % (lang, error))
            problems += 1
            continue

        flat = flatten(data)
        missing = sorted(html_keys - set(flat))
        unused = sorted(set(flat) - html_keys)
        empty = sorted(k for k, v in flat.items() if not str(v).strip())

        status = "OK" if not (missing or empty) else "PROBLEMS"
        print("%s.json  %d keys  %s" % (lang, len(flat), status))

        for key in missing:
            print("    MISSING : %s" % key)
        for key in empty:
            print("    EMPTY   : %s" % key)
        for key in unused:
            print("    unused  : %s" % key)

        if missing or empty:
            problems += 1

    print()
    if problems:
        print("%d language file(s) need attention." % problems)
        return 1
    print("All translation files look good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
