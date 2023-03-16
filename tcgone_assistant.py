from selenium import webdriver
import time
import os
from os import getcwd,sep
cwd = getcwd()
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
import pandas as pd
import imagehash
from PIL import Image, ImageGrab
import numpy as np
import requests
import base64
import pandas.io.clipboard as cb
import configparser

cf=configparser.ConfigParser()
cf.read("config.ini",encoding="utf-8-sig")
loginid=cf.get("USER","userid")
loginpw=cf.get("USER","userpwd")
autosizew=int(cf.get("Size","width"))
autosizeh=int(cf.get("Size","high"))

print("================================\nTCG ONE助手\n================================")
print("请不要关闭本窗口，在弹出的窗口中操作\n================================")


transinfo=pd.read_excel("database/translist.xlsx",index_col="En_Name")
dcd=transinfo.to_dict()
str_dick=dcd["Cn_Name"]
str_search=dcd["优先级"]

if os.path.isfile("chromedriver.exe"):
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    print("正在打开浏览器")
    driver=webdriver.Chrome(f'{cwd}{sep}chromedriver',chrome_options=options)
else:
    print("找不到chromedriver，尝试寻找edgedriver")
    driver=webdriver.Edge(f'{cwd}{sep}msedgedriver')

size=0
lastk=""




showlist=[]
findcard=[]
changecardlist=[]

sg.theme('DarkAmber')
layout=[
    [sg.Button("扩展",key='expand',font="黑体"),sg.Button("清屏",key='clean',font="黑体")],
    [sg.Listbox(values=showlist,key='infolist',size=(35,9),enable_events=True,font="黑体",background_color="#191631",text_color="#b6b3d0"),sg.Listbox(values=findcard,key='findlist',size=(35,9),enable_events=True,font="黑体",background_color="#191631",text_color="#b6b3d0")],
    [sg.ML(key="rolltext",size=(35,25),autoscroll=True,font="黑体",background_color="#191631",text_color="#b6b3d0"),sg.Image(key="showpic",filename="db/1-基本草能量.png")],
    [sg.Text("卡查功能：",font="黑体"),sg.InputText(key='inputfind',font="黑体",background_color="#191631",text_color="#b6b3d0"),sg.Button("查询",font="黑体"),sg.Button("重载数据库",font="黑体")],
    [sg.Text(key="TipText",font="黑体",size=(65,1))]
]

window= sg.Window('TCG ONE助手', layout,size=(300,450),keep_on_top=True)
driver.get("https://play.tcgone.net/")

try:
    #自动登录
    driver.find_element(By.XPATH,'/html/body/div/form/div[1]/input').send_keys(loginid)
    driver.find_element(By.XPATH,'/html/body/div/form/div[2]/input').send_keys(loginpw)
except:
    pass


def getlistinfo():
    global lastk
    outlastk=[]
    showk=""
    try:
        #es=driver.find_element_by_xpath('//*[@id="ROOT-2521314"]/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[1]/div/div[2]/div')
        es=driver.find_element(By.XPATH,'//*[@id="ROOT-2521314"]/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[1]/div/div[2]/div')
        k=es.text
        showk=k.replace(lastk,"")
        showk=showk.replace("●","\n\n●").replace("\n\n\n","\n\n")
        for key in str_dick:
            if(key in showk):
                showk=showk.replace(key,str_dick[key])
                if(str_search[key]==1 or str_search[key]==5):
                    outlastk.append(str_dick[key])
            
        if "●" in showk:
            #print(showk)
            pass
        lastk=k
    except Exception as e:
        #print(e)
        pass
    try:
        if("untap.in" in driver.current_url):
            es=driver.find_element(By.XPATH,'//*[@id="game-chat-wrap"]/div[2]/section/div[1]/div')
            k=es.text
            showk=k.replace(lastk,"").replace("\n","\n\n")
            for key in str_dick:
                if(key in showk):
                    showk=showk.replace(key,str_dick[key])
                    if(str_search[key]==1 or str_search[key]==5):
                        outlastk.append(str_dick[key])
            lastk=k
    except Exception as e:
        pass
    return outlastk,showk


def getbigpic():
    try:
        bpic=driver.find_element(By.XPATH,'//*[@id="ROOT-2521314-overlays"]/div[3]/div/div/div[3]/div/div/div[3]/div/img')
        src=bpic.get_attribute("src")
        get_src=requests.get(src)
        if get_src.status_code == 200:
            with open("search_pic/grab_clipboard.jpg", 'wb') as f:
                f.write(get_src.content)
    except:
        pass
    try:
        bpic=driver.find_element(By.XPATH,'//*[@id="ROOT-2521314-overlays"]/div[3]/div/div/div[3]/div/div/div/div/img')
        src=bpic.get_attribute("src")
        get_src=requests.get(src)
        if get_src.status_code == 200:
            with open("search_pic/grab_clipboard.jpg", 'wb') as f:
                f.write(get_src.content)
    except:
        pass
    try:
        bpic=driver.find_element(By.XPATH,'//*[@id="ROOT-2521314-overlays"]/div[5]/div/div/div[3]/div/div/div/div/img')
        src=bpic.get_attribute("src")
        get_src=requests.get(src)
        if get_src.status_code == 200:
            with open("search_pic/grab_clipboard.jpg", 'wb') as f:
                f.write(get_src.content)
    except:
        pass
    


def changecardpic():
    global changecardlist
    for i in changecardlist:
        with open("db/"+i[1], 'rb') as file:
            data = file.read()
            encodestr = base64.b64encode(data)
            image_data = str(encodestr, 'utf-8')
        driver.execute_script('''
        var imglist=document.querySelectorAll("img[src='{oldsrc}']")
        for(var i of imglist){
            i.src="{newsrc}"
        }
        '''.format(outsrc=i[0],newsrc=image_data))

