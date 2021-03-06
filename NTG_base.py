#-*- coding:utf-8 -*-
#CREATER: NTGtech-ShenAo
import qrcode
from typing import List
import requests
from lxml import etree
import json
import urllib
import urllib3
import tkinter as tk
import threading
from tkinter import Frame, filedialog
import os
import tkinter.messagebox
from pathlib import Path
import PIL.Image
#功能性函数
#text content cookie
def get(url,header,data,proxy):
    response = requests.get(url = url, headers = header, data = data, proxies = proxy, verify = False)
    cookie_value = ''
    for key,value in response.cookies.items():  
        cookie_value += key + '=' + value + ';'  
    return response.text,response.content, cookie_value

def post(url,header,data,proxy):
    response = requests.post(url = url, headers = header, data = data, proxies = proxy, verify = False)
    cookie_value = ''
    for key,value in response.cookies.items():  
        cookie_value += key + '=' + value + ';'  
    return response.text,response.content, cookie_value

def put(url,header,data,proxy):
    response = requests.put(url = url, headers = header, data = data, proxies = proxy, verify = False)
    cookie_value = ''
    for key,value in response.cookies.items():  
        cookie_value += key + '=' + value + ';'  
    return response.text,response.content, cookie_value

def getSubstr(input,start,end):
    #php中的setsubstr    获取在input中夹在start和end中间的文本
    find_num = input.find(start)
    result = input[find_num+len(start):]
    find_end_num = result.find(end)
    result = result[:find_end_num]
    return result

def strstr(input,fn):
    #php中的strstr      获取input中fn后的所有文本
    find_num = input.find(fn)
    result = input[find_num+len(fn):]
    return result

def strstr_front(input,fn):
    #获取input中fn前的所有文本
    find_num = input.find(fn)
    result = input[:find_num]
    return result

def read_file(path):
    with open(path) as fp:
        content = fp.read()
    return content

def write_file(filepath,insert):
    filepath = filepath.replace('/','\\')
    with open(filepath,'w') as wf:
        wf.write(insert)
    return True

def urlencode(str) :
    reprStr = repr(str).replace(r'\x', '%')
    return reprStr[1:-1]

def size(input):
    input = int(input)
    if input < 8:
        result = [input,'B']
    elif input < 64:
        result = [int(input/8),'B']
    elif input < 8192:
        result = [int(input/64),'字节']
    elif input < 1048576:
        result = [int(input/8192),'KB']
    elif input < 1073741824:
        result = [int(input/1048576),'MB']
    else:
        result = [int(input/1073741824),'GB']
    return result

def get_back_path(input):
    if input != '/':
        input = input.split('/')
        len_show = len(input) - 2
        temp = -1
        temp_result = '/'
        while temp < len_show:
            temp += 1
            temp_result = temp_result + '/' + input[temp]
    else:
        temp_result = '/'
    temp_result = temp_result.replace('//','/')
    return temp_result

def process_exits_file(input,path_output):
    a = 0
    while a == 0:
        is_file = os.path.exists(input)
        if is_file == False:
            return input
        else:
            input = input.replace('/','\\')
            path_output = path_output.replace('/','\\')
            change_name = input.split('\\')[-1] #获取文件名
            if_has_change = '- 副本' in change_name
            if if_has_change == True:               #如果[源文件]有副本字样
                muti_change_times = 1               #定义 - 副本 () 中的数字
                while True:
                    muti_change_times += 1
                    file_name_rebuild = input.split('\\')[-1].split('.')[-2] + ' - 副本 (' + str(muti_change_times) + ')' + '.' + input.split('.')[-1]#定义新文件的名称，匹配名称是否存在
                    file_exist = Path(path_output + '\\' +  + file_name_rebuild)      #检测调整后的文件名是否存在
                    if file_exist.is_file() == False:                        #文件不存在
                        result = path_output + '\\' + file_name_rebuild
                        break
            else:                                   #如果[源文件]没有副本字样
                try:
                    muti_change_times = int(change_name.split(' - 副本 (')[-1].split(')')[-2])               #定义 - 副本 () 中的数字
                    if muti_change_times == '':                         #(可能会弃用)提取副本中的数字
                        muti_change_times = 1
                except:
                    muti_change_times = 1
                while True:
                    muti_change_times += 1
                    file_name_rebuild = change_name.split('\\')[-1].split('.')[-2] + ' - 副本 (' + str(muti_change_times) + ')' + '.' + change_name.split('.')[-1]#定义新文件的名称，匹配名称是否存在
                    file_exist = Path(path_output + '\\' + file_name_rebuild)      #检测调整后的文件名是否存在
                    if file_exist.is_file() == False:                        #文件存在                                             #不存在，复制重命名的文件，打破循环
                        result = path_output + '\\' + file_name_rebuild
                        break
                result = result.replace('\\','/')
            return result

def process_file_name(input):
    input = input.replace('/','')
    input = input.replace('|','')
    input = input.replace('<','')
    input = input.replace('>','')
    input = input.replace('\\','')
    input = input.replace('\"','')
    input = input.replace('\'','')
    input = input.replace(':','')
    input = input.replace('?','')
    input = input.replace('*','')
    input = input.replace('|','')
    return input

def process_html_text(input):
    input = input.replace('&quot;','\"')
    input = input.replace('&amp;','&')
    input = input.replace('&lt;','<')
    input = input.replace('&gt;','>')
    input = input.replace('&nbsp;',' ')
    return input
    
def make_qr(str, path):
    qr=qrcode.QRCode(
        version=4,  #生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
        error_correction=qrcode.constants.ERROR_CORRECT_M, #L:7% M:15% Q:25% H:30%
        box_size=10, #每个格子的像素大小
        border=2, #边框的格子宽度大小
    )
    qr.add_data(str)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(path)
    return 0

