import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import datetime
import json
import threading
import urllib
from http import cookiejar

import execjs, os
import requests
from bs4 import BeautifulSoup
import time, logUntil, Config
from urllib import request, parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Content-Type': 'application/json'}

server = 'http://www.zuanke8.com/zuixin.php'

#  dingding请求地址
DingPost_url = "https://oapi.dingtalk.com/robot/send?access_token=b63c5a144e9102029af7ef052c20150503441101f54dbb1c81a47285d56105d9"
cookiestrHead = r'ki1e_2132_connect_is_bind=1; ki1e_2132_smile=1D1; ki1e_2132_atlist=179919%2C730672%2C891213%2C69238%2C4%2C18%2C3; __gads=Test; ki1e_2132_atarget=1; ki1e_2132_saltkey=BOFHWJus; ki1e_2132_lastvisit=1575848667; ki1e_2132_auth=7ec3SUJXMYbXjWIBi%2BWbubChIaBTk%2Fqh0tZrX33i%2F5yx5y6HNY0HfW7Zlo%2Bf936GbiBteSs6cAoPLkFDHAa4wd8TjFQ; ki1e_2132_pc_size_c=0; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1576199433,1576456388,1576542119,1576630816; timestamp=1576636591000; sign=DB3D4C55FA5ACF1ECCEB850D3C7C7543; td_cookie=30223767; ki1e_2132_lastviewtime=538097%7C1576649069; ki1e_2132_nofocus_forum=1; ki1e_2132_clearUserdata=forum; ki1e_2132_creditnotice=0D0D0D0D0D0D0D0D0D538097; ki1e_2132_creditbase=0D1639D0D0D0D0D0D0D0; ki1e_2132_creditrule=%E5%8F%91%E8%A1%A8%E5%9B%9E%E5%A4%8D; ki1e_2132_connect_not_sync_t=1; ki1e_2132_connect_not_sync_feed=1; ki1e_2132_forum_lastvisit=D_19_1573625063D_25_1576137386D_22_1576137419D_26_1576648030D_11_1576654048; ki1e_2132_ulastactivity=1576660463%7C0; ki1e_2132_dismobilemessage=1; ki1e_2132_mobile=no; ki1e_2132_checkpm=1; ki1e_2132_sendmail=1; ki1e_2132_lastcheckfeed=538097%7C1576660554; ki1e_2132_checkfollow=1; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1576660556; amvid=f7dbb54ebd542d284d740bc3176fec0d; ki1e_2132_lastact=1576660558%09forum.php%09viewthread; ki1e_2132_viewid=tid_6699009'

keyword = ['速度', 'bug', '快', '水', '有了', '好价', '赶紧', '作业', '速撸', '撒果', '首发', '平行', '神价', '线报', '爱奇艺', '好莱坞', '周卡', '月卡',
           '可以', '冲', '招行抽奖']

cfg = Config.ReadConfig()

# 推送到钉钉
isPostToDing = int(cfg.get_val("system", "isPostToDing", "1"))
DingPost_url = cfg.get_val("system", "DingPost_url",
                           "https://oapi.dingtalk.com/robot/send?access_token=b63c5a144e9102029af7ef052c20150503441101f54dbb1c81a47285d56105d9")

curPath = os.getcwd()
if os.path.exists(curPath + "cookies.txt"):
    f = open(curPath + '\\cookies.txt')
    cookiestrHead = f.read()
    f.close()
