@app.route('/api/assessinfomation', methods=['GET'])
def getassessinfo():
    print(request)
    message = request.args.get('message')
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
    render = ["弱", "较弱", "中", "较强", "强"]
    erender = ["lower", "low", "mid", "high", "higher"]
    table = ['indexdata1', 'indexdata2', 'indexdata3', 'indexdata4', 'indexdata5', 'indexdata6', 'indexdata7']
    db = pymysql.connect("localhost", "root", "123p123p", "temp", use_unicode=True, charset="utf8")
    cursor = db.cursor()

    sql = "SELECT  Name,English_Name,Time,INVENTED_COUNTRY,Subject  FROM Information_Information where name = '%s'" % message
    try:
        cursor.execute(sql)
        result = cursor.fetchone()

        if result:
            datai = {'chiname': result[0], 'engname': result[1], 'time': result[2]}
    except:
        print("Error: unable to fetch data")
        info = sys.exc_info()
        print(info[0], ":", info[1])

    level = pd.read_sql("select * from %s where name = '%s'" % (table[kind], message), con=db)
    level = level.values
    level = level[0][1]
    datai['rander'] = render[level]
    datai['engrander'] = erender[level]
    ans = (random.uniform(2 * (level + 1), 2 * (level + 2)))
    datai['impact'] = ans - ans % 0.01

    db.close()
    words = "对于%s领域内的科技事件，聘请了多位领域内的专家对该领域的科技事件进行了评估\n\t专家认为，%s科技事件的影响力等级为：%s" % (
        result[4][3:], message, render[level])
    datai['brief'] = words
    data = json.dumps(datai, ensure_ascii=False)

    return data