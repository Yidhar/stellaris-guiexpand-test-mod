"""Installs / removes the test mod in the user's Stellaris mod folder and in the active playset (dlc_load.json).

    python tools/mod_install.py install            copy mod/guidll_test_mod into <Documents>/Paradox Interactive/Stellaris/mod and enable it
    python tools/mod_install.py install --link     enable it in place: the .mod file's path= points into this repository (edit, restart the game, no copy)
    python tools/mod_install.py uninstall          disable it and remove what install made
    python tools/mod_install.py status

Only the entry `mod/guidll_test_mod.mod` of enabled_mods is added or removed; the rest of dlc_load.json is left as it is. Mods are read when the game
starts, so a running game has to be restarted. The launcher (stl) or the Paradox launcher can do the same by hand: this is the scripted way.
"""
import ctypes
import json
import os
import shutil
import sys

NAME = "guidll_test_mod"
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "mod", NAME))
ENTRY = f"mod/{NAME}.mod"


def documents():
    buf = ctypes.create_unicode_buffer(260)
    ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)  # CSIDL_PERSONAL
    return os.path.join(buf.value, "Paradox Interactive", "Stellaris")


def paths():
    docs = documents()
    return os.path.join(docs, "mod"), os.path.join(docs, "dlc_load.json")


def load_cfg(dlc):
    if not os.path.exists(dlc):
        return {"disabled_dlcs": [], "enabled_mods": []}
    with open(dlc, encoding="utf-8") as f:
        return json.load(f)


def save_cfg(dlc, cfg):
    tmp = dlc + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, separators=(",", ":"))
    os.replace(tmp, dlc)


def install(link):
    mod_dir, dlc = paths()
    os.makedirs(mod_dir, exist_ok=True)
    if link:
        target = SRC
    else:
        target = os.path.join(mod_dir, NAME)
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(SRC, target)
    with open(os.path.join(mod_dir, f"{NAME}.mod"), "w", encoding="utf-8", newline="\n") as f:
        with open(os.path.join(SRC, "descriptor.mod"), encoding="utf-8") as d:
            f.write(d.read().rstrip("\n") + "\n")
        f.write('path="%s"\n' % target.replace("\\", "/"))
    cfg = load_cfg(dlc)
    if ENTRY not in cfg.setdefault("enabled_mods", []):
        cfg["enabled_mods"].append(ENTRY)
    save_cfg(dlc, cfg)
    print(f"installed ({'linked to ' + target if link else 'copied'}); enabled_mods: {cfg['enabled_mods']}")
    print("restart the game: mods are read at start")


def uninstall():
    mod_dir, dlc = paths()
    cfg = load_cfg(dlc)
    if ENTRY in cfg.get("enabled_mods", []):
        cfg["enabled_mods"].remove(ENTRY)
        save_cfg(dlc, cfg)
    shutil.rmtree(os.path.join(mod_dir, NAME), ignore_errors=True)
    p = os.path.join(mod_dir, f"{NAME}.mod")
    if os.path.exists(p):
        os.remove(p)
    print("uninstalled; enabled_mods:", cfg.get("enabled_mods"))


def status():
    mod_dir, dlc = paths()
    cfg = load_cfg(dlc)
    mod_file = os.path.join(mod_dir, f"{NAME}.mod")
    print("mod folder:", mod_dir)
    print(".mod file :", "present" if os.path.exists(mod_file) else "absent")
    print("enabled   :", ENTRY in cfg.get("enabled_mods", []))


def main():
    a = sys.argv[1:]
    if a[:1] == ["install"]:
        install("--link" in a)
    elif a[:1] == ["uninstall"]:
        uninstall()
    elif a[:1] == ["status"]:
        status()
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