else:
    f = open(curPath + '\\cookies.txt', 'w')
    f.write(
        r'ki1e_2132_connect_is_bind=1; ki1e_2132_smile=1D1; ki1e_2132_atlist=179919%2C730672%2C891213%2C69238%2C4%2C18%2C3; __gads=Test; ki1e_2132_atarget=1; ki1e_2132_saltkey=BOFHWJus; ki1e_2132_lastvisit=1575848667; ki1e_2132_auth=7ec3SUJXMYbXjWIBi%2BWbubChIaBTk%2Fqh0tZrX33i%2F5yx5y6HNY0HfW7Zlo%2Bf936GbiBteSs6cAoPLkFDHAa4wd8TjFQ; ki1e_2132_pc_size_c=0; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1576199433,1576456388,1576542119,1576630816; timestamp=1576636591000; sign=DB3D4C55FA5ACF1ECCEB850D3C7C7543; td_cookie=30223767; ki1e_2132_lastviewtime=538097%7C1576649069; ki1e_2132_nofocus_forum=1; ki1e_2132_clearUserdata=forum; ki1e_2132_creditnotice=0D0D0D0D0D0D0D0D0D538097; ki1e_2132_creditbase=0D1639D0D0D0D0D0D0D0; ki1e_2132_creditrule=%E5%8F%91%E8%A1%A8%E5%9B%9E%E5%A4%8D; ki1e_2132_connect_not_sync_t=1; ki1e_2132_connect_not_sync_feed=1; ki1e_2132_forum_lastvisit=D_19_1573625063D_25_1576137386D_22_1576137419D_26_1576648030D_11_1576654048; ki1e_2132_ulastactivity=1576660463%7C0; ki1e_2132_dismobilemessage=1; ki1e_2132_mobile=no; ki1e_2132_checkpm=1; ki1e_2132_sendmail=1; ki1e_2132_lastcheckfeed=538097%7C1576660554; ki1e_2132_checkfollow=1; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1576660556; amvid=f7dbb54ebd542d284d740bc3176fec0d; ki1e_2132_lastact=1576660558%09forum.php%09viewthread; ki1e_2132_viewid=tid_6699009')
    f = f.close()
    f = open(curPath + '\\cookies.txt')
    cookiestrHead = f.read()
    f.close()

keywordStr = cfg.get_val("system", "keyword", "速度,bug,快,水,有了,好价,赶紧,作业,速撸,撒果,首发,平行,神价,线报,爱奇艺,好莱坞,周卡,月卡,可以,冲,招行抽奖,教程")
keyword = keywordStr.split(',')
lstExistArg = []
lstErrorArg = []  # 已删除获取权限过高的帖子集合

log = logUntil.logs()

# 失败次数统计
global failReqCnt

JSCode = r'''
                function do_encrypt_rc4(src, passwd) {
                    passwd = passwd + '';
                    var i, j = 0, a = 0, b = 0, c = 0, temp;
                    var plen = passwd.length,
                        size = src.length;

                    var key = Array(256); //int
                    var sbox = Array(256); //int
                    var output = Array(size); //code of data
                    for (i = 0; i < 256; i++) {
                        key[i] = passwd.charCodeAt(i % plen);
                        sbox[i] = i;
                    }
                    for (i = 0; i < 256; i++) {
                        j = (j + sbox[i] + key[i]) % 256;
                        temp = sbox[i];
                        sbox[i] = sbox[j];
                        sbox[j] = temp;
                    }
                    for (i = 0; i < size; i++) {
                        a = (a + 1) % 256;
                        b = (b + sbox[a]) % 256;
                        temp = sbox[a];
                        sbox[a] = sbox[b];
                        sbox[b] = temp;
                        c = (sbox[a] + sbox[b]) % 256;
                        temp = src.charCodeAt(i) ^ sbox[c];//String.fromCharCode(src.charCodeAt(i) ^ sbox[c]);
                        temp = temp.toString(16);
                        if (temp.length === 1) {
                            temp = '0' + temp;
                        } else if (temp.length === 0) {
                            temp = '00';
                        }
                        output[i] = temp;
                    }
                    return output.join('');
                }
    '''


