import importlib
import random
import string
import sys
import urllib.error
import urllib.request
from urllib.parse import quote

import numpy as np
import pandas as pd
import pymysql
import xlrd
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans

importlib.reload(sys)

subject = ["", "机械", "交通", "生物", "信息", "医学", "中国科学", "化学"]
render = ["弱", "较弱", "中", "较强", "强"]


def takeSecond(elem):
    return elem[1]


class Douban_Spider():
    def __init__(self):
        self.url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=&tn=baiduerr&bar=&wd="

    def getheaders(self):
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        UserAgent = random.choice(user_agent_list)
        headers = {'User-Agent': UserAgent}
        return headers

    def get_page(self, url):
        try:
            headers = self.getheaders()

            requests = urllib.request.Request(url=url, headers=headers)
            html = urllib.request.urlopen(requests)
        except urllib.error.HTTPError as e:
            print(e.code)
            html = None
        return html

    def get_info(self, html):
        if html != None:
            soup = BeautifulSoup(html, 'html.parser')
            name = soup.find("span", {"class": "nums_text"}).get_text()  # 片名
        return name

    def begin(self, key):
        temp_url = self.url + key
        temp_url = quote(temp_url, safe=string.printable)
        html = self.get_page(temp_url)
        temp_info = self.get_info(html)
        return temp_info


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normset = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    normset = dataSet - np.tile(minVals, (m, 1))
    normset = normset / np.tile(ranges, (m, 1))
    return normset


def readdata(kind):
    db = pymysql.connect("localhost", "root", "123p123p", "temp")
    # data = pd.read_sql('select * from  7_years ', con=db);
    # namelist = pd.read_sql('select Name from  7_years ', con=db)
    # namelist = namelist.values
    namelist=list()
    temp = pd.read_sql('select * from allthing', con=db)
    temp = temp.values
    data = list()
    if kind == 6:
        data = data.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]]
    if kind == 3:
        data = data.iloc[:, [3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]]
    if kind == 4:
        data = data.iloc[:, [4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]]
    if kind == 0:
        data = data.iloc[:, [4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]]
    if kind == 5:
        data = data.iloc[:, [3, 5, 6, 18, 19, 20, 21, 22]]
    if kind == 1:
        data = data.iloc[:, [3, 6, 18, 19, 20, 21, 22]]
    if kind == 2:
        data = data.iloc[:, [5, 18, 19, 20, 21, 22]]
    if kind == 8:
        datai = spider()
        for i in range(len(datai)):
            namelist.append(datai[i][0])
            data.append(
                [datai[i][1], temp[i][1], temp[i][1], temp[i][1], temp[i][1], temp[i][1], temp[i][1], temp[i][1]])

    # data = data.values
    data = np.array(data)
    db.close()
    return namelist, data


def spider():
    spider = Douban_Spider()
    baidu = list()
    num = list()
    db = pymysql.connect("localhost", "root", "123p123p", "temp")
    searchdata = pd.read_sql('select * from allthing', con=db);
    searchdata = searchdata.values
    namelist = searchdata[:, 2]
    for name in namelist:
        # name.encode('ascii')
        ans = spider.begin(name)
        for i in ans:
            if i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                num.append(i)
        stringnum = ''.join(num)
        print(stringnum)
        baidu.append([name, int(stringnum)])
        num.clear()
    '''
    cursor = db.cursor()
    sql = "create table %s(name varchar(50),baiduspider int)" % "spider"
    cursor.execute(sql)
    db.commit()
    for i in baidu:
        sql = "INSERT INTO %s (name,baiduspider)VALUES ('%s','%d')" % (
            "spider", i[0], i[1])
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    '''
    print(baidu)
    return baidu


