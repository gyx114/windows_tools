#!/usr/bin/env python3
"""
Windows Tools GUI - 图形化界面版
基于 tkinter，共用 config.py 的业务逻辑
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    add_tool, remove_tool, create_category,
    get_config_status, get_config_path,
    import_tools_from_file, reset_config,
)
from tools_data import get_active_tools, reload_tools, get_categories, search_tools, CATEGORY_OTHER


class WindowsToolsGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows Tools Launcher")
        self.root.geometry("820x580")
        self.root.minsize(700, 450)

        self._build_ui()
        self._load_tools()

    # ── 界面构建 ──

    def _build_ui(self):
        """构建完整界面"""
        # 搜索栏
        search_frame = ttk.Frame(self.root, padding=5)
        search_frame.pack(fill=tk.X)

        ttk.Label(search_frame, text="🔍").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<Return>", lambda e: self._on_search())
        ttk.Button(search_frame, text="清空", command=self._clear_search, width=6).pack(side=tk.LEFT, padx=(5, 0))

        # 主区域 - 分类(左) + 工具列表(右)
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        # 左 - 分类列表
        left_frame = ttk.LabelFrame(paned, text="分类", padding=2)
        self.cat_listbox = tk.Listbox(left_frame, width=22, font=("Microsoft YaHei UI", 10))
        self.cat_listbox.pack(fill=tk.BOTH, expand=True)
        self.cat_listbox.bind("<<ListboxSelect>>", self._on_category_select)
        paned.add(left_frame, weight=1)

        # 右 - 工具列表
        right_frame = ttk.LabelFrame(paned, text="工具（双击启动）", padding=2)
        columns = ("cmd", "name", "desc")
        self.tool_tree = ttk.Treeview(right_frame, columns=columns, show="headings",
                                       selectmode="browse")
        self.tool_tree.heading("cmd", text="命令")
        self.tool_tree.heading("name", text="名称")
        self.tool_tree.heading("desc", text="描述")
        self.tool_tree.column("cmd", width=140, minwidth=100)
        self.tool_tree.column("name", width=120, minwidth=80)
        self.tool_tree.column("desc", width=250, minwidth=150)
        self.tool_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # 滚动条
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tool_tree.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.tool_tree.configure(yscrollcommand=scrollbar.set)

        # 双击启动
        self.tool_tree.bind("<Double-1>", self._on_tool_launch)
        # 回车启动
        self.tool_tree.bind("<Return>", self._on_tool_launch)

        # 右键菜单
        self._build_context_menu()

        paned.add(right_frame, weight=3)

        # 按钮栏
        btn_frame = ttk.Frame(self.root, padding=5)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="🚀 启动", command=self._launch_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="➕ 添加", command=self._add_tool_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="➖ 删除", command=self._remove_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="📁 创建分类", command=self._create_category_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🔄 刷新", command=self._load_tools).pack(side=tk.LEFT, padx=2)

        # 重置按钮(右侧)
        ttk.Button(btn_frame, text="⚙ 重置配置", command=self._reset_config).pack(side=tk.RIGHT, padx=2)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN,
                               anchor=tk.W, padding=(5, 2), foreground="gray")
        status_bar.pack(fill=tk.X)

        # 键盘快捷键
        self.root.bind("<Control-f>", lambda e: self.search_entry.focus_set())
        self.root.bind("<F5>", lambda e: self._load_tools())

    def _build_context_menu(self):
        """构建右键菜单"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="🚀 启动", command=self._launch_selected)
        self.context_menu.add_command(label="✏️ 编辑", command=self._edit_tool_dialog)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="➖ 删除", command=self._remove_selected)
        self.tool_tree.bind("<Button-3>", self._show_context_menu)

    def _show_context_menu(self, event):
        selection = self.tool_tree.selection()
        if selection:
            self.context_menu.tk_popup(event.x_root, event.y_root)

    # ── 数据加载 ──

    def _load_tools(self):
        """加载工具数据到界面"""
        reload_tools()
        self.all_tools = get_active_tools()
        self.categories = get_categories(self.all_tools)

        # 更新分类列表
        self.cat_listbox.delete(0, tk.END)
        for cat in self.categories:
            self.cat_listbox.insert(tk.END, cat)

        # 选中第一个分类
        if self.categories:
            self.cat_listbox.selection_set(0)
            self._on_category_select()

        # 更新状态栏
        status = get_config_status()
        config_path = status["config_path"]
        source = "配置文件" if status["config_exists"] else "内置数据(硬编码)"
        self.status_var.set(
            f"共 {status['total_tools']} 个工具 | {status['total_categories']} 个分类 | "
            f"数据源: {source}"
        )

    def _on_category_select(self, event=None):
        """分类选择事件"""
        selection = self.cat_listbox.curselection()
        if not selection:
            return
        category = self.cat_listbox.get(selection[0])
        self._display_tools(category)

    def _display_tools(self, category):
        """在右侧显示指定分类的工具"""
        # 清空
        for item in self.tool_tree.get_children():
            self.tool_tree.delete(item)

        # 填充
        for cmd, name, cat, desc in self.all_tools:
            if cat == category and cmd:
                self.tool_tree.insert("", tk.END, values=(cmd, name, desc or ""))

    def _on_search(self, *args):
        """搜索事件"""
        keyword = self.search_var.get().strip()
        if not keyword:
            # 清空搜索，回到选中分类
            self._on_category_select()
            return

        # 清空
        for item in self.tool_tree.get_children():
            self.tool_tree.delete(item)

        # 搜索
        results = search_tools(keyword, self.all_tools)
        for cmd, name, cat, desc in results:
            self.tool_tree.insert("", tk.END, values=(cmd, name, desc or ""))

        self.status_var.set(f"搜索「{keyword}」: 找到 {len(results)} 个结果")

    def _clear_search(self):
        """清空搜索"""
        self.search_var.set("")
        self.search_entry.focus_set()
        self._on_category_select()

    # ── 工具操作 ──

    def _get_selected_tool(self):
        """获取当前选中的工具信息"""
        selection = self.tool_tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请先选择一个工具")
            return None
        values = self.tool_tree.item(selection[0], "values")
        if not values:
            return None
        return values  # (cmd, name, desc)

    def _launch_selected(self, event=None):
        """启动选中的工具"""
        tool = self._get_selected_tool()
        if not tool:
            return
        cmd = tool[0]
        try:
            if cmd.endswith((".msc", ".cpl")):
                subprocess.run(f"start {cmd}", shell=True, check=True,
                               stderr=subprocess.DEVNULL)
            else:
                subprocess.run(cmd, shell=True, check=True,
                               stderr=subprocess.DEVNULL)
            self.status_var.set(f"✅ 已启动: {cmd}")
        except Exception as e:
            messagebox.showerror("启动失败", f"无法启动 {cmd}\n该命令可能已从系统中移除")

    def _on_tool_launch(self, event):
        """双击/回车启动"""
        self._launch_selected()

    def _add_tool_dialog(self):
        """添加工具对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加工具")
        dialog.geometry("450x250")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="命令:").grid(row=0, column=0, sticky=tk.W, pady=5)
        cmd_entry = ttk.Entry(frame, width=40)
        cmd_entry.grid(row=0, column=1, pady=5)
        cmd_entry.focus_set()

        ttk.Label(frame, text="名称:").grid(row=1, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(frame, width=40)
        name_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="分类:").grid(row=2, column=0, sticky=tk.W, pady=5)
        cat_combo = ttk.Combobox(frame, values=self.categories, width=37, state="normal")
        cat_combo.grid(row=2, column=1, pady=5)
        cat_combo.set(CATEGORY_OTHER)

        ttk.Label(frame, text="描述:").grid(row=3, column=0, sticky=tk.W, pady=5)
        desc_entry = ttk.Entry(frame, width=40)
        desc_entry.grid(row=3, column=1, pady=5)

        def do_add():
            cmd = cmd_entry.get().strip()
            name = name_entry.get().strip()
            cat = cat_combo.get().strip()
            desc = desc_entry.get().strip()
            if not cmd or not name:
                messagebox.showwarning("输入不完整", "命令和名称为必填项")
                return
            success, msg = add_tool(cmd, name, cat or CATEGORY_OTHER, desc)
            if success:
                self._load_tools()
                dialog.destroy()
                self.status_var.set(f"✅ {msg}")
            else:
                messagebox.showwarning("添加失败", msg)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(btn_frame, text="确定", command=do_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def _edit_tool_dialog(self):
        """编辑工具对话框（仅编辑描述和分类）"""
        tool = self._get_selected_tool()
        if not tool:
            return
        cmd_orig, name_orig, desc_orig = tool

        # 查找当前分类
        current_cat = CATEGORY_OTHER
        for c, n, cat, d in self.all_tools:
            if c == cmd_orig:
                current_cat = cat
                break

        dialog = tk.Toplevel(self.root)
        dialog.title(f"编辑: {cmd_orig}")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=f"命令: {cmd_orig}").grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=3)
        ttk.Label(frame, text=f"名称: {name_orig}").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=3)

        ttk.Label(frame, text="分类:").grid(row=2, column=0, sticky=tk.W, pady=5)
        cat_combo = ttk.Combobox(frame, values=self.categories, width=35, state="normal")
        cat_combo.grid(row=2, column=1, pady=5)
        cat_combo.set(current_cat)

        ttk.Label(frame, text="描述:").grid(row=3, column=0, sticky=tk.W, pady=5)
        desc_entry = ttk.Entry(frame, width=35)
        desc_entry.grid(row=3, column=1, pady=5)
        desc_entry.insert(0, desc_orig)

        def do_edit():
            new_cat = cat_combo.get().strip()
            new_desc = desc_entry.get().strip()
            # 移除旧条目，添加新条目
            success, msg, _ = remove_tool(cmd_orig)
            if success:
                add_tool(cmd_orig, name_orig, new_cat or current_cat, new_desc)
                self._load_tools()
                dialog.destroy()
                self.status_var.set(f"✅ 已更新: {cmd_orig}")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(btn_frame, text="确定", command=do_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def _remove_selected(self):
        """删除选中的工具"""
        tool = self._get_selected_tool()
        if not tool:
            return
        cmd = tool[0]
        if messagebox.askyesno("确认删除", f"确定要删除「{cmd}」吗？"):
            success, msg, info = remove_tool(cmd)
            if success:
                self._load_tools()
                self.status_var.set(f"✅ {msg}")
            else:
                messagebox.showerror("删除失败", msg)

    def _create_category_dialog(self):
        """创建分类对话框"""
        name = simpledialog.askstring("创建分类", "请输入新分类名称:", parent=self.root)
        if not name:
            return
        name = name.strip()
        if not name:
            return
        success, msg = create_category(name)
        if success:
            self._load_tools()
            self.status_var.set(f"✅ {msg}")
        else:
            messagebox.showwarning("创建失败", msg)

    def _reset_config(self):
        """重置配置"""
        if messagebox.askyesno("确认重置", "确定要删除配置文件、恢复内置数据吗？"):
            success, msg = reset_config()
            self._load_tools()
            self.status_var.set(f"{'✅' if success else '⚠'} {msg}")

    # ── 启动 ──

    def run(self):
        self.root.mainloop()


def main():
    app = WindowsToolsGUI()
    app.run()


if __name__ == "__main__":
    main()
