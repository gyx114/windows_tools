#!/usr/bin/env python3
"""
Windows Tools CLI - 通过命令行快速启动 Windows 系统工具
支持 Win+R 中常用的 .msc、.cpl 及其他系统命令
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
from tools_data import TOOLS, get_tools_by_category, get_categories, search_tools, CATEGORY_OTHER
from config import (
    add_tool, remove_tool, create_category,
    get_config_status, get_config_path,
    import_tools_from_file, reset_config,
)


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
║      {Color.BOLD}Windows Tools Launcher{Color.RESET}{Color.CYAN}              ║
║      {Color.DIM}快速启动 Windows 系统工具{Color.RESET}{Color.CYAN}           ║
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
    # 检查命令是否存在
    cmd_lower = command.lower()

    # shutdown 需要参数
    if cmd_lower in ("shutdown",):
        print(f"{Color.YELLOW}⚠ 请使用完整参数启动，例如: shutdown /s /t 0{Color.RESET}")
        return

    # .msc/.cpl 文件：检查 System32 目录
    if command.endswith((".msc", ".cpl")):
        sys_path = Path(os.environ["SystemRoot"], "System32", command)
        if not sys_path.exists():
            print(f"{Color.RED}✘ 未找到: {command}{Color.RESET}")
            return
    else:
        # 可执行文件：用 shutil.which 搜索 PATH
        found = shutil.which(command)
        if not found:
            print(f"{Color.RED}✘ 未找到: {command}（该程序可能未安装或已从系统中移除）{Color.RESET}")
            return

    # 启动（使用 start 异步启动，避免 GUI 程序拦截控制台）
    try:
        subprocess.run(f"start \"\" {command}", shell=True,
                       stderr=subprocess.DEVNULL)
        print(f"{Color.GREEN}✔ 已启动: {command}{Color.RESET}")
    except Exception:
        print(f"{Color.RED}✘ 启动失败: {command}{Color.RESET}")


def interactive_mode():
    """交互式模式 - 选择工具启动"""
    categories = get_categories()

    # 显示分类菜单
    print(f"\n{Color.BOLD}请选择分类:{Color.RESET}")
    for i, category in enumerate(categories, 1):
        print(f"  {Color.GREEN}{i:>2}.{Color.RESET} {category}")

    # 添加搜索选项
    print(f"  {Color.GREEN} 0.{Color.RESET} {Color.CYAN}搜索工具{Color.RESET}")
    print(f"  {Color.GREEN} g.{Color.RESET} {Color.BLUE}图形界面模式{Color.RESET}")
    print(f"  {Color.GREEN} m.{Color.RESET} {Color.MAGENTA}管理工具（添加/删除）{Color.RESET}")
    print(f"  {Color.GREEN} q.{Color.RESET} 退出")

    choice = input(f"\n{Color.BOLD}请输入选项: {Color.RESET}").strip().lower()

    if choice == "q":
        return False
    elif choice == "0":
        search_and_launch()
        return True
    elif choice == "g":
        launch_gui()
        return True
    elif choice == "m":
        show_manage_tools()
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


def launch_gui():
    """从 CLI 交互模式启动图形界面"""
    print(f"\n{Color.CYAN}正在启动图形界面...{Color.RESET}")
    try:
        import wtools_gui
        wtools_gui.main()
    except ImportError as e:
        print(f"{Color.RED}✘ 无法加载图形界面: {e}{Color.RESET}")
        print(f"{Color.YELLOW}  请确保 wtools_gui.py 存在{Color.RESET}")
    input(f"\n{Color.DIM}按 Enter 返回 CLI 菜单...{Color.RESET}")


def show_manage_tools():
    """在交互模式中管理工具（直接使用 config 模块，无需 adder）"""
    print(f"\n{Color.BOLD}{Color.MAGENTA}▓ 管理工具{Color.RESET}")
    print(f"\n  {Color.GREEN}1.{Color.RESET} 添加工具")
    print(f"  {Color.GREEN}2.{Color.RESET} 删除工具")
    print(f"  {Color.GREEN}3.{Color.RESET} 查看配置状态")
    print(f"  {Color.GREEN}4.{Color.RESET} 创建新分类")
    print(f"  {Color.GREEN}5.{Color.RESET} 从 JSON 文件导入")
    print(f"  {Color.GREEN}6.{Color.RESET} 重置配置")
    print(f"  {Color.GREEN}0.{Color.RESET} 返回主菜单")
    print(f"  {Color.GREEN}q.{Color.RESET} 退出")

    choice = input(f"\n{Color.BOLD}请选择: {Color.RESET}").strip()

    if choice == "1":
        cmd = input("命令 (例如: wt.exe): ").strip()
        name = input("显示名称 (例如: Terminal): ").strip()
        if cmd and name:
            cat = input("分类 (按Enter使用「其他工具」): ").strip() or CATEGORY_OTHER
            desc = input("描述 (可选): ").strip()
            success, msg = add_tool(cmd, name, cat, desc)
            print(f"{Color.GREEN if success else Color.YELLOW}{'✔' if success else '⚠'} {msg}{Color.RESET}")

    elif choice == "2":
        target = input("要删除的命令: ").strip()
        if target:
            success, msg, info = remove_tool(target)
            if success:
                print(f"{Color.GREEN}✔ {msg}{Color.RESET}")
                for c, n, cat in info:
                    print(f"  已删除: [{cat}] {c} → {n}")
            else:
                print(f"{Color.YELLOW}⚠ {msg}{Color.RESET}")

    elif choice == "3":
        status = get_config_status()
        print(f"\n{Color.BOLD}配置状态:{Color.RESET}")
        print(f"  配置文件: {Color.CYAN}{status['config_path']}{Color.RESET}")
        print(f"  状态:     {'✅ 存在' if status['config_exists'] else '❌ 不存在（使用内置数据）'}")
        print(f"  工具总数: {status['total_tools']}")
        print(f"  分类数量: {status['total_categories']}")

    elif choice == "4":
        cat_name = input("新分类名称: ").strip()
        if cat_name:
            success, msg = create_category(cat_name)
            print(f"{Color.GREEN if success else Color.YELLOW}{'✔' if success else '⚠'} {msg}{Color.RESET}")

    elif choice == "5":
        fp = input("JSON 文件路径: ").strip()
        if fp:
            success, msg, added, skipped = import_tools_from_file(fp)
            print(f"{Color.GREEN if success else Color.RED}{'✔' if success else '✘'} {msg}{Color.RESET}")

    elif choice == "6":
        confirm = input(f"{Color.YELLOW}确定要重置配置吗？(y/N): {Color.RESET}").strip().lower()
        if confirm == "y":
            success, msg = reset_config()
            print(f"{Color.GREEN if success else Color.YELLOW}{'✔' if success else '⚠'} {msg}{Color.RESET}")

    elif choice == "q":
        return False

    input(f"\n{Color.DIM}按 Enter 继续...{Color.RESET}")


def show_help():
    """显示帮助信息"""
    print(f"""
{Color.BOLD}使用方法:{Color.RESET}
  python windows_tools_cli.py              {Color.DIM}# 交互式模式{Color.RESET}
  python windows_tools_cli.py list          {Color.DIM}# 列出所有工具{Color.RESET}
  python windows_tools_cli.py run <命令>    {Color.DIM}# 直接启动指定工具{Color.RESET}
  python windows_tools_cli.py search <关键词> {Color.DIM}# 搜索工具{Color.RESET}
  python windows_tools_cli.py --gui         {Color.DIM}# 启动图形界面{Color.RESET}
  python windows_tools_cli.py help          {Color.DIM}# 显示帮助{Color.RESET}

{Color.BOLD}管理工具（添加/删除/导入）:{Color.RESET}
  python adder.py help     {Color.DIM}# 查看 adder 使用说明{Color.RESET}
  python adder.py add <命令> <名称> [分类] [描述]  {Color.DIM}# 添加工具{Color.RESET}
  python adder.py remove <命令>  {Color.DIM}# 删除工具{Color.RESET}
  python adder.py category <分类名> {Color.DIM}# 新建分类{Color.RESET}
  python adder.py import <文件.json> {Color.DIM}# 批量导入{Color.RESET}

{Color.BOLD}示例:{Color.RESET}
  python windows_tools_cli.py run services.msc
  python windows_tools_cli.py run appwiz.cpl
  python windows_tools_cli.py search 网络
  python windows_tools_cli.py --gui
  python adder.py add wt.exe Terminal 终端 "Windows Terminal"
""")


def main():
    # --gui 参数：启动图形界面
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--gui", "-g"):
        try:
            from wtools_gui import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"{Color.RED}✘ 无法加载图形界面: {e}{Color.RESET}")
            print(f"  {Color.DIM}请确保 wtools_gui.py 在同目录下{Color.RESET}")
        return

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
