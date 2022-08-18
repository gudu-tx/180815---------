# _*_ coding:utf-8
# 作者:me
# @Time: 2021/4/16 15:14
# @File: user-client3.py

# _*_ coding:utf-8
# 作者:me
# @Time: 2021/3/19 13:46
# @File: user.py

# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.messagebox
import pickle
import socket
import threading
import json
from tkinter.scrolledtext import ScrolledText


user = ''
password = ''
listbox1 = ''  # 用于显示在线用户的列表框
ii = 0  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = ''  # 聊天对象, 默认为群聊

#窗口
window = tk.Tk()
window.title('欢迎进入聊天室')
window.geometry('500x300')

# 画布放置图片
canvas = tk.Canvas(window, height=300, width=500)
imagefile = tk.PhotoImage(file='ax57h-4za7j.png')
image = canvas.create_image(0, 0, anchor='nw', image=imagefile)
canvas.place(x=0, y=0)
# 标签 用户名密码
tk.Label(window, text='用户名:').place(x=100, y=150)
tk.Label(window, text='密码:').place(x=100, y=190)
# 用户名输入框
var_usr_name = tk.StringVar()
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
# 密码输入框
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)



# 登录函数
def log_in():
    # 输入框获取用户名密码
    global user
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    user = usr_name

    # 从本地字典获取用户信息，如果没有则新建本地数据库
    try:
        with open('usr_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('usr_info.pickle', 'wb') as usr_file:
            pickle.dump(usrs_info, usr_file)  #将用户信息保存到文件里面
    # 判断用户名和密码是否匹配
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title='welcome', message='欢迎您：' + usr_name)
            window.destroy()
        else:
            tk.messagebox.showerror(message='密码错误')
    # 用户名密码不能为空
    elif usr_name == '' or usr_pwd == '':
        tk.messagebox.showerror(message='用户名或密码为空')
    # 不在数据库中弹出是否注册的框
    else:
        is_signup = tk.messagebox.askyesno('欢迎', '您还没有注册，是否现在注册')
        if is_signup:
            sign_up()

# 退出的函数
def sign_quit():
    window.destroy()


# 注册函数
def sign_up():
    # 确认注册时的相应函数
    def signtowcg():
        # 获取输入框内的内容
        nn = new_name.get()
        np = new_pwd.get()
        npf = new_pwd_confirm.get()

        # 本地加载已有用户信息,如果没有则已有用户信息为空
        try:
            with open('usr_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
        except FileNotFoundError:
            exist_usr_info = {}

            # 检查用户名存在、密码为空、密码前后不一致
        if nn in exist_usr_info:
            tk.messagebox.showerror('错误', '用户名已存在')
        elif np == '' or nn == '':
            tk.messagebox.showerror('错误', '用户名或密码为空')
        elif np != npf:
            tk.messagebox.showerror('错误', '密码前后不一致')
        # 注册信息没有问题则将用户名密码写入数据库
        else:
            exist_usr_info[nn] = np
            with open('usr_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('欢迎', '注册成功')
            # 注册成功关闭注册框
            window_sign_up.destroy()

    # 新建注册界面
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('注册')
    # 用户名变量及标签、输入框
    new_name = tk.StringVar()
    tk.Label(window_sign_up, text='用户名：').place(x=30, y=10)
    tk.Entry(window_sign_up, textvariable=new_name).place(x=150, y=10)
    # 密码变量及标签、输入框
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='请输入密码：').place(x=30, y=50)
    tk.Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=150, y=50)
    # 重复密码变量及标签、输入框
    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='请再次输入密码：').place(x=10, y=90)
    tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*').place(x=150, y=90)
    # 确认注册按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='确认注册',
                                   command=signtowcg)
    bt_confirm_sign_up.place(x=150, y=130)


# 登录 注册按钮
bt_login = tk.Button(window, text='登录', command=log_in)
window.bind('<Return>', log_in)            # 回车绑定登录功能
bt_login.place(x=140, y=230)
bt_logup = tk.Button(window, text='注册', command=sign_up, cursor='plus')
bt_logup.place(x=210, y=230)
bt_logquit = tk.Button(window, text='退出', command=sign_quit)
bt_logquit.place(x=280, y=230)


# 主循环
window.mainloop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8888))
if user:
    s.send(user.encode())  # 发送用户名
else:
    s.send('nobody'.encode())  # 没有输入用户名则标记nobody

# 如果没有用户名则将ip和端口号设置为用户名
# addr = s.getsockname()  # 获取客户端ip和端口号
# addr = addr[0] + ':' + str(addr[1])
# if user == '':
#     user = addr

