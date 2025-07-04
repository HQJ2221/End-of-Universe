# lang.py
import json
import sys
import os

def get_resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发和打包环境"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

CONFIG_PATH = get_resource_path('config.json')

class LangManager:
    def __init__(self):
        self.lang_code = self.load_config()
        self.lang_data = {}
        self.load_language()

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f).get("language", "zh")
        return "zh"

    def load_language(self):
        path = os.path.join(os.path.dirname(__file__), 'i18n', f'{self.lang_code}.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.lang_data = json.load(f)
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m 加载语言文件失败: {e}")
            self.lang_data = {}

    def set_language(self, lang_code):
        self.lang_code = lang_code
        self.load_language()

    def get(self, key):
        # 支持嵌套路径解析
        keys = key.split('.')
        data = self.lang_data
        for k in keys:
            try:
                data = data[k]
            except (KeyError, TypeError):
                return "Missing translation"
        return data

# 全局语言对象
lang = LangManager()
