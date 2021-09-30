#-*- coding:utf-8 -*-
#CREATER: NTGtech-ShenAo
import requests
from lxml import etree
import json
import urllib
import urllib3
import threading
import os
from pathlib import Path
import tkinter.messagebox

import NTG_base
#用来根据tag过滤
def slect_tag(result_input, tag_input):
    result = []
    for sg in result_input:
        ct = 0
        for sg_tag in sg['tags']:
            for ipt_tag_sg in tag_input:
                if ipt_tag_sg == sg_tag:
                    ct += 1
        if ct == len(tag_input):
            result.append(sg)
    return result

def get_tag_inf(cookie, keyword, page, proxy, user_id):
    url = 'https://www.pixiv.net/ajax/search/artworks/' + urllib.parse.quote(keyword) + '?word=' + urllib.parse.quote(keyword) + '&order=date_d&mode=all&p=' + str(page) + '&s_mode=s_tag&type=all&lang=zh'
    header = {
        'authority': 'www.pixiv.net',
        'method': 'GET',
        'path': '/ajax/search/artworks/' + urllib.parse.quote(keyword) + '?word=' + urllib.parse.quote(keyword) + '&order=date_d&mode=all&p=' + str(page) + '&s_mode=s_tag&type=all&lang=zh',
        'scheme': 'https',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': cookie,
        'referer': 'https://www.pixiv.net/tags/' + urllib.parse.quote(keyword) + '/artworks',
        'sec-ch-ua': '\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"92\"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
        'x-user-id': str(user_id),
    }
    data = {
        'word': urllib.parse.quote(keyword),
        'order': 'date_d',
        'mode': 'all',
        'p': 'page',
        's_mode': 's_tag_full',
        'type': 'all',
        'lang': 'zh',
    }
    result = NTG_base.get(url, header, data, proxy)
    return result[0]

def process_tag(input):
    input = json.loads(input)
    input = input['body']['illustManga']['data']
    result = []
    for sg in input:
        result.append({
            'id':sg['id'],
            'title':sg['title'],
            'userId':sg['userId'],
            'url':sg['url'],
            'tags':sg['tags'],
        })
    return result


def get_image_oring(input, path, proxy, page, keyword, name, path_oring, keyword_oring, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct):
    global count, skip
    count += 1
    if count > skip:                                                    #用来跳过，如果下的计数比跳过的多就继续下
        header = {
            'Referer': 'https://www.pixiv.net/',
            'sec-ch-ua': '\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"92\"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
        }
        url = NTG_base.getSubstr(input, '/img-master/img/', '_square1200.jpg')   #取中间的信息(jpg)
        com = '.net' in url
        if com == True:
            url = NTG_base.getSubstr(input, 'custom-thumb/img/', '_custom1200')  #取中间的信息(gif)
            url = 'https://i.pximg.net/img-original/img/' + url + '.jpg'
        else:
            url = 'https://i.pximg.net/img-original/img/' + url + '.jpg'
        file = requests.get(url = url, headers = header, proxies = proxy, stream=True).content      #错误就改成png
        if file == b'<!DOCTYPE html>\n<html>\n    <h1>404 Not Found</h1>\n</html>\n':
            url = url[:-3] + 'png'
            path = path[:-3] + 'png'
            file = requests.get(url = url, headers = header, proxies = proxy, stream=True).content  #再错就改成gif
        if file == b'<!DOCTYPE html>\n<html>\n    <h1>404 Not Found</h1>\n</html>\n':
            url = url[:-3] + 'gif'
            path = path[:-3] + 'gif'
            file = requests.get(url = url, headers = header, proxies = proxy, stream=True).content
        path = NTG_base.process_exits_file(path,path_oring)                      #检测文件是否存在，存在就重命名
        try:
            sat_label_tag['text'] = '下载个数:' + str(count) + '\n' + '页数:' + str(page) +'  名称:' + str(name) + '\n' + '链接:' + str(url)
            sat_label_tag.update()
            sat_label_ct['text'] = '下载个数:' + str(count) + '\n' + '页数:' + str(page) +'  名称:' + str(name) + '\n' + '链接:' + str(url)
            sat_label_ct.update()
        except:
            sat_label_tag['text'] = '下载个数:' + str(count) + '\n' + '页数:' + str(page) + '\n' + '链接:' + str(url)
            sat_label_tag.update()
            sat_label_ct['text'] = '下载个数:' + str(count) + '\n' + '页数:' + str(page) + '\n' + '链接:' + str(url)
            sat_label_ct.update()
        with open(path, "wb") as fw:                                    #写入文件
            fw.write(file)
        fw.close()
        if os.path.getsize(path) == 58:                                 #写入后在检测一边，如果还是错误，那就是mp4了
            try:
                os.remove(path)
            except:
                print('')
            sat_label_tag['text'] = '图片类型不支持\n' + input
            sat_label_tag.update()
            sat_label_ct['text'] = '图片类型不支持\n' + input
            sat_label_ct.update()
    else:
        sat_label_tag['text'] = str(count) + '跳过-原因:下载过的文件.'
        sat_label_tag.update()
        sat_label_ct['text'] = str(count) + '跳过-原因:下载过的文件.'
        sat_label_ct.update()
    NTG_base.write_file('./conf/' + NTG_base.process_file_name(keyword_oring) + '.ntg', str(count))