class PythonService(win32serviceutil.ServiceFramework):
    # 服务名
    _svc_name_ = "getzk"
    # 服务显示名称
    _svc_display_name_ = "getzk"
    # 服务描述
    _svc_description_ = "getzk  Is Exist License windows"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.run = True

    def isExistLst(self, value):
        try:
            log.info("已推送帖个数:" + str(len(lstExistArg)))
            # 帖子大于30就把前10条清空
            if len(lstExistArg) > 30:
                del lstExistArg[0:10]
            lstExistArgSet = set(lstExistArg)
            if value in lstExistArgSet:
                return True
            else:
                lstExistArg.append(value)
                return False
        except Exception as e:
            log.error('isExistLst error:' + str(e))

    def isExistErrorLst(self, value):
        try:
            log.info("权限帖个数:" + str(len(lstErrorArg)))
            lstErrorArgSet = set(lstErrorArg)
            if len(lstErrorArg) > 20:
                del lstErrorArg[0:1]
            if value in lstErrorArgSet:
                return True
            else:
                # lstErrorArg.append(value)
                return False
        except Exception as e:
            log.error('isExistErrorLst error:' + str(e))

    def get_contents(self, chapter):
        sucFlag = 0
        try:
            req = request.Request(chapter)
            # 设置cookie
            req.add_header('cookie', cookiestrHead)
            # 设置请求头
            req.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')

            resp = request.urlopen(req)

            rlt = resp.read().decode('gbk', 'ignore').encode('utf-8')
            soup = BeautifulSoup(rlt, 'html.parser')
            a = soup.find_all('table')
            ArgLst = []  # 文章信息列表
            firstArgTitle = ""
            for each in a:
                sucFlag = 1
                try:
                    b = each.find('center')
                    # print('xxx:' + str(b))
                    if b != None:
                        x = b.string
                        if x <= '最新交流消息':
                            c = each.select('tr')
                            # print(each)
                            # write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log.txt", str(each), 'utf8')
                            log.info(1 + len(c))
                            for d in c:
                                e = d.find_all('th')
                                for f in e:
                                    g = f.find_all('a')
                                    iscontinue = False
                                    remark = ''
                                    for w in g:
                                        if (iscontinue):
                                            iscontinue = False
                                            continue
                                        ftitleTemp = w.string
                                        ftitle = w.string.replace('\n', '').encode('gbk')
                                        # print(ftitleTemp)
                                        # print('赚品交换'.encode('gbk'))
                                        # print(ftitle)
                                        fdic = ['赚品交换'.encode('gbk'), '果果换物'.encode('gbk'), '做任务赚果果'.encode('gbk'),
                                                '邀请专区'.encode('gbk')]

                                        if (ftitle in fdic):
                                            # if (ftitle == '赚品交换'.encode('gbk') or ftitle == '果果换物'.encode('gbk') or ftitle == '做任务赚果果'.encode('gbk')):
                                            iscontinue = True
                                            continue
                                        if (ftitle == '赚客大家谈'.encode('gbk') or ftitle == '活动线报'.encode(
                                                'gbk') or ftitle == '活动秘籍'.encode('gbk') or ftitle == '求助咨询区'.encode(
                                            'gbk')):
                                            remark = ftitleTemp
                                            # print(remark)
                                        else:
                                            argUrl = w.get('href')
                                            if not self.isExistErrorLst(argUrl):
                                                for key in keyword:
                                                    if ftitleTemp.find(key) != -1:
                                                        log.info("匹配:" + key)
                                                        if not self.isExistLst(ftitleTemp):
                                                            if isPostToDing == 1:
                                                                (remark, comments, picurl) = self.get_onpage(argUrl,
                                                                                                             cookiestrHead)
                                                                if len(ArgLst) == 0:
                                                                    firstArgTitle = ftitleTemp
                                                                log.info("send " + ftitleTemp)
                                                                ArgLst.append(
                                                                    self.GetDingMarkDownText(
                                                                        str(len(ArgLst) + 1) + ":" + ftitleTemp, remark,
                                                                        comments,
                                                                        argUrl, picurl))


                except Exception as e:
                    log.error('get_contents error1:' + str(e))
            if len(ArgLst) > 0:
                self.DingPostMarkDown(firstArgTitle, ArgLst)
            return sucFlag
        except Exception as e:
            log.error('get_contents error:' + str(e))
            return sucFlag

    def get_onpage(self, chapter, cookiesStr):
        try:
            req = request.Request(chapter)
            # 设置cookie
            req.add_header('cookie', cookiestrHead)
            # 设置请求头
            req.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')

            resp = request.urlopen(req)

            rlt = resp.read().decode('gbk')
            soup = BeautifulSoup(rlt, 'html.parser')

            title = soup.find('head').find('title').text
            # write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log2.html", str(soup), 'gbk')
            # content1 = soup.find('td', class_='t_f').text
            if (title == '提示信息 -  赚客吧'):
                log.info(title)
                log.info('session 过期或 权限不足，请重新获取')
                # wx.MessageBox("error", 'session 过期，请重新获取', wx.YES_NO)
                if not self.isExistErrorLst(chapter):
                    lstErrorArg.append(chapter)
                return ''
            else:
                # content1 = soup.find('td', class_='t_f').text
                comments = soup.find_all('td', 't_f')
                cnt = 0
                remarks = ''
                picUrl = ''
                commentsStr = []
                for comment in comments:
                    if cnt == 0:
                        remarks = comment.text
                        mbn = comment.find("img", class_="zoom")
                        if not mbn == None:
                            picUrl = mbn['file']
                    else:
                        commentsStr.append(comment.text)
                    cnt = cnt + 1
                    # print(comment.text)
                return (remarks, '|'.join(commentsStr), picUrl)
                # print(content1)
        except Exception as e:
            log.error('get_onpage error:' + str(e))

    def DingDingPost(self, title, content, picUrl, comments, argUrl):
        try:
            # 消息头部
            headers = {'Content-Type': 'application/json'}
            if not picUrl.strip():
                content = "标题:" + title + '\n' + '*' * (len(title) + 6) + '\n' + "内容：" + content + '\n' + '*' * (
                        len(title) + 6) + '\n' + "评论:" + comments + '\n' + '*' * (len(title) + 6) + "\n 帖子地址:" + argUrl
                # 消息主体
                data = {
                    "msgtype": "text",
                    "text": {"content": content, }
                }
            else:
                data = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": title,
                        "text": "内容：" + content + "\n ![图片]" + "(" + picUrl + ")\n 评论：" + comments + "\n \n 帖子地址:" + argUrl
                    }
                }

            # 使用post请求推送消息
            requests.post(DingPost_url, data=json.dumps(data), headers=headers)
        except Exception as e:
            log.error('DingDingPost error:' + str(e))

    def DingPostMarkDown(self, title, textLst):
        try:
            text = ""
            for i in textLst:
                text += i
            if len(text) > 0:
                data = {
                    "msgtype": "markdown",
                    "markdown": {
                        "title": title,
                        "text": text
                    }
                }
                # 使用post请求推送消息
                x = requests.post(DingPost_url, data=json.dumps(data), headers=headers)
                log.info("post rlt:" + x.text)
        except Exception as e:
            log.error('DingPostMarkDown error:' + str(e))

    def GetDingMarkDownText(self, title, content, comments, messageURL, picURL):
        try:
            timeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if len(picURL) == 0:
                text = "# " + title + " \n" + "### " + content + "  \n" + "* " + comments + " \n " + "> ###### " + str(
                    timeStr) + "获取 [原文](" + messageURL + ") \n \n \n"
            else:
                text = "# " + title + " \n" + "### " + content + "  \n" + "* " + comments + " \n " + "![screen](" + picURL + ") \n" + "> ###### " + str(
                    timeStr) + "获取 [原文](" + messageURL + ") \n \n \n"
            return text
        except Exception as e:
            log.error('GetDingMarkDownText error:' + str(e))
        return ""

    def GetDingFcardLinks(self, title, messageURL, picURL):
        dic = {"title": title, "messageURL": messageURL, "picURL": picURL}
        return dic

    def DingPostFcard(self, links):
        data1 = {"feedCard": {"links": links}, "msgtype": "feedCard"}
        # 使用post请求推送消息
        x = requests.post(DingPost_url, data=json.dumps(data1), headers=headers)
        log.info("post rlt:" + x.text)

    # key 13位UNIX时间 data 密码
    def get_des_psswd(self, data, key):
        try:
            CTX = execjs.compile(JSCode)
            return CTX.call('do_encrypt_rc4', data, key)
            # jsstr = get_js()
            # ctx = execjs.compile(jsstr)  # 加载JS文件
            # return (ctx.call('do_encrypt_rc4', data, key))  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数
        # return execjs.compile(open(r"E:\\bReadyWorking\\gothonweb\\bin\\loginCheck.js").read().decode("utf-8")).call('do_encrypt_rc4', data,key)
        except Exception as e:
            log.error('GetDingMarkDown error:' + str(e))

    def login(self):
        try:
            log.info("login ")
            millis = int(round(time.time() * 1000))
            # psw = js2pyTest("123456", millis)
            psw = self.get_des_psswd("123456", millis)
            # 1.代码登录
            # 1.1 登录的网址
            login_url = "http://191.168.4.1/ac_portal/login.php"
            login_form_data = {
                "opr": "pwdLogin",
                "userName": "翁兆炜",
                "pwd": psw,
                "auth_tag": millis,
                "rememberPwd": 0
            }
            # auth_tag 取到毫秒转化成Unix时间

            # 1.3 发送登录请求POST
            cook_jar = cookiejar.CookieJar()
            # 定义有添加 cook 功能的 处理器
            cook_hanlder = urllib.request.HTTPCookieProcessor(cook_jar)
            # 根据处理器 生成 opener
            opener = urllib.request.build_opener(cook_hanlder)

            # 带着参数 发送post请求
            # 添加请求头
            headers2 = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3650.400 QQBrowser/10.4.3341.400"}
            # 1 参数 将来 需要转译 转码； 2 post 请求的 data 要求是bytes
            login_str = parse.urlencode(login_form_data).encode('utf-8')
            login_request = urllib.request.Request(login_url, headers=headers2, data=login_str)
            # 如果登录成功，cookjar自动保存cookie
            opener.open(login_request)
            cookieStr = ''
            for item in cook_jar:
                cookieStr = cookieStr + item.name + '=' + item.value + ';'
            log.info("cookie:" + cookieStr)
        except Exception as e:
            log.info('login error:' + str(e))

    def loginThd(self):
        while True:
            try:
                # 范围时间
                d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '01:00', '%Y-%m-%d%H:%M')
                d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '01:03', '%Y-%m-%d%H:%M')

                # 当前时间
                n_time = datetime.datetime.now()

                # 判断当前时间是否在范围时间内
                if n_time > d_time and n_time < d_time1:
                    self.login()
            except Exception as e:
                log.error('loginThd error:' + str(e))
            time.sleep(100)

    def GetContentThd(self):
        failReqCnt = 0
        while True:
            try:
                log.info("*****************begin*********************")
                if self.get_contents(server) == 0:
                    failReqCnt = failReqCnt + 1
                else:
                    failReqCnt = 0
                if failReqCnt >= 400:
                    self.login()
                log.info(str(time.ctime()) + "  获取数据完毕")
            except Exception as e:
                log.error('main error:' + str(e))
            time.sleep(10)

    def SvcDoRun(self):
        '''服务启动后执行'''
        threading.Thread(target=self.loginThd, args=()).start()
        threading.Thread(target=self.GetContentThd, args=()).start()

        while self.run:
            try:
                log.info("*****************心跳维持*********************")
            except Exception as e:
                log.error('main error:' + str(e))
            time.sleep(60 * 60)

    def SvcStop(self):
        '''服务停止时执行'''
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False
        self._Log('stop')

    def _Log(self, str):
        with open('F:/helloServices.txt', 'a') as f:
            f.writelines('hello world' + str + '\n')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PythonService)
