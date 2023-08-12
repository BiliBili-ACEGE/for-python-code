from PIL import Image, ImageTk
import pyautogui
import time
import keyboard
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

class KeyPresser:
    def __init__(self):
        self.is_running = False
        self.root = tk.Tk()
        self.root.title("按键精灵")
        
        # 更换窗口图标
        self.icon_image = tk.PhotoImage(file="icon.png")
        self.root.iconphoto(False, self.icon_image)

        # 选择自定义背景图
        self.background_image = self.load_and_remove_background("back.png")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.root.geometry("1920x1080")
        custom_font = ("微软雅黑", 12, "bold")

        self.label = tk.Label(self.root, text="按下 F6 启动/停止模拟按键", font=custom_font)
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.num_clicks_label = tk.Label(self.root, text="输入点击次数:", font=custom_font)
        self.num_clicks_label.place(relx=0.5, rely=0.2, anchor="center")

        self.num_clicks_entry = tk.Entry(self.root, font=custom_font)
        self.num_clicks_entry.place(relx=0.5, rely=0.25, anchor="center")

        self.key_to_simulate_label = tk.Label(self.root, text="输入模拟按键:", font=custom_font)
        self.key_to_simulate_label.place(relx=0.5, rely=0.35, anchor="center")

        self.key_to_simulate_entry = tk.Entry(self.root, font=custom_font)
        self.key_to_simulate_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.simulation_speed_label = tk.Label(self.root, text="输入点击速度 (秒):", font=custom_font)
        self.simulation_speed_label.place(relx=0.5, rely=0.5, anchor="center")

        self.simulation_speed_entry = tk.Entry(self.root, font=custom_font)
        self.simulation_speed_entry.place(relx=0.5, rely=0.55, anchor="center")

        # 创建圆角按钮
        self.button_style = ttk.Style()
        self.button_style.configure("BlueButton.TButton", borderwidth=0, bordercolor="white",
                                    focusthickness=3, focuscolor="none",
                                    relief="flat", background="#007ACC", foreground="black")
        self.button_style.map("BlueButton.TButton", background=[("active", "#FFFFFF"), ("!active", "#007ACC")])

        self.start_button = ttk.Button(self.root, text="开始", command=self.toggle_pressing, style="BlueButton.TButton")
        self.start_button.place(relx=0.5, rely=0.65, anchor="center")

        # 绑定 F6 快捷键
        keyboard.add_hotkey('F6', self.toggle_pressing)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_pressing(self):
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
            simulation_speed = float(self.simulation_speed_entry.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数点击次数和模拟速度。")
            return

        key_to_simulate = self.key_to_simulate_entry.get()
        
        for _ in range(num_clicks):
            pyautogui.press(key_to_simulate)
            time.sleep(simulation_speed)

        self.is_running = False
        self.start_button.config(text="开始")

    def load_and_remove_background(self, image_path):
        # 打开图片并移除白色背景
        img = Image.open(image_path)
        img = img.convert("RGBA")
        data = img.getdata()
        new_data = []
        for item in data:
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)

        return ImageTk.PhotoImage(img)

    def on_closing(self):
        if self.is_running:
            messagebox.showinfo("注意", "请先停止模拟按键再关闭窗口。")
        else:
            self.root.destroy()

    def run(self):
        self.root.mainloop()

keypresser = KeyPresser()
keypresser.run()
