import sys, os, hmac, html, pymysql, requests, json, time, re, random, hashlib
from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
sys.path.append('../..')
import go
import tools


def chaQQ(meta_data):
    userid = go.getCQValue('qq', meta_data.get('message'))
    data = requests.get('https://qb-api.ltd/allcha.php?qq={0}'.format(userid)).json()
    if data.get('code') != 200:
        return go.send(meta_data, '[CQ:face,id=171] 查询失败！')
    data = data.get('data')
    message = '[CQ:face,id=171] 用户QQ：{0}\n[CQ:face,id=171] 手机号：{1}\n[CQ:face,id=171] 地区：{2}\n[CQ:face,id=171] LOL：{3}\n[CQ:face,id=171] 微博：{4}'.format(data.get('qq'), data.get('mobile'), data.get('place'), data.get('lol'), data.get('wb'))
    go.send(meta_data, message)

def listPlugins(meta_data):
    message = '小猪比机器人-插件列表'
    for i in go.pluginsList:
        message += '\n[CQ:face,id=161] 插件名称：'+str(i)
    message += '\n\n所有插件均原创插件'
    go.send(meta_data, message)

def dui(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    message1 = message.split(' ')
    userid = go.getCQValue('qq', message1[0])
    cishu = int(message1[1])
    jiangetime = int(message1[2])
    while cishu > 0:
        dataa = requests.get(url=meta_data.get('botSettings').get('duiapi'))
        dataa.enconding = "utf-8"
        go.send(meta_data, '[CQ:at,qq='+str(userid)+']'+str(dataa.text))
        time.sleep(jiangetime+random.uniform(0, 2))
        
        cishu -= 1


def whoonline(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    dataa = requests.get(url=meta_data.get('botSettings').get('httpurl')+'/get_online_clients')
    datajson = dataa.json()
    go.send(meta_data, datajson)

def chuo(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    message1 = go.getCQValue('qq', message)
    go.send(meta_data, '[CQ:poke,qq='+message1+']')
    
def zhuan(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    go.send(meta_data, "[CQ:tts,text="+str(message)+"]")
        
def echo(meta_data):
    go.send(meta_data, meta_data.get('message'))

def haoyoufa(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    dataa = requests.get(url=meta_data.get('botSettings').get('httpurl')+'/get_friend_list')
    datajson = dataa.json()
    sum = 0
    for i in datajson.get('data'):
        if i.get('user_id') == 66600000:
            CrashReport(meta_data.get('uuid'), '沙雕babyQ！预祝腾讯好死！', '友发')
            continue
        go.send(meta_data, message)
        go.send(meta_data, '好友 '+str(i.get('nickname'))+' 发送完毕')
        sum += 1
    go.send(meta_data, '发送完毕，总好友数：'+str(sum))

def qunfa(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    # 同步公告到数据库
    formatmsg = message.replace('\n', '<br>')
    postdata = {"content":formatmsg}
    requests.post('https://qb.xzy.center/savenotice', data=postdata)
    
    dataa = requests.get(url=meta_data.get('botSettings').get('httpurl')+'/get_group_list')
    datajson = dataa.json()
    sum = 0
    for i in datajson.get('data'):
        go.SendOld(meta_data.get('uuid'), uid, message, i.get('group_id'))
        go.send(meta_data, '群聊 '+str(i.get('group_name'))+' 发送完毕')
        time.sleep(1)
        sum += 1
    go.send(meta_data, '发送完毕，总群聊数：'+str(sum))

def cqcode(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    print('init cqcode')
    message1 = message.split(' ')
    message = '[CQ:'+str(message1[0])
    for i in message1:
        if '=' in i:
            message += ','+i
        else:
            continue
    message += ']'
    go.send(meta_data, message)

def md5(meta_data):
    message = meta_data.get('message')
    go.send(meta_data, 'MD5加密结果：'+str(hashlib.md5(message.encode(encoding='UTF-8')).hexdigest()))

def mysqlselect(meta_data):
    message = meta_data.get('message')
    go.send(meta_data, go.selectx(message))
    
def mysqlgo(meta_data):
    message = meta_data.get('message')
    go.commonx(message)
    go.send(meta_data, '[CQ:face,id=161] 执行完毕！')

def twbw(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    go.send(meta_data, '玩命翻译中...')
    message1 = '翻译结果：'
    for i in message:
        message1 += go.translator(i)+' '
    go.send(meta_data, message1)
    
def baiduSearch(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    go.send(meta_data, '[CQ:face,id=189] 开始搜索...')
    message = message.lstrip().rstrip().replace(' ', '%20')
    
    meta_data['message'] = 'https://baidu.com/s?word='+str(message)+' 1 baiduSearch.png'
    getWP(meta_data)

def getWP(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    if ('pornhub' in message) or ('pronhub' in message) or ('pixiv' in message):
        go.send(meta_data, '不可以涩涩哦~')
    else:
        if message[0:7] == "http://" or message[0:8] == "https://":
            print('x2')
            go.send(meta_data, '玩命截图中...')
            
            waittime = 1
            url = message
            if ' ' in message:
                message1 = message.split(' ')
                url = message1[0]
                waittime = message1[1]
                filename = message[2]
            else:
                filename1 = parse.urlparse(str(message))
                filename = filename1[1] + '.png'
            
            options=webdriver.ChromeOptions()
            # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
            options.add_argument('--headless')
            # 谷歌文档提到需要加上这个属性来规避bug
            options.add_argument('--disable-gpu')
            # 取消沙盒模式
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # 指定浏览器分辨率
            options.add_argument('window-size=1920x1080')
            driver=webdriver.Chrome(options=options)
            #网页地址
            driver.get(str(url))
            #等待2秒再截图，如果网页渲染的慢截图的内容会有问题
            go.send(meta_data, '等待加载时间：'+str(waittime)+'秒')
            time.sleep(int(waittime))
            #截图
            driver.get_screenshot_as_file('/www/wwwroot/xzydwz/qqbot/websitepic/'+str(filename))
            #退出
            driver.close()
            
            go.send(meta_data, "[CQ:image,cache=0,url=https://xzy.xzy.center/qqbot/websitepic/"+str(filename)+",file=https://xzy.xzy.center/qqbot/websitepic/"+str(filename)+"] 以上图片内容与本机器人无关，本机器人只提供截图服务！")
        else:
            go.send(meta_data, '[CQ:face,id=151] 请使用正确的协议头！')
            
def renpin(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    rnd = random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(uid))
    lucknum = rnd.randint(1,100)
    go.send(meta_data, '[CQ:at,qq='+str(uid)+'] 您的今日人品为：'+str(lucknum))

def QuiteGroup(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    go.send(meta_data, '机器人即将退群！')
    data = requests.get(url=meta_data.get('botSettings').get('httpurl')+'/set_group_leave?group_id={0}'.format(gid))

def TurnOffBot(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    sql = 'UPDATE `botSettings` SET `power`=0 WHERE `qn`='+str(gid)
    go.commonx(sql)
    go.send(meta_data, '用户 [CQ:at,qq='+str(uid)+'] 关闭了机器人\n再见了呜呜呜，希望机器人的下一次开机~')
    tools.loadConfig(meta_data)

def getHeadImage(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    message1 = go.getCQValue('qq', message)
    data = requests.get(meta_data.get('botSettings').get('headImageApi').format(message1))
    dataa = data.json()
    imgurl = dataa.get('data').get('imgurl2')
    name = str(dataa.get('data').get('name'))
    
    go.send(meta_data, '用户 '+message+' 的头像为\n[CQ:image,cache=0,url='+imgurl+',file='+imgurl+']')

def xinshou(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    message = '[CQ:face,id=189] 小猪比机器人-新手教学\n\n[CQ:face,id=151] 综述：\n猪比现已有了50多个指令，总共60多项功能，有关键词回复、违禁词、防刷屏、网页截图、同步服务器消息等等。\n猪比现在还在进一步开发中，可能有时候会暂停运行或者不稳定，那就是我正在开发。\n机器人分为主人和副主人，副主人出售，同时对本机器人宣传等各方面有贡献的可以获得相应的奖励qwq\n\n[CQ:face,id=151] 使用教程：\n发送“菜单”可以查看指令，使用“指令帮助”指令可以查看指令的帮助信息。使用指令时要注意：\n    一、指令列表中的<>与[]分别代表必须的项目和可选的，使用时不需要带有该符号！\n    二、请注意空格的个数！\n\n除了菜单中的指令，机器人还有违禁词检测、防刷屏、入群欢迎、出群提醒等各种功能，发送“设置列表”可以查看这些功能的配置。\n使用set指令时请注意，===前的内容是项目名，例如 “防撤回 recallFlag：1” ，那么这时，就应该写成 “set recallFlag===值\n\n[CQ:face,id=151] 最后\n如果您还有不会的地方或者是改进意见，请联系我的主人：'+str(go.yamldata.get('chat').get('owner'))
    go.send(meta_data, message)
    
def yunshi(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    cid = meta_data.get('se').get('channel_id')
    
    if cid != None:
        strr = 'cid'
        sqlstr = '`cid`="{0}"'.format(uid)
    else:
        strr = 'qn'
        sqlstr = '`qn`={0}'.format(uid)
    ob = meta_data.get('userInfo')
    
    if ob==404:
        return go.send(meta_data, '请先发送“注册”，注册后再测运势')
    
    if ob.get('zong') == '' or ob.get('shiye') == 0 or ob.get('taohua') == 0 or ob.get('cai') == 0:
        go.send(meta_data, '[CQ:face,id=151] 祈祷中...')
        shiye = random.randint(1, 100)
        taohua = random.randint(1, 100)
        cai = random.randint(1, 100)
        zong = random.randint(0, 4)
        zongarr = ['大凶','小凶','凶带吉','吉带凶','小吉','大吉']
        zongstr = zongarr[zong]
        sql = 'UPDATE `botCoin` SET `zong`="{0}",`shiye`={1},`taohua`={2},`cai`={3} WHERE {4}'.format(zongstr, shiye, taohua, cai, sqlstr)
        go.commonx(sql)
        tools.loadConfig(meta_data)
        
        go.send(meta_data, '[CQ:face,id=151] [CQ:at,qq='+str(uid)+']您的运势：\n桃花运：'+str(taohua)+'\n事业运：'+str(shiye)+'\n财运：'+str(cai)+'\n运势：'+zongstr)
    else:
        shiye = ob.get('shiye')
        taohua = ob.get('taohua')
        cai = ob.get('cai')
        zongstr = ob.get('zong')
        
        go.send(meta_data, '[CQ:face,id=151] [CQ:at,qq='+str(uid)+']\n你今天已经测过运势了喵~\n命运是不可以改变的喵~\n\>w</\n桃花运：'+str(taohua)+'\n事业运：'+str(shiye)+'\n财运：'+str(cai)+'\n运势：'+zongstr)
        
def jiami(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    artext = go.googletrans.translate(message, dest='ar').text
    amtext = go.googletrans.translate(artext, dest='am').text
    fin = go.googletrans.translate(amtext, dest='az').text
    go.send(meta_data, '[CQ:face,id=161] 加密成功：'+str(fin))
    
def shengchenghonglian(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    go.send(meta_data, '正在努力生成...')
    
    meta_data['message'] = 'https://c.pc.qq.com/middlem.html?pfurl='+str(message)+'&pfuin=2417481092&pfto=qq.msg&type=0&gjlevel=15&gjsublevel=2804&iscontinue=0&ADUIN=2417481092&ADSESSION=1649083748&ADTAG=CLIENT.QQ.5887_AIO.0&ADPUBNO=27211 1 shengchenghonglian.png'
    getWP(meta_data)