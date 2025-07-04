import tkinter as tk
from tkinter import ttk, Menu
import os
import sys
import json
from components import NumberConverter, CppReference
from lang import lang

def get_resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发和打包环境"""
    try:
        # PyInstaller 运行时，资源位于 sys._MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境，使用项目根目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# 配置文件路径
CONFIG_PATH = get_resource_path('config.json')


class ToolSelector:
    def __init__(self, root):
        self.root = root
        self.load_version()

        # 设置应用图标
        self.set_icon()

        self.build_ui()
        
        
    def build_ui(self):
        """构建主界面UI"""
        # 全局样式设置
        self.apply_global_style()

        self.root.title(f"{lang.get('title')} {self.version}")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
    
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
       
        
        # 菜单栏
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        lang_menu = Menu(menubar, tearoff=0)
        lang_menu.add_command(label="简体中文", command=lambda: self.switch_language("zh"))
        lang_menu.add_command(label="English", command=lambda: self.switch_language("en"))
        menubar.add_cascade(label=f"{lang.get('lang-selector')}", menu=lang_menu)

        self.build_frame()
        
        # 状态栏
        self.status_var = tk.StringVar(value=f"{lang.get('status-ready')}")
        status_bar = ttk.Label(
            root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def build_frame(self):
        # 清除旧 frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # 标题
        title_label = ttk.Label(self.main_frame, text=f"{lang.get('title')}", style="main-title.TLabel")
        title_label.pack(pady=20)
        
        # 工具选择框架
        tool_frame = ttk.LabelFrame(self.main_frame, text=f"{lang.get('select-tool')}")
        tool_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        # 工具按钮
        hex_button = ttk.Button(
            tool_frame, 
            text=f"{lang.get('btn-hex')}", 
            command=self.open_hex_converter,
            width=30
        )
        hex_button.pack(pady=15, padx=20)
        
        cpp_button = ttk.Button(
            tool_frame, 
            text=f"{lang.get('btn-cpp')}", 
            command=self.open_cpp_reference,
            width=30
        )
        cpp_button.pack(pady=15, padx=20)
        
    def set_icon(self):
        """设置应用图标"""
        try:
            base_path = self.get_base_path()
            icon_path = os.path.join(base_path, "assets", "head.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(e)
    
    def apply_global_style(self):
        font_config = FONT_MAP.get(lang.lang_code, FONT_MAP["en"])
        default_font = font_config["font"]
        button_font = font_config["button_font"]
        title_font = font_config["title_font"]

        self.style = ttk.Style()
        self.style.configure(".", font=default_font)  # 全局默认字体
        self.style.configure("TLabel", font=default_font)
        self.style.configure("TButton", font=button_font, padding=10)
        self.style.configure("main-title.TLabel", font=title_font)

        

    def get_base_path(self):
        """获取资源文件的基础路径"""
        return get_resource_path(".")
    
    def open_hex_converter(self):
        """打开进制转换工具"""
        self.status_var.set(f"{lang.get('status-open-hex')}")
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        NumberConverter(self.main_frame, return_callback=self.build_frame)
        self.status_var.set(f"{lang.get('status-ready')}")

    def open_cpp_reference(self):
        """打开C++参考工具"""
        self.status_var.set(f"{lang.get('status-open-cpp')}")
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        CppReference(self.main_frame, return_callback=self.build_frame)
        self.status_var.set(f"{lang.get('status-ready')}")

    def switch_language(self, lang_code):
            from lang import lang  # 确保是最新 lang
            lang.set_language(lang_code)
            
            # 重建 UI
            for widget in self.root.winfo_children():
                widget.destroy()
            self.build_ui()

    def load_version(self):
        """加载版本信息"""
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.version = config.get("version", "Unknown")

DEFAULT_FS = 14
FONT_MAP = {
    "zh": {
        "font": ("等线", DEFAULT_FS),
        "button_font": ("等线", DEFAULT_FS, "bold"),
        "title_font": ("等线", 22, "bold")
    },
    "en": {
        "font": ("Roboto Mono", DEFAULT_FS),
        "button_font": ("Roboto Mono", DEFAULT_FS, "bold"),
        "title_font": ("Roboto Mono", 22, "bold")
    }
}

def save_config(lang_code="zh", version="Unknown"):
    """保存语言配置到文件"""
    config = {"language": lang_code, "version": version}
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToolSelector(root)
    root.mainloop()
    save_config(lang.lang_code, app.version)  # 保存当前语言和版本信息