import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from lang import lang

class NumberConverter(tk.Frame):
    def __init__(self, parent, return_callback=None):
        super().__init__(parent)
        self.return_callback = return_callback
        self.pack(fill="both", expand=True)
        
        # 输入部分
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=15, padx=20, fill="x")

        ttk.Label(input_frame, text=f"{lang.get('number-converter.input')}").grid(row=0, column=0, padx=(0, 5))
        self.number_entry = ttk.Entry(input_frame, width=25)
        self.number_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text=f"{lang.get('number-converter.num-system')}").grid(row=0, column=2, padx=(10, 5))
        self.base_var = tk.StringVar()
        self.base_combobox = ttk.Combobox(
            input_frame, 
            textvariable=self.base_var,
            width=10,
            state="readonly"
        )
        self.base_combobox["values"] = ("Binary", "Octal", "Decimal", "Hexadecimal")
        self.base_combobox.current(2)  # 默认十进制
        self.base_combobox.grid(row=0, column=3, padx=5)
        
        # 转换按钮
        convert_btn = ttk.Button(
            self, 
            text=f"{lang.get('number-converter.convert')}",
            command=self.convert,
            width=15
        )
        convert_btn.pack(pady=10)
        
        # 结果展示
        result_frame = ttk.LabelFrame(self, text=f"{lang.get('number-converter.results')}")
        result_frame.pack(pady=15, padx=20, fill="both", expand=True)
        
        # 创建结果标签
        bases = [("Binary", 2), ("Octal", 8), ("Decimal", 10), ("Hexadecimal", 16)]
        self.result_vars = {}
        
        for i, (base_name, base_value) in enumerate(bases):
            ttk.Label(result_frame, text=f"{base_name}:").grid(
                row=i, column=0, padx=10, pady=5, sticky="e"
            )
            self.result_vars[base_value] = tk.StringVar(value="")
            ttk.Label(
                result_frame, 
                textvariable=self.result_vars[base_value],
                foreground="blue",
                font=("Arial", 10, "bold")
            ).grid(row=i, column=1, padx=10, pady=5, sticky="w")

        # 返回按钮
        if self.return_callback:
            back_btn = ttk.Button(self, text=f"← {lang.get('back')}", command=self.return_callback)
            back_btn.pack(pady=(5, 10))

    def convert(self):
        # 获取输入
        input_str = self.number_entry.get().strip()
        base_type = self.base_var.get()
        
        # 验证输入
        if not input_str:
            messagebox.showerror("Error", "Please enter a number")
            return
        
        # 根据进制类型进行转换
        try:
            base_map = {
                "Binary": 2,
                "Octal": 8,
                "Decimal": 10,
                "Hexadecimal": 16
            }
            base_value = base_map[base_type]
            
            # 特殊处理：十六进制允许带0x前缀
            if base_value == 16 and input_str.startswith("0x"):
                input_str = input_str[2:]
            
            # 转换为十进制
            decimal_value = int(input_str, base_value)
            
            # 转换为其他进制
            self.result_vars[2].set(bin(decimal_value))
            self.result_vars[8].set(oct(decimal_value))
            self.result_vars[10].set(str(decimal_value))
            self.result_vars[16].set(hex(decimal_value))
            
        except ValueError as e:
            error_msg = f"{lang.get('number-converter.invalid-input')}:\n {str(e)}"
            if base_value == 2:
                error_msg = "Binary can only contain 0 and 1"
            elif base_value == 8:
                error_msg = "Octal can only contain 0-7"
            elif base_value == 16:
                error_msg = "Hexadecimal can only contain 0-9 and A-F"
            messagebox.showerror("Conversion Error", error_msg)
            # 清空结果
            for var in self.result_vars.values():
                var.set("")
    
    def get_base_path(self):
        """获取资源文件的基础路径"""
        try:
            # 处理 PyInstaller 打包后的路径
            if getattr(sys, 'frozen', False):
                # 打包后的可执行文件路径
                base_path = sys._MEIPASS
            else:
                # 开发环境路径
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            return base_path
        except Exception:
            return os.path.dirname(os.path.abspath(sys.argv[0]))

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberConverter(root)
    root.mainloop()