from lxml import etree
import json
import os
import tkinter.messagebox

import NTG_base
import NTG_inf_seeting

def GetLanZouInf(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'
    }
    result = NTG_base.get(url, header, '', '')[0]
    html = etree.HTML(result)
    result = str(html.xpath('/html/body/div/div/div/table/tr/td/text()')[7])
    result = result.replace('*','\"')
    result = result.replace('\\\\n{','{')
    result = result.replace('\\\\t  \\','')
    result = NTG_base.process_html_text(result)
    return result

def GetUpdateStuation():
    try:
        update_url = 'https://ntgpro.lanzoui.com/iFxw8saom1a'
        result = GetLanZouInf(update_url)
        result = json.loads(result)
        Get_version = result['version']
        Get_function = result['function']
        Get_url = result['url']
        Get_update_inf = result['text'].replace('\\n','\n')
        if NTG_inf_seeting.version != Get_version:
            ask = tkinter.messagebox.askyesno("有更新,是否更新？",Get_update_inf)
            if ask == True:
                os.system('start ' + Get_url)
    except:
        return 0

def GetCentence(say):
    try:
        cen_url = 'https://ntgpro.lanzoui.com/i1uASsaqdxa'
        result = GetLanZouInf(cen_url)
        result = json.loads(result)
        say['text'] = result['text']
        say.update()
        return 0
    except:
        return 0