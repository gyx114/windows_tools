#!/usr/bin/env python3
"""
Windows Tools CLI - 通过命令行快速启动 Windows 系统工具
支持 Win+R 中常用的 .msc、.cpl 及其他系统命令
"""

import subprocess
import sys
import os
from tools_data import TOOLS, get_tools_by_category, get_categories, search_tools


# ── 控制台颜色 ──
class Color:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def print_banner():
    """打印程序标题"""
    banner = f"""
{Color.CYAN}╔══════════════════════════════════════════╗
║      {Color.BOLD}Windows Tools Launcher{Color.RESET}{Color.CYAN}        ║
║      {Color.DIM}快速启动 Windows 系统工具{Color.RESET}{Color.CYAN}      ║
╚══════════════════════════════════════════╝{Color.RESET}
"""
    print(banner)


def list_all_tools():
    """分类列出所有工具"""
    categories = get_categories()
    for category in categories:
        print(f"\n{Color.BOLD}{Color.YELLOW}▓ {category}{Color.RESET}")
        print(f"{Color.DIM}{'─' * 50}{Color.RESET}")
        tools = get_tools_by_category()[category]
        for cmd, name, desc in tools:
            print(f"  {Color.GREEN}{cmd:<22}{Color.RESET} {Color.CYAN}{name:<18}{Color.RESET} {Color.DIM}{desc}{Color.RESET}")


def launch_tool(command):
    """启动指定的 Windows 工具"""
    try:
        # 某些命令需要以特定方式启动
        if command.lower() in ("shutdown",):
            print(f"{Color.YELLOW}⚠ 请使用完整参数启动，例如: shutdown /s /t 0{Color.RESET}")
            return

        # 对于 .msc 和 .cpl 文件，使用 start 命令
        if command.endswith((".msc", ".cpl")):
            subprocess.run(f"start {command}", shell=True, check=True)
        else:
            subprocess.run(command, shell=True, check=True)

        print(f"{Color.GREEN}✔ 已启动: {command}{Color.RESET}")
    except subprocess.CalledProcessError:
        print(f"{Color.RED}✘ 启动失败: {command}{Color.RESET}")
    except FileNotFoundError:
        print(f"{Color.RED}✘ 未找到命令或文件: {command}{Color.RESET}")


def interactive_mode():
    """交互式模式 - 选择工具启动"""
    categories = get_categories()

    # 显示分类菜单
    print(f"\n{Color.BOLD}请选择分类:{Color.RESET}")
    for i, category in enumerate(categories, 1):
        print(f"  {Color.GREEN}{i:>2}.{Color.RESET} {category}")

    # 添加搜索选项
    print(f"  {Color.GREEN} 0.{Color.RESET} {Color.CYAN}搜索工具{Color.RESET}")
    print(f"  {Color.GREEN} q.{Color.RESET} 退出")

    choice = input(f"\n{Color.BOLD}请输入选项: {Color.RESET}").strip().lower()

    if choice == "q":
        return False
    elif choice == "0":
        search_and_launch()
        return True

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(categories):
            category = categories[idx]
            tools = get_tools_by_category()[category]

            print(f"\n{Color.BOLD}{Color.YELLOW}▓ {category}{Color.RESET}")
            for i, (cmd, name, desc) in enumerate(tools, 1):
                print(f"  {Color.GREEN}{i:>2}.{Color.RESET} {Color.CYAN}{cmd:<22}{Color.RESET} {name:<16} {Color.DIM}{desc}{Color.RESET}")

            tool_choice = input(f"\n{Color.BOLD}选择工具编号 (或按 Enter 返回): {Color.RESET}").strip()
            if tool_choice:
                try:
                    t_idx = int(tool_choice) - 1
                    if 0 <= t_idx < len(tools):
                        launch_tool(tools[t_idx][0])
                except ValueError:
                    pass
        else:
            print(f"{Color.RED}无效选项{Color.RESET}")
    except ValueError:
        print(f"{Color.RED}无效选项{Color.RESET}")

    return True


def search_and_launch():
    """搜索工具并启动"""
    keyword = input(f"{Color.BOLD}请输入搜索关键词: {Color.RESET}").strip()
    if not keyword:
        return

    results = search_tools(keyword)
    if not results:
        print(f"{Color.YELLOW}未找到匹配的工具{Color.RESET}")
        return

    print(f"\n{Color.BOLD}搜索结果 ({len(results)} 个匹配):{Color.RESET}")
    for i, (cmd, name, category, desc) in enumerate(results, 1):
        print(f"  {Color.GREEN}{i:>2}.{Color.RESET} {Color.CYAN}{cmd:<22}{Color.RESET} {name:<16} {Color.DIM}[{category}] {desc}{Color.RESET}")

    choice = input(f"\n{Color.BOLD}选择编号启动 (或 Enter 返回): {Color.RESET}").strip()
    if choice:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                launch_tool(results[idx][0])
        except ValueError:
            pass


def show_help():
    """显示帮助信息"""
    print(f"""
{Color.BOLD}使用方法:{Color.RESET}
  python windows_tools_cli.py              {Color.DIM}# 交互式模式{Color.RESET}
  python windows_tools_cli.py list          {Color.DIM}# 列出所有工具{Color.RESET}
  python windows_tools_cli.py run <命令>    {Color.DIM}# 直接启动指定工具{Color.RESET}
  python windows_tools_cli.py search <关键词> {Color.DIM}# 搜索工具{Color.RESET}
  python windows_tools_cli.py help          {Color.DIM}# 显示帮助{Color.RESET}

{Color.BOLD}示例:{Color.RESET}
  python windows_tools_cli.py run services.msc
  python windows_tools_cli.py run appwiz.cpl
  python windows_tools_cli.py search 网络
  python windows_tools_cli.py search disk
""")


def main():
    if len(sys.argv) == 1:
        # 交互式模式
        print_banner()
        print(f"{Color.DIM}输入 q 退出 | 支持 Win+R 常用命令快速启动{Color.RESET}")
        running = True
        while running:
            running = interactive_mode()
    else:
        cmd = sys.argv[1].lower()

        if cmd == "list":
            print_banner()
            list_all_tools()
        elif cmd == "run" and len(sys.argv) > 2:
            launch_tool(sys.argv[2])
        elif cmd == "search" and len(sys.argv) > 2:
            keyword = " ".join(sys.argv[2:])
            results = search_tools(keyword)
            if results:
                print(f"{Color.BOLD}搜索结果 ({len(results)} 个匹配):{Color.RESET}\n")
                for cmd_name, name, category, desc in results:
                    print(f"  {Color.GREEN}{cmd_name:<22}{Color.RESET} {Color.CYAN}{name:<18}{Color.RESET} [{category}] {Color.DIM}{desc}{Color.RESET}")
            else:
                print(f"{Color.YELLOW}未找到匹配的工具{Color.RESET}")
        elif cmd == "help":
            print_banner()
            show_help()
        else:
            print_banner()
            print(f"{Color.YELLOW}未知命令: {cmd}{Color.RESET}")
            show_help()


if __name__ == "__main__":
    main()
