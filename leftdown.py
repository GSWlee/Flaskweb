
@app.route('/api/eventlist')
def getnamelist():
    db = pymysql.connect("localhost", "root", "123p123p", "temp")
    searchdata = pd.read_sql('select Name,DTime,Search_index from search_month', con=db);
    aaa = pd.read_sql('select * from NYX', con=db);
    searchdata = searchdata.values
    namelist = searchdata[:, 0]
    q = list()
    for i in namelist:
        if i not in q:
            q.append(i)
    Time = list()
    for n in q:
        cursor = db.cursor()
        sql = "select Name,English_Name,Time from `Information_Information` where Name = '%s'" % n
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            Time.append(result)
        else:
            data = 'f'
    Time = json.dumps(Time, ensure_ascii=False)
    return Time