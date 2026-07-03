"""
Windows 常用工具数据定义
包含通过 Win+R 可调用的各种系统工具、管理控制台、控制面板项等

数据来源优先级:
  ① tools.json 配置文件（由 adder 工具管理）
  ② 本文件的 TOOLS 硬编码列表（回退方案）
"""

import config

# 工具分类
CATEGORY_SYSTEM = "系统管理"
CATEGORY_HARDWARE = "硬件与设备"
CATEGORY_NETWORK = "网络与连接"
CATEGORY_DISK = "磁盘与存储"
CATEGORY_USER = "用户与安全"
CATEGORY_PERFORMANCE = "性能与诊断"
CATEGORY_APPEARANCE = "外观与辅助"
CATEGORY_OTHER = "其他工具"

# 工具数据: (命令, 名称, 分类, 描述)
TOOLS = [
    # ========== 管理控制台 (.msc) ==========
    ("compmgmt.msc",      "计算机管理",     CATEGORY_SYSTEM,      "集成的计算机管理控制台（磁盘、服务、事件等）"),
    ("devmgmt.msc",       "设备管理器",     CATEGORY_HARDWARE,    "查看和更新硬件设备驱动"),
    ("diskmgmt.msc",      "磁盘管理",       CATEGORY_DISK,        "磁盘分区、格式化、更改驱动器号"),
    ("eventvwr.msc",      "事件查看器",     CATEGORY_SYSTEM,      "查看系统和应用程序日志"),
    ("fsmgmt.msc",        "共享文件夹",     CATEGORY_NETWORK,     "管理共享文件夹和会话"),
    ("gpedit.msc",        "本地组策略编辑器", CATEGORY_USER,       "编辑系统组策略（Windows Pro/Enterprise）"),
    ("lusrmgr.msc",       "本地用户和组",   CATEGORY_USER,        "管理本地用户账户和组"),
    ("perfmon.msc",       "性能监视器",     CATEGORY_PERFORMANCE, "监视系统性能和数据收集器集"),
    ("secpol.msc",        "本地安全策略",   CATEGORY_USER,        "配置本地安全策略"),
    ("services.msc",      "服务",           CATEGORY_SYSTEM,      "管理系统服务的启动和运行状态"),
    ("taskschd.msc",      "任务计划程序",   CATEGORY_SYSTEM,      "创建和管理计划任务"),
    ("certlm.msc",        "证书管理器",     CATEGORY_USER,        "管理本地计算机证书"),
    ("certmgr.msc",       "证书管理(用户)", CATEGORY_USER,        "管理当前用户证书"),
    ("azman.msc",         "授权管理器",     CATEGORY_USER,        "管理授权和角色"),
    ("wmimgmt.msc",       "WMI 管理",       CATEGORY_SYSTEM,      "配置 Windows Management Instrumentation"),
    ("tpm.msc",           "TPM 管理",       CATEGORY_HARDWARE,    "管理受信任的平台模块（TPM）"),
    ("printmanagement.msc", "打印管理",     CATEGORY_HARDWARE,    "管理打印机和打印服务器"),
    ("rsop.msc",          "策略结果集",     CATEGORY_USER,        "查看组策略应用结果"),

    # ========== 控制面板项 (.cpl) ==========
    ("appwiz.cpl",        "程序和功能",     CATEGORY_SYSTEM,      "卸载或更改已安装的程序"),
    ("desk.cpl",          "显示设置",       CATEGORY_APPEARANCE,  "调整显示分辨率和多显示器设置"),
    ("firewall.cpl",      "Windows Defender 防火墙", CATEGORY_NETWORK, "配置防火墙规则"),
    ("hdwwiz.cpl",        "设备管理器(CPL)", CATEGORY_HARDWARE,   "添加硬件向导"),
    ("inetcpl.cpl",       "Internet 属性",  CATEGORY_NETWORK,     "配置 Internet 连接和浏览器设置"),
    ("intl.cpl",          "区域",           CATEGORY_SYSTEM,      "设置日期、时间、数字和货币格式"),
    ("main.cpl",          "鼠标属性",       CATEGORY_HARDWARE,    "配置鼠标按钮、指针和移动选项"),
    ("mmsys.cpl",         "声音",           CATEGORY_HARDWARE,    "管理音频设备和声音方案"),
    ("ncpa.cpl",          "网络连接",       CATEGORY_NETWORK,     "查看和管理网络适配器"),
    ("powercfg.cpl",      "电源选项",       CATEGORY_SYSTEM,      "配置电源计划和节能设置"),
    ("sysdm.cpl",         "系统属性",       CATEGORY_SYSTEM,      "查看计算机信息、硬件和远程设置"),
    ("timedate.cpl",      "日期和时间",     CATEGORY_SYSTEM,      "调整系统日期、时间和时区"),
    ("wscui.cpl",         "安全和维护",     CATEGORY_USER,        "查看安全状态和系统维护"),
    ("joy.cpl",           "游戏控制器",     CATEGORY_HARDWARE,    "配置游戏手柄和操纵杆"),
    ("tabletpc.cpl",      "Tablet PC 设置", CATEGORY_HARDWARE,    "配置笔和触摸输入"),

    # ========== 常用系统命令 ==========
    ("cmd",               "命令提示符",     CATEGORY_SYSTEM,      "打开命令提示符窗口"),
    ("powershell",        "PowerShell",     CATEGORY_SYSTEM,      "打开 PowerShell 窗口"),
    ("regedit",           "注册表编辑器",   CATEGORY_SYSTEM,      "查看和编辑 Windows 注册表"),
    ("notepad",           "记事本",         CATEGORY_OTHER,       "打开记事本"),
    ("calc",              "计算器",         CATEGORY_OTHER,       "打开计算器"),
    ("mspaint",           "画图",           CATEGORY_OTHER,       "打开画图程序（Windows 10/11 可能需安装画图3D）"),
    ("explorer",          "文件资源管理器", CATEGORY_OTHER,       "打开文件资源管理器"),
    ("taskmgr",           "任务管理器",     CATEGORY_PERFORMANCE, "查看进程、性能和系统资源使用"),
    ("msconfig",          "系统配置",       CATEGORY_SYSTEM,      "配置启动项、服务和引导选项"),
    ("dxdiag",            "DirectX 诊断工具", CATEGORY_PERFORMANCE, "诊断 DirectX 和多媒体相关组件"),
    ("winver",            "Windows 版本",   CATEGORY_SYSTEM,      "查看 Windows 版本信息"),
    ("osk",               "屏幕键盘",       CATEGORY_APPEARANCE,  "打开屏幕键盘"),
    ("magnify",           "放大镜",         CATEGORY_APPEARANCE,  "打开放大镜辅助工具"),
    ("snippingtool",      "截图工具",       CATEGORY_OTHER,       "打开截图工具"),
    ("control",           "控制面板",       CATEGORY_SYSTEM,      "打开经典控制面板"),
    ("cleanmgr",          "磁盘清理",       CATEGORY_DISK,        "清理磁盘上的临时文件和垃圾文件"),
    ("msinfo32",          "系统信息",       CATEGORY_SYSTEM,      "查看详细的系统硬件和软件信息"),
    ("resmon",            "资源监视器",     CATEGORY_PERFORMANCE, "实时监视 CPU、内存、磁盘和网络"),
    ("charmap",           "字符映射表",     CATEGORY_OTHER,       "查看和选择特殊字符与符号"),
    ("write",             "写字板",         CATEGORY_OTHER,       "打开写字板（Windows 11 24H2+ 已移除）"),
    ("eudcedit",          "专用字符编辑器", CATEGORY_OTHER,       "创建自定义字符"),
    ("odbcad32",          "ODBC 数据源管理器", CATEGORY_SYSTEM,    "管理 ODBC 数据源"),
    ("wscript",           "Windows 脚本宿主设置", CATEGORY_SYSTEM, "配置脚本执行设置"),
    ("cliconfg",          "SQL Server 客户端网络实用工具", CATEGORY_NETWORK, "配置 SQL Server 客户端网络协议"),
    ("dcomcnfg",          "组件服务",       CATEGORY_SYSTEM,      "管理 COM+ 和 DCOM 应用程序"),
    ("dfrgui",            "碎片整理和优化驱动器", CATEGORY_DISK,   "分析和优化磁盘驱动器"),
    ("shrpubw",           "创建共享文件夹向导", CATEGORY_NETWORK,  "创建共享文件夹"),
    ("iexpress",          "IExpress 向导",  CATEGORY_OTHER,       "创建自解压安装包"),
    ("logoff",            "注销",           CATEGORY_SYSTEM,      "注销当前用户"),
    ("shutdown",          "关机/重启",      CATEGORY_SYSTEM,      "关机 (/s)、重启 (/r)、休眠 (/h)"),
    ("utilman",           "轻松访问中心",   CATEGORY_APPEARANCE,  "配置辅助功能设置"),
    ("printui",           "打印用户界面",   CATEGORY_HARDWARE,    "管理打印机和打印首选项"),
    ("mblctr",            "Windows 移动中心", CATEGORY_SYSTEM,     "调整亮度、音量、电池等（笔记本）"),
    ("stikynot",          "便签",           CATEGORY_OTHER,       "打开便签应用"),
    ("schedreg",          "计划注册表任务", CATEGORY_OTHER,       "计划注册表维护任务"),
]


