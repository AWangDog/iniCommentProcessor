from tkinter import *
from tkinter import filedialog, ttk, messagebox
import threading
import configparser
import os


class App:
    def __init__(self, master):
        self.config = configparser.ConfigParser()
        self.keywords_path = StringVar(value=self.config.get('Paths', 'keywords_path', fallback=''))
        self.master = master
        master.title("注释转换器")
        self.config = configparser.ConfigParser()
        if not os.path.exists('config.ini'):
            self.create_default_config()
        self.config.read('config.ini')
        self.rules_path = StringVar(value=self.config.get('Paths', 'rules_path', fallback=''))
        self.output_path = StringVar(value=self.config.get('Paths', 'output_path', fallback=''))
        self.keywords_path = StringVar(value=self.config.get('Paths', 'keywords_path', fallback=''))        
        self.rules_label = Label(master, text="请选择输入文件：")
        self.rules_label.grid(row=0, column=0, padx=10, pady=10)
        self.rules_entry = Entry(master, textvariable=self.rules_path, width=50)
        self.rules_entry.grid(row=0, column=1, padx=10, pady=10)
        self.rules_button = Button(master, text="选择文件", command=self.choose_rules_file)
        self.rules_button.grid(row=0, column=2, padx=10, pady=10)
        self.output_label = Label(master, text="请选择输出文件：")
        self.output_label.grid(row=1, column=0, padx=10, pady=10)
        self.output_entry = Entry(master, textvariable=self.output_path, width=50)
        self.output_entry.grid(row=1, column=1, padx=10, pady=10)
        self.output_button = Button(master, text="选择文件", command=self.choose_output_file)
        self.output_button.grid(row=1, column=2, padx=10, pady=10)
        self.keywords_label = Label(master, text="请选择关键字文件：")
        self.keywords_label.grid(row=2, column=0, padx=10, pady=10)
        self.keywords_entry = Entry(master, textvariable=self.keywords_path, width=50)
        self.keywords_entry.grid(row=2, column=1, padx=10, pady=10)
        self.keywords_button = Button(master, text="选择文件", command=self.choose_keywords_file)
        self.keywords_button.grid(row=2, column=2, padx=10, pady=10)
        self.progress_label = Label(master, text="注释进度：")
        self.progress_label.grid(row=3, column=0, padx=10, pady=10)
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=3, column=1, padx=10, pady=10)
        self.run_button = Button(master, text="开始运行", command=self.run)
        self.run_button.grid(row=4, column=1, padx=10, pady=10)

    def create_default_config(self):
        self.config['Paths'] = {
            'rules_path': '',
            'output_path': '',
            'keywords_path': ''
        }
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def choose_rules_file(self):
        filename = filedialog.askopenfilename(
            defaultextension="*.ini",
            filetypes=[("Initialization File", "*.ini"), ("Text File", "*.txt"), ("All File", "*.*")]
        )
        self.rules_path.set(filename)
        self.config.set('Paths', 'rules_path', filename)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def choose_output_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension="*.ini",
            filetypes=[("Initialization File", "*.ini"), ("Text File", "*.txt"), ("All File", "*.*")]
        )
        self.output_path.set(filename)
        self.config.set('Paths', 'output_path', filename)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def choose_keywords_file(self):
        filename = filedialog.askopenfilename(
            defaultextension="*.ini",
            filetypes=[("Initialization File", "*.ini"), ("Text File", "*.txt"), ("All File", "*.*")]
        )
        self.keywords_path.set(filename)
        self.config.set('Paths', 'keywords_path', filename)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def run(self):
        rules = self.rules_path.get()
        output = self.output_path.get()
        keywords = self.keywords_path.get()
        if not rules or not output or not keywords:
            messagebox.showerror("错误", "请选择输入、输出和关键字文件！")
            return
        if rules == output or rules == keywords or output == keywords:
            messagebox.showerror("错误", "输入、输出和关键字文件不能相同！")
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
        keyword_dict = {}
        config = configparser.ConfigParser()
        config.optionxform = str  # 禁用关键字的大小写转换
        config.read(keywords, encoding="utf-8")
        for section in config.sections():
            for key, value in config.items(section):
                keyword_dict[key] = value
        total_lines = 0
        with open(rules, 'r', encoding='utf-8') as file:
            for line in file:
                total_lines += 1
        processed_lines = 0
        with open(rules, 'r', encoding='utf-8') as file:
            with open(output, 'w', encoding='utf-8') as output_file:
                for line in file:
                    for keyword, comment in keyword_dict.items():
                        if line.startswith(keyword + "="):
                            # 在关键字后面添加注释
                            line = line.rstrip() + " ;" + comment + "\n"
                            break
                    output_file.write(line)
                    processed_lines += 1
                    progress = processed_lines / total_lines * 100
                    self.progress_bar["value"] = progress
                    self.progress_bar.update()
        messagebox.showinfo("完成", "注释转换完成！")
        self.run_button.config(state=NORMAL)


root = Tk()
app = App(root)
root.mainloop()