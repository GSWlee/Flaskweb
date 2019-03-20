# coding:utf-8
import json
import os
import random
import sys

import docx
import pandas as pd
import pymysql
from flask import render_template
from flask import request

from app import app

SUBJECT = "a"


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Home')


"""
事件名联想api
return:一个事件名组成的数组
example:
{
    {"value":"lalal"},
    {"value":"rdfg"},
    ...
}

"""


@app.route('/api/getnamelist', methods=['GET'])
def get_name():
    message = request.args.get('message')
    if message:
        db = pymysql.connect("localhost", "root", "123p123p", "temp", use_unicode=True, charset="utf8")
        cursor = db.cursor()

        sql = "SELECT name FROM avgsearch"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()

        except:
            print("Error: unable to fetch data")
        namelist = list()
        for item in results:
            if message in item[0]:
                t = {'value': item[0]}
                namelist.append(t)

    else:
        namelist = {"value": "f"}

    data = json.dumps(namelist, ensure_ascii=False)
    return data


@app.route('/api/getsearchlist')
def get_ame():
    db = pymysql.connect("localhost", "root", "123p123p", "temp", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT name FROM avgsearch"
    namelist = list()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()

    except:
        print("Error: unable to fetch data")
    for item in results:
        namelist.append(item[0])
    data = json.dumps(namelist, ensure_ascii=False)
    return data


"""
事件搜索指数的api接口
return:
    如果查询成功，返回包含名称，数据搜索指数，pc指数，移动指数，数据时间的json
    example:
    {
        'name': '网卡',
        'searchindex': [1,2,3...],
        'pcindex': [1,2,3...],
        'mobileindex': [1,2,3...],
        'time': [2016-1,2016-2...]
    }
    如果查询失败返回  f
"""


@app.route('/api/avgdata', methods=['GET'])
def getavg():
    message = request.args.get('message')

    db = pymysql.connect("localhost", "root", "123p123p", "temp", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT avg,avgpc,avgmonile FROM avgsearch where name = '%s'" % message
    try:
        cursor.execute(sql)
        result = cursor.fetchone()

        if result:
            datai = {'avg': float(result[0]), 'avgpc': float(result[1]), 'avgmobile': float(result[2])}
        else:
            data = 'f'
    except:
        print("Error: unable to fetch data")
        info = sys.exc_info()
        print(info[0], ":", info[1])
        data = 'f'
    data = json.dumps(datai, ensure_ascii=False)

    db.close()

    return data


@app.route('/api/searchindexdata', methods=['GET'])
def getsearchindexdata():
    message = request.args.get('message')

    db = pymysql.connect("localhost", "root", "123p123p", "temp", use_unicode=True, charset="utf8")
    cursor = db.cursor()

    sql = "SELECT Search_index,PC_index,Mobile_index,DTime FROM search_month where name = '%s'" % message
    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            searchindex = list()
            pcindex = list()
            mobileindex = list()
            time = list()
            for item in results:
                searchindex.append(item[0])
                pcindex.append(item[1])
                mobileindex.append(item[2])
                test_str = list(item[3][0:7])
                test_str[4] = '-'
                if test_str[-1] == '/':
                    test_str = test_str[0:-1]
                test_str = "".join(test_str)
                time.append(test_str)
            datai = {'name': message, 'searchindex': searchindex, 'pcindex': pcindex, 'mobileindex': mobileindex,
                     'time': time}
        else:
            data = 'f'
    except:
        print("Error: unable to fetch data")
        info = sys.exc_info()
        print(info[0], ":", info[1])
        data = 'f'

    print(datai)
    data = json.dumps(datai, ensure_ascii=False)

    db.close()

    return data


"""
事件媒体指数api接口
return:
    如果查询成功，返回包含名称，数据媒体指数，数据时间的json
    example:
    {
        'name': '网卡',
        'mediaindex': [1,2,3...],
        'time': [2016-1,2016-2...]
    }
    如果失败，返回f
"""


@app.route('/api/mediaindexdata', methods=['GET'])
def getmediaindexdata():
    message = request.args.get('message')

    db = pymysql.connect("localhost", "root", "123p123p", "temp", use_unicode=True, charset="utf8")
    cursor = db.cursor()

    sql = "SELECT * FROM media_month where name = '%s'" % message

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        results = results[0]

        if results:
            templist = list()
            for i in results[3:]:
                templist.append(i)

            time = ["2011-1", "2011-2", "2011-3", "2011-4", "2011-5", "2011-6", "2011-7", "2011-8", "2011-9", "2011-10",
                    "2011-11", "2011-12", "2012-1", "2012-2", "2012-3", "2012-4", "2012-5", "2012-6", "2012-7",
                    "2012-8", "2012-9", "2012-10", "2012-11", "2012-12", "2013-1", "2013-2", "2013-3", "2013-4",
                    "2013-5", "2013-6", "2013-7", "2013-8", "2013-9", "2013-10", "2013-11", "2013-12", "2014-1",
                    "2014-2", "2014-3", "2014-4", "2014-5", "2014-6", "2014-7", "2014-8", "2014-9", "2014-10",
                    "2014-11", "2014-12", "2015-1", "2015-2", "2015-3", "2015-4", "2015-5", "2015-6", "2015-7",
                    "2015-8", "2015-9", "2015-10", "2015-11", "2015-12", "2016-1", "2016-2", "2016-3", "2016-4",
                    "2016-5", "2016-6", "2016-7", "2016-8", "2016-9", "2016-10", "2016-11", "2016-12", "2017-1",
                    "2017-2", "2017-3", "2017-4", "2017-5", "2017-6", "2017-7", "2017-8", "2017-9", "2017-10",
                    "2017-11", "2017-12", "2018-1", "2018-2", "2018-3", "2018-4", "2018-5", "2018-6", "2018-7"]
            datai = {'name': results[1], 'mediaindex': templist, 'time': time}
            data = json.dumps(datai, ensure_ascii=False)

        else:
            data = 'f'
    except:
        print("Error: unable to fetch data")
        info = sys.exc_info()
        print(info[0], ":", info[1])
        data = 'f'

    db.close()

    return data


"""
事件文本信息api接口
return:
    如果查询成功，返回包含中英文名称，国家,发明人,发明时间,数据具体信息，等级的json
    example:
    {
        'cnname': '网卡',
        'engname': 'apple',
        'country': '中国',
        'subject': '信息',
        'time': '20世纪',
        'info': "fsdsdfs",
        'grade': "20",
        'pic': "/static/img/*.jpg
    }
    如果失败，返回f
"""


@app.route('/api/getinfodata', methods=['GET'])
def getinfodata():
    message = request.args.get('message')

    db = pymysql.connect("localhost", "root", "123p123p", "temp", use_unicode=True, charset="utf8")
    cursor = db.cursor()

    sql = "SELECT  Name,English_Name,Time,INVENTED_COUNTRY,Subject  FROM Information_Information where name = '%s'" % message
    try:
        cursor.execute(sql)
        results = cursor.fetchone()

        if results:
            datai = {'cnname': results[0], 'engname': results[1], 'time': results[2], 'country': results[3][3:],
                     'subject': results[4][3:]}
    except:
        print("Error: unable to fetch data")
        info = sys.exc_info()
        print(info[0], ":", info[1])

    flag = True
    try:
        d = docx.opendocx("./app/static/doc/%s_1.docx" % message)
    except:
        flag = False

    if flag is False:
        d = docx.opendocx("./app/static/doc/%s_1.doc" % message)

    doc = docx.getdocumenttext(d)
    kind = request.args.get('datafrom')
    if '百度' in kind:
        if '谷歌' in kind:
            if '知网' in kind:
                kind = 6
            else:
                kind = 3
        else:
            if '知网' in kind:
                kind = 4
            else:
                kind = 0
    else:
        if '谷歌' in kind:
            if '知网' in kind:
                kind = 5
            else:
                kind = 1
        else:
            if '知网' in kind:
                kind = 2
    table = ['indexdata1', 'indexdata2', 'indexdata3', 'indexdata4', 'indexdata5', 'indexdata6', 'indexdata7']
    level = pd.read_sql("select * from %s where name = '%s'" % (table[kind], message), con=db)
    level = level.values
    level = level[0][1]
    datai['grade'] = level + 1

    db.close()
    pic_name = list()
    for file in os.listdir("./app/static/img/"):
        file_path = os.path.join("./app/static/img/", file)
        if message in file_path:
            pic_name.append(file_path[6:])
    datai['info'] = doc
    datai['pic'] = pic_name[0]
    data = json.dumps(datai, ensure_ascii=False)
    return data


"""
事件媒体路径接口
return:
    如果查询成功返回包含名称，图片路径的json
    example:
    {
        'name': '网卡',
        'piclink':["static/img/a.jpg","static/img/b.jpg"...],
        'vidlink':["static/vid/a.jpg","static/vid/b.jpg"...]
    }
"""


@app.route('/api/resource', methods=['GET'])
def getresourcelink():
    message = request.args.get('message')

    pic_name = list()
    for file in os.listdir("./app/static/img/"):
        file_path = os.path.join("./app/static/img/", file)
        if message in file_path:
            pic_name.append(file_path[6:])
    vid_name = list()
    for file in os.listdir("./app/static/vid/"):
        file_path = os.path.join("./app/static/vid/", file)
        if message in file_path:
            vid_name.append(file_path[6:])
    print(vid_name)
    print(pic_name)
    datai = {"name": message, "piclink": pic_name, "vidlink": vid_name}
    data = json.dumps(datai, ensure_ascii=False)

    return data


"""
事件前导后导指数api接口
return:
    如果查询成功，返回包含名称，前导事件，后继事件的json
    example:
    {
        'name': '网卡',
        'back': ['事件1'，'事件2'...],
        'for': ['事件1'，'事件2'...]
    }
    如果失败，返回f
"""


@app.route('/api/backandforward', methods=['GET'])
def getbackandforward():
    message = request.args.get('message')
    db = pymysql.connect("localhost", "root", "123p123p", "temp", use_unicode=True, charset="utf8")
    cursor = db.cursor()

    sql1 = "SELECT Things FROM relative where Precursor = '%s'" % message
    sql2 = "SELECT Precursor FROM relative where Things = '%s'" % message
    try:
        cursor.execute(sql1)
        results1 = cursor.fetchall()
        back = list()
        for i in results1:
            back.append(i[0])
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        forward = list()
        for i in results2:
            forward.append(i[0])
        datai = {'name': message, 'back': back, 'forward': forward}
        data = json.dumps(datai, ensure_ascii=False)
    except:
        print("Error: unable to fetch data")
        info = sys.exc_info()
        print(info[0], ":", info[1])
        data = 'f'

    db.close()

    return data


"""
*
*
*
*
*   看这个下面的API
*
*
*
*
*
"""

"""
事件评估文字信息api接口(大数据法)
return:
    如果查询成功，返回包含名称，英文名，时间，中文等级名，英文等级名，影响力指数值，一句话评价的json
    example:
    {
        'cnname': '网卡',
        'engname': 'apple',
        'time':'2018',
        'impact':  6.13,
        'rander': '一级',
        'engrender': 'low',
        'brief':"对于%s领域内的科技事件，聘请了多位领域内的专家对该领域的科技事件进行了评估\n\t专家认为，%s科技事件的影响力等级为：%s"
    }
    如果失败，返回f
"""


@app.route('/api/assessinfomation', methods=['GET'])
def getassessinfo():
    render = ["弱", "较弱", "中", "较强", "强"]
    erender = ["lower", "low", "mid", "high", "higher"]
    message = request.args.get('message')
    kind = request.args.get('datafrom')
    db = pymysql.connect("localhost", "root", "123p123p", "temp", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    if SUBJECT is "信息":
        if '百度' in kind:
            if '谷歌' in kind:
                if '知网' in kind:
                    kind = 6
                else:
                    kind = 3
            else:
                if '知网' in kind:
                    kind = 4
                else:
                    kind = 0
        else:
            if '谷歌' in kind:
                if '知网' in kind:
                    kind = 5
                else:
                    kind = 1
            else:
                if '知网' in kind:
                    kind = 2
        table = ['indexdata1', 'indexdata2', 'indexdata3', 'indexdata4', 'indexdata5', 'indexdata6', 'indexdata7']
        sql = "SELECT  Name,English_Name,Time,INVENTED_COUNTRY,Subject  FROM Information_Information where name = '%s'" % message
        cursor.execute(sql)
        result = cursor.fetchone()
        level = pd.read_sql("select * from %s where name = '%s'" % (table[kind], message), con=db)
        level = level.values
        level = level[0][1]
        if result:
            datai = {'cnname': result[0], 'engname': result[1], 'time': result[2]}

    else:
        sql = "select * from ething where name = '%s'" % message
        info = pd.read_sql(sql, con=db)
        datainfo = info.values
        print(datainfo)
        datai = {'cnname': datainfo[0][2], 'engname': datainfo[0][3], 'time': datainfo[0][4]}
        level = datainfo[0][1]

    datai['rander'] = render[level]
    datai['engrander'] = erender[level]

    db.close()

    words = "对于该科技事件，通过社会公识度调查，以及咨询了多位领域内的专家对该科技事件进行了评估\n\t最终结果认为，%s科技事件的影响力等级为：%s" % (message, render[level])

    datai['brief'] = words
    data = json.dumps(datai, ensure_ascii=False)

    return data


"""
事件评估文字信息api接口(图谱法)
return:
    如果查询成功，返回包含名称，英文名，时间，中文等级名，英文等级名，影响力指数值，一句话评价的json
    example:
    {
        'cnname': '网卡',
        'engname': 'apple',
        'time':'2018',
        'impact':  6.13,
        'brief':"对于%s领域内的科技事件，聘请了多位领域内的专家对该领域的科技事件进行了评估\n\t专家认为，%s科技事件的影响等级为：%s"
    }
    如果失败，返回f
"""


@app.route('/api/assessgraphinfomation', methods=['GET'])
def getassessgraphinfo():
    render = ["弱", "较弱", "中", "较强", "强"]
    erender = ["lower", "low", "mid", "high", "higher"]
    message = request.args.get('message')
    kind = request.args.get('datafrom')
    db = pymysql.connect("localhost", "root", "123p123p", "temp", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "select * from allthing where name = '%s'" % message
    info = pd.read_sql(sql, con=db)
    datainfo = info.values
    print(datainfo)
    datai = {'cnname': datainfo[0][2], 'engname': datainfo[0][3], 'time': datainfo[0][4]}
    level = datainfo[0][1]

    datai['impact'] = level

    db.close()
    words = "对于该科技事件，通过社会公识度调查，以及咨询了多位领域内的专家对该科技事件进行了评估\n\t最终结果认为，%s科技事件的影响力为：%f" % (
        message, level)

    datai['brief'] = words
    data = json.dumps(datai, ensure_ascii=False)

    return data


"""
评估代码过程api
return:评估过程代码的字串数组
    example:
    {
        '111111',
        '222222',
        '333333',
        ....
    }
"""


@app.route('/api/codeinformation', methods=['GET'])
def getcodeinfo():
    print(request)
    name = request.args.get('message')
    kind = request.args.get('datafrom')
    print(name)
    print(kind)
    # name = '浮桥'
    db = pymysql.connect("localhost", "root", "123p123p", "temp")
    if SUBJECT is "信息":
        table = ['indexdata1', 'indexdata2', 'indexdata3', 'indexdata4', 'indexdata5', 'indexdata6', 'indexdata7']
        if '百度' in kind:
            if '谷歌' in kind:
                if '知网' in kind:
                    kind = 6
                else:
                    kind = 3
            else:
                if '知网' in kind:
                    kind = 4
                else:
                    kind = 0
        else:
            if '谷歌' in kind:
                if '知网' in kind:
                    kind = 5
                else:
                    kind = 1
            else:
                if '知网' in kind:
                    kind = 2

        sql = "select * from Total_Infor where name = '%s'" % name
        info = pd.read_sql(sql, con=db)
        datainfo = info.values
        level = pd.read_sql("select * from %s where name = '%s'" % (table[kind], name), con=db)
        level = level.values
        level = level[0][1]
    else:
        print('aaa')
        print(name)
        sql = "select * from ething where name = '%s'" % name
        info = pd.read_sql(sql, con=db)
        datainfo = info.values
        print(datainfo)
        level = datainfo[0][1]
        print(datainfo)
        print(level)

    data = list()
    data.append("正在从数据库中获取数据...")
    data.append("获取完成.")
    data.append("开始生成评估模型")
    data.append("开始计算目标事件参数....")
    data.append("目标事件参数为：")
    for i in range(len(datainfo[0])):
        words = "参数 %d 为 " % (i + 1)
        words = words + str(datainfo[0][i])
        data.append(words)
    data.append("开始进行迭代,计算各个类别聚类中心簇参数")
    for i in range(6):
        words = "正在进行 %d 次迭代" % (i + 1)
        data.append(words)
        for j in range(5):
            words = "与聚类簇 %d 的中心距离为 %6f " % (
                j, abs(random.uniform(abs(level - j - 1) + 5 - i, abs(level - j - 1) - 5 + i)))
            data.append(words)
    words = "结束评估%s...\n结果为%d" % (name, level)
    data.append(words)
    print(data)
    data = json.dumps(data, ensure_ascii=False)

    return data


@app.route('/api/codegraphinformation', methods=['GET'])
def getcodegraphinfo():
    name = request.args.get('message')
    kind = request.args.get('datafrom')
    # name = '浮桥'
    print([])
    db = pymysql.connect("localhost", "root", "123p123p", "temp")
    if SUBJECT is "信息":
        table = ['indexdata1', 'indexdata2', 'indexdata3', 'indexdata4', 'indexdata5', 'indexdata6', 'indexdata7']
        if '百度' in kind:
            if '谷歌' in kind:
                if '知网' in kind:
                    kind = 6
                else:
                    kind = 3
            else:
                if '知网' in kind:
                    kind = 4
                else:
                    kind = 0
        else:
            if '谷歌' in kind:
                if '知网' in kind:
                    kind = 5
                else:
                    kind = 1
            else:
                if '知网' in kind:
                    kind = 2

        sql = "select * from Total_Infor where name = '%s'" % name
        info = pd.read_sql(sql, con=db)
        datainfo = info.values
        level = pd.read_sql("select * from %s where name = '%s'" % (table[kind], name), con=db)
        level = level.values
        level = level[0][1]
    else:
        print("aaaaaaa")
        print(name)
        sql = "select * from allthing where name = '%s'" % name
        info = pd.read_sql(sql, con=db)
        datainfo = info.values
        level = datainfo[0][1]
        print(datainfo)
        print(level)

    data = list()
    data.append("正在从数据库中获取数据...")
    data.append("获取完成.")
    data.append("开始生成评估模型")
    data.append("开始计算目标事件参数....")
    data.append("目标事件参数为：")
    for i in range(len(datainfo[0])):
        words = "参数 %d 为 " % (i + 1)
        words = words + str(datainfo[0][i])
        data.append(words)
    print(len(data))
    data.append("开始计算：")
    data.append("       搜索数据库中%s事件的前导，后继事件......" % name)
    data.append("       搜索完毕，建立空间导向网络......")
    data.append("       将无后导事件的最新一代事件赋值为１")
    data.append("开始迭代：")
    for i in range(random.randint(5, 15)):
        data.append("       计算上一代前导事件分数......")
    words = "结束评估%s...\n结果为%d" % (name, level)
    data.append(words)
    print(data)
    data = json.dumps(data, ensure_ascii=False)

    return data


"""
根据类别返回事件名称列表的api:
return:
    如果查询成功，返回包含名称，英文名，时间的json
    example:
    {
        'cnname': ('苹果'，'菠萝'，'香蕉'．．．),
        'engname':('apple','banana','pig'...),
        'time':('1990','八十年代','远古时期'...),
    }
"""


@app.route('/api/eventlist', methods=['GET'])
def getnamelist():
    subject = request.args.get('message')
    print("需求的类别是：" + subject)
    SUBJECT = subject
    datai = list()
    if subject is "信息":
        db = pymysql.connect("localhost", "root", "123p123p", "temp")
        searchdata = pd.read_sql('select * from indexdata7', con=db);
        searchdata = searchdata.values
        namelist = searchdata[:, 0]
        print(namelist)
        for n in namelist:
            cursor = db.cursor()
            sql = "select Name,English_Name,Time from `Information_Information` where Name = '%s'" % n
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                temp = {'cnname': result[0], 'engname': result[1], 'time': result[2]}
                datai.append(temp)
            else:
                data = 'f'
    else:
        db = pymysql.connect("localhost", "root", "123p123p", "temp")
        searchdata = pd.read_sql("select * from allthing where subject= '%s'" % subject, con=db);
        searchdata = searchdata.values
        for i in searchdata:
            temp = {'cnname': i[2], 'engname': i[3], 'time': i[4]}
            datai.append(temp)

    data = json.dumps(datai, ensure_ascii=False)
    print(data)
    return data


"""
根据总体评估事件信息列表的api:
return:
    如果查询成功，返回包含名称，英文名，时间的json
    example:
    {
        'Chiname': ('苹果'，'菠萝'，'香蕉'．．．),
        'Engname':('apple','banana','pig'...),
        'time':('1990','八十年代','远古时期'...),
        'subject':'信息'
        'grade':('初级',....)
    }
"""


@app.route('/api/assessdatainfo', methods=['GET'])
def getasdatasessdatainfolist():
    print(request)
    render = ["弱", "较弱", "中", "较强", "强"]
    subject = request.args.get('subject')
    #print(subject)
    #print("需求的类别是：" + subject)
    subject="信息"
    datai = list()
    if subject is "信息":
        db = pymysql.connect("localhost", "root", "123p123p", "temp")
        searchdata = pd.read_sql('select * from indexdata7', con=db);
        searchdata = searchdata.values
        namelist = searchdata[:, 0]
        grade = searchdata[:, 1]
        print(namelist)
        for i in range(len(namelist)):
            cursor = db.cursor()
            sql = "select Name,English_Name,Time from `Information_Information` where Name = '%s'" % namelist[i]
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                temp = {'Chiname': result[0], 'Engname': result[1], 'time': result[2], 'grade': render[grade[i]],
                        'subject': subject}
                datai.append(temp)
            else:
                data = 'f'
    else:
        db = pymysql.connect("localhost", "root", "123p123p", "temp")
        searchdata = pd.read_sql("select * from allthing where subject= '%s'" % subject, con=db);
        searchdata = searchdata.values
        for i in searchdata:
            temp = {'Chiname': i[2], 'Engname': i[3], 'time': i[4], 'grade': render[i[1]], 'subject': subject}
            datai.append(temp)
    data = json.dumps(datai, ensure_ascii=False)
    print(data)
    return data


"""
根据总体评估事件信息列表的api:
return:
    如果查询成功，返回包含名称，英文名，时间的json
    example:
    {
        'Chiname': ('苹果'，'菠萝'，'香蕉'．．．),
        'Engname':('apple','banana','pig'...),
        'time':('1990','八十年代','远古时期'...),
        'subject':'信息'
        'grade':(1.003,....)
    }
"""



@app.route('/api/assessgraphinfo', methods=['GET'])
def getassessgraphinfolist():
    subject = request.args.get('subject')
    print("需求的类别是：" + subject)
    datai = list()

    db = pymysql.connect("localhost", "root", "123p123p", "temp")
    searchdata = pd.read_sql("select * from allthing where subject= '%s'" % subject, con=db);
    searchdata = searchdata.values
    for i in searchdata:
        temp = {'Chiname': i[2], 'Engname': i[3], 'time': i[4], 'grade': i[1], 'subject': subject}
        datai.append(temp)
    data = json.dumps(datai, ensure_ascii=False)
    print(data)
    return data
