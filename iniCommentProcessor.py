from tkinter import *
from tkinter import filedialog, ttk, messagebox
import threading
import configparser
import os
import json
import datetime
import time
import re
import urllib.request
import hashlib

class App:    
    def __init__(self, master):
        self.config = configparser.ConfigParser()
        self.keywords_path = StringVar(value=self.config.get('Paths', 'keywords_path', fallback=''))
        self.remove_comments = BooleanVar(value=True)
        self.master = master
        master.title("ini注释器")
        url = "https://raw.fgit.cf/AWangDog/iniCommentProcessor/main/1.ico"
        if not os.path.exists("1.ico"):
            download_thread = threading.Thread(target=self.download_file, args=(url, "1.ico"))
            download_thread.start()
        elif self.calculate_file_hash("1.ico") != "70cc49b88e390848700222dd3cd19df2":
            download_thread = threading.Thread(target=self.download_file, args=(url, "1.ico"))
            download_thread.start()
        else:
            master.iconbitmap("1.ico")
        master.resizable(False, False)
        self.config = configparser.ConfigParser()
        self.read_config(True)

        # 选择文件组
        self.input_entry = Entry(master, textvariable=self.input_path, width=50)
        self.input_entry.grid(row=0, column=0, padx=10, pady=10)
        self.input_button = Button(master, text="选择输入文件", command=self.choose_input_file)
        self.input_button.grid(row=0, column=1, padx=10, pady=10)
        self.output_entry = Entry(master, textvariable=self.output_path, width=50)
        self.output_entry.grid(row=1, column=0, padx=10, pady=10)
        self.output_button = Button(master, text="选择输出文件", command=self.choose_output_file)
        self.output_button.grid(row=1, column=1, padx=10, pady=10)
        self.keywords_entry = Entry(master, textvariable=self.keywords_path, width=50)
        self.keywords_entry.grid(row=2, column=0, padx=10, pady=10)
        self.keywords_button = Button(master, text="选择注释文件", command=self.choose_keywords_file)
        self.keywords_button.grid(row=2, column=1, padx=10, pady=10)

        # 进度条组
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=3, column=0, padx=10, pady=10)

        # 添加注释组
        self.add_comments_checkbox = Checkbutton(master, text="添加注释", variable=self.add_comments, command=self.function_add)
        self.add_comments_checkbox.grid(row=0, column=2, padx=10, pady=10)
        self.comment_mode_radio1 = Radiobutton(master, text="追加注释", variable=self.comment_mode, value=0, command=self.function_mode)
        self.comment_mode_radio1.grid(row=1, column=2, padx=10, pady=5)
        self.comment_mode_radio2 = Radiobutton(master, text="覆盖注释", variable=self.comment_mode, value=1, command=self.function_mode)
        self.comment_mode_radio2.grid(row=2, column=2, padx=10, pady=5)
        self.comment_mode_radio3 = Radiobutton(master, text="删除注释", variable=self.comment_mode, value=2, command=self.function_mode)
        self.comment_mode_radio3.grid(row=3, column=2, padx=10, pady=5)

        # 开始运行组
        self.run_button = Button(master, text="开始运行", command=self.run)
        self.run_button.grid(row=3, column=1, padx=10, pady=10)

    def calculate_file_hash(self, file_path):
        with open(file_path, 'rb') as file:
            data = file.read()
            md5_hash = hashlib.md5(data).hexdigest()
            return md5_hash

    def create_default_config(self):
        self.config['Paths'] = {
            'input_path': '',
            'output_path': '',
            'keywords_path': ''
        }
        self.config['function'] = {
            'add': 'True',
            'mode': '0',
            'algorithm': '0',
            'fps': '1'
        }
        with open('config.cfg', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def read_config(self, main):
        if not os.path.exists('config.cfg'):
            self.create_default_config()
        self.config.read('config.cfg', encoding='utf-8')
        self.algorithm = self.config.getint('function', 'algorithm', fallback=0)
        self.input_path = StringVar(value=self.config.get('Paths', 'input_path', fallback=''))
        self.output_path = StringVar(value=self.config.get('Paths', 'output_path', fallback=''))
        self.keywords_path = StringVar(value=self.config.get('Paths', 'keywords_path', fallback=''))
        self.fps = self.config.getint('function', 'fps', fallback=1)
        if main:
            self.add_comments = BooleanVar(value=self.config.getboolean('function', 'add', fallback=True))
            self.comment_mode = IntVar(value=self.config.getint('function', 'mode', fallback=0))
    
    def download_file(self, url, file_path):
        urllib.request.urlretrieve(url, file_path)

    def choose_input_file(self):
        filename = filedialog.askopenfilename(
            defaultextension="*.ini",
            filetypes=[("Initialization File", "*.ini"), ("Text File", "*.txt"), ("All File", "*.*")]
        )
        self.input_path.set(filename)
        if not self.config.has_section('Paths'):
            self.config.add_section('Paths')
        self.config.set('Paths', 'input_path', filename)
        with open('config.cfg', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def choose_output_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension="*.ini",
            filetypes=[("Initialization File", "*.ini"), ("Text File", "*.txt"), ("All File", "*.*")]
        )
        self.output_path.set(filename)
        if not self.config.has_section('Paths'):
            self.config.add_section('Paths')
        self.config.set('Paths', 'output_path', filename)
        with open('config.cfg', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def choose_keywords_file(self):
        filename = filedialog.askopenfilename(
            defaultextension="*.ini",
            filetypes=[("Initialization File", "*.ini"), ("Text File", "*.txt"), ("All File", "*.*")]
        )
        self.keywords_path.set(filename)
        if not self.config.has_section('Paths'):
            self.config.add_section('Paths')
        self.config.set('Paths', 'keywords_path', filename)
        with open('config.cfg', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def function_add(self):
        if not self.config.has_section('function'):
            self.config.add_section('function')
        self.config.set('function', 'add', str(self.add_comments.get()))
        with open('config.cfg', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def function_mode(self):
        if not self.config.has_section('function'):
            self.config.add_section('function')
        self.config.set('function', 'mode', str(self.comment_mode.get()))
        with open('config.cfg', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def run(self):
        input = self.input_path.get()
        output = self.output_path.get()
        keywords = self.keywords_path.get()
        if not input or not output or not keywords:
            messagebox.showerror("错误", "请选择输入、输出、注释文件！")
            return
        if input == output or input == keywords or output == keywords:
            messagebox.showerror("错误", "输入、输出、注释文件不能相同！")
            return
        self.run_button.config(state=DISABLED)
        self.progress_bar["value"] = 0
        self.progress_bar.update()
        threading.Thread(target=self.process_file, args=(input, output, keywords)).start()
    
    def format_time(self, seconds):
        if seconds < 1:
            milliseconds = seconds * 1000
            return f"{int(milliseconds)}ms"
        elif seconds < 60:
            milliseconds = (seconds % 1) * 1000
            return f"{int(seconds)}s {int(milliseconds)}ms"
        elif seconds < 3600:
            minutes = seconds // 60
            seconds = seconds % 60
            milliseconds = (seconds % 1) * 1000
            return f"{int(minutes)}min {int(seconds)}s {int(milliseconds)}ms"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = (seconds % 3600) % 60
            milliseconds = (seconds % 1) * 1000
            return f"{int(hours)}h {int(minutes)}min {int(seconds)}s {int(milliseconds)}ms"

    def process_file(self, input, output, keywords):
        self.read_config(False)
        if not self.config.has_section('function'):
            self.config.add_section('function')
        self.config.set('function', 'algorithm', str(self.algorithm))
        with open('config.cfg', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        def algorithm1():
            global algorithm_str
            algorithm_str = "1-整体"
            processed_key = 0
            global fps
            fps = len(keyword_dict) * (self.fps / 100)
            global all_processed
            all_processed = len(keyword_dict)
            with open(input, 'r', encoding='utf-8') as input_file:  # 打开规则文件进行读取
                            with open(output, 'w', encoding='utf-8') as output_file:  # 打开输出文件进行写入
                                if self.comment_mode.get() == 0 or self.comment_mode.get() == 2:
                                    file_str = input_file.read()
                                    if self.comment_mode.get() == 2:
                                        file_str = re.sub(r"\n([\r|\t|\f| ]?);(.*)", "", re.sub(r"(.+?);(.*)", "\g<1>", file_str))
                                    for keyword, comment in keyword_dict.items():  # 遍历关键字字典的每个关键字和注释
                                        regex = rf"(\n[\r|\t|\f| ]?{keyword}[\r|\t|\f| ]?=[\r|\t|\f| ]?[^;|\n]*);?(.*)"
                                        subst = f"\\g<1>;\\g<2> {comment}"
                                        file_str = re.sub(regex, subst, file_str)
                                        processed_key += 1
                                        if processed_key % int(fps) == 0:
                                            progress = processed_key / len(keyword_dict) * 100  # 计算进度百分比
                                            self.progress_bar["value"] = progress  # 更新进度条的值
                                            self.progress_bar.update()  # 更新进度条显示
                                    output_file.write(file_str)
                                elif self.comment_mode.get() == 1:
                                    file_str = input_file.read()
                                    for keyword, comment in keyword_dict.items():  # 遍历关键字字典的每个关键字和注释
                                        regex = rf"(\n[\r|\t|\f| ]?{keyword}[\r|\t|\f| ]?=[\r|\t|\f| ]?[^;|\n]*);?(.*)"
                                        subst = f"\\g<1>; {comment}"
                                        file_str = re.sub(regex, subst, file_str)
                                        processed_key += 1
                                        if processed_key % int(fps) == 0:
                                            progress = processed_key / len(keyword_dict) * 100  # 计算进度百分比
                                            self.progress_bar["value"] = progress  # 更新进度条的值
                                            self.progress_bar.update()  # 更新进度条显示
                                    output_file.write(file_str)


        def algorithm2():
            global algorithm_str
            global fps
            global all_processed
            algorithm_str = "2-逐行"
            processed_lines = 0  # 初始化已处理行数
            all_processed = input_lines
            with open(input, 'r', encoding='utf-8') as input_file:  # 打开规则文件进行读取
                with open(output, 'w', encoding='utf-8') as output_file:  # 打开输出文件进行写入
                    fps = input_lines * (self.fps / 100)
                    if self.comment_mode.get() == 0:
                                for line in input_file:  # 遍历规则文件的每一行
                                    if not line:
                                        break
                                    for keyword, comment in keyword_dict.items():  # 遍历关键字字典的每个关键字和注释
                                        if line.startswith(keyword + "="):  # 如果行以关键字开头
                                            line = line.rstrip() + " ;" + comment + "\n"  # 在行尾添加注释
                                            break
                                    output_file.write(line)  # 将处理后的行写入输出文件
                                    processed_lines += 1  # 增加已处理行数计数
                                    if processed_lines % int(fps) == 0:
                                        progress = processed_lines / input_lines * 100  # 计算进度百分比
                                        self.progress_bar["value"] = progress  # 更新进度条的值
                                        self.progress_bar.update()  # 更新进度条显示
                    
                    elif self.comment_mode.get() == 1:
                                for line in input_file:  # 遍历规则文件的每一行
                                    for keyword, comment in keyword_dict.items():  # 遍历关键字字典的每个关键字和注释
                                        if line.startswith(keyword + "="):  # 如果行以关键字开头
                                            line = line.split(';')[0]  # 移除行中的注释部分
                                            line = line.rstrip() + " ;" + comment + "\n"  # 在行尾添加注释
                                            break
                                    output_file.write(line)  # 将处理后的行写入输出文件
                                    processed_lines += 1  # 增加已处理行数计数
                                    if processed_lines % int(fps) == 0:
                                        progress = processed_lines / input_lines * 100  # 计算进度百分比
                                        self.progress_bar["value"] = progress  # 更新进度条的值
                                        self.progress_bar.update()  # 更新进度条显示

                    elif self.comment_mode.get() == 2:
                                for line in input_file:  # 遍历规则文件的每一行
                                    for keyword, comment in keyword_dict.items():  # 遍历关键字字典的每个关键字和注释
                                        line = line.split(';')[0]  # 移除行中的注释部分
                                        if not(not line):
                                            line = line.rstrip() + "\n"
                                        if line.startswith(keyword + "="):  # 如果行以关键字开头
                                            line = line.rstrip() + " ;" + comment + "\n"  # 在行尾添加注释
                                            break
                                    if not keyword_dict:
                                        line = line.split(';')[0]  # 移除行中的注释部分
                                        if not(not line):
                                            line = line.rstrip() + "\n"

                                    output_file.write(line)  # 将处理后的行写入输出文件
                                    processed_lines += 1  # 增加已处理行数计数
                                    if processed_lines % int(fps) == 0:
                                        progress = processed_lines / input_lines * 100  # 计算进度百分比
                                        self.progress_bar["value"] = progress  # 更新进度条的值
                                        self.progress_bar.update()  # 更新进度条显示
        start_time = time.time() 
        keyword_dict = {}  # 创建一个空的关键字字典
        if self.add_comments.get():
            config = configparser.ConfigParser()  # 创建一个ConfigParser对象
            config.optionxform = str
            config.read(keywords, encoding="utf-8")  # 从指定的关键字文件中读取配置
            for section in config.sections():  # 遍历所有的节
                for key, value in config.items(section):  # 遍历每个节的键值对
                    keyword_dict[key] = value  # 将关键字和注释添加到关键字字典中
        with open(input, 'r', encoding='utf-8') as input_file:
                input_lines = sum(1 for _ in input_file)
        auto_algorithm_str = "手动-"
        if self.algorithm == 0:
            auto_algorithm_str = "自动-"
            if len(keyword_dict) <= input_lines:
                algorithm1()
            elif len(keyword_dict) > input_lines:
                algorithm2()
        elif self.algorithm == 1:
            algorithm1()
        elif self.algorithm == 2:
            algorithm2()

        if self.comment_mode.get() == 2 and not self.add_comments.get():
            mode_str = "清除所有注释"
        elif (self.comment_mode.get() == 0 or self.comment_mode.get() == 1 ) and not self.add_comments.get():
            mode_str = "未进行操作"        
        elif self.comment_mode.get() == 0 and self.add_comments.get():
            mode_str = "追加注释"
        elif self.comment_mode.get() == 1 and self.add_comments.get():
            mode_str = "覆盖注释"
        elif self.comment_mode.get() == 2 and self.add_comments.get():
            mode_str = "删除注释"
        with open(output, 'r', encoding='utf-8') as input_file:
            output_lines = sum(1 for _ in input_file)
        self.progress_bar["value"] = 100  # 更新进度条的值
        self.progress_bar.update()  # 更新进度条显示
        elapsed_time = time.time() - start_time 
        log_data = { 
            "config": { 
                "add": self.add_comments.get(),
                "mode": self.comment_mode.get(), 
                "algorithm": self.algorithm, 
                "fps": f"{self.fps}%",
            }, 
            "date": {
                "fps": f"{fps}/{all_processed}"

            },
            "file": { 
                "input": { 
                    "path": input, 
                    "line": input_lines 
                }, 
                "output": { 
                    "path": output, 
                    "line": output_lines 
                }, 
                "keywords": { 
                    "path": self.keywords_path.get(), 
                    "key_line": len(keyword_dict) 
                } 
            }, 
            "time": { 
                "start": datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S.%f"), 
                "stop": datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S.%f"), 
                "elapsed": str(datetime.timedelta(seconds=elapsed_time))
            } 
        } 
        with open("log.json", "a", encoding='utf-8') as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + "\n")
        print(json.dumps(log_data, ensure_ascii=False), end="")
        print("\n")
        messagebox.showinfo("注释完成！", f"操作: {mode_str}\n算法: {auto_algorithm_str}{algorithm_str}\n用时: {self.format_time(elapsed_time)}\n进度条刷新率: {self.fps}%")
        self.run_button.config(state=NORMAL)

root = Tk()
app = App(root)
root.mainloop()