# stellaris-guiexpand-test-mod

[English](README.md) | [简体中文](README.zh-CN.md)

A small mod for **Stellaris 4.5.2** that exists to test and demonstrate [stellaris-guiexpand](https://github.com/Yidhar/stellaris-guiexpand), the shared GUI host plugin. It is also the smallest
complete example of a mod that **declares a panel**: copy its layout for your own.

It does nothing by itself. With stellaris-guiexpand installed it adds one window, *Mod panel (declared in script)*, which shows live values from your empire, values that the mod's
script computes (a counter, a flag, a script value), and has buttons that run the mod's five button effects.

| File | What it is |
|---|---|
| `mod/guiexpand_test_mod/interface/stl_gui/guiexpand_test.txt` | the panel declaration (see stellaris-guiexpand's [mod author guide](https://github.com/Yidhar/stellaris-guiexpand/blob/main/docs/mod-authors.md)) |
| `mod/guiexpand_test_mod/common/button_effects/guiexpand_test.txt` | five button effects: grant 100 energy; set a country flag; clear it; add 1 to a counter variable; one that needs a million alloys (so the engine refuses it, to show the refusal text) |
| `mod/guiexpand_test_mod/common/scripted_loc/`, `common/script_values/` | what the panel's last lines show: a `scripted_loc` chosen by a trigger (the flag), and a script value (10, or 15 while the flag is set) behind a `scripted_loc`. Together with the counter variable and `[Root.GetName]` these are the four kinds of "values the script computes" (stellaris-guiexpand's [mod author guide](https://github.com/Yidhar/stellaris-guiexpand/blob/main/docs/mod-authors.md#showing-values-the-script-computes)) |
| `mod/guiexpand_test_mod/localisation/{english,simp_chinese}/` | the texts in two languages (UTF-8 with BOM) |
| `tools/mod_install.py` | install / uninstall into your mod folder and playset |
| `tools/check_mod.py` | static checks: loc keys in every language, effects exist, BOM |

The effects and the flag are also what the *Command Deck* of [stellaris-argon-ui](https://github.com/Yidhar/stellaris-argon-ui) uses on its script page (`guiexpand_test_grant_energy`, `guiexpand_test_set_mark`, `guiexpand_test_clear_mark`,
`guiexpand_test_rich_only`; the flag is `guiexpand_test_marked`).

## Use

```
python tools/mod_install.py install            # copies the mod into Documents\Paradox Interactive\Stellaris\mod and enables it in dlc_load.json
python tools/mod_install.py install --link     # same, but the .mod file points into this repository: edit here, restart the game
python tools/mod_install.py uninstall          # disables it and removes what install made
```

Only the entry `mod/guiexpand_test_mod.mod` of `enabled_mods` is added or removed. Mods are read when the game starts, so restart the game. (The launcher's `stl launch`
rewrites `dlc_load.json` from the active playset: enable the mod in the playset instead if you start the game that way.)

Then start the game with the Stellaris launcher with the stellaris-guiexpand plugin enabled, load a save, and the panel appears on the left of the screen.

The buttons run script effects for the player country: they change a **save**. Use a throwaway save. In multiplayer the effects are checked by every client; this has not been tested.

## Checks

```
python tools/check_mod.py
```

CI runs it on every push.

## License

MIT, see `LICENSE`.
