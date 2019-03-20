
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