def cont():
    '''
    table = ['indexdata1', 'indexdata2', 'indexdata3', 'indexdata4', 'indexdata5', 'indexdata6', 'indexdata7']
    for i in range(7):
        namelist, data = readdata(i)
        data = autoNorm(data)

        n_clusters = 5

        cls = KMeans(n_clusters).fit(data)
        cls.labels_

        db = pymysql.connect("localhost", "root", "123p123p", "temp")

        cursor = db.cursor()

        sql = "drop table %s" % table[i]
        print(sql)
        cursor.execute(sql)
        db.commit()

        sql = "create table %s(name varchar(50),level int)" % table[i]
        print("正在输入地%d个表" % i)
        cursor.execute(sql)
        db.commit()
        for j in range(len(cls.labels_)):
            sql = "INSERT INTO %s (name,level)VALUES ('%s','%d')" % (table[i], namelist[j][0], cls.labels_[j])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        print("输入完成")

        db.close()
    '''
    namelist, data = readdata(8)
    data = autoNorm(data)

    n_clusters = 5

    cls = KMeans(n_clusters).fit(data)
    cls.labels_

    db = pymysql.connect("localhost", "root", "123p123p", "temp")

    cursor = db.cursor()
    datai = pd.read_sql('select * from allthing', con=db)
    datai=datai.values
    sql = "create table %s(id varchar(50),level int,name varchar(50),en_name varchar(50),time varchar(50) ,subject varchar(50))" % "ething"
    cursor.execute(sql)
    db.commit()
    for i in range(len(datai)):
        sql = "INSERT INTO %s (id,level,name,en_name,time,subject)VALUES ('%s','%d','%s','%s','%s','%s')" % (
            "ething", datai[i][0], cls.labels_[i], datai[i][2], datai[i][3], datai[i][4], datai[i][5])
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    print("输入完成")

    '''
    sql = "drop table %s" % table[i]
    print(sql)
    cursor.execute(sql)
    db.commit()

    sql = "create table %s(name varchar(50),level int)" % table[i]
    print("正在输入地%d个表" % i)
    cursor.execute(sql)
    db.commit()
    for j in range(len(cls.labels_)):
        sql = "INSERT INTO %s (name,level)VALUES ('%s','%d')" % (table[i], namelist[j][0], cls.labels_[j])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    print("输入完成")

    db.close()
    print("finsh")
    '''


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]  # 返回的类型为列表


def get_val(list, value):
    return [item[1:] for item in list if item[0] == value]


