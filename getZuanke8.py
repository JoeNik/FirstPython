import requests
import codecs
from bs4 import BeautifulSoup
import sys
import importlib
import chardet
import time
import mysql_DBUtils
import io
import base64
from mysql_DBUtils import MyPymysqlPool
#import requests
from urllib import request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions  as EC

#from __future__ import unicode_literals
import wxpy
from wechat_sender import listen
#bot = wxpy.Bot('bot.pkl')

##图片识别
from PIL import Image, ImageEnhance
import PIL.ImageOps
import pytesser3


importlib.reload(sys)
importlib.reload(sys)

# python2 和 python3的兼容代码
# try:
#     # python2 中
#     import cookielib
#     print(f"user cookielib in python2.")
# except:
#     # python3 中
#     as cookielib
#     print(f"user cookielib in python3.")

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8') #改变标准输出的默认编码

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}

server = 'http://www.zuanke8.com/zuixin.php'

mysql = MyPymysqlPool("dbMysql")

cookiestrHead = r'ki1e_2132_saltkey=lsBSSV39; ki1e_2132_lastvisit=1559725160; ki1e_2132_auth=c705jfbJcHk%2B3iB3qmrPG1BrW5ijmJ6TRrgoHFm3EvazA85CtaRR%2BPp9LAoFz0Gr11Bm9hCt8iXL0eErm8Kyb9OcApg; ki1e_2132_connect_is_bind=1; ki1e_2132_smile=1D1; ki1e_2132_pc_size_c=0; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1559780847,1559810342,1559810796,1560127058; ki1e_2132_creditnotice=0D0D0D0D0D0D0D0D0D538097; ki1e_2132_creditbase=0D1303D0D0D0D0D0D0D0; ki1e_2132_clearUserdata=forum; ki1e_2132_connect_not_sync_t=1; ki1e_2132_creditrule=%E5%8F%91%E8%A1%A8%E5%9B%9E%E5%A4%8D; td_cookie=18446744071559493794; timestamp=1560130076000; sign=4CBD74A5DD4643A9A56601CC25825DB4; ki1e_2132_nofocus_forum=1; ki1e_2132_atarget=1; ki1e_2132_forum_lastvisit=D_26_1560131402; ki1e_2132_ulastactivity=1560132614%7C0; ki1e_2132_checkpm=1; ki1e_2132_sendmail=1; ki1e_2132_lastcheckfeed=538097%7C1560132615; ki1e_2132_checkfollow=1; ki1e_2132_noticeTitle=1; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1560132616; amvid=c3faf2181a26daf6a98851670ae53153; ki1e_2132_lastact=1560132619%09forum.php%09viewthread; ki1e_2132_viewid=tid_6113962'

keyword =['速度', 'bug', '快', '招行']
def weSend(flag, sendTo, content):
    # 个人
    if flag == 1:
        sender = bot.friends().search(sendTo)[0]
    else:
        sender = bot.groups().search(sendTo)[0]

    sender.send(content)


def write_txt(chapter, content, code):
    with codecs.open(chapter, 'a', encoding=code)as f:
        f.write(content)

# 写入数据库
def write_db(chapter, content , remark, comments):
    sql = "INSERT INTO articlelist (title, content , remark, comments) VALUES(%(title)s, %(content)s, %(remark)s, %(comments)s);"
    param = {"title": chapter, "content": content, "remark": remark, "comments": comments}
    print("成功入库:", str(mysql.insert(sql, param)), "条")
    mysql.end('commit')

def getInsertId():
    idSql = "SELECT LAST_INSERT_ID()"
    return mysql.getOne(idSql)


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
    #print(chardet.detect(html))
    for each in a:
        try:
            b = each.find('center')
            #print('xxx:' + str(b))
            if b != None:
                x = b.string
                if x <= '最新交流消息':
                    c = each.select('tr')
                    #print(each)
                    #write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log.txt", str(each), 'utf8')
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
                                fdic = ['赚品交换'.encode('gbk'), '果果换物'.encode('gbk'), '做任务赚果果'.encode('gbk'), '邀请专区'.encode('gbk')]

                                if (ftitle in fdic):
                                #if (ftitle == '赚品交换'.encode('gbk') or ftitle == '果果换物'.encode('gbk') or ftitle == '做任务赚果果'.encode('gbk')):
                                    iscontinue = True
                                    continue
                                if(ftitle == '赚客大家谈'.encode('gbk') or ftitle == '活动线报'.encode('gbk') or ftitle == '活动秘籍'.encode('gbk') or ftitle == '求助咨询区'.encode('gbk')):
                                    remark = ftitleTemp
                                    print(remark)
                                else:
                                    (remark, comments) = get_onpage(w.get('href'), cookiestrHead)
                                    write_db(ftitleTemp, w.get('href'), remark, comments)
                                    # for key in keyword:
                                    #     if ftitleTemp.find(key) != -1:
                                    #         weSend(1, 'JoeNik', remark + ' ' + w.get('href'))
                                    #id = getInsertId()

                                # print(ftitleTemp)
                                # print(w.get('href'))
                                # print('\r\n')



                           # write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log1.txt", str(g), 'utf8')
                        #print(e)
                        # if d.string <= '赚客大家谈':
                        #     e = d.get('href')
                        #     print(d.get('title'))
                        #write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log1.txt", str(e), 'utf8')

        except Exception as e:
            print('error:' + str(e))

