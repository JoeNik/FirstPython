import _thread
import json
import threading
import time
import webbrowser
import win32gui

import requests
import win32con
import wx, os, win32api
import sys
import pyperclip
from urllib import request

from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

server = 'http://www.zuanke8.com/zuixin.php'
#  dingding请求地址
DingPost_url = "https://oapi.dingtalk.com/robot/send?access_token=b63c5a144e9102029af7ef052c20150503441101f54dbb1c81a47285d56105d9"
cookiestrHead = r'ki1e_2132_connect_is_bind=1; ki1e_2132_smile=1D1; ki1e_2132_atlist=179919%2C730672%2C891213%2C69238%2C4%2C18%2C3; __gads=Test; ki1e_2132_atarget=1; ki1e_2132_saltkey=BOFHWJus; ki1e_2132_lastvisit=1575848667; ki1e_2132_auth=7ec3SUJXMYbXjWIBi%2BWbubChIaBTk%2Fqh0tZrX33i%2F5yx5y6HNY0HfW7Zlo%2Bf936GbiBteSs6cAoPLkFDHAa4wd8TjFQ; ki1e_2132_pc_size_c=0; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1576199433,1576456388,1576542119,1576630816; timestamp=1576636591000; sign=DB3D4C55FA5ACF1ECCEB850D3C7C7543; td_cookie=30223767; ki1e_2132_lastviewtime=538097%7C1576649069; ki1e_2132_nofocus_forum=1; ki1e_2132_clearUserdata=forum; ki1e_2132_creditnotice=0D0D0D0D0D0D0D0D0D538097; ki1e_2132_creditbase=0D1639D0D0D0D0D0D0D0; ki1e_2132_creditrule=%E5%8F%91%E8%A1%A8%E5%9B%9E%E5%A4%8D; ki1e_2132_connect_not_sync_t=1; ki1e_2132_connect_not_sync_feed=1; ki1e_2132_forum_lastvisit=D_19_1573625063D_25_1576137386D_22_1576137419D_26_1576648030D_11_1576654048; ki1e_2132_ulastactivity=1576660463%7C0; ki1e_2132_dismobilemessage=1; ki1e_2132_mobile=no; ki1e_2132_checkpm=1; ki1e_2132_sendmail=1; ki1e_2132_lastcheckfeed=538097%7C1576660554; ki1e_2132_checkfollow=1; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1576660556; amvid=f7dbb54ebd542d284d740bc3176fec0d; ki1e_2132_lastact=1576660558%09forum.php%09viewthread; ki1e_2132_viewid=tid_6699009'
# packages = [('jessica alba', 'pomona', '1981'), ('sigourney weaver', 'new york', '1949'),
#             ('angelina jolie', 'los angeles', '1975'), ('natalie portman', 'jerusalem', '1981'),
#             ('rachel weiss', 'london', '1971'), ('scarlett johansson', 'new york', '1984')]
packages = [('jessica alba', 'pomona', '1981', 'test')]
# keyword = ['速度', 'bug', '快', '招行', '水', '有了', '好价', '赶紧', '作业', '速撸', '撒果', '首发', '平行', '神价', '线报', '爱奇艺', '周卡', '月卡',
#            '可以', '冲']
keyword = ['速度', 'bug', '快', '水', '有了', '好价', '赶紧', '作业', '速撸', '撒果', '首发', '平行', '神价', '线报', '爱奇艺', '周卡', '月卡',
           '可以', '冲']
