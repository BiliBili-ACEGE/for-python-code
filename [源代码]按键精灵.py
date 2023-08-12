import pyautogui
import time
import keyboard
import threading
import tkinter as tk
from tkinter import messagebox

class KeyPresser:
    def __init__(self):
        self.is_running = False
        self.root = tk.Tk()
        self.root.title("按键精灵")
        
        # 更换窗口图标
        self.icon_image = tk.PhotoImage(file="icon.png")
        self.root.iconphoto(False, self.icon_image)

         # 选择自定义背景图
        self.background_image = tk.PhotoImage(file="back.png")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        
        self.root.geometry("1920x1080")
        custom_font = ("微软雅黑", 12, "bold")
        
        self.label = tk.Label(self.root, text="按下 F6 启动/停止", font=custom_font)
        self.label.pack(pady=10)

        self.num_clicks_label = tk.Label(self.root, text="输入点击次数:", font=custom_font)
        self.num_clicks_label.pack()

        self.num_clicks_entry = tk.Entry(self.root, font=custom_font)
        self.num_clicks_entry.pack()

        self.key_to_simulate_label = tk.Label(self.root, text="输入模拟按键:", font=custom_font)
        self.key_to_simulate_label.pack()

        self.key_to_simulate_entry = tk.Entry(self.root, font=custom_font)
        self.key_to_simulate_entry.pack()

        self.start_button = tk.Button(self.root, text="开始", command=self.toggle_pressing, font=custom_font)
        self.start_button.pack()

        keyboard.add_hotkey('F6', self.toggle_pressing)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_pressing(self, event=None):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="开始")
        else:
            self.is_running = True
            self.start_button.config(text="停止")
            self.start_pressing()

    def start_pressing(self):
        try:
            num_clicks = int(self.num_clicks_entry.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数点击次数。")
            return

        key_to_simulate = self.key_to_simulate_entry.get()
        
        for _ in range(num_clicks):
            pyautogui.press(key_to_simulate)
            time.sleep(0.1)

        self.is_running = False
        self.start_button.config(text="开始")

    def on_closing(self):
        if self.is_running:
            messagebox.showinfo("注意", "请先停止模拟按键再关闭窗口。")
        else:
            self.root.destroy()

    def run(self):
        self.root.mainloop()

keypresser = KeyPresser()
keypresser.run()