def get_onpage(chapter, cookiesStr):
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
    #write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log2.html", str(soup), 'gbk')
    #content1 = soup.find('td', class_='t_f').text
    if (title == '提示信息 -  赚客吧'):
        print(title)
        print('session 过期，请重新获取')
        return ''
    else:
        #content1 = soup.find('td', class_='t_f').text
        comments = soup.find_all('td', 't_f')
        cnt = 0
        remarks = ''
        commentsStr = []
        for comment in comments:
            if cnt == 0:
                remarks = comment.text
            else:
                commentsStr.append(comment.text)
            cnt = cnt + 1
            #print(comment.text)
        return (remarks,'|'.join(commentsStr))
        #print(content1)

# b = a[0].find_all('center')
#
# print(b)
# print('xxxxxxxxxxxxxxxxxxxxx')
# print(a[3])
# write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log.txt", str(a[2]),'utf8')
# write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log.txt", 'xxxxxxxxxxxxxxxxxxxxx', 'utf8')
# write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log.txt", str(a[3]), 'utf8')

def moveslide():
    try:
        driver = webdriver.Chrome()
        driver.get("http://www.zuanke8.com/member.php?mod=logging&action=login")
        button = driver.find_element_by_id('nc_1_n1z')  # 找到“蓝色滑块”
        action = ActionChains(driver)  # 实例化一个action对象
        action.click_and_hold(button).perform()  # perform()用来执行ActionChains中存储的行为
        action.reset_actions()
        action.move_by_offset(250, 0).perform()  # 移动滑块
        userbox = driver.find_element_by_id("nc_1__scale_text")
        print('**********************************')
        print(userbox)
        print('**********************************')
        time.sleep(10)
        driver.quit()
    except Exception as e:
        print('-----------------------------')
        print(e)
        print('-----------------------------')
        driver.quit()

# 循环输入验证码，因为一遍可能不能正确识别，直到正确识别，再进行其他操作
#def TypePicCode:
    # accept = False
    # while not accept :
    #     try:
    #
    #     except UnicodeDecodeError:
    #         accept = False
    #         time.sleep(3)

def getPicFromBs64(picStr):
    try:
        with open('1.jpg', 'wb') as f:
            f.write(base64.b64decode(picStr))
    except Exception as e:
        print('getPicFromBs64 error:', str(e))

def testf():
    driver = webdriver.Chrome()
    driver.get("http://www.baidu.com")
    print(driver.page_source)
    driver.quit()

def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table
def Binary(x,y,img):
    for i  in range(x):
        for j in range(y):
            if img[i,j] > 180:
                img[i,j] = 255
            else:
                img[i,j] = 0
    return  img
def doWithPic(pic):
    im = Image.open(pic)
    # 图片的处理过程
    im = im.convert('L')
    binaryImage = im.point(initTable(), '1')
    im1 = binaryImage.convert('L')
    im2 = PIL.ImageOps.invert(im1)
    im3 = im2.convert('1')
    im4 = im3.convert('L')
    # 将图片中字符裁剪保留
    box = (0, 0, 90, 42)
    region = im4.crop(box)
    # 将图片字符放大
    out = region.resize((120, 38))
    asd = pytesser3.image_to_string(out)
    print(asd)
   # print(out.show())


def main():
    while True:
        get_contents(server)
        print(str(time.ctime()) + "  获取数据完毕")
        time.sleep(120)
    mysql.dispose()

    # (remark, comments) = get_onpage('http://www.zuanke8.com/thread-6026398-1-1.html', cookiestrHead)
    # print(remark)
    # print(comments)
    #moveslide()
    #testf()
    #picStr = '''data:image/jpg;base64,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'''
    #getPicFromBs64(picStr)
    #im1 = Image.open('1.png')
   # print('-----------------------------')
   #  im = Image.open('3.png')
   #  imgry = im.convert("L")
   #  sharpness = ImageEnhance.Contrast(imgry)
   #  sharp_img = sharpness.enhance(3)
   #  sharp_img.save('3.jpg')
   #  # #sharp_img.show()
   #  im = Image.open('3.jpg')
   #  result = pytesser3.image_to_string(im)

   # print(result)
   #  print('-----------------------------')
   #  #doWithPic('3.png')
   #
   #  img = Image.open('3.png')
   #  img = img.convert('L')
   #  x, y = img.size
   #  imgdata = img.load()
   #
   #  imgdata = Binary(x, y, imgdata)
   #  print(pytesser3.image_to_string(img))


if __name__ == '__main__':
    main()