# 推送到钉钉
isPostToDing = 1
# 窗口气泡弹出
isShowCapture = 0
global frame
global t


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, size):
        try:
            wx.Frame.__init__(self, parent, id, title, size)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self, -1)

            self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
            self.list.InsertColumn(0, 'title', width=140)
            self.list.InsertColumn(1, 'url', width=130)
            self.list.InsertColumn(2, 'content', width=150)
            self.list.InsertColumn(3, 'comments', width=150)
            self.list.InsertColumn(4, 'show pic', width=150)

            # for i in packages:
            #     index = self.list.InsertStringItem(0, i[0])
            #     self.list.SetStringItem(index, 1, i[1])
            #     self.list.SetStringItem(index, 2, i[2])
            #     self.list.SetStringItem(index, 3, i[3])
            # button = wx.Button(self.list, wx.ID_ANY, label="show")
            # self.list.SetItem(index, 4, button, -1)

            self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDclick)
            self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.Choose, self.list)

            hbox.Add(self.list, 1, wx.EXPAND)
            panel.SetSizer(hbox)

            self.Centre()

            x = self.list.ItemCount
        except Exception as e:
            print('error:' + str(e))

    def insert1(self, title, url, content, comments):
        # index = self.list.InsertStringItem(sys.maxsize, name)
        index = self.list.InsertStringItem(0, title)
        self.list.SetStringItem(index, 1, url)
        self.list.SetStringItem(index, 2, content)
        self.list.SetStringItem(index, 3, comments)
        # button = wx.Button(self, id=1, label="show")
        # self.list.SetItem(index, 4, button)

    def isExist(self, title):
        try:
            count = self.list.ItemCount
            for i in range(count):
                title1 = self.list.GetItem(i, 0)
                a = title1.Text
                if title.strip() == a.strip():
                    return True
        except Exception as e:
            print('error:' + str(e))

        return False

    def OnDclick(self, event):
        try:
            # wx.MessageBox("Double Cilcked", "Double cilck", wx.YES_NO)
            # webbrowser.open("http://www.baidu.com", new=0)
            ad_data = event.GetIndex()  # 获得被激活表项的索引号
            adTitle = self.list.GetItem(ad_data, 0).GetText()
            adUrl = self.list.GetItem(ad_data, 1).GetText()
            adContent = self.list.GetItem(ad_data, 2).GetText()
            adComments = self.list.GetItem(ad_data, 3).GetText()
            webbrowser.open(adUrl, new=0)
        except Exception as e:
            print('OnDclick error:' + str(e))
            wx.MessageBox("DoubleCilcked error", str(e), wx.YES_NO)

    def Choose(self, event):
        try:
            ad_data = event.GetIndex()  # 获得被激活表项的索引号
            adTitle = self.list.GetItem(ad_data, 0).GetText()
            adUrl = self.list.GetItem(ad_data, 1).GetText()
            adContent = self.list.GetItem(ad_data, 2).GetText()
            adComments = self.list.GetItem(ad_data, 3).GetText()
            cpStr = adTitle + "\r\n" + adUrl + "\r\n" + adContent
            pyperclip.copy(cpStr)
            t.showMsg("提示", "选中消息已复制")
        except Exception as e:
            print('OnDclick error:' + str(e))


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, id=-1, title="Monitor", size=(800, 600))
        frame.Show(True)
        self.SetTopWindow(frame)
        # frame.insert1("test", "testplace")
        while True:
            get_contents(server)
            print(str(time.ctime()) + "  获取数据完毕")
            time.sleep(10)
        return True


class TestTaskbarIcon:
    def __init__(self):
        # 注册一个窗口类
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbarDemo"
        wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy, }
        classAtom = win32gui.RegisterClass(wc)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom, "Taskbar Demo", style,
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        nid = (self.hwnd, 0, win32gui.NIF_ICON, win32con.WM_USER + 20, hicon, "Demo")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

    def showMsg(self, title, msg):
        # 原作者使用Shell_NotifyIconA方法代替包装后的Shell_NotifyIcon方法
        # 据称是不能win32gui structure, 我稀里糊涂搞出来了.
        # 具体对比原代码.
        nid = (self.hwnd,  # 句柄
               0,  # 托盘图标ID
               win32gui.NIF_INFO,  # 标识
               0,  # 回调消息ID
               0,  # 托盘图标句柄
               "TestMessage",  # 图标字符串
               msg,  # 气球提示字符串
               0,  # 提示的显示时间
               title,  # 提示标题
               win32gui.NIIF_INFO  # 提示用到的图标
               )
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.


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
                                    (remark, comments, picurl) = get_onpage(w.get('href'), cookiestrHead)
                                    for key in keyword:
                                        if ftitleTemp.find(key) != -1:
                                            print("匹配:" + key)
                                            if not frame.isExist(ftitleTemp):
                                                frame.insert1(ftitleTemp, w.get('href'), remark, comments)
                                                if isShowCapture == 1:
                                                    p = ShowPopView("新消息来了", ftitleTemp)
                                                if isPostToDing == 1:
                                                    DingDingPost(ftitleTemp, remark, picurl, comments, w.get('href'))

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
            # wx.MessageBox("error", 'session 过期，请重新获取', wx.YES_NO)
            t.showMsg("error", 'session 过期或 权限不足，请重新获取')
            return ''
        else:
            # content1 = soup.find('td', class_='t_f').text
            comments = soup.find_all('td', 't_f')
            cnt = 0
            remarks = ''
            commentsStr = []
            picUrl = ""
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
        print('get_onpage error:' + str(e))


def get_data(threadName, delay):
    while True:
        get_contents(server)
        print(str(time.ctime()) + "  获取数据完毕")
        time.sleep(10)


def hello(id, times):
    for i in range(times):
        print
        "hello %s time is %d\n" % (id, i)


def DingDingPost(title, content, picUrl, comments, argUrl):
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
        print('DingDingPost error:' + str(e))


def ShowPopView(title, content):
    t.showMsg(title, content)


if __name__ == '__main__':
    # app = MyApp()
    # app.MainLoop()
    t = TestTaskbarIcon()
    app = wx.App()
    frame = MyFrame(None, id=-1, title="Monitor", size=(800, 600))
    frame.Show(True)
    app.SetTopWindow(frame)
    b = frame.isExist('jessica alba')

    # frame.insert1("test", "testplace")
    try:
        _thread.start_new_thread(get_data, ("Thread-1", 2,))
        app.MainLoop()
        # t = threading.Thread(target=hello, args=("hawk", 5))
        # t.start()
    except Exception as e:
        print("Error: 无法启动线程;" + str(e))
