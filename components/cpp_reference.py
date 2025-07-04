import tkinter as tk
from tkinter import ttk
import os
import sys
from lang import lang

class CppReference(tk.Frame):
    
    def __init__(self, parent, return_callback=None):
        super().__init__(parent)
        self.return_callback = return_callback
        self.pack(fill="both", expand=True)
        
        # 主框架
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧：数据结构选择
        left_frame = ttk.LabelFrame(main_frame, text=f"{lang.get('cpp-reference.data-structures')}")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=5)
        
        # 数据结构列表
        self.structures_list = tk.Listbox(
            left_frame, 
            width=15,
            font=("Arial", 14),
            relief="groove",
        )
        self.structures_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 填充数据结构列表
        for structure in sorted(CPP_DATA.keys()):
            self.structures_list.insert(tk.END, structure)
        
        # 默认选择第一个
        self.structures_list.selection_set(0)
        self.structures_list.bind("<<ListboxSelect>>", self.on_structure_select)
        
        # 右侧：详细信息
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 数据结构描述
        desc_frame = ttk.LabelFrame(right_frame, text=f"{lang.get('cpp-reference.description')}")
        desc_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.desc_var = tk.StringVar()
        desc_label = ttk.Label(
            desc_frame, 
            textvariable=self.desc_var,
            wraplength=500,
            font=("Times", 14),
        )
        desc_label.pack(padx=10, pady=10, fill=tk.X)
        
        # 函数列表
        func_frame = ttk.LabelFrame(right_frame, text=f"{lang.get('cpp-reference.functions')}")
        func_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建树状视图
        columns = ("function", "description")
        self.func_tree = ttk.Treeview(
            func_frame, 
            columns=columns, 
            show="headings",
            selectmode="browse"
        )

        # 设置表行间距
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)  # 设置行高为 30 像素
        style.configure("Treeview.Heading", font=("Times", 12, "bold"))
        
        # 设置列
        self.func_tree.heading("function", text=f"{lang.get('cpp-reference.functions')}")
        self.func_tree.heading("description", text=f"{lang.get('cpp-reference.description')}")
        self.func_tree.column("function", width=150, minwidth=100)
        self.func_tree.column("description", width=350, minwidth=200)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(func_frame, orient="vertical", command=self.func_tree.yview)
        self.func_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.func_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 返回按钮
        if self.return_callback:
            back_btn = ttk.Button(self, text=f"← {lang.get('back')}", command=self.return_callback)
            back_btn.pack(pady=(5, 10))
        
        # 初始化显示
        self.on_structure_select()
    
    def get_base_path(self):
        """获取资源文件的基础路径"""
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            return os.path.dirname(base_path)  # 返回到项目根目录
        except Exception:
            return os.path.dirname(os.path.abspath(sys.argv[0]))
    
    def on_structure_select(self, event=None):
        """当选择数据结构时更新显示"""
        selection = self.structures_list.curselection()
        if not selection:
            return
        
        structure = self.structures_list.get(selection[0])
        data = CPP_DATA.get(structure, {})
        
        # 更新描述
        self.desc_var.set(data.get("description", ""))
        
        # 更新函数列表
        self.func_tree.delete(*self.func_tree.get_children())
        
        for func, desc in data.get("functions", {}).items():
            self.func_tree.insert("", tk.END, values=(func, desc))


# C++数据结构参考数据
CPP_DATA = {
    "vector": {
        "description": "std::vector - 动态数组容器",
        "functions": {
            "push_back()": "在向量末尾添加元素",
            "pop_back()": "删除向量末尾的元素",
            "at(index)": "访问指定位置的元素，带边界检查",
            "size()": "返回向量中的元素数量",
            "clear()": "清除向量中的所有元素",
            "reserve(size)": "预留存储空间",
            "resize(size)": "改变向量的大小",
            "empty()": "检查向量是否为空",
            "front()": "访问第一个元素",
            "back()": "访问最后一个元素",
        }
    },
    "list": {
        "description": "std::list - 双向链表容器",
        "functions": {
            "push_front()": "在链表开头插入元素",
            "push_back()": "在链表末尾插入元素",
            "pop_front()": "删除链表开头的元素",
            "pop_back()": "删除链表末尾的元素",
            "insert(iterator, value)": "在指定位置插入元素",
            "erase(iterator)": "删除指定位置的元素",
            "size()": "返回链表中的元素数量",
            "clear()": "清除链表中的所有元素",
            "sort()": "对链表元素进行排序",
            "merge(list)": "合并两个有序链表",
        }
    },
    "map": {
        "description": "std::map - 关联容器，键值对集合",
        "functions": {
            "insert({key, value})": "插入键值对",
            "erase(key)": "删除指定键的元素",
            "find(key)": "查找指定键的元素",
            "at(key)": "访问指定键的元素，带边界检查",
            "size()": "返回map中的元素数量",
            "clear()": "清除map中的所有元素",
            "count(key)": "返回具有指定键的元素数量",
            "empty()": "检查map是否为空",
            "begin()": "返回指向第一个元素的迭代器",
            "end()": "返回指向末尾的迭代器",
        }
    },
    "string": {
        "description": "std::string - 字符串类",
        "functions": {
            "length()": "返回字符串长度",
            "append(str)": "在字符串末尾添加内容",
            "substr(start, length)": "返回子字符串",
            "find(str)": "查找子字符串",
            "replace(pos, len, str)": "替换字符串的一部分",
            "c_str()": "返回C风格字符串",
            "clear()": "清除字符串内容",
            "empty()": "检查字符串是否为空",
            "at(index)": "访问指定位置的字符",
            "compare(str)": "比较两个字符串",
        }
    },
    "array": {
        "description": "std::array - 固定大小数组容器",
        "functions": {
            "at(index)": "访问指定位置的元素，带边界检查",
            "operator[]": "访问指定位置的元素",
            "front()": "访问第一个元素",
            "back()": "访问最后一个元素",
            "size()": "返回数组中的元素数量",
            "fill(value)": "用指定值填充数组",
            "empty()": "检查数组是否为空",
            "begin()": "返回指向第一个元素的迭代器",
            "end()": "返回指向末尾的迭代器",
            "data()": "返回指向数组第一个元素的指针",
        }
    },
    "set": {
        "description": "std::set - 有序唯一元素集合",
        "functions": {
            "insert(value)": "插入元素",
            "erase(value)": "删除元素",
            "find(value)": "查找元素",
            "size()": "返回set中的元素数量",
            "clear()": "清除set中的所有元素",
            "count(value)": "返回具有指定值的元素数量",
            "empty()": "检查set是否为空",
            "begin()": "返回指向第一个元素的迭代器",
            "end()": "返回指向末尾的迭代器",
        }
    }
}
