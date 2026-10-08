"""Static checks for the test mod (no game needed; also run by CI):

  * descriptor.mod has name / version / supported_version
  * every localisation key the declared panel uses (title, text, label, ...) exists in every language file
  * every button effect the panel names is defined in common/button_effects
  * the localisation files are UTF-8 with BOM, as the engine requires, and have the same keys in both languages
  * the panel file starts with stl_gui_version = 1

    python tools/check_mod.py
"""
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mod", "guidll_test_mod"))
problems = []


def bad(msg):
    problems.append(msg)


def read(path, bom_ok=False):
    raw = open(path, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
        has_bom = True
    else:
        has_bom = False
    return raw.decode("utf-8"), has_bom


desc, _ = read(os.path.join(ROOT, "descriptor.mod"))
for key in ("name", "version", "supported_version"):
    if not re.search(rf'^{key}\s*=', desc, re.M):
        bad(f"descriptor.mod: {key} is missing")

# localisation
langs = {}
for path in glob.glob(os.path.join(ROOT, "localisation", "*", "*.yml")):
    text, has_bom = read(path)
    lang = os.path.basename(os.path.dirname(path))
    if not has_bom:
        bad(f"{os.path.relpath(path, ROOT)}: no UTF-8 BOM (the engine ignores the file)")
    if not re.match(rf"\s*l_{lang}:", text):
        bad(f"{os.path.relpath(path, ROOT)}: first line is not l_{lang}:")
    langs[lang] = set(re.findall(r"^\s+([A-Za-z0-9_.\-]+):\d*\s+\"", text, re.M))
if len(langs) < 2:
    bad(f"expected at least two languages, found {sorted(langs)}")
all_keys = set().union(*langs.values()) if langs else set()
for lang, keys in langs.items():
    for k in sorted(all_keys - keys):
        bad(f"localisation/{lang}: {k} is missing")

# the declared panel
panel_files = glob.glob(os.path.join(ROOT, "interface", "stl_gui", "*.txt"))
effects_defined = set()
for path in glob.glob(os.path.join(ROOT, "common", "button_effects", "*.txt")):
    text, _ = read(path)
    effects_defined |= set(re.findall(r"^([A-Za-z0-9_]+)\s*=\s*\{", text, re.M))
for path in panel_files:
    text, _ = read(path)
    text_nc = re.sub(r"#.*", "", text)
    rel = os.path.relpath(path, ROOT)
    if not re.search(r"^\s*stl_gui_version\s*=\s*1\b", text_nc, re.M):
        bad(f"{rel}: stl_gui_version = 1 is missing")
    for key in re.findall(r"\b(?:title|text|label|yes|no)\s*=\s*([A-Z][A-Z0-9_]+)\b", text_nc):
        if key not in all_keys:
            bad(f"{rel}: localisation key {key} is not defined")
    for eff in re.findall(r"\b(?:effect|probe)\s*=\s*([a-z][a-z0-9_]+)\b", text_nc):
        if eff not in effects_defined:
            bad(f"{rel}: button effect {eff} is not defined in common/button_effects")

if problems:
    print("mod check FAILED:", file=sys.stderr)
    for p in problems:
        print("  " + p, file=sys.stderr)
    sys.exit(1)
print(f"mod ok: {len(all_keys)} localisation keys in {len(langs)} languages, {len(effects_defined)} button effects, {len(panel_files)} panel file(s)")
