#-*- coding:utf-8 -*-
#CREATER: NTGtech-ShenAo
import tkinter as tk
import threading
from tkinter import Frame, filedialog
import os
import tkinter.messagebox

import NTG_base
import NTG_get_creater
import NTG_get_tag
import NTG_inf_seeting
import NTG_Other_function

def about():
    tkinter.messagebox.showinfo('Hi, 初次见面请多指教',NTG_inf_seeting.abt_msg)


def save_conf(cookie_,path_,proxy_):
    global  cookie, path, proxy
    cookie = cookie_
    path = path_
    proxy = proxy_
    NTG_base.write_file('./conf/cookie.ntg',cookie_)
    NTG_base.write_file('./conf/path.ntg',path_)
    NTG_base.write_file('./conf/proxy.ntg',proxy_)
    tkinter.messagebox.showinfo('完成ヾ(≧▽≦*)o','保存完成')
    return 0

def path_wr():
    path_text = tk.filedialog.askdirectory()
    Entry_path.delete(0, 999999)
    Entry_path.insert(0, path_text)

def show_main(cookie, path):
    if cookie == '' or path == '':
        tkinter.messagebox.showwarning('警告＞︿＜','您并没有设置cookie或下载路径,请前往设置填写')
    else:
        Frame_Main.place_forget()
        Frame_Tag.place(x=0, y=0)

def show_creater(cookie, path):
    if cookie == '' or path == '':
        tkinter.messagebox.showwarning('警告＞︿＜','您并没有设置cookie或下载路径,请前往设置填写')
    else:
        Frame_Main.place_forget()
        Frame_Creater.place(x=0, y=0)

def show_config():
    Frame_Main.place_forget()
    Frame_Seeting.place(x=0, y=0)

def show_donate():
    Frame_Main.place_forget()
    Frame_donate.place(x=0, y=0)

def de_show_config():
    Frame_Seeting.place_forget()
    Frame_Main.place(x=0, y=0)
    
def de_show_creater():
    Frame_Creater.place_forget()
    Frame_Main.place(x=0,y=0)

def de_show_main():
    Frame_Tag.place_forget()
    Frame_Main.place(x=0,y=0)

def de_show_donate():
    Frame_donate.place_forget()
    Frame_Main.place(x=0,y=0)


