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


#   CreaterCode


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

def process_ct(input):
    input = json.loads(input)
    input = input['body']['works']
    result_ = []
    for sg in input:
        result_.append(input[sg])
    result = []
    for sg in result_:
        result.append({
            'id':sg['id'],
            'title':sg['title'],
            'userId':sg['userId'],
            'url':sg['url'],
            'tags':sg['tags'],
        })
    return result

def first_layer_process(cookie, creater_id, proxy):
    url = 'https://www.pixiv.net/ajax/user/' + str(creater_id) + '/profile/all?lang=zh'
    header = {
        'authority': 'www.pixiv.net',
        'method': 'GET',
        'path': '/ajax/user/' + str(creater_id) + '/profile/all?lang=zh',
        'scheme': 'https',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': cookie,
        'referer': 'https://www.pixiv.net/users/' + str(creater_id),
        'sec-ch-ua': '\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"92\"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
        #'x-user-id': '51489246'
    }
    result = NTG_base.get(url, header, '', proxy)[0]
    result = json.loads(result)['body']['illusts']
    list = []
    for sg in result:
        list.append(sg)
    return list

def second_layer_process(input, creater_id, cookie, proxy, page):
    url = 'https://www.pixiv.net/ajax/user/' + str(creater_id) + '/profile/illusts?'
    for sg in input:
        if sg == input[0]:
            url += 'ids%5B%5D=' + str(sg)
        else:
            url += '&ids%5B%5D=' + str(sg)
    url += '&work_category=illustManga&is_first_page=' + str(page) + '&lang=zh'
    url_path = '/ajax/user/' + str(creater_id) + '/profile/illusts?'
    for sg in input:
        if sg == input[0]:
            url_path += 'ids%5B%5D=' + str(sg)
        else:
            url_path += '&ids%5B%5D=' + str(sg)
    url_path += '&work_category=illustManga&is_first_page=' + str(page) + '&lang=zh'
    header = {
        'authority': 'www.pixiv.net',
        'method': 'GET',
        'path': url_path,
        'scheme': 'https',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': cookie,
        'referer': 'https://www.pixiv.net/users/' + str(creater_id) + '/artworks',
        'sec-ch-ua': '\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99", \"Microsoft Edge\";v=\"92\"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
    }
    result = NTG_base.get(url, header, '', proxy)[0]
    return result

def creater_start(cookie, creater_id, proxy, path, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct):
    sg_ = -1
    result = first_layer_process(cookie, creater_id, proxy)
    page_t = int(len(result) / 48)
    if page_t < len(result) / 48:
        page_t += 1
    while sg_ < page_t or sg == page_t:
        sg_ += 1
        list = []
        ct = sg_ * 48
        t1 = -1
        while t1 < 48 or t1 == 48:
            t1 += 1
            try:
                list.append(result[ct + t1 - 1])
            except:
                break
        if len(result) < 48 or len(result) == 48:                   #如果数量不到48，处理后上传时会出错，所以让他直接等于result
            list = result
        sat_label_tag['text'] = '图片列表获取完成 请稍后...'
        sat_label_tag.update()
        sat_label_ct['text'] = '图片列表获取完成 请稍后...'
        sat_label_ct.update()
        result_ = second_layer_process(list, creater_id, cookie, proxy, '0')
        try:
            result_ = process_ct(result_)                                #处理json，取重要信息
        except:
            break
        for sg in result_:                                           #将处理的信息通过function取链接下载
            url = sg['url']
            #input, path, proxy, page, keyword, name, path_oring, keyword_oring
            get_image_oring(url, path + '/' + NTG_base.process_file_name(sg['title']) + '.jpg', proxy, '全部', creater_id, NTG_base.process_file_name(sg['title']), path, creater_id, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct)

def pull_function_creater(cookie, creater_id, path, proxy, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct):
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
    if cookie == '' or creater_id == '' or dir_true == False:
        tkinter.messagebox.showerror('警告(っ °Д °;)っ','请检查您是否少填信息后重试\n或是填写了不存在的下载路径')
    else:
        if path == '':
            path = '.'
            tkinter.messagebox.showinfo('提示(～￣▽￣)～','我们检测到您并没有填写下载路径，下载仍会继续，下载的图片将会保存到此软件目录下')
        is_file = os.path.exists('./conf/' + creater_id + '.ntg')
        if is_file == True:
            skip = int(NTG_base.read_file('./conf/' + creater_id + '.ntg'))
        else:
            skip = 0
        count = 0
        try:
            creater_start(cookie, creater_id, proxy, path, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct)
        except ValueError as error_:
            tkinter.messagebox.showerror('错误/(ㄒoㄒ)/~~','下载数量:'+str(count) + '\n' + str(error_))
    sat_label_tag['text'] = '完成！'
    sat_label_tag.update()
    sat_label_ct['text'] = '完成！'
    sat_label_ct.update()
    start_bt_tag.config(state = 'normal')
    start_bt_tag.update()
    start_bt_ct.config(state = 'normal') 
    start_bt_ct.update()
    return 0


def pull_function_ct(cookie, creater_id, path, proxy, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct):
    try:
        tFC = threading.Thread(target=pull_function_creater,args=(cookie, creater_id, path, proxy, start_bt_tag, start_bt_ct, sat_label_tag, sat_label_ct))
        tFC.start()
    except:
        return 0