def start(cookie, keyword, page, proxy, path, slect, keyword_oring, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct):
    if cookie != '':
        #获取user id
        cookie_list = cookie.split(';')
        for i in cookie_list:
            i1 = 'PHPSESSID' in i
            if i1 == True:
                user_id = NTG_base.getSubstr(i, 'PHPSESSID=', '_')
                break
            else:
                user_id = ''
        if user_id == '':
            tkinter.messagebox.showwarning('WARNING','无法在您的Cookie中获取到user id，请更换cookie后重试！\n下载仍会继续但无法下载18+图片')
        result = get_tag_inf(cookie,keyword,page,proxy,user_id)     #获取json List
        result = process_tag(result)                                #处理json，取重要信息
        sat_label_tag['text'] = '图片列表获取完成 请稍后...'
        sat_label_tag.update()
        sat_label_ct['text'] = '图片列表获取完成 请稍后...'
        sat_label_ct.update()
        if type(slect) == list and len(slect) > 1:
            result = slect_tag(result, slect)
        for sg in result:                                           #将处理的信息通过function取链接下载
            url = sg['url']
            get_image_oring(url, path + '/' + NTG_base.process_file_name(sg['title']) + '.jpg', proxy, page, keyword, NTG_base.process_file_name(sg['title']), path, keyword_oring, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct)
        
            

def pull_function(cookie, keyword, path, proxy, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct):
    try:
        tFC = threading.Thread(target=pull_function_True,args=(cookie, keyword, path, proxy, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct))
        tFC.start()
    except:
        return 0

def pull_function_True(cookie,keyword,path,proxy, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct):
    global count, skip
    start_bt_tag.config(state = 'disabled')
    start_bt_tag.update()
    start_bt_ct.config(state = 'disabled') 
    start_bt_ct.update()
    if proxy != '':
        proxy = {
            'http':proxy,
            'https':proxy,
        }
    dir_true = os.path.exists(path)
    sat_label_tag['text'] = '请稍后...'
    sat_label_tag.update()
    sat_label_ct['text'] = '请稍后...'
    sat_label_ct.update()
    if cookie == '' or keyword == '' or dir_true == False:
        tkinter.messagebox.showerror('警告(っ °Д °;)っ','请检查您是否少填信息后重试\n或是填写了不存在的下载路径')
    else:
        if path == '':
            path = '.'
            tkinter.messagebox.showinfo('提示(～￣▽￣)～','我们检测到您并没有填写下载路径，下载仍会继续，下载的图片将会保存到此软件目录下')
        slect = keyword.replace('，',',')
        slect = slect.split(',')
        keyword_oring = NTG_base.process_file_name(keyword)
        is_file = os.path.exists('./conf/' + NTG_base.process_file_name(keyword) + '.ntg')
        if is_file == True:
            skip = int(NTG_base.read_file('./conf/' + NTG_base.process_file_name(keyword) + '.ntg'))
        else:
            skip = 0
        page = int(skip / 60)
        count = page * 60
        if type(slect) == list and len(slect) > 1:
            page = 0
            count = 0
            keyword = slect[0]
        print(keyword,page,count,skip)
        while True:
            page += 1
            try:
                start(cookie,keyword,page,proxy,path,slect,keyword_oring, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct)
            except ValueError as error_:
                tkinter.messagebox.showerror('错误/(ㄒoㄒ)/~~','下载数量:'+str(count) + '\n' + str(error_))
                break
    sat_label_tag['text'] = '完成'
    sat_label_tag.update()
    sat_label_ct['text'] = '完成'
    sat_label_ct.update()
    start_bt_tag.config(state = 'normal')
    start_bt_tag.update()
    start_bt_ct.config(state = 'normal') 
    start_bt_ct.update()
    return 0
        