# 聊天窗口
root = tkinter.Tk()
root.title(user)  # 窗口命名为用户名
root['height'] = 600
root['width'] = 800
root.resizable(0, 0)  # 限制窗口大小

canvas = tk.Canvas(root, bg='gray', height=600, width=800)
# image_file = tk.PhotoImage(file='a7m3k-rlygy.png')
# image = canvas.create_image(400, 0, anchor='n', image=image_file)
# canvas.place(x=0, y=0)


# 创建多行文本框
listbox = ScrolledText(root)
listbox.place(x=170, y=150, width=570, height=350)
# 文本框使用的字体颜色
listbox.tag_config('red', foreground='red')
listbox.tag_config('blue', foreground='blue')
listbox.tag_config('green', foreground='green')
listbox.tag_config('pink', foreground='pink')


# 创建多行文本框, 显示在线用户
listbox1 = tkinter.Listbox(root)
listbox1.place(x=5, y=150, width=145, height=343)


def showUsers():
    global listbox1, ii
    if ii == 1:
        listbox1.place(x=5, y=150, width=145, height=343)
        ii = 0
    else:
        listbox1.place_forget()  # 隐藏控件
        ii = 1


# 查看在线用户按钮
button1 = tkinter.Button(root, text='联系人', command=showUsers)
button1.place(x=170, y=500, width=90, height=30)

# 创建输入文本框和关联变量
a = tkinter.StringVar()
a.set('')
entry = tkinter.Entry(root, width=150, textvariable=a)
entry.place(x=170, y=530, width=570, height=60)


def send(*args):
    # 没有添加的话发送信息时会提示没有聊天对象
    users.append('')
    print(chat)
    if chat not in users:
        tkinter.messagebox.showerror('注意', message='没有聊天对象!')
        return
    if chat == user:
        tkinter.messagebox.showerror('注意', message='自己不能和自己进行对话!')
        return
    mes = entry.get() + ':;' + user + ':;' + chat  # 添加聊天对象标记
    s.send(mes.encode())
    a.set('')  # 发送后清空文本框


# 创建发送按钮
button = tkinter.Button(root, text='发送', command=send)
button.place(x=665, y=545, width=60, height=30)
root.bind('<Return>', send)  # 绑定回车发送信息


# 私聊功能
def private(*args):
    global chat
    # 获取点击的索引然后得到内容(用户名)
    indexs = listbox1.curselection()
    index = indexs[0]
    if index > 0:
        chat = listbox1.get(index)
        # 修改客户端名称
        if chat == '':
            root.title(user)
            return
        ti = user + '  ->  ' + chat
        root.title(ti)


# 在显示用户列表框上设置绑定事件
listbox1.bind('<ButtonRelease-1>', private)


# 用于时刻接收服务端发送的信息并打印
def recv():
    global users
    while True:
        data = s.recv(1024)
        data = data.decode()
        # 没有捕获到异常则表示接收到的是在线用户列表
        try:
            data = json.loads(data)
            users = data
            listbox1.delete(0, tkinter.END)  # 清空列表框
            number = ('   当前用户数: ' + str(len(data)))
            listbox1.insert(tkinter.END, number)
            listbox1.itemconfig(tkinter.END, fg='red', bg="#f0f0ff")
            listbox1.insert(tkinter.END, '')
            listbox1.itemconfig(tkinter.END)
            for i in range(len(data)):
                listbox1.insert(tkinter.END, (data[i]))
                listbox1.itemconfig(tkinter.END, fg='blue')
        except:
            data = data.split(':;')
            data1 = data[0].strip()  # 消息
            data2 = data[1]  # 发送信息的用户名
            data3 = data[2]  # 聊天对象
            data1 = '\n' + data1 #用户换行
            if data3 == '':
                if data2 == user:  # 如果是自己则将则字体变为蓝色
                    listbox.insert(tkinter.END, data1, 'blue')
                else:
                    listbox.insert(tkinter.END, data1, 'green')  # END将信息加在最后一行
                if len(data) == 4:
                    listbox.insert(tkinter.END, '\n' + data[3], 'pink')
            elif data2 == user or data3 == user:  # 显示私聊
                listbox.insert(tkinter.END, data1, 'red')  # END将信息加在最后一行
            listbox.see(tkinter.END)  # 显示在最后


r = threading.Thread(target=recv)
r.start()  # 开始线程接收信息

root.mainloop()
s.close()  # 关闭图形界面后关闭TCP连接