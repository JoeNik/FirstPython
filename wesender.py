from __future__ import unicode_literals
import wxpy
from wechat_sender import listen
import mysql_DBUtils
from mysql_DBUtils import MyPymysqlPool
import time

#bot = wxpy.Bot('bot.pkl')

mysql = MyPymysqlPool("dbMysql")
def str_to_zhongwen(var):
    #print "str_to_zhongwen : ",var

    not_end = True
    while not_end:
        start1 = var.find("\\x")
        if start1 > -1:
            str1 = var[start1+2:start1+4]

            start2 = var[start1+4:].find("\\x")+start1+4
            if start2 > -1:
                str2 = var[start2+2:start2+4]

                start3 = var[start2+4:].find("\\x")+start2+4
                if start3 > -1:
                    str3 = var[start3+2:start3+4]
        else:
            not_end = False
        if start1 > -1 and start2>-1 and start3>-1:
            str_all = str1+str2+str3
            str_all = str_all.decode('hex')

            str_re = var[start1:start3+4]
            #print str_all, "   " ,str_re
            var = var.replace(str_re, str_all)
    #print(var.decode('utf-8'))
    return var
def checkDb():
    sql = "select * from articlelist where create_time>date_sub(now(),interval 2 minute)"
    while True:
        result = mysql.getAll(sql)
        for temp in result:
            print(str(temp.get('UID')) + ' '+str_to_zhongwen(str(temp.get('title')))+ ' '+ str(temp.get('content'))+ ' '+ str(temp.get('remark')))
            #+ temp.get('title')+ ' '+ temp.get('content')+ ' '+ temp.get('remark')+ ' '+ temp.get('comments')

        time.sleep(120)
    mysql.dispose()

def main():
    checkDb()

if __name__ == '__main__':
    main()
#listen(bot,receivers=None,token='123456')
# alarm_group=bot.groups().search('集团军')[0]
# alarm_group.send('this is test msg')

# my_friends = bot.friends()
#
# sex_dict = {'male': 0, 'female': 0, 'other': 0}
#
# for friend in my_friends:
#     if friend.sex == 1:
#         sex_dict['male'] += 1
#     elif friend.sex == 2:
#         sex_dict['female'] += 1
#     else:
#         sex_dict['other'] += 1
#
# print(sex_dict)
# print("Total numbers of my friends: ", len(my_friends))


# province_dict = {
#                     '北京': 0, '上海': 0, '天津': 0, '重庆': 0, '西藏': 0,
#                     '河北': 0, '山西': 0, '吉林': 0, '辽宁': 0, '黑龙江': 0,
#                     '陕西': 0, '甘肃': 0, '青海': 0, '山东': 0, '福建': 0,
#                     '浙江': 0, '台湾': 0, '河南': 0, '湖北': 0, '湖南': 0,
#                     '江西': 0, '江苏': 0, '安徽': 0, '广东': 0, '海南': 0,
#                     '四川': 0, '贵州': 0, '云南': 0, '香港': 0, '澳门': 0,
#                     '内蒙古': 0, '新疆': 0, '宁夏': 0, '广西': 0, '其他': 0,
#                 }
# for friend in my_friends:
#     if friend.province in province_dict.keys():
#         province_dict[friend.province] += 1
#     else:
#         province_dict['其他'] += 1
#
# print(province_dict)
