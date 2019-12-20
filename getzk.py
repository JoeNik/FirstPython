import json
import requests
from bs4 import BeautifulSoup
import time, logUntil
from urllib import request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Content-Type': 'application/json'}

server = 'http://www.zuanke8.com/zuixin.php'

#  dingding请求地址
DingPost_url = "https://oapi.dingtalk.com/robot/send?access_token=b63c5a144e9102029af7ef052c20150503441101f54dbb1c81a47285d56105d9"
cookiestrHead = r'ki1e_2132_connect_is_bind=1; ki1e_2132_smile=1D1; ki1e_2132_atlist=179919%2C730672%2C891213%2C69238%2C4%2C18%2C3; __gads=Test; ki1e_2132_atarget=1; ki1e_2132_saltkey=BOFHWJus; ki1e_2132_lastvisit=1575848667; ki1e_2132_auth=7ec3SUJXMYbXjWIBi%2BWbubChIaBTk%2Fqh0tZrX33i%2F5yx5y6HNY0HfW7Zlo%2Bf936GbiBteSs6cAoPLkFDHAa4wd8TjFQ; ki1e_2132_pc_size_c=0; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1576199433,1576456388,1576542119,1576630816; timestamp=1576636591000; sign=DB3D4C55FA5ACF1ECCEB850D3C7C7543; td_cookie=30223767; ki1e_2132_lastviewtime=538097%7C1576649069; ki1e_2132_nofocus_forum=1; ki1e_2132_clearUserdata=forum; ki1e_2132_creditnotice=0D0D0D0D0D0D0D0D0D538097; ki1e_2132_creditbase=0D1639D0D0D0D0D0D0D0; ki1e_2132_creditrule=%E5%8F%91%E8%A1%A8%E5%9B%9E%E5%A4%8D; ki1e_2132_connect_not_sync_t=1; ki1e_2132_connect_not_sync_feed=1; ki1e_2132_forum_lastvisit=D_19_1573625063D_25_1576137386D_22_1576137419D_26_1576648030D_11_1576654048; ki1e_2132_ulastactivity=1576660463%7C0; ki1e_2132_dismobilemessage=1; ki1e_2132_mobile=no; ki1e_2132_checkpm=1; ki1e_2132_sendmail=1; ki1e_2132_lastcheckfeed=538097%7C1576660554; ki1e_2132_checkfollow=1; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1576660556; amvid=f7dbb54ebd542d284d740bc3176fec0d; ki1e_2132_lastact=1576660558%09forum.php%09viewthread; ki1e_2132_viewid=tid_6699009'

keyword = ['速度', 'bug', '快', '水', '有了', '好价', '赶紧', '作业', '速撸', '撒果', '首发', '平行', '神价', '线报', '爱奇艺', '好莱坞', '周卡', '月卡',
           '可以', '冲', '招行抽奖']
# 推送到钉钉
isPostToDing = 1

lstExistArg = []
lstErrorArg = []  # 已删除获取权限过高的帖子集合

log = logUntil.logs()


def isExistLst(value):
    try:
        lstExistArgSet = set(lstExistArg)
        if value in lstExistArgSet:
            return True
        else:
            lstExistArg.append(value)
            return False
        # 帖子大于30就把前10条清空
        if len(lstExistArg) > 30:
            del lstExistArg[0:10]
    except Exception as e:
        log.error('isExistLst error:' + str(e))


def isExistErrorLst(value):
    try:
        lstErrorArgSet = set(lstErrorArg)
        if value in lstErrorArgSet:
            return True
        else:
            lstErrorArg.append(value)
            return False
        if len(lstErrorArg) > 20:
            del lstErrorArg[0:1]
    except Exception as e:
        log.error('isExistErrorLst error:' + str(e))


def get_contents(chapter):
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
        ArgLst = []  # 文章信息列表
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
                        log.debug(1 + len(c))
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
                                        if not isExistErrorLst(argUrl):
                                            (remark, comments, picurl) = get_onpage(argUrl, cookiestrHead)
                                            for key in keyword:
                                                if ftitleTemp.find(key) != -1:
                                                    log.debug("匹配:" + key)
                                                    if not isExistLst(ftitleTemp):
                                                        if isPostToDing == 1:
                                                            log.debug("send " + ftitleTemp)
                                                            # DingDingPost(ftitleTemp, remark, picurl, comments,
                                                            #              w.get('href'))
                                                            ArgLst.append(
                                                                GetDingMarkDownText(ftitleTemp, remark, comments,
                                                                                    argUrl, picurl))
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
                log.error('get_contents error1:' + str(e))
        if len(ArgLst) > 0:
            DingPostMarkDown("新消息来啦", ArgLst)
    except Exception as e:
        log.error('get_contents error:' + str(e))


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
            log.debug(title)
            log.debug('session 过期或 权限不足，请重新获取')
            # wx.MessageBox("error", 'session 过期，请重新获取', wx.YES_NO)
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
        log.error('DingDingPost error:' + str(e))


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
            x = requests.post(DingPost_url, data=json.dumps(data), headers=headers)
            log.debug("post rlt:" + x.text)
    except Exception as e:
        log.error('DingPostMarkDown error:' + str(e))


def GetDingMarkDownText(title, content, comments, messageURL, picURL):
    try:
        timeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if len(picURL) == 0:
            text = "# " + title + " \n" + "## " + content + "  \n" + "* " + comments + " \n " + "> ###### " + str(
                timeStr) + "获取 [原文](" + messageURL + ") \n \n"
        else:
            text = "# " + title + " \n" + "## " + content + "  \n" + "* " + comments + " \n " + "![screen](" + picURL + ") \n" + "> ###### " + str(
                timeStr) + "获取 [原文](" + messageURL + ") \n \n"
        return text
    except Exception as e:
        log.error('GetDingMarkDownText error:' + str(e))
    return ""


def GetDingFcardLinks(title, messageURL, picURL):
    dic = {"title": title, "messageURL": messageURL, "picURL": picURL}
    return dic


def DingPostFcard(links):
    data1 = {"feedCard": {"links": links}, "msgtype": "feedCard"}
    # 使用post请求推送消息
    x = requests.post(DingPost_url, data=json.dumps(data1), headers=headers)
    log.debug("post rlt:" + x.text)


def main():
    while True:
        try:
            log.debug("*****************begin*********************")
            get_contents(server)
            log.debug(str(time.ctime()) + "  获取数据完毕")
            time.sleep(10)
        except Exception as e:
            log.error('main error:' + str(e))


if __name__ == '__main__':
    main()
