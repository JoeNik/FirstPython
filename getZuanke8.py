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

##图片识别
from PIL import Image
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

def write_txt(chapter, content, code):
    with codecs.open(chapter, 'a', encoding=code)as f:
        f.write(content)

# 写入数据库
def write_db(chapter, content , remark):
    sql = "INSERT INTO articlelist (title, content , remark) VALUES(%(title)s, %(content)s, %(remark)s);"
    param = {"title": chapter, "content": content, "remark": remark}
    print("成功入库:", str(mysql.insert(sql, param)), "条")
    mysql.end('commit')

def get_contents(chapter):
    req = requests.get(url=chapter)
    html = req.content
    print('xx:')
    html_doc = str(html, 'gbk')
    soup = BeautifulSoup(html_doc, 'html.parser')

    # a = soup.find('div', id='wp')
    a = soup.find_all('table')
    # print(a)
    # write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log.txt", str(a), 'utf8')
    print(chardet.detect(html))
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
                                    write_db(ftitleTemp, w.get('href'), remark)
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
    req.add_header('cookie', cookiesStr)
    # 设置请求头
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')

    resp = request.urlopen(req)

    rlt = resp.read().decode('gbk')
    #write_txt("E:\\bReadyWorking\\gothonweb\\bin\\log.html", rlt, 'gbk')

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


def main():
	# while True:
	# 	get_contents(server)
	# 	print(str(time.ctime()) + "  获取数据完毕")
	# 	time.sleep(60)
    #mysql.dispose()
    cookiestr = r'_uab_collina=146763932554686089915037; ki1e_2132_nofavfid=1; _umdata=486B7B12C6AA95F221463E658E168EB108E4AEF692E6EA54DD24B6C9120D0F79592617DDF17D419ECD43AD3E795C914CCCDA482549063C73F3CED72B166C5F67; ki1e_2132_atlist=179919%2C3%2C366314%2C633570; ki1e_2132_atarget=1; ki1e_2132_saltkey=d1BaEe3m; ki1e_2132_lastvisit=1556254216; ki1e_2132_auth=aaffFqNN5mcTysdaHUosEPeLrm2pmMJDQPOenZ4dyjhWWVyFRR33md%2BplXvoRP3DclzADYUPamG%2Bqppd%2BfgF6BZjVUc; td_cookie=18446744072832140176; ki1e_2132_forum_lastvisit=D_26_1557104496D_31_1557123383D_19_1557141668D_15_1557141693; ki1e_2132_lastviewtime=538097%7C1557219450; Hm_ck_1557275765978=is-cookie-enabled; ki1e_2132_viewid=tid_6026492; ki1e_2132_smile=1D1; ki1e_2132_ulastactivity=1557277270%7C0; ki1e_2132_pc_size_c=0; ki1e_2132_lastcheckfeed=538097%7C1557277270; ki1e_2132_lastact=1557277270%09home.php%09misc; ki1e_2132_connect_is_bind=1; ki1e_2132_sendmail=1; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1557223388,1557223400,1557227611,1557275738; Hm_lpvt_da6569f688ba2c32429af00afd9eb8a1=1557277274; amvid=31b984f31d1611003a9276ae06666336'
    #get_onpage('http://www.zuanke8.com/thread-6026398-1-1.html', cookiestr)
    #moveslide()
    #testf()
    picStr = '''data:image/jpg;base64,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'''
    #getPicFromBs64(picStr)
    #im1 = Image.open('1.png')
    print('-----------------------------')
    result = pytesser3.image_file_to_string('1.png', graceful_errors=True)
    print('-----------------------------')
    print(result)

if __name__ == '__main__':
    main()
