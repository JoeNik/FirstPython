from bs4 import BeautifulSoup
from urllib import request
import wx, json
import requests
import time
from http import cookiejar  # 保存cookie用的
from urllib import parse  # 转译
import urllib.request  # 请求库
import execjs,js2py

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Content-Type': 'application/json'}

cookiestrHead = r'ki1e_2132_saltkey=lsBSSV39; ki1e_2132_lastvisit=1559725160; ki1e_2132_auth=c705jfbJcHk%2B3iB3qmrPG1BrW5ijmJ6TRrgoHFm3EvazA85CtaRR%2BPp9LAoFz0Gr11Bm9hCt8iXL0eErm8Kyb9OcApg; ki1e_2132_connect_is_bind=1; ki1e_2132_smile=1D1; ki1e_2132_pc_size_c=0; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1559780847,1559810342,1559810796,1560127058; ki1e_2132_creditnotice=0D0D0D0D0D0D0D0D0D538097; ki1e_2132_creditbase=0D1303D0D0D0D0D0D0D0; ki1e_2132_clearUserdata=forum; ki1e_2132_connect_not_sync_t=1; ki1e_2132_creditrule=%E5%8F%91%E8%A1%A8%E5%9B%9E%E5%A4%8D; td_cookie=18446744071559493794; timestamp=1560130076000; sign=4CBD74A5DD4643A9A56601CC25825DB4; ki1e_2132_nofocus_forum=1; ki1e_2132_atarget=1; ki1e_2132_forum_lastvisit=D_26_1560131402; ki1e_2132_ulastactivity=1560132614%7C0; ki1e_2132_checkpm=1; ki1e_2132_sendmail=1; ki1e_2132_lastcheckfeed=538097%7C1560132615; ki1e_2132_checkfollow=1; ki1e_2132_noticeTitle=1; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1560132616; amvid=c3faf2181a26daf6a98851670ae53153; ki1e_2132_lastact=1560132619%09forum.php%09viewthread; ki1e_2132_viewid=tid_6113962'
DingPost_url = "https://oapi.dingtalk.com/robot/send?access_token=b63c5a144e9102029af7ef052c20150503441101f54dbb1c81a47285d56105d9"


# key 13位UNIX时间 data 密码
def get_des_psswd(data, key):
    try:
        jsstr = get_js()
        ctx = execjs.compile(jsstr)  # 加载JS文件
        return (ctx.call('do_encrypt_rc4', data, key))  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数
       #return execjs.compile(open(r"E:\\bReadyWorking\\gothonweb\\bin\\loginCheck.js").read().decode("utf-8")).call('do_encrypt_rc4', data,key)
    except Exception as e:
        print('GetDingMarkDown error:' + str(e))

def js2pyTest(src,key):
    try:
        data = open('E:\\bReadyWorking\\gothonweb\\bin\\loginCheck.js', 'r', encoding='utf8').read()

        print(type(data))

        data = js2py.eval_js(data)

        print(data(src, key))
    except Exception as e:
        print('js2pyTest error:' + str(e))



def get_js():
    try:
        f = open("E:\\bReadyWorking\\gothonweb\\bin\\loginCheck.js", 'r', encoding='utf-8')  # 打开JS文件
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr
    except Exception as e:
        print('GetDingMarkDown error:' + str(e))


#current_milli_time = lambda: int(round(time.time() * 1000))
millis = int(round(time.time() * 1000))
psw = js2pyTest("123456", millis)

