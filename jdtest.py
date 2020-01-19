import datetime
from urllib import request
import time


class JudjeTime(object):
    # def __init__(self):
    # self.start = str(start)
    # self.end = str(end)

    def judje(self, start, end):
        n_time = datetime.datetime.now()  # 获取当前时间
        start = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.start, '%Y-%m-%d%H:%M:%S')
        # print(start)
        end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.end, '%Y-%m-%d%H:%M:%S')
        # print(end)
        if n_time > start and n_time < end:
            print(True)
            print('任务执行:' + datetime.datetime.strftime(n_time, '%Y-%m-%d %H:%M:%S'))
            return True

    def judje2(self, btime):
        n_time = datetime.datetime.now()  # 获取当前时间
        start = datetime.datetime.strptime(str(datetime.datetime.now().date()) + btime, '%Y-%m-%d%H:%M:%S')
        #print(start)
        # end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.end, '%Y-%m-%d%H:%M:%S')
        end = start + datetime.timedelta(seconds=4)
        #print(end)
        if n_time > start and n_time < end:
            print(True)
            print('任务执行:' + datetime.datetime.strftime(n_time, '%Y-%m-%d %H:%M:%S'))
            return True


def main():
    chapter = r'https://api.m.jd.com/client.action?functionId=newReceiveRvcCoupon&body=%7B%22extend%22%3A%220271DFD6890D3B60ACB8BA8A9E49BEB17FE8E6323A36834B63FE69E95D38088E5E6BC390040B149A36073440BB0F65357F8CA0711A5D39BEF962DED99FF4BF2F7930479CE07BD526F1F06368513674DAFE62BCCADA468D6308DEE97A46911D09%22%2C%22source%22%3A%22couponCenter_app%22%2C%22rcType%22%3A%221%22%2C%22shshshfpb%22%3A%22biJomXyYtzt%2BpYNC7uieFHs%5C/E3DDDM82Q9eKcBLkuqgRxEv%5C/EUw38t65oNRCVXXiZX7byKPAHvTLgHy%2Br9d7apA%3D%3D%22%2C%22pageClickKey%22%3A%22CouponCenter%22%2C%22eid%22%3A%22eidI0e828121bcsbTYijzrdmTZe66xnbgVTCy02IpTibA5HQHx%2BX6px1t3i1UYQvuQs6CXNFnEwPQhFDtXEFYz%2BAG2emRjRrHFFwZBd%5C/GwA0bFD60%2B9i%22%2C%22childActivityUrl%22%3A%22openapp.jdmobile%253a%252f%252fvirtual%253fparams%253d%257b%255c%2522category%255c%2522%253a%255c%2522jump%255c%2522%252c%255c%2522des%255c%2522%253a%255c%2522couponCenter%255c%2522%257d%22%7D&build=166736&client=apple&clientVersion=8.3.6&d_brand=apple&d_model=iPhone8%2C1&eid=eidI0e828121bcsbTYijzrdmTZe66xnbgVTCy02IpTibA5HQHx%2BX6px1t3i1UYQvuQs6CXNFnEwPQhFDtXEFYz%2BAG2emRjRrHFFwZBd/GwA0bFD60%2B9i&isBackground=N&joycious=632&lang=en_US&networkType=wifi&networklibtype=JDNetworkBaseAF&openudid=85c38dc67787e4860cfe964f171e5e0fa848ee14&osVersion=10.3.3&partner=apple&rfs=0000&scope=01&screen=750%2A1334&sign=127cbf11702f55a879ad55c9715852ab&st=1579069035029&sv=102&uuid=coW0lj7vbXVin6h7ON%2BtMNFQqYBqMahr&wifiBssid=1199a589c5b4acda7658124c78c517ff'
    cookiestrHead = r'subAbTest=20180202000730070_68; shshshfpa=a8dfe08d-b3c9-b0dd-417d-0721342c97ee-1532931711; commonAddress=360544783; regionAddress=16%2C1303%2C3484%2C48726; shshshfpb=23458e80995f740a7b4286cc864255a6d5b024f94fb30c3d10b40c6632; pinId=jXUpX0nG0qRUAbyk8LvjBg; pin=andyjiao15; unick=andyjiao15; _tp=qLnfxgw3nj1MEmQXUqi2iQ%3D%3D; _pst=andyjiao15; __jdu=15117954500991589524254; jcap_dvzw_fp=1de1ea5dbf3a179e0368381b67c15e7e$635649273564; autoOpenApp_downCloseDate_auto=1578640222632_21600000; whwswswws=; areaId=16; mt_xid=V2_52007VwMWUl1eWl4aTRhdDW8DFltVXFFfHE0cbFFiVxJRWl8FRkobEFUZYlQTU0FQAlIaVRtYUmUFE1tVD1ENTHkaXQZmHxNSQVhWSx5AElgBbAMbYl9oUWobSh9cAGAzElZc; ipLoc-djd=16-1303-3484-48726; unpl=V2_ZzNtbUQFRRFzC09VeREIUmJWF1oRVhMTdwhDXC9OD1FgUEVbclRCFnQUR1RnGVgUZwcZX0tcQxZFCEdkexhdBGYCE1VAUHMRdwFHXH0pWAduAhpbclRDJXQ4RlB7GVoNYwYWXENfSxVxAU5QeBxfAWIzIl1KU3MScQpEUnwfVAVvBiINCgkYS0UKQVF%2bHlwDbgAiXHJWc1QbDkRTeRBaSGcHEl1EX0cQcQlHXHMZWAxvBxFYQVNGJXQ4RQ%3d%3d; __jdv=122270672|www.zuanke8.com|t_1000000936_538097|tuiguang|7c75728039ef4d46b0a73149efbe6bf7|1579073893707; user-key=1f3744e9-8e81-412d-8f3a-043bd47fc2a0; cn=3; shshshfp=3ba4172025cd49a978ad3f04925bc587; TrackID=1PqjP6P0WdaoE5NMgd9v9TKE86Js_6EcsmGE88s6Oav74Xe88sPGtYS6E950iUrSWJqNyEMlqFdxVSiqPmcdfaA; thor=45A41644EC8A691E6C3B8C7E0AE9C443A79BA40F1AD8C4D2757FF5E2F329EBB58B291D10E700844DF5C9BA40EC96FD2CB9E483DD31444F8A8A185513A7BFE2FAAE7F73BF7FC82ABB4F1139966940AF69E6660A654E0EC77F6FDFB1CABE47A606693C5945EE1D64A9D026D1762D29F28F75D0EB840D7355A00DF7D4830E70279656B818099977ABAEC5EC4D2984002388; ceshi3.com=201; __jda=76161171.15117954500991589524254.NaN.1579161444.1579239971.512; __jdb=76161171.4.15117954500991589524254|512.1579239971; __jdc=76161171; shshshsID=52250c851840b218ab64b5c42a4df9e6_1_1579239990760'
    reqCnt = 0  # 为避免账号限制,只在固定时间请求5次
    #btime = '14:31:00'
    #timeArray = ['14:40:00', '19:59:59', '09:59:59']
    timeArray = ['14:40:00', '14:40:20', '14:40:40']

    while True:
        # if JudjeTime(btime, etime).judje() and reqCnt < 6:
        for btime in timeArray:
            if JudjeTime().judje2(btime):
                if reqCnt >= 6:
                    time.sleep(2)
                    reqCnt = 0
                req = request.Request(chapter)
                # 设置cookie
                req.add_header('cookie', cookiestrHead)
                # 设置请求头
                req.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')
                # resp = request.urlopen(req)
                # rlt = resp.read().decode('utf-8')
                reqCnt += 1
                # print(rlt)
        time.sleep(1)

    print(rlt)


if __name__ == '__main__':
    main()
