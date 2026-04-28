import atexit
import os
import sys
import time
import webview
import keyboard
import pyperclip

class Texts:
    def __init__(self):
        self.texts:str=''
        self.can_write:bool=False
        self.hotkey=None
        self.bind_keyboard()
        atexit.register(self.clear_keyboard)
    def get_texts(self, texts):
        self.texts=texts
        self.process()
        self.can_write=True
        # print(self.texts)
        return {"status": "success", "message": "代码已保存"}
    def process(self):
        text:str=''
        lines=self.texts.splitlines()
        for i,line in enumerate(lines):
            line=line.strip()
            if not line or line=='':
                continue
            clear_line:str = line.strip() + " "
            space_num=(len(clear_line)-len(clear_line.lstrip()))//4
            text+=clear_line+'\n'
            for j in range(space_num):
                text+='\b'
        self.texts=text.rstrip('\n')
    def write(self):
        if self.can_write:
            time.sleep(0.5)
            keyboard.write(self.texts,delay=0.008)
            time.sleep(0.5)
    def clear_texts(self):
        self.texts=''
        self.can_write=False
        return {"status": "success", "message": "已清空代码"}
    def bind_keyboard(self):
        if self.hotkey:
            keyboard.remove_hotkey(self.hotkey)
        self.hotkey=keyboard.add_hotkey('ctrl+alt+space', self.write)
    def clear_keyboard(self):
        keyboard.remove_hotkey(self.hotkey)
    def read_clipboard(self):
        try:
            clipboard_text = pyperclip.paste()
            if not clipboard_text or clipboard_text.strip()=='':
                return {"status": "warring", "message": "当前粘贴板内容不是文本或为空文本，请先复制非空文本代码"}
            self.can_write=False
            return {"status": "success", "text": clipboard_text}
        except Exception as e:
            return {"status": "error", "message": "粘贴失败！请尝试重启此软件或重启电脑！"}

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)


if __name__ == '__main__':
    api = Texts()  # 创建API实例
    window = webview.create_window(
        title='PDSU_ACM代码写入工具 by Herobrine1224 版本: v2.0.2',
        url = resource_path('index.html'),  # 本地 HTML 文件路径
        width=800,
        height=600,
        js_api=api,  # 传递API实例
    )
    webview.start(debug=False)