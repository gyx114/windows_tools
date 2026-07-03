#!/usr/bin/env python3
"""
Windows Tools Adder - 管理工具条目（基于 config.py 的 CLI 包装）

用法:
  adder add <命令> <名称> [分类] [描述]    添加工具
  adder remove <命令>                      删除工具
  adder category <分类名>                  创建新分类
  adder list                               查看配置状态
  adder import <文件.json>                 从 JSON 文件批量导入
  adder reset                              重置配置，恢复内置数据
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    add_tool, remove_tool, create_category,
    get_config_status, import_tools_from_file, reset_config,
    get_config_path,
)
from tools_data import CATEGORY_OTHER


class Color:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def print_banner():
    print(f"""
{Color.CYAN}╔══════════════════════════════════════════╗
║      {Color.BOLD}Windows Tools Adder{Color.RESET}{Color.CYAN}             ║
║      {Color.DIM}管理工具条目与分类{Color.RESET}{Color.CYAN}              ║
╚══════════════════════════════════════════╝{Color.RESET}
""")


def cmd_add(args):
    if len(args) < 2:
        print(f"用法: {Color.BOLD}adder add <命令> <名称> [分类] [描述]{Color.RESET}")
        return
    cmd_name = args[0]
    display_name = args[1]
    category = args[2] if len(args) > 2 else CATEGORY_OTHER
    desc = args[3] if len(args) > 3 else ""

    success, msg = add_tool(cmd_name, display_name, category, desc)
    if success:
        print(f"{Color.GREEN}✔ {msg}{Color.RESET}")
        print(f"  配置: {Color.DIM}{get_config_path()}{Color.RESET}")
    else:
        print(f"{Color.YELLOW}⚠ {msg}{Color.RESET}")


def cmd_remove(args):
    if not args:
        print(f"用法: {Color.BOLD}adder remove <命令>{Color.RESET}")
        return
    success, msg, info = remove_tool(args[0])
    if success:
        print(f"{Color.GREEN}✔ {msg}{Color.RESET}")
        for c, n, cat in info:
            print(f"  已删除: [{cat}] {c} → {n}")
    else:
        print(f"{Color.YELLOW}⚠ {msg}{Color.RESET}")


def cmd_category(args):
    if not args:
        print(f"用法: {Color.BOLD}adder category <分类名称>{Color.RESET}")
        return
    success, msg = create_category(args[0])
    if success:
        print(f"{Color.GREEN}✔ {msg}{Color.RESET}")
        print(f"  配置: {Color.DIM}{get_config_path()}{Color.RESET}")
    else:
        print(f"{Color.YELLOW}⚠ {msg}{Color.RESET}")


def cmd_list(args):
    status = get_config_status()
    print(f"\n{Color.BOLD}配置状态:{Color.RESET}")
    print(f"  配置文件: {Color.CYAN}{status['config_path']}{Color.RESET}")
    print(f"  状态:     {'✅ 存在' if status['config_exists'] else '❌ 不存在（使用内置数据）'}")
    print(f"\n{Color.BOLD}工具概览:{Color.RESET}")
    print(f"  工具总数: {status['total_tools']}")
    print(f"  分类数量: {status['total_categories']}")
    print(f"\n{Color.BOLD}分类列表:{Color.RESET}")
    for cat, count in status['categories'].items():
        print(f"  {Color.GREEN}{cat}{Color.RESET} ({count} 个工具)")


def cmd_import(args):
    if not args:
        print(f"用法: {Color.BOLD}adder import <文件.json>{Color.RESET}")
        return
    success, msg, added, skipped = import_tools_from_file(args[0])
    if success:
        print(f"{Color.GREEN}✔ {msg}{Color.RESET}")
        print(f"  来源: {Color.DIM}{args[0]}{Color.RESET}")
    else:
        print(f"{'✘' if '失败' in msg else '⚠'} {msg}{Color.RESET}")


def cmd_reset(args):
    success, msg = reset_config()
    if success:
        print(f"{Color.GREEN}✔ {msg}{Color.RESET}")
        print(f"  下次将使用内置硬编码数据")
    else:
        print(f"{Color.YELLOW}⚠ {msg}{Color.RESET}")


def show_usage():
    print_banner()
    print(f"""{Color.BOLD}用法:{Color.RESET}
  {Color.GREEN}adder add <命令> <名称> [分类] [描述]{Color.RESET}
        添加一个新工具（分类不存在时自动创建）

  {Color.GREEN}adder remove <命令>{Color.RESET}
        删除指定工具

  {Color.GREEN}adder category <分类名>{Color.RESET}
        创建一个新的空分类

  {Color.GREEN}adder list{Color.RESET}
        查看配置状态和工具概览

  {Color.GREEN}adder import <文件.json>{Color.RESET}
        从 JSON 文件批量导入工具

  {Color.GREEN}adder reset{Color.RESET}
        重置配置，恢复为内置数据

{Color.BOLD}示例:{Color.RESET}
  adder add wt.exe Terminal 终端 "Windows Terminal"
  adder add bash C:\\Windows\\System32\\bash.exe "WSL"
  adder remove bash
  adder category "开发者工具"
  adder import my_tools.json
""")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help', 'help'):
        show_usage()
        return

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    cmds = {
        'add': cmd_add, 'remove': cmd_remove, 'category': cmd_category,
        'list': cmd_list, 'import': cmd_import, 'reset': cmd_reset,
    }

    if cmd in cmds:
        cmds[cmd](args)
    else:
        print(f"{Color.RED}未知命令: {cmd}{Color.RESET}\n")
        show_usage()


if __name__ == '__main__':
    main()
