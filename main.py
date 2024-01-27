import os
import threading
import time

from mcrcon import MCRcon
import tkinter as tk
import tkinter.font as tkFont
import customtkinter as ctk
from tkinter import messagebox as tkm

import players

ip = None
port = None
password = None


class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = ctk.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = ctk.CTkButton(self, text="选择", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return

    def remove_index(self, index):
        label = self.label_list[index]
        button = self.button_list[index]
        label.destroy()
        button.destroy()
        self.label_list.remove(label)
        self.button_list.remove(button)
        return

    def size(self):
        return len(self.button_list)


class LoginApp:
    rt = None

    def __init__(self, root):
        global rt
        rt = root
        # setting title
        root.title("MMCSL-登录")
        # setting window size
        width = 540
        height = 340
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_227 = ctk.CTkLabel(root, width=541, height=53, text="登录到你的服务器")
        ft = tkFont.Font(family='Times', size=23)
        GLabel_227["font"] = ft
        GLabel_227["fg"] = "#333333"
        GLabel_227["justify"] = "center"
        GLabel_227.place(x=0, y=0)

        GButton_246 = ctk.CTkButton(root, width=70, height=25, text="登录", command=self.GButton_246_command)
        GButton_246["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_246["font"] = ft
        GButton_246["fg"] = "#000000"
        GButton_246["justify"] = "center"
        GButton_246.place(x=450, y=300)

        self.ip = tk.StringVar()
        self.password = tk.StringVar()
        self.port = tk.IntVar()

        self.ip.set('localhost')
        self.password.set('passwordddd')
        self.port.set(25575)

        self.GLineEdit_334 = ctk.CTkEntry(root, width=381, height=61, textvariable=self.ip)
        self.GLineEdit_334["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.GLineEdit_334["font"] = ft
        self.GLineEdit_334["fg"] = "#333333"
        self.GLineEdit_334["justify"] = "center"
        self.GLineEdit_334["text"] = "Entry"
        self.GLineEdit_334.place(x=80, y=70)

        self.GLineEdit_400 = ctk.CTkEntry(root, width=381, height=61, textvariable=self.port)
        self.GLineEdit_400["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.GLineEdit_400["font"] = ft
        self.GLineEdit_400["fg"] = "#333333"
        self.GLineEdit_400["justify"] = "center"
        self.GLineEdit_400["text"] = "Entry"
        self.GLineEdit_400.place(x=80, y=150)

        self.GLineEdit_313 = ctk.CTkEntry(root, width=381, height=61, textvariable=self.password)
        self.GLineEdit_313["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.GLineEdit_313["font"] = ft
        self.GLineEdit_313["fg"] = "#333333"
        self.GLineEdit_313["justify"] = "center"
        self.GLineEdit_313["text"] = "Entry"
        self.GLineEdit_313.place(x=80, y=230)

        self.GLabel_415 = ctk.CTkLabel(root, width=70, height=25, text="IP")
        ft = tkFont.Font(family='Times', size=10)
        self.GLabel_415["font"] = ft
        self.GLabel_415["fg"] = "#333333"
        self.GLabel_415["justify"] = "center"
        self.GLabel_415.place(x=10, y=90)

        self.GLabel_902 = ctk.CTkLabel(root, width=70, height=25, text="RCON端口")
        ft = tkFont.Font(family='Times', size=10)
        self.GLabel_902["font"] = ft
        self.GLabel_902["fg"] = "#333333"
        self.GLabel_902["justify"] = "center"
        self.GLabel_902.place(x=10, y=170)

        self.GLabel_586 = ctk.CTkLabel(root, width=70, height=25, text="RCON密码")
        ft = tkFont.Font(family='Times', size=10)
        self.GLabel_586["font"] = ft
        self.GLabel_586["fg"] = "#333333"
        self.GLabel_586["justify"] = "center"
        self.GLabel_586.place(x=10, y=250)

    def GButton_246_command(self):
        global ip, port, password, rt
        print("command")
        ip = self.ip.get()
        port = self.port.get()
        password = self.password.get()
        if not ip:
            tkm.showerror('错误', '请填写ip')
            return False
        if not port:
            tkm.showerror('错误', '请填写端口')
            return False
        if not password:
            tkm.showerror('错误', '请填写密码')
            return False
        rt.destroy()


ListBoxobj = None


class MainApp:
    def __init__(self, root):
        global ListBoxobj
        # setting title
        root.title("MMCSL")
        # setting window size
        width = 1080
        height = 640
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # create scrollable label and button frame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=root, width=258, height=551,
                                                                        command=self.label_button_frame_event,
                                                                        corner_radius=0)

        self.scrollable_label_button_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
        self.scrollable_label_button_frame.place(x=820, y=40)

        GLabel_224 = tk.Label(root)
        GLabel_224["anchor"] = "center"
        ft = tkFont.Font(family='Times', size=18)
        GLabel_224["font"] = ft
        GLabel_224["fg"] = "#333333"
        GLabel_224["justify"] = "center"
        GLabel_224["text"] = "Players"
        GLabel_224.place(x=820, y=0, width=259, height=41)

        GLabel_309 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=18)
        GLabel_309["font"] = ft
        GLabel_309["fg"] = "#333333"
        GLabel_309["justify"] = "center"
        GLabel_309["text"] = "MMCSL"
        GLabel_309.place(x=0, y=0, width=823, height=43)

        GButton_548 = ctk.CTkButton(root, width=70, height=25, text='Kick Player', command=self.GButton_548_command)
        GButton_548["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_548["font"] = ft
        GButton_548["fg"] = "#000000"
        GButton_548["justify"] = "center"
        GButton_548.place(x=820, y=600)

        GButton_187 = ctk.CTkButton(root, width=70, height=25, text="Ban Player", command=self.GButton_187_command)
        GButton_187["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_187["font"] = ft
        GButton_187["fg"] = "#000000"
        GButton_187["justify"] = "center"
        GButton_187.place(x=910, y=600)

        GButton_958 = ctk.CTkButton(root, width=70, height=25, text="Refresh", command=self.GButton_958_command)
        GButton_958["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_958["font"] = ft
        GButton_958["fg"] = "#000000"
        GButton_958["justify"] = "center"
        GButton_958.place(x=1000, y=600)
        '''
        # curselection()
        self.GListBox_810 = tk.Listbox(root)
        self.GListBox_810["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.GListBox_810["font"] = ft
        self.GListBox_810["fg"] = "#333333"
        self.GListBox_810["justify"] = "center"
        self.GListBox_810.place(x=820, y=40, width=258, height=551)
        ListBoxobj = self.GListBox_810
        '''
        self.GListBox_832 = tk.Listbox(root, selectmode='multiple', justify='left')
        self.GListBox_832["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.GListBox_832["font"] = ft
        self.GListBox_832["fg"] = "#333333"
        self.GListBox_832["justify"] = "left"
        self.GListBox_832.place(x=0, y=40, width=821, height=551)

        self.GLineEdit_253 = ctk.CTkEntry(root, width=700, height=41)
        self.GLineEdit_253["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.GLineEdit_253["font"] = ft
        self.GLineEdit_253["fg"] = "#333333"
        self.GLineEdit_253["justify"] = "center"
        self.GLineEdit_253["text"] = "Entry"
        self.GLineEdit_253.place(x=10, y=595)

        GButton_706 = ctk.CTkButton(root, width=91, height=30, text="Send", command=self.GButton_706_command)
        GButton_706["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_706["font"] = ft
        GButton_706["fg"] = "#000000"
        GButton_706["justify"] = "center"
        GButton_706.place(x=720, y=600)

    item = None

    def GButton_548_command(self):
        print("GButton_548_command")
        player = self.item
        print(player)
        resp = players.player_operate(player, 'k')
        msend(resp)

    def GButton_187_command(self):
        print("GButton_187_command")
        player = self.item
        print(player)
        resp = players.player_operate(player, 'b')
        msend(resp)

    def GButton_958_command(self):
        data = players.get_players_from_data(msend('list'))
        if len(data) == 1 and data[0] == '':
            return
        for i in range(self.scrollable_label_button_frame.size()):
            self.scrollable_label_button_frame.remove_index(i)
        for d in data:
            self.scrollable_label_button_frame.add_item(d)

    '''def GButton_958_command(self):
        print("GButton_958_command")
        if not self.GListBox_810.curselection():
            return None
        player_data = players.player_operate(self.GListBox_810.curselection(), 'i')
        tkm.showinfo('Player Info', f"name:{player_data['name']}\nuuid:{player_data['uuid']}")'''

    def GButton_706_command(self):
        self.GListBox_832.insert(self.GListBox_832.size(), f">{self.GLineEdit_253.get()}")
        resp = msend(self.GLineEdit_253.get())
        self.GListBox_832.insert(self.GListBox_832.size(), resp)
        self.GListBox_832.insert(self.GListBox_832.size(), '')

    def label_button_frame_event(self, item):
        self.item = item


def msend(command):
    try:
        resp = mcr.command(command)
    except Exception as e:
        resp = f'error!{e}'
    if not resp:
        resp = f'success'
    return resp


def main():
    global mcr
    # 定义窗口
    loginroot = ctk.CTk()
    loginapp = LoginApp(loginroot)
    # 登录窗口循环
    loginroot.mainloop()

    if not ip:
        tkm.showerror('错误', '请填写ip')
        exit(0)
    if not port:
        tkm.showerror('错误', '请填写端口')
        exit(0)
    if not password:
        tkm.showerror('错误', '请填写密码')
        exit(0)

    # 链接RCON
    mcr = MCRcon(host=str(ip), password=str(password), port=int(port))
    try:
        mcr.connect()
    except Exception as e:
        tkm.showerror('连接失败', e)
        exit(0)

    # 窗口主循环
    mainroot = ctk.CTk()
    mainapp = MainApp(mainroot)

    '''
    # 获取玩家子进程
    players_thread = threading.Thread(target=mainapp.GListBox_810_command)
    players_thread.daemon = True
    players_thread.start()
    '''

    # 主窗口循环
    mainroot.mainloop()


if __name__ == '__main__':
    try:
        main()
    except:
        pass
    exit(0)
