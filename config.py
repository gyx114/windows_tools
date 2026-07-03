"""
配置管理模块
处理 tools.json 的读写和路径查找

策略: 分级查找配置文件
  ① <exe/脚本所在目录>/tools.json    ← 便携模式
  ② APPDATA/windows_tools/tools.json  ← 系统安装模式（如放入 System32）
  ③ 都不存在 → 使用内置硬编码数据（只读回退）
"""

import os
import sys
import json

CONFIG_FILENAME = 'tools.json'


def get_exe_dir():
    """获取 exe（PyInstaller 打包后）或脚本所在目录"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def get_config_dir():
    """
    获取配置目录（分级查找）
    返回一个可写入的目录路径
    """
    exe_dir = get_exe_dir()
    exe_config = os.path.join(exe_dir, CONFIG_FILENAME)

    # ① 如果 exe 目录已有配置文件，直接用（便携模式）
    if os.path.exists(exe_config):
        return exe_dir

    # ② 检查 exe 目录是否可写（非系统目录时可写）
    test_file = os.path.join(exe_dir, '.write_test')
    try:
        with open(test_file, 'w') as f:
            f.write('')
        os.remove(test_file)
        return exe_dir
    except (IOError, PermissionError, OSError):
        pass

    # ③ 回退到 %APPDATA% （System32 等只读目录时）
    appdata_dir = os.path.join(
        os.environ.get('APPDATA', os.path.expanduser('~')),
        'windows_tools'
    )
    os.makedirs(appdata_dir, exist_ok=True)
    return appdata_dir


def get_config_path():
    """获取 tools.json 完整路径"""
    return os.path.join(get_config_dir(), CONFIG_FILENAME)


def load_tools():
    """
    从 JSON 配置文件加载工具列表
    返回: [(cmd, name, category, desc), ...] 或 None（文件不存在/解析失败）
    """
    config_path = get_config_path()
    if not os.path.exists(config_path):
        return None

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        tools = []
        for item in data.get('tools', []):
            if isinstance(item, list) and len(item) >= 4:
                tools.append((item[0], item[1], item[2], item[3]))
            elif isinstance(item, dict):
                tools.append((
                    item.get('cmd', ''),
                    item.get('name', ''),
                    item.get('category', '其他工具'),
                    item.get('desc', '')
                ))
        return tools if tools else None

    except (json.JSONDecodeError, IOError, KeyError):
        return None


def save_tools(tools):
    """
    保存工具列表到 JSON 配置文件
    tools: [(cmd, name, category, desc), ...]
    返回: 保存的完整路径
    """
    config_path = get_config_path()
    data = {
        'version': 1,
        'tools': [[cmd, name, cat, desc] for cmd, name, cat, desc in tools],
    }
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return config_path


# ═══════════════════════════════════════════════
# 核心管理逻辑（会被 wtools.exe 和 adder.py 共用）
# ═══════════════════════════════════════════════

def add_tool(cmd_name, display_name, category="其他工具", desc=""):
    """
    添加一个工具到配置。
    返回: (success, message)
    """
    # 延迟导入 tools_data，避免循环依赖
    from tools_data import get_active_tools, reload_tools

    tools = get_active_tools()
    for existing_cmd, _, _, _ in tools:
        if existing_cmd.lower() == cmd_name.lower():
            return False, f"工具 '{cmd_name}' 已存在"

    tools.append((cmd_name, display_name, category, desc))
    config_path = save_tools(tools)
    reload_tools()
    return True, f"已添加: [{category}] {cmd_name} → {display_name}"


def remove_tool(cmd_name):
    """
    从配置中删除一个工具。
    返回: (success, message, removed_info)
    """
    from tools_data import get_active_tools, reload_tools

    target = cmd_name.lower()
    tools = get_active_tools()
    removed = []
    keep = []

    for t in tools:
        if t[0].lower() == target:
            removed.append(t)
        else:
            keep.append(t)

    if not removed:
        return False, f"未找到工具: {cmd_name}", None

    save_tools(keep)
    reload_tools()
    info = [(r[0], r[1], r[2]) for r in removed]
    return True, f"已删除: {cmd_name}", info


def create_category(name):
    """
    创建一个新分类（通过添加标记条目）。
    返回: (success, message)
    """
    from tools_data import get_active_tools, reload_tools, get_categories

    tools = get_active_tools()
    existing = get_categories(tools)

    if name in existing:
        return False, f"分类 '{name}' 已存在"

    tools.append(("", f"[{name}]", name, ""))
    save_tools(tools)
    reload_tools()
    return True, f"已创建分类: {name}"


def get_config_status():
    """
    获取配置状态概览。
    返回: dict
    """
    from tools_data import get_active_tools, get_categories

    tools = get_active_tools()
    config_path = get_config_path()
    categories = get_categories(tools)

    cat_counts = {}
    for cat in categories:
        count = sum(1 for _, _, c, _ in tools if c == cat and _ != "")
        cat_counts[cat] = count

    return {
        "config_path": config_path,
        "config_exists": os.path.exists(config_path),
        "total_tools": len(tools),
        "total_categories": len(categories),
        "categories": cat_counts,
    }


def import_tools_from_file(filepath):
    """
    从 JSON 文件批量导入工具。
    返回: (success, message, added_count, skipped_count)
    """
    from tools_data import get_active_tools, reload_tools, CATEGORY_OTHER

    if not os.path.exists(filepath):
        return False, f"文件不存在: {filepath}", 0, 0

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, f"读取文件失败: {e}", 0, 0

    imported = []
    for item in data.get("tools", []):
        if isinstance(item, list) and len(item) >= 4:
            imported.append((item[0], item[1], item[2], item[3]))
        elif isinstance(item, dict):
            imported.append((
                item.get("cmd", ""),
                item.get("name", ""),
                item.get("category", CATEGORY_OTHER),
                item.get("desc", ""),
            ))

    if not imported:
        return False, "文件中未找到有效工具数据", 0, 0

    tools = get_active_tools()
    existing_cmds = {t[0].lower() for t in tools}
    added = 0
    skipped = 0

    for item in imported:
        if not item[0]:
            continue
        if item[0].lower() in existing_cmds:
            skipped += 1
            continue
        tools.append(item)
        existing_cmds.add(item[0].lower())
        added += 1

    if added > 0:
        save_tools(tools)
        reload_tools()

    return True, f"导入完成: 新增 {added}, 跳过 {skipped}", added, skipped


def reset_config():
    """
    删除配置文件，恢复内置数据。
    返回: (success, message)
    """
    config_path = get_config_path()
    if not os.path.exists(config_path):
        return False, "无配置文件需要重置"

    from tools_data import reload_tools
    os.remove(config_path)
    reload_tools()
    return True, f"已删除配置文件: {config_path}"