# ── 动态加载（优先 JSON 配置，回退硬编码） ──

_ACTIVE_TOOLS = None


def get_active_tools():
    """
    获取当前活跃的工具列表
    优先使用 JSON 配置文件，不存在则回退到硬编码 TOOLS
    """
    global _ACTIVE_TOOLS
    if _ACTIVE_TOOLS is None:
        loaded = config.load_tools()
        _ACTIVE_TOOLS = loaded if loaded is not None else TOOLS
    return _ACTIVE_TOOLS


def reload_tools():
    """清除缓存，下次调用 get_active_tools 时重新从配置文件读取"""
    global _ACTIVE_TOOLS
    _ACTIVE_TOOLS = None


def get_tools_by_category(tools_list=None):
    """按分类返回工具字典"""
    tools = tools_list if tools_list is not None else get_active_tools()
    result = {}
    for cmd, name, category, desc in tools:
        result.setdefault(category, []).append((cmd, name, desc))
    return result


def search_tools(keyword, tools_list=None):
    """搜索工具"""
    tools = tools_list if tools_list is not None else get_active_tools()
    keyword = keyword.lower()
    results = []
    for cmd, name, category, desc in tools:
        if keyword in cmd.lower() or keyword in name.lower() or keyword in desc.lower():
            results.append((cmd, name, category, desc))
    return results


def get_categories(tools_list=None):
    """获取所有分类（保持顺序）"""
    tools = tools_list if tools_list is not None else get_active_tools()
    seen = []
    for _, _, category, _ in tools:
        if category not in seen:
            seen.append(category)
    return seen