def getcard(cardname):
    database1=pd.read_json("database/ptcglist.json",dtype='str')
    cards=database1[database1["卡片名称"].str.contains(cardname)]
    outcard=pd.DataFrame(cards,columns=["序号","卡片名称"])
    outcard.set_index("序号",inplace=True)
    outlist=str(outcard).split("\n")
    del outlist[0]
    del outlist[0]
    return outlist

def getcardpic(num):
    database1=pd.read_json("database/ptcglist.json",dtype='str')
    cards=database1[database1["序号"]==num]
    return cards.iloc[0]["文件名"]

def find_keys(dict, val):
  return list(key for key, value in dict.items() if value == val)

def getcut():
    # 保存剪切板内图片
    im = ImageGrab.grabclipboard() 
    if isinstance(im, Image.Image):
        lastlist=[]
        lastpic=""
        #print("Image: size : %s, mode: %s" % (im.size, im.mode))
        im.save("search_pic/grab_clipboard.png")
        with Image.open("search_pic/grab_clipboard.png") as img:
            img=img.resize((300,417))
            img=img.crop((25,50,280,200))
            hash1 = imagehash.average_hash(img, 10).hash
        #print(hash1)
        rget=np.load("database/npy/imgdata.npy",allow_pickle=True)
        belike=50
        while belike<100:
            getlist=[]
            threshold = 1 - belike/100
            diff_limit = int(threshold*(10**2))
            for i in rget:
                hash2=i[1]
                #print(hash2)
                if np.count_nonzero(hash1 != hash2) <= diff_limit:
                    getlist.append(i[0].replace(".png","").replace("-"," "))
                    lastpic=i[0]
            if len(getlist)<5 and len(lastlist)==0:
                lastlist=getlist
            if(len(getlist)>1):
                belike+=1
            else:
                break
        cb.copy("")
        return lastpic,lastlist
    else:
        lastlist=[]
        lastpic=""
        getbigpic()
        with Image.open("search_pic/grab_clipboard.jpg") as img:
            img=img.resize((300,417))
            img=img.crop((25,50,280,200))
            hash1 = imagehash.average_hash(img, 10).hash
        #print(hash1)
        rget=np.load("database/npy/imgdata.npy",allow_pickle=True)
        belike=50
        while belike<100:
            getlist=[]
            threshold = 1 - belike/100
            diff_limit = int(threshold*(10**2))
            for i in rget:
                hash2=i[1]
                #print(hash2)
                if np.count_nonzero(hash1 != hash2) <= diff_limit:
                    getlist.append(i[0].replace(".png","").replace("-"," "))
                    lastpic=i[0]
            if len(getlist)<5 and len(lastlist)==0:
                lastlist=getlist
            if(len(getlist)>1):
                belike+=1
            else:
                break
        return lastpic,lastlist

showword=""
while True:
    event,value = window.Read(timeout=3000)
    if(event=="infolist"):
        if size==0:
            window['expand'].update("精简")
            window.Size=(autosizew,autosizeh)
            size=1
        try:
            findlist=getcard(showlist[window['infolist'].GetIndexes()[0]])
            window['findlist'].update(findlist)
            try:
                window['findlist'].update(set_to_index=0)
                outpic=getcardpic(findlist[window['findlist'].GetIndexes()[0]].split(" ")[0])
                outpic='db/'+outpic+'.png'
                window['showpic'].update(outpic)
            except:
                pass
        except:
            pass
    if(event=="findlist"):
        try:
            outpic=getcardpic(findlist[window['findlist'].GetIndexes()[0]].split(" ")[0])
            outpic='db/'+outpic+'.png'
            window['showpic'].update(outpic)
        except:
            pass
    if(event=="重载数据库"):
        try:
            transinfo=pd.read_excel("database/translist.xlsx",index_col="En_Name")
            dcd=transinfo.to_dict()
            str_dick=dcd["Cn_Name"]
            str_search=dcd["优先级"]
        except:
            pass

    if(event=="查询"):
        try:
            searchword=window["inputfind"].Get()
            if(len(searchword)>0):
                findlist=getcard(searchword)
                window['findlist'].update(findlist)
                try:
                    window['findlist'].update(set_to_index=0)
                    outpic=getcardpic(findlist[window['findlist'].GetIndexes()[0]].split(" ")[0])
                    outpic='db/'+outpic+'.png'
                    window['showpic'].update(outpic)
                except:
                    pass
            else:
                findcard,findlist=getcut()
                window['findlist'].update(findlist)
                try:
                    #window['findlist'].update(set_to_index=0)
                    #outpic=getcardpic(findlist[window['findlist'].GetIndexes()[0]].split(" ")[0])
                    outpic='db/'+findcard
                    window['showpic'].update(outpic)
                except:
                    pass
        except Exception as e:
            print(e)
        try:
            outkeys=find_keys(str_dick,window["inputfind"].Get())
            if(len(outkeys)>0):
                window['TipText'].update("英文可能为："+outkeys[0])
            else:
                window['TipText'].update("")
        except:
            pass
    if(event=="expand"):
        if size==0:
            window['expand'].update("精简")
            window.Size=(autosizew,autosizeh)
            size=1
        else:
            window['expand'].update("扩展")
            window.Size=(300,450)
            size=0
    if(event=="clean"):
        lastk=""
        showword=""
    if(event==WIN_CLOSED):
        break
        
    getinfo,showk=getlistinfo()
    for i in getinfo:
        if i!="" or i!="\n":
            if i in showlist:
                pass
            else:
                if len(showlist)>8:
                    del showlist[0]
                showlist.append(i)
    showword+=showk
    window['rolltext'].update(showword)
    window['infolist'].update(showlist)
