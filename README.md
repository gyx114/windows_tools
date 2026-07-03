# Windows Tools Launcher

一键启动 Windows 系统工具的 CLI 工具，支持所有常用的 Win+R 命令。

单个 `wtools.exe` 即可使用全部功能（**含管理/添加/删除工具**），无需安装 Python。

## 功能

- 🚀 列出并启动 **管理控制台** (.msc) — `services.msc`, `compmgmt.msc` 等
- 🚀 列出并启动 **控制面板项** (.cpl) — `appwiz.cpl`, `ncpa.cpl` 等
- 🚀 列出并启动 **系统命令** — `regedit`, `dxdiag`, `msconfig` 等
- 📋 交互式菜单浏览和启动
- 🔍 关键词搜索
- 📂 按分类组织（系统管理、硬件设备、网络、磁盘、用户安全等）
- ✏️ **内置管理功能** — 添加/删除/导入工具，无需额外工具
- �️ **图形界面模式** — `--gui` 或交互菜单按 `g` 启动
- �💾 配置文件自动保存，支持便携模式和系统安装模式

## 快速使用（无需 Python）

```cmd
wtools.exe                   # 交互式菜单
wtools.exe list              # 列出所有工具
wtools.exe run calc          # 启动计算器
wtools.exe --gui             # 启动图形界面
wtools.exe run services.msc
wtools.exe search 网络
```

> 将 exe 所在目录添加到系统 PATH 后，可直接在 **Win+R** 运行 `wtools`。

### 图形界面模式

按 `g` 或使用 `--gui` 参数启动 tkinter 图形界面，分类浏览和搜索更直观：

```
┌──────────────────────────────────────────────┐
│  Windows Tools Launcher    [🔍 搜索...]      │
├────────────┬─────────────────────────────────┤
│  📂 系统管理  │  compmgmt.msc    计算机管理   │
│  📂 硬件设备  │  services.msc    服务         │
│  📂 网络连接  │  ...                          │
│  ...         │         [🚀 启动]  [✏️ 编辑]   │
├────────────┴─────────────────────────────────┤
│  配置文件: D:\...\tools.json  (68 个工具)    │
└──────────────────────────────────────────────┘
```

### 管理工具（交互式菜单按 `m` 键）

```
┌─ 主菜单 ──────────────────────────┐
│   1. 系统管理                     │
│   ...                             │
│   0. 搜索工具                     │
│   g. 图形界面模式  ← 新增        │
│   m. 管理工具（添加/删除）        │
│   q. 退出                         │
└───────────────────────────────────┘

┌─ 管理工具 (m) ───────────────────┐
│   1. 添加工具                     │
│   2. 删除工具                     │
│   3. 查看配置状态                  │
│   4. 创建新分类                   │
│   5. 从 JSON 文件导入             │
│   6. 重置配置                     │
└───────────────────────────────────┘
```

## 配置文件说明

程序自动在以下位置查找 `tools.json`：

| 优先级 | 位置 | 适用场景 |
|--------|------|---------|
| ① | `exe 同目录/tools.json` | 便携模式（U盘、自定义目录） |
| ② | `%APPDATA%\windows_tools\tools.json` | System32 等只读目录 |
| ③ | 无配置文件 | **回退使用内置硬编码数据** |

## 管理工具（命令行）

通过 `adder.py` 可在命令行中管理工具条目：

```bash
# 添加工具
python adder.py add wt.exe Terminal 终端 "Windows Terminal"

# 删除工具
python adder.py remove wt.exe

# 创建新分类
python adder.py category "开发者工具"

# 查看配置状态
python adder.py list

# 从 JSON 文件批量导入
python adder.py import my_tools.json

# 重置配置，恢复内置数据
python adder.py reset
```

或使用批处理文件：
```cmd
adder list
adder add wt.exe Terminal 终端 "Windows Terminal"
```

## 包含的工具分类

| 分类 | 数量 | 示例 |
|------|------|------|
| 系统管理 | 23 | compmgmt.msc, services.msc, regedit, msconfig |
| 硬件与设备 | 9 | devmgmt.msc, main.cpl, mmsys.cpl |
| 磁盘与存储 | 3 | diskmgmt.msc, cleanmgr, dfrgui |
| 网络与连接 | 6 | ncpa.cpl, firewall.cpl, inetcpl.cpl |
| 用户与安全 | 8 | gpedit.msc, lusrmgr.msc, secpol.msc |
| 性能与诊断 | 4 | taskmgr, perfmon.msc, resmon, dxdiag |
| 外观与辅助 | 4 | desk.cpl, osk, magnify |
| 其他工具 | 10 | notepad, calc, mspaint, snippingtool |

> 可通过 `adder add` 或交互菜单添加更多工具和分类。

## 项目结构

```
windows_tools/
├── dist/                   # 编译好的 exe 文件
│   └── wtools.exe          # 单文件，自带全部功能
├── windows_tools_cli.py    # 主程序入口（CLI + --gui 启动器）
├── wtools_gui.py           # tkinter 图形界面
├── adder.py                # 命令行管理工具
├── config.py               # 配置读写 + 路径查找 + 核心管理逻辑
├── tools_data.py           # 硬编码工具数据（回退方案）
├── wtools.bat              # 批处理启动脚本
├── adder.bat               # 批处理管理脚本
├── .gitignore
└── README.md
```

## 自行打包 exe

```bash
pip install pyinstaller
pyinstaller --onefile --name wtools --console windows_tools_cli.py
# 生成的 exe 在 dist/wtools.exe
```
