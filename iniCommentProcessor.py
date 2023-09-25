from tkinter import *
from tkinter import filedialog, ttk, messagebox
import threading
import configparser
import os

class App:
    def __init__(self, master):
        self.config = configparser.ConfigParser()
        self.keywords_path = StringVar(value=self.config.get('Paths', 'keywords_path', fallback=''))
        self.remove_comments = BooleanVar(value=True)
        self.master = master
        master.title("ini注释器")
        self.config = configparser.ConfigParser()
        if not os.path.exists('config.ini'):
            self.create_default_config()
        self.config.read('config.ini')
        self.rules_path = StringVar(value=self.config.get('Paths', 'rules_path', fallback=''))
        self.output_path = StringVar(value=self.config.get('Paths', 'output_path', fallback=''))
        self.keywords_path = StringVar(value=self.config.get('Paths', 'keywords_path', fallback=''))
        self.add_comments = BooleanVar(value=self.config.getboolean('function', 'add', fallback=True))
        self.comment_mode = IntVar(value=self.config.getint('function', 'mode', fallback=0))


        # 选择文件组
        self.rules_entry = Entry(master, textvariable=self.rules_path, width=50)
        self.rules_entry.grid(row=0, column=0, padx=10, pady=10)
        self.rules_button = Button(master, text="选择输入文件", command=self.choose_rules_file)
        self.rules_button.grid(row=0, column=1, padx=10, pady=10)
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

    def create_default_config(self):
        self.config['Paths'] = {
            'rules_path': '',
            'output_path': '',
            'keywords_path': ''
        }
        self.config['function'] = {
            'add': 'True',
            'mode': '0',
        }
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def choose_rules_file(self):
        filename = filedialog.askopenfilename(
            defaultextension="*.ini",
            filetypes=[("Initialization File", "*.ini"), ("Text File", "*.txt"), ("All File", "*.*")]
        )
        self.rules_path.set(filename)
        if not self.config.has_section('Paths'):
            self.config.add_section('Paths')
        self.config.set('Paths', 'rules_path', filename)
        with open('config.ini', 'w') as configfile:
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
        with open('config.ini', 'w') as configfile:
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
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def function_add(self):
        if not self.config.has_section('function'):
            self.config.add_section('function')
        self.config.set('function', 'add', str(self.add_comments.get()))
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def function_mode(self):
        if not self.config.has_section('function'):
            self.config.add_section('function')
        self.config.set('function', 'mode', str(self.comment_mode.get()))
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def run(self):
        rules = self.rules_path.get()
        output = self.output_path.get()
        keywords = self.keywords_path.get()
        if not rules or not output or not keywords:
            messagebox.showerror("错误", "请选择输入、输出、注释文件！")
            return
        if rules == output or rules == keywords or output == keywords:
            messagebox.showerror("错误", "输入、输出和注释文件不能相同！")
            return
        self.config.set('Paths', 'rules_path', rules)
        self.config.set('Paths', 'output_path', output)
        self.config.set('Paths', 'keywords_path', keywords)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        self.run_button.config(state=DISABLED)
        self.progress_bar["value"] = 0
        self.progress_bar.update()
        threading.Thread(target=self.process_file, args=(rules, output, keywords)).start()

    def process_file(self, rules, output, keywords):
        keyword_dict = {}  # 创建一个空的关键字字典
        if self.add_comments.get():
            config = configparser.ConfigParser()  # 创建一个ConfigParser对象
            config.optionxform = str
            config.read(keywords, encoding="utf-8")  # 从指定的关键字文件中读取配置
            for section in config.sections():  # 遍历所有的节
                for key, value in config.items(section):  # 遍历每个节的键值对
                    keyword_dict[key] = value  # 将关键字和注释添加到关键字字典中

        with open(rules, 'r', encoding='utf-8') as file:
            total_lines = sum(1 for _ in file)
        processed_lines = 0  # 初始化已处理行数

        if self.comment_mode.get() == 0:
            with open(rules, 'r', encoding='utf-8') as file:  # 打开规则文件进行读取
                with open(output, 'w', encoding='utf-8') as output_file:  # 打开输出文件进行写入
                    for line in file:  # 遍历规则文件的每一行
                        for keyword, comment in keyword_dict.items():  # 遍历关键字字典的每个关键字和注释
                            if line.startswith(keyword + "="):  # 如果行以关键字开头
                                line = line.rstrip() + " ;" + comment + "\n"  # 在行尾添加注释
                                break
                        output_file.write(line)  # 将处理后的行写入输出文件
                        processed_lines += 1  # 增加已处理行数计数
                        progress = processed_lines / total_lines * 100  # 计算进度百分比
                        self.progress_bar["value"] = progress  # 更新进度条的值
                        self.progress_bar.update()  # 更新进度条显示
        
        elif self.comment_mode.get() == 1:
            with open(rules, 'r', encoding='utf-8') as file:  # 打开规则文件进行读取
                with open(output, 'w', encoding='utf-8') as output_file:  # 打开输出文件进行写入
                    for line in file:  # 遍历规则文件的每一行
                        for keyword, comment in keyword_dict.items():  # 遍历关键字字典的每个关键字和注释
                            if line.startswith(keyword + "="):  # 如果行以关键字开头
                                line = line.split(';')[0]  # 移除行中的注释部分
                                line = line.rstrip() + " ;" + comment + "\n"  # 在行尾添加注释
                                break
                        output_file.write(line)  # 将处理后的行写入输出文件
                        processed_lines += 1  # 增加已处理行数计数
                        progress = processed_lines / total_lines * 100  # 计算进度百分比
                        self.progress_bar["value"] = progress  # 更新进度条的值
                        self.progress_bar.update()  # 更新进度条显示

        elif self.comment_mode.get() == 2:
            with open(rules, 'r', encoding='utf-8') as file:  # 打开规则文件进行读取
                with open(output, 'w', encoding='utf-8') as output_file:  # 打开输出文件进行写入
                    for line in file:  # 遍历规则文件的每一行
                        for keyword, comment in keyword_dict.items():  # 遍历关键字字典的每个关键字和注释
                            line = line.split(';')[0]  # 移除行中的注释部分
                            if line.startswith(keyword + "="):  # 如果行以关键字开头
                                line = line.rstrip() + " ;" + comment + "\n"  # 在行尾添加注释
                                break
                        if not keyword_dict:
                            line = line.split(';')[0]  # 移除行中的注释部分
                            line = line.rstrip() + "\n"

                        output_file.write(line)  # 将处理后的行写入输出文件
                        processed_lines += 1  # 增加已处理行数计数
                        progress = processed_lines / total_lines * 100  # 计算进度百分比
                        self.progress_bar["value"] = progress  # 更新进度条的值
                        self.progress_bar.update()  # 更新进度条显示

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

        messagebox.showinfo("注释完成！","模式: " + mode_str)
        self.run_button.config(state=NORMAL)

root = Tk()
app = App(root)
root.mainloop()