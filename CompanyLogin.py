import time
import urllib
from http import cookiejar
from urllib import parse

import execjs

import logUntil

log = logUntil.logs()
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


# key 13位UNIX时间 data 密码
def get_des_psswd(data, key):
    try:
        CTX = execjs.compile(JSCode)
        return CTX.call('do_encrypt_rc4', data, key)
        # jsstr = get_js()
        # ctx = execjs.compile(jsstr)  # 加载JS文件
        # return (ctx.call('do_encrypt_rc4', data, key))  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数
    # return execjs.compile(open(r"E:\\bReadyWorking\\gothonweb\\bin\\loginCheck.js").read().decode("utf-8")).call('do_encrypt_rc4', data,key)
    except Exception as e:
        log.error('GetDingMarkDown error:' + str(e))


def login():
    try:
        millis = int(round(time.time() * 1000))
        # psw = js2pyTest("123456", millis)
        psw = get_des_psswd("123456", millis)
        # 1.代码登录
        # 1.1 登录的网址
        login_url = "http://191.168.4.1/ac_portal/login.php"
        login_form_data = {
            "opr": "pwdLogin",
            "userName": "郑乔",
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
        log.error('login error:' + str(e))


def main():
    log.info("login begin")
    login()
    log.info("login end")
    time.sleep(10)


if __name__ == '__main__':
    main()
