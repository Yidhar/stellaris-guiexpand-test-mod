# stellaris-guiexpand-test-mod

[English](README.md) | [简体中文](README.zh-CN.md)

**Stellaris 4.5.2** 的一个小 mod，用来测试和演示公共 GUI 宿主插件 [stellaris-guiexpand](https://github.com/Yidhar/stellaris-guiexpand)。它也是“**声明面板**”的 mod 里最小的完整示例：写自己的 mod 时可以照抄它的目录结构。

它自己什么也不做。装了 stellaris-guiexpand 之后，它多一个窗口 *Mod 面板（脚本声明）*：显示你帝国的实时数值和 mod 脚本算出来的值（计数器、旗标、脚本值），并有按钮执行 mod 的五个 button effect。

| 文件 | 内容 |
|---|---|
| `mod/guiexpand_test_mod/interface/stl_gui/guiexpand_test.txt` | 面板声明（语法见 stellaris-guiexpand 的[mod 作者指南](https://github.com/Yidhar/stellaris-guiexpand/blob/main/docs/mod-authors.zh-CN.md)） |
| `mod/guiexpand_test_mod/common/button_effects/guiexpand_test.txt` | 五个 button effect：注入 100 能量币；设置国家旗标；清除旗标；给计数器变量加 1；需要一百万合金的一个（引擎会拒绝它，用来演示拒绝原因的文字） |
| `mod/guiexpand_test_mod/common/scripted_loc/`、`common/script_values/` | 面板最后几行显示的内容：由触发器选择的 `scripted_loc`（旗标），以及放在 `scripted_loc` 后面的脚本值（10，旗标设置后是 15）。加上计数器变量和 `[Root.GetName]`，就是四种"脚本算出来的值"（见 stellaris-guiexpand 的 [mod 作者指南](https://github.com/Yidhar/stellaris-guiexpand/blob/main/docs/mod-authors.zh-CN.md#显示脚本算出来的值)） |
| `mod/guiexpand_test_mod/localisation/{english,simp_chinese}/` | 两种语言的文字（UTF-8 带 BOM） |
| `tools/mod_install.py` | 安装 / 卸载到你的 mod 文件夹和播放集 |
| `tools/check_mod.py` | 静态检查：每种语言的 loc 键、effect 是否存在、BOM |

这些 effect 和旗标也是 stellaris-guiexpand 自己的 *Command Deck* 脚本页用的（`guiexpand_test_grant_energy`、`guiexpand_test_set_mark`、`guiexpand_test_clear_mark`、`guiexpand_test_rich_only`；旗标是 `guiexpand_test_marked`）。

## 使用

```
python tools/mod_install.py install            # 把 mod 复制到 Documents\Paradox Interactive\Stellaris\mod，并在 dlc_load.json 里启用
python tools/mod_install.py install --link     # 同上，但 .mod 文件指向本仓库：在这里改，重启游戏即可
python tools/mod_install.py uninstall          # 停用并删掉 install 做的东西
```

只会在 `enabled_mods` 里增删 `mod/guiexpand_test_mod.mod` 这一项。mod 在游戏启动时读取，所以要重启游戏。（启动器的 `stl launch` 会按当前播放集重写 `dlc_load.json`：用它启动的话请在播放集里启用这个 mod。）

然后启用了 stellaris-guiexpand 插件、用 Stellaris 启动器启动游戏、读一个存档，面板就出现在屏幕左侧。

按钮会为玩家国家执行脚本 effect：会改动**存档**，请用一次性的存档。多人时 effect 由每个客户端校验；未测试。

## 检查

```
python tools/check_mod.py
```

CI 每次推送都会运行。

## 许可

MIT，见 `LICENSE`。