# 1.代码登录
# 1.1 登录的网址
login_url = "http://191.168.4.1/ac_portal/disclaimer/pc.html?template=disclaimer&tabs=pwd&vlanid=0&_ID_=0&switch_url=&url=https://hao.360.com/?wd_xp1&controller_type=&mac=00-00-00-00-00-00"
login_form_data = {
    "opr": "pwdLogin",
    "userName": "郑乔",
    "pwd": "ee772406c049",
    "auth_tag": "1576831030768",
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


def get_contents(chapter):
    req = request.Request(chapter)
    # 设置cookie
    req.add_header('cookie', cookiestrHead)
    # 设置请求头
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')

    resp = request.urlopen(req)

    rlt = resp.read().decode('gbk')
    soup = BeautifulSoup(rlt, 'html.parser')

    # req = requests.get(url=chapter)
    # html = req.content
    # print('xx:')
    # html_doc = str(html, 'gbk')
    # soup = BeautifulSoup(html_doc, 'html.parser')

    # a = soup.find('div', id='wp')
    a = soup.find_all('table')
    # print(a)
    # write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log.txt", str(a), 'utf8')
    # print(chardet.detect(html))
    for each in a:
        try:
            b = each.find('center')
            # print('xxx:' + str(b))
            if b != None:
                x = b.string
                if x <= '最新交流消息':
                    c = each.select('tr')
                    # print(each)
                    # write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log.txt", str(each), 'utf8')
                    print(1 + len(c))
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
                                    print(remark)
                                else:
                                    (remark, comments) = get_onpage(w.get('href'), cookiestrHead)
                                    for key in keyword:
                                        if ftitleTemp.find(key) != -1:
                                            print("匹配:" + key)
                                            if not frame.isExist(ftitleTemp):
                                                frame.insert1(ftitleTemp, w.get('href'), remark, comments)
                                                p = ShowPopView("新消息来了", ftitleTemp)

                                # write_db(ftitleTemp, w.get('href'), remark, comments)
                                # for key in keyword:
                                #     if ftitleTemp.find(key) != -1:
                                #         weSend(1, 'JoeNik', remark + ' ' + w.get('href'))
                                # id = getInsertId()

                            # print(ftitleTemp)
                            # print(w.get('href'))
                            # print('\r\n')

                    # write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log1.txt", str(g), 'utf8')
                    # print(e)
                    # if d.string <= '赚客大家谈':
                    #     e = d.get('href')
                    #     print(d.get('title'))
                    # write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log1.txt", str(e), 'utf8')

        except Exception as e:
            print('error:' + str(e))


def get_onpage(chapter, cookiesStr):
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
            print(title)
            print('session 过期，请重新获取')
            wx.MessageBox("error", 'session 过期，请重新获取', wx.YES_NO)
            return ''
        else:
            # content1 = soup.find('td', class_='t_f').text
            comments = soup.find_all('td', 't_f')
            cnt = 0
            remarks = ''
            commentsStr = []
            for comment in comments:
                if cnt == 0:
                    remarks = comment.text
                    mbn = comment.find("img", class_="zoom")
                    mbn2 = mbn['file']
                else:
                    commentsStr.append(comment.text)
                cnt = cnt + 1
                # print(comment.text)
            return (remarks, '|'.join(commentsStr))
            # print(content1)
    except Exception as e:
        print('error:' + str(e))


get_onpage("http://www.zuanke8.com/thread-6702621-1-1.html", cookiestrHead)


def DingDingPost(title, content, picUrl, comments):
    try:
        # 消息头部
        headers = {'Content-Type': 'application/json'}

        if not picUrl.strip():
            content = "标题:" + title + '\n' + '*' * (len(title) + 6) + '\n' + "内容：" + content + '\n' + '*' * (
                    len(title) + 6) + '\n' + "评论:" + comments
            # 消息主体
            data = {
                "msgtype": "text",
                "text": {"content": content, }
            }
        else:
            url = "http://www.baidu.com"
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": "### **" + title + "** #### " + content + "\n ![图片]" + "(" + picUrl + ")\n **评论：**" + " ####  " + comments + "\n \n [这是一个地址，点此前往]" + "(" + url + ") \n"
                }
            }
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": "test",
                    "text": "### **test** "
                            + "> #### 内容测试\n "
                            + "> ![图片](https://p0.ssl.qhimg.com/t0170483da9aa036e6c.png)\n"
                            + "> **评论：** ####  评论测试\n \n "
                            + "> [这是一个地址，点此前往](www.baidu.com) \n"
                }
            }
            # data ={
            #     "msgtype": "markdown",
            #     "markdown": {
            #         "title": "杭州天气",
            #         "text": "#### 杭州天气 @156xxxx8827\n" +
            #                 "> 9度，西北风1级，空气良89，相对温度73%\n\n" +
            #                 "> ![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png)\n" +
            #                 "> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n"
            #     },
            #     "at": {
            #         "atMobiles": [
            #             "156xxxx8827",
            #             "189xxxx8325"
            #         ],
            #         "isAtAll": False
            #     }
            # }
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "首屏会话透出的展示内容",
                "text": "# " + title + " \n" + "## " + content + "  \n" + "* " + comments + " \n " + "![alt 啊](" + picUrl + ") \n" + "> ###### 10点20分发布 [天气](" + url + ") \n"
                        + "# " + title + "2 \n" + "### " + content + "2  \n" + "* " + comments + " \n " + "![alt 啊](" + picUrl + ") \n" + "> ###### 10点20分发布 [天气](" + url + ") \n"
            }
        }

        # 使用post请求推送消息
        requests.post(DingPost_url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print('DingDingPost error:' + str(e))


def DingPostMarkDown(title, textLst):
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
            requests.post(DingPost_url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print('GetDingMarkDown error:' + str(e))


def GetDingMarkDownText(title, content, comments, messageURL, picURL):
    try:
        timeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        text = "# " + title + " \n" + "## " + content + "  \n" + "* " + comments + " \n " + "![alt 啊](" + picURL + ") \n" + "> ###### " + timeStr + "获取 [原文](" + messageURL + ") \n"
        return text
    except Exception as e:
        print('GetDingMarkDownText error:' + str(e))
    return ""


def GetDingFcardLinks(title, messageURL, picURL):
    dic = {"title": title, "messageURL": messageURL, "picURL": picURL}
    return dic


def DingPostFcard(links):
    data1 = {"feedCard": {"links": links}, "msgtype": "feedCard"}
    # 使用post请求推送消息
    x = requests.post(DingPost_url, data=json.dumps(data1), headers=headers)
    print("post rlt:" + x.text)


def DingPostTest():
    data = {
        "feedCard": {
            "links": [
                {
                    "title": "时代的火车向前开",
                    "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                    "picURL": "https://www.dingtalk.com/"
                },
                {
                    "title": "时代的火车向前开2",
                    "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                    "picURL": "https://www.dingtalk.com/"
                }
            ]
        },
        "msgtype": "feedCard"
    }

    links = []
    dic1 = {"title": "时代的火车向前开",
            "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
            "picURL": "https://www.dingtalk.com/"}
    dic2 = {"title": "时代的火车向前开2",
            "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
            "picURL": "https://www.dingtalk.com/"}
    links.append(dic1)
    links.append(dic2)
    data1 = {"feedCard": {"links": links}, "msgtype": "feedCard"}

    # 使用post请求推送消息
    # x = requests.post(DingPost_url, data=json.dumps(data1), headers=headers)
    # print("post rlt:" + x.text)


# DingDingPost("大标题", "内容测试", "https://p0.ssl.qhimg.com/t0170483da9aa036e6c.png", "评论测试")
# DingPostTest()
text = GetDingMarkDownText("测试标题1", "这是一本正经的内容", "这是一条很长的评论", "http://www.baidu.com",
                           "https://p0.ssl.qhimg.com/t0170483da9aa036e6c.png")
text2 = GetDingMarkDownText("测试标题2222222222222222222", "这是一本正经的内容22222222222", "这是一条很长的评论22222222222222",
                            "http://www.baidu.com", "https://p0.ssl.qhimg.com/t0170483da9aa036e6c.png")
text3 = text + text2
DingPostMarkDown("新消息来了", text3)