def myget():
    myScore = [1 for i in range(788)]
    myScore1 = [1 for i in range(788)]
    print('myScore的长度是%d' % (len(myScore)))
    excel = xlrd.open_workbook("/home/gswlee/桌面/science_events.xlsx")  # 打开文件
    # excel = xlrd.open_workbook("/home/gswlee/桌面/score.xlsx")  # 打开文件
    print("okokoko")
    sheet0 = excel.sheet_by_index(0)  # 获取第一个sheet表格
    sheet3 = excel.sheet_by_index(3)  # 获取第四个sheet表格
    # print(excel.sheet_names()) #表的名字
    # print(sheet.nrows)  #  表格有多少行
    # row = sheet0.row_values(0)  # 输出某一行的值
    # print(row)
    col0_0 = sheet0.col_values(0)  # 获取第一个sheet表格某一列的值
    col0_1 = sheet0.col_values(1)
    col0_2 = sheet0.col_values(2)
    col0_9 = sheet0.col_values(9)
    col0_3 = sheet0.col_values(3)
    col0_4 = sheet0.col_values(4)  # 获取第一个sheet表格某一列的值

    # 获取第四个表格的某一列的值   科技事件的导向关系
    col3_0 = sheet3.col_values(0)
    col3_1 = sheet3.col_values(1)
    for i in range(592):
        if not isinstance(col3_0[i], str):
            col3_0[i] = str(col3_0[i])
        if not isinstance(col3_1[i], str):
            col3_1[i] = str(col3_1[i])

    # 将第1列和第2列输科技事件合起来  用来查询
    for i in range(1, len(col0_9)):
        col0_9[i] = int(col0_9[i])
    scienceThing = list(zip(col0_0[1:], col0_1[1:], col0_2[1:], col0_3[1:], col0_9[1:]))

    # 对表格中的数据进行处理
    # print(col[1:])
    time = []
    info = {}
    # position = {}
    print(list(zip(col0_0[1:], col0_4[1:])))
    for item in list(zip(col0_0[1:], col0_4[1:])):
        if isinstance(item[1], str):
            # print(item[1][0:6])
            info[item[0]] = float(item[1][0:4])
        else:
            info[item[0]] = float(int(item[1]))
    print(len(info))
    print(info)  # 科技事件字典

    # 按时间顺序排序后的事件顺序
    list1 = sorted(info.values())  # 将时间按照从小到大的顺序排序

    # 前导科技事件表格
    print(list(zip(col3_0[1:], col3_1[1:])))
    count = 0
    mmm = 2
    for item in list(zip(col3_0[1:], col3_1[1:])):
        if item[1].strip() == "":
            count = count + 1

    print(len(list(zip(col3_0[1:], col3_1[1:]))))
    print("前导科技事件为空的科技事件的个数为%d" % count)
    print("文件读取完毕")

    for item in col0_4[1:]:
        if isinstance(item, str):  # 判断列表内的元素是否为字符串
            item = item[0:4]
            time.append(float(item))
        else:
            time.append(float(int(item)))
            # time.append(int(item))
    print(time)
    time.sort()  # 将科技事件的时间顺序进行排序
    # 排序后的时间
    print(time)

    print(len(time))
    time_set = set(time)
    print(len(time_set))  # 用来判断列表中是否有相等的元素
    new_time = list(time_set)
    new_time.sort()
    print(new_time)

    thing = []
    eventRelationship = [[0 for i in range(788)] for j in range(788)]
    # print(eventRelationship)
    for index, t in enumerate(time):
        if len(get_key(info, t)) == 1:
            key = get_key(info, t)[0]
            if not isinstance(key, str):
                key = str(key)[0:8]
            eventRelationship[index][index] = ''.join(str(get_key(info, t)[0:]))
            thing.append(''.join(key))
            # 查询此科技事件的前导事件
            for item in list(zip(col3_0[1:], col3_1[1:])):
                # if item[0] == get_key(info, t)[0] and item[1] != '':
                if item[0] == ''.join(key) and item[1] != '':
                    for index1, val in enumerate(thing):
                        if val == item[1]:
                            eventRelationship[index][index1] = item[1]
        if len(get_key(info, t)) > 1:
            key = get_key(info, t)[0]
            if not isinstance(key, str):
                key = str(key)[0:8]
            # print("此时间对应%d个科技事件"%len(get_key(info, t)))
            for index2, item in enumerate(get_key(info, t)):
                if item not in thing:
                    thing.append(item)
                    break
            num = len(get_key(info, t))  # 用来存储发生时间相同的科技事件个数
            eventRelationship[index][index] = thing[-1]
            for item in list(zip(col3_0[1:], col3_1[1:])):
                if item[0] == thing[-1] and item[1] != '':
                    for index1, val in enumerate(thing):
                        if val == item[1]:
                            eventRelationship[index][index1] = item[1]
        if len(get_key(info, t)) == 0:
            print("此时间没有对应的科技事件")
    print("事件导向关系建立完毕")
    for i in range(len(thing)):
        if not isinstance(thing[i], str):
            thing[i] = str(thing[i])[0:8]
    # 相关联科技事件之间的间隔
    step = []
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print('科技事件个数%d' % (len(set(thing))))
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # 开始对科技事件评分
    SCORE = []
    row = len(eventRelationship)  # 获取行数
    print(row)
    column = len(eventRelationship[0])  # 获取列数
    print(column)
    print('-------------------------')
    # count = 0  # 统计某行有多少个直接前导事件
    generation = 0  # 记录科技事件发生时间在网络中所处的代数
    # for r in range(242,243):
    for r in range(0, row):
        print("===============-========这是第%d行" % r)
        if r != 0:
            n = 0  # 对数组下标进行计数
            count = 0  # 统计该行有多少个直接前导事件
            for index, val in enumerate(eventRelationship[r]):
                if val != 0:
                    # print("index=%d"%index) #获取该值的下标
                    count = count + 1

            print(count)

            if count == 1:
                print("没有前导事件")
                changeScore = 0
                continue
            if count == 2:
                print("只有一个前导事件")

                changeScore = 1  # 将某个科技事件的得分按照前导事件的数量进行平分
            if count > 2:
                print("有多个前导事件")
                changeScore = 1 / (count - 1)  # 有多个前导事件时，前导事件平分得分的变化
            # print("changeScore=%f"%changeScore)
            # print("第" + str(r) + "行")
            # 取出对角线上事件，方便后续查找此事件在整个网络中所处的“代数”
            current_event = eventRelationship[r][r]
            if len(current_event) > 8:
                current_event = current_event[2:10]
            print("该代的科技事件为：" + current_event)
            # 在字典中查找此科技事件的发生的时间
            period = info[current_event]
            print("发生时间为：" + str(period))
            # 查找该事件在整个导向网络中所处的“代数”
            for index, val in enumerate(new_time):
                if val == period:
                    generation = index
                    print("在网络中处于第" + str(generation) + "代")

            for index, val1 in enumerate(eventRelationship[r]):
                if val1 != 0 and index < r:
                    period1 = info[val1]  # 找出该事件的时间
                    print(period1)
                    for index1, val in enumerate(new_time):
                        if val == period1:
                            generation1 = index1
                            print(str(period1) + "在网络中处于第" + str(generation1) + "代")

                    # myScore[index] = myScore[index] + changeScore / (math.pow(1.5, r - index - 1))
                    myScore[index] = myScore[index] + changeScore / (generation - generation1 + 1)
                    SCORE.append(myScore)
                    step.append(r - index)
            # print(myScore)
            if r > 1:  # 间接前导科技事件的得分计算
                for index, val in enumerate(eventRelationship[r]):
                    if val != 0 and index < r:
                        for index1, val1 in enumerate(eventRelationship[index]):
                            if val1 != 0:
                                count = count + 1
                        for index1, val1 in enumerate(eventRelationship[index]):
                            if count == 1:
                                # print("没有前导事件")
                                changeScore = 0
                                continue
                            if count == 2:
                                # print("只有一个前导事件")
                                changeScore = (myScore[index] - myScore1[index]) / 2  # 得分的变化
                            if count > 2:
                                changeScore = (myScore[index] - myScore1[index]) / (count - 1)  # 有多个前导事件时，前导事件平分得分的变化
                            if val1 != 0 and index1 < index:
                                current_event = eventRelationship[index][index]
                                # 在字典中查找此科技事件的发生的时间
                                if len(current_event) > 8:
                                    current_event = current_event[2:10]
                                period = info[current_event]
                                # print(period)
                                # 查找该事件在整个导向网络中所处的“代数”
                                for index2, val in enumerate(new_time):
                                    if val == period:
                                        generation = index2
                                        # print(generation)
                                if val1 != 0:
                                    period1 = info[val1]  # 找出该事件的时间
                                    for index3, val in enumerate(new_time):
                                        if val == period1:
                                            generation1 = index3

                                myScore[index1] = myScore[index1] + changeScore / (generation - generation1 + 1)
                                SCORE.append(myScore)
                        myScore1 = myScore
    print('评分计算完毕')
    x1 = []
    for item in list(zip(thing, time, myScore)):
        a = get_val(scienceThing, item[0])
        if len(a) > 0:
            item = list(item)
            print(item)
            print(a)
            x1.append([item[0], item[2], a[0][0], a[0][1], a[0][2], subject[a[0][3]]])
        # print(str(item) + '名称：' + str(a))
    x1.sort(key=takeSecond)
    db = pymysql.connect("localhost", "root", "123p123p", "temp")

    cursor = db.cursor()

    sql = "drop table %s" % "allthing"
    cursor.execute(sql)
    db.commit()

    sql = "create table %s(id varchar(50),level float ,name varchar(50),en_name varchar(50),time varchar(50) ,subject varchar(50))" % "allthing"
    cursor.execute(sql)
    db.commit()
    for i in x1:
        sql = "INSERT INTO %s (id,level,name,en_name,time,subject)VALUES ('%s','%f','%s','%s','%s','%s')" % (
            "allthing", i[0], i[1], i[2], i[3], i[4], i[5])
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    print("输入完成")

    db.close()
    return SCORE