def ui():
    global Entry_path, Frame_Main, Frame_Tag
    global Frame_Creater, Frame_Seeting, cookie, path, proxy, Frame_donate
    global start_bt_tag, start_bt_ct
    root = tk.Tk()
    donate_url = 'wxp://f2f0mNWRm4FpJsc_C_rjsZTq_NrD2HzyhQie'
    NTG_base.make_qr(donate_url, './conf/donate.png')
    img_QR = tk.PhotoImage(file='./conf/donate.png')
    img =  tk.PhotoImage(file='./conf/show.png')
    print(img)
    root.iconbitmap ('./conf/logo.ico')
    gray_0 = '#c0c0c0'
    gray_1 = '#747474'
    gray_2 = '#353535'
    gray_font = '#5a5a5a'
    root.configure(bg = gray_0)
    root.geometry('800x490')
    root.title('Pixiv Tab Downloader ! - o((>ω< ))o - Power by NTGtechGroup')
    root.resizable(0,0)
    entry_x = 320
    entry_y = 10
    pd_x = 10
    pd_y = 0
    
    is_file = os.path.exists("./conf/cookie.ntg")
    if is_file == True:
        cookie = NTG_base.read_file('./conf/cookie.ntg')
    else:
        cookie = ''
    is_file = os.path.exists("./conf/path.ntg")
    if is_file == True:
        path = NTG_base.read_file('./conf/path.ntg')
    else:
        path = ''
    is_file = os.path.exists("./conf/proxy.ntg")
    if is_file == True:
        proxy = NTG_base.read_file('./conf/proxy.ntg')
    else:
        proxy = ''
    #       Donate Frame
    Frame_donate = tk.Frame(root, bg = gray_0, height = 1000, width = 1000)
    Frame_donate.place(x=0, y=0)
    keyword_label = tk.Label(Frame_donate, text='微信支付:', fg = '#fc00ff', bg=gray_0,height=1,font=("Arial", 12))
    keyword_label.grid(row=1, column=0, padx=pd_x, pady=10)
    donate_label = tk.Label(Frame_donate, text='', image = img_QR, bg=gray_0)
    donate_label.grid(row=2, column=0, padx=pd_x, pady=pd_y)
    keyword_label = tk.Label(Frame_donate, text='您的支持是我创作的唯一动力！', fg = '#fc00ff', bg=gray_0,height=1,font=("Arial", 12))
    keyword_label.grid(row=3, column=0, padx=pd_x, pady=pd_y)
    #返回按钮
    back_bt_ct = tk.Button(Frame_donate, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:de_show_donate(),
            bd = -1, text = '返回', image = img, fg = 'white')
    back_bt_ct.grid(row=12, column=0, padx=10, pady=10)

    #       Tag Frame
    Frame_Tag = tk.Frame(root, bg = gray_0, height = 1000, width = 1000)
    Frame_Tag.place(x=0, y=0)
    #标题
    title = tk.Label(Frame_Tag,text='Pixiv Tab Downloader',font=("Arial", 20), fg = gray_font, bg=gray_0)
    title.grid(row=0, padx=pd_x, pady=10)
    #搜索文本label
    keyword_label = tk.Label(Frame_Tag, text='要下载的Tag(例:女の子 或 女の子,猫口[第二种慢,不推荐]):', fg = gray_font, bg=gray_0,height=1,font=("Arial", 12))
    keyword_label.grid(row=1, column=0, padx=pd_x, pady=pd_y)
    #搜索文本entry
    Entry_keyword_tag = tk.Entry(Frame_Tag, fg = gray_2, bg=gray_1,relief='flat')
    Entry_keyword_tag.grid(row=2, column=0, padx=pd_x, pady=pd_y, ipadx=entry_x, ipady=entry_y)
    #状态label
    sat_label_tag = tk.Label(Frame_Tag, text='Hi, 我是个状态条', fg = 'white', bg=gray_1,height=3,
        font=("Arial", 9),compound='center',width=111)
    sat_label_tag.grid(row=9, column=0, padx=pd_x, pady=30)
    #启动按钮    
    start_bt_tag = tk.Button(Frame_Tag, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:NTG_get_tag.pull_function(cookie,Entry_keyword_tag.get(),path,proxy,
            start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct),
            bd = -1, text = 'Go!', image = img, fg = 'white')
    start_bt_tag.grid(row=10, column=0, padx=10, pady=0)
    #返回按钮
    back_bt_ct = tk.Button(Frame_Tag, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:de_show_main(),
            bd = -1, text = '返回', image = img, fg = 'white')
    back_bt_ct.grid(row=12, column=0, padx=10, pady=10)



    #       Creater Frame
    Frame_Creater = tk.Frame(root, bg = gray_0, height = 1000, width = 1000)
    Frame_Creater.place(x=0, y=0)
    title = tk.Label(Frame_Creater,text='Pixiv Creater Downloader',font=("Arial", 20), fg = gray_font, bg=gray_0)
    title.grid(row=0, padx=pd_x, pady=10)
    #搜索文本label
    keyword_label = tk.Label(Frame_Creater, text='请输入要爬取的画师ID(例:1193008):', fg = gray_font, bg=gray_0,height=1,font=("Arial", 12))
    keyword_label.grid(row=1, column=0, padx=pd_x, pady=pd_y)
    #搜索文本entry
    Entry_keyword_ct = tk.Entry(Frame_Creater, fg = gray_2, bg=gray_1,relief='flat')
    Entry_keyword_ct.grid(row=2, column=0, padx=pd_x, pady=pd_y, ipadx=entry_x, ipady=entry_y)
    #状态label
    sat_label_ct = tk.Label(Frame_Creater, text='Hi, 我是个状态条', fg = 'white', bg=gray_1,height=3,
        font=("Arial", 9),compound='center',width=111)
    sat_label_ct.grid(row=9, column=0, padx=pd_x, pady=30)
    #启动按钮    
    start_bt_ct = tk.Button(Frame_Creater, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:NTG_get_creater.pull_function_ct(cookie,Entry_keyword_ct.get(),path,proxy,
            start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct),
            bd = -1, text = 'Go!', image = img, fg = 'white')
    start_bt_ct.grid(row=10, column=0, padx=10, pady=0)
    #返回按钮
    back_bt_ct = tk.Button(Frame_Creater, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:de_show_creater(),
            bd = -1, text = '返回', image = img, fg = 'white')
    back_bt_ct.grid(row=12, column=0, padx=10, pady=10)




    #       Seeting Frame
    Frame_Seeting = tk.Frame(root, bg = gray_0, height = 1000, width = 1000)
    Frame_Seeting.place(x=0, y=0)
    title = tk.Label(Frame_Seeting,text='PTD! - Setting - 设置',font=("Arial", 20), fg = gray_font, bg=gray_0)
    title.grid(row=0, padx=pd_x, pady=10)
    #路径label
    path_label = tk.Label(Frame_Seeting, text='请输入或是点击右侧浏览按钮设置下载路径:', fg = gray_font, bg=gray_0,height=1,font=("Arial", 12))
    path_label.grid(row=1, column=0, padx=pd_x, pady=pd_y)
    #路径entry
    Entry_path = tk.Entry(Frame_Seeting, fg = gray_2, bg=gray_1,relief='flat')
    Entry_path.grid(row=2, column=0, padx=pd_x, pady=pd_y, ipadx=300, ipady=entry_y, sticky='W')
    #浏览按钮    
    path_bt = tk.Button(Frame_Seeting, width=30, height=35,relief='flat', compound='center',bg = gray_2,
            command = lambda:path_wr(),
            bd = -1, text = '浏览', image = img, fg = 'white')
    path_bt.place(x=760,y=83)
    #代理label
    proxy_label = tk.Label(Frame_Seeting, text='请输入HTTP(S)代理(例:127.0.0.1:20051)   #注:冒号请用输入法英文打:', fg = gray_font, bg=gray_0,height=1,font=("Arial", 12))
    proxy_label.grid(row=3, column=0, padx=pd_x, pady=pd_y)
    #代理entry
    Entry_proxy = tk.Entry(Frame_Seeting, fg = gray_2, bg=gray_1,relief='flat')
    Entry_proxy.grid(row=4, column=0, padx=pd_x, pady=pd_y, ipadx=entry_x, ipady=entry_y)
    #cookie label
    cookie_label = tk.Label(Frame_Seeting, text='请输入您的Pixiv账号的cookie:', fg = gray_font, bg=gray_0,height=1,font=("Arial", 12))
    cookie_label.grid(row=5, column=0, padx=pd_x, pady=pd_y)
    #cookie entry
    cookie_entry = tk.Entry(Frame_Seeting, fg = gray_2, bg=gray_1,relief='flat')
    cookie_entry.grid(row=6, column=0, padx=pd_x, pady=pd_y, ipadx=entry_x, ipady=entry_y)
    #启动按钮    
    start_bt = tk.Button(Frame_Seeting, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:save_conf(cookie_entry.get(),Entry_path.get(),Entry_proxy.get()),
            bd = -1, text = '保存', image = img, fg = 'white')
    start_bt.grid(row=7, column=0, padx=10, pady=10)
    #关于按钮
    about_bt = tk.Button(Frame_Seeting, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:about(),
            bd = -1, text = 'About us...', image = img, fg = 'white')
    about_bt.grid(row=8, column=0, padx=10, pady=0)
    #返回按钮
    back_bt_ct = tk.Button(Frame_Seeting, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:de_show_config(),
            bd = -1, text = '返回', image = img, fg = 'white')
    back_bt_ct.grid(row=12, column=0, padx=10, pady=10)


    is_file = os.path.exists("./conf/cookie.ntg")
    if is_file == True:
        cookie_entry.delete(0, 9999999)
        cookie_entry.insert(0,NTG_base.read_file('./conf/cookie.ntg'))
    is_file = os.path.exists("./conf/path.ntg")
    if is_file == True:
        Entry_path.delete(0, 9999999)
        Entry_path.insert(0,NTG_base.read_file('./conf/path.ntg'))
    is_file = os.path.exists("./conf/proxy.ntg")
    if is_file == True:
        Entry_proxy.delete(0, 9999999)
        Entry_proxy.insert(0,NTG_base.read_file('./conf/proxy.ntg'))




    
    #       Main Frame
    Frame_Main = tk.Frame(root, bg = gray_0, height = 1000, width = 1000)
    Frame_Main.place(x=0, y=0)
    #say
    say = tk.Label(Frame_Main,text=NTG_inf_seeting.say_text,font=("Arial", 8), fg = gray_font, bg=gray_0)
    say.grid(row=0, padx=pd_x, pady=0)
    #标题
    title = tk.Label(Frame_Main,text='PTD! - WELCOME - ',font=("Arial", 30), fg = gray_font, bg=gray_0)
    title.grid(row=1, padx=pd_x, pady=70)
    #version
    title = tk.Label(Frame_Main,text='version : ' + NTG_inf_seeting.version,font=("Arial", 10), fg = gray_font, bg=gray_0)
    title.grid(row=2, padx=pd_x, pady=0)
    #TAG按钮    
    start_bt = tk.Button(Frame_Main, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:show_main(cookie, path),
            bd = -1, text = '按照Tag爬取', image = img, fg = 'white')
    start_bt.grid(row=3, column=0, padx=10, pady=10)
    #creater按钮
    creater_bt = tk.Button(Frame_Main, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:show_creater(cookie, path),
            bd = -1, text = '按照画师爬取', image = img, fg = 'white')
    creater_bt.grid(row=4, column=0, padx=10, pady=10)
    #seeting按钮
    seeting_bt = tk.Button(Frame_Main, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:show_config(),
            bd = -1, text = '设置', image = img, fg = 'white')
    seeting_bt.grid(row=5, column=0, padx=10, pady=10)
    #Donate按钮
    donate_bt = tk.Button(Frame_Main, width=780, height=30,relief='flat', compound='center',bg = gray_2,
            command = lambda:show_donate(),
            bd = -1, text = '赞助', image = img, fg = 'gold')
    donate_bt.grid(row=6, column=0, padx=10, pady=10)

    Frame_donate.place_forget()
    Frame_Seeting.place_forget()
    Frame_Creater.place_forget()
    Frame_Tag.place_forget()
    is_file = os.path.exists("./conf/policy.ntg")
    if is_file == False:
        ask = tkinter.messagebox.askyesno("用户协议 - 按回车同意",NTG_inf_seeting.policy)
        if ask == False:
            os._exit(0)
        else:
            NTG_base.write_file("./conf/policy.ntg", '1')
    Tupdate = threading.Thread(target=NTG_Other_function.GetUpdateStuation,args=())
    Tsay = threading.Thread(target=NTG_Other_function.GetCentence,args=(say,))
    Tsay.start()
    Tupdate.start()
    root.mainloop()
    os._exit(0)


if __name__ == '__main__':
    tUI = threading.Thread(target=ui,args=())
    tUI.start()