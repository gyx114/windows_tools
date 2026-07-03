# Windows Tools Launcher

一键启动 Windows 系统工具的 CLI 工具，支持所有常用的 Win+R 命令。

## 功能

- 列出并启动 **管理控制台** (.msc) — `services.msc`, `compmgmt.msc` 等
- 列出并启动 **控制面板项** (.cpl) — `appwiz.cpl`, `ncpa.cpl` 等
- 列出并启动 **系统命令** — `regedit`, `dxdiag`, `msconfig` 等
- 交互式菜单浏览和启动
- 关键词搜索
- 按分类组织（系统管理、硬件设备、网络、磁盘、用户安全等）

## 快速使用（无需 Python）

直接用预编译的 exe 即可，无需安装 Python：

```cmd
# 下载后直接在命令行运行
dist\wtools.exe              # 交互式菜单
dist\wtools.exe list         # 列出所有工具
dist\wtools.exe run calc     # 启动计算器
dist\wtools.exe run services.msc
dist\wtools.exe search 网络
```

> 将 exe 所在目录添加到系统 PATH 后，可直接在 **Win+R** 运行 `wtools`。

## 使用方法（Python 源码）

需要 Python 3.x 环境：

### 交互式模式
```bash
python windows_tools_cli.py
```

### 列出所有工具
```bash
python windows_tools_cli.py list
```

### 直接启动指定工具
```bash
python windows_tools_cli.py run services.msc
python windows_tools_cli.py run appwiz.cpl
python windows_tools_cli.py run regedit
```

### 搜索工具
```bash
python windows_tools_cli.py search 网络
python windows_tools_cli.py search disk
```

### 使用批处理文件
```cmd
wtools list
wtools run services.msc
wtools search 网络
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

共计 **67** 个工具。

## 项目结构

```
windows_tools/
├── dist/                   # 编译好的 exe 文件
│   └── wtools.exe
├── windows_tools_cli.py    # 主程序
├── tools_data.py           # 工具数据
├── wtools.bat              # 批处理启动脚本
├── .gitignore
└── README.md
```

## 自行打包 exe

```bash
pip install pyinstaller
pyinstaller --onefile --name wtools --console windows_tools_cli.py
# 生成的 exe 在 dist/wtools.exe
```
