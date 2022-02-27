import pymysql
import pandas as pd

def makePYDE(host,user,password):
    # mysql 연결
    conn = pymysql.connect(host=host, user=user, password=password, db='medii', charset='utf8mb4')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    # 의사별 질병코드 연구년도 가져오기
    sql1 = """SELECT * FROM network.new_scholar_year"""

    curs.execute(sql1)
    rows_scholar = curs.fetchall()
    scholar = pd.DataFrame(rows_scholar)
    scholar = scholar.fillna("")

    scholar_data = pd.DataFrame({'id':scholar['id'],'name':scholar['name'],'belong':scholar['belong'],'title':scholar['title'],'year':scholar['year'],'disease':scholar['disease']})

    dict = {}


    # dictionary : key = 논문제목, value = 참여한 사람 id, 작성 년도, 질병코드
    for i in range(len(scholar_data)):
        if scholar_data.loc[i][3] not in dict:
            dict[scholar_data.loc[i][3]] = []
            dict[scholar_data.loc[i][3]].append(scholar_data.loc[i][4])
            dict[scholar_data.loc[i][3]].append(scholar_data.loc[i][5])
            dict[scholar_data.loc[i][3]].append([])

    for i in range(len(scholar_data)):
        dict[scholar_data.loc[i][3]][2].append(scholar_data.loc[i][0])

    print(dict)

    for item in dict:
        id_list = dict[item][2]
        for i in range(len(id_list)):
            for j in range(i+1,len(id_list)):
                new_set = []
                new_set.append(id_list[i])
                new_set.append(id_list[j])
                new_set = tuple(new_set)
                dict[item].append(new_set)

    new_dict = {}
    for item in dict:
       if (len(dict[item][2])>1):
           for i in range(3,len(dict[item])):
               if dict[item][i] not in new_dict:
                   a = dict[item][i]
                   new_dict[a] = {}

    for item in dict:
       if (len(dict[item][2])>1):
           for i in range(3,len(dict[item])):
               a = dict[item][i]
               new_dict[a][dict[item][0]] = {}

    for item in dict:
       if (len(dict[item][2]) > 1):
           for i in range(3, len(dict[item])):
               a = dict[item][i]
               if(dict[item][1]) not in new_dict[a][dict[item][0]]:
                new_dict[a][dict[item][0]][dict[item][1]] = 1
               else:
                   new_dict[a][dict[item][0]][dict[item][1]] += 1


    # 논문 제목별로 의사들 간의 관계성 나타낸 dictionary

    relation_dict = {}
    for items in new_dict:
        relation_dict[items] = {}
        for item in new_dict[items]:
            if(int(item)>2005) :
                relation_dict[items][item] = ""
            elif (int(item)<=2005):
                relation_dict[items]['2005'] = ""

    for items in new_dict:
        for item in new_dict[items]:
            for i in new_dict[items][item]:
                if int(item) > 2005:
                    if i != "":
                        relation_dict[items][item] += i
                    else:
                        relation_dict[items][item] += "None"
                    relation_dict[items][item] += ":"
                    relation_dict[items][item] += str(new_dict[items][item][i])
                    relation_dict[items][item] += "|"
                elif int(item) <= 2005:
                    if i != "":
                        relation_dict[items]['2005'] += i
                    else:
                        relation_dict[items]['2005'] += "None"
                    relation_dict[items]['2005'] += ":"
                    relation_dict[items]['2005'] += str(new_dict[items][item][i])
                    relation_dict[items]['2005'] += "|"

    total_dict = {}

    for items in new_dict:
        cnt = 0
        for item in new_dict[items]:
            for i in new_dict[items][item]:
                cnt += new_dict[items][item][i]
        total_dict[items] = cnt

    a2021 = ""
    a2020 = ""
    a2019 = ""
    a2018 = ""
    a2017 = ""
    a2016 = ""
    a2015 = ""
    a2014 = ""
    a2013 = ""
    a2012 = ""
    a2011 = ""
    a2010 = ""
    a2009 = ""
    a2008 = ""
    a2007 = ""
    a2006 = ""
    a2005 = ""

    # db에 추가

    sql = "INSERT INTO medii.scholar_year (id,fromit,toit, total,y2021,y2020,y2019,y2018,y2017,y2016,y2015,y2014,y2013,y2012,y2011,y2010,y2009,y2008,y2007,y2006,to2005) VALUES (%s, %s, %s, %s, %s,%s,%s, %s, %s, %s, %s,%s,%s, %s, %s, %s, %s,%s,%s, %s, %s)"

    id = 1

    for items in relation_dict:
        year_list = []

        for item in relation_dict[items]:
            year_list.append(item)

        if '2021' in year_list:
            a2021 = relation_dict[items]['2021'][:-1]
        else:
            a2021 = ''
        if '2020' in year_list:
            a2020 = relation_dict[items]['2020'][:-1]
        else:
            a2020 = ''
        if '2019' in year_list:
            a2019 = relation_dict[items]['2019'][:-1]
        else:
            a2019 = ''
        if '2018' in year_list:
            a2018 = relation_dict[items]['2018'][:-1]
        else:
            a2018 = ''
        if '2017' in year_list:
            a2017 = relation_dict[items]['2017'][:-1]
        else:
            a2017 = ''
        if '2016' in year_list:
            a2016 = relation_dict[items]['2016'][:-1]
        else:
            a2016 = ''
        if '2015' in year_list:
            a2015 = relation_dict[items]['2015'][:-1]
        else:
            a2015 = ''
        if '2014' in year_list:
            a2014 = relation_dict[items]['2014'][:-1]
        else:
            a2014 = ''
        if '2013' in year_list:
            a2013 = relation_dict[items]['2013'][:-1]
        else:
            a2013 = ''
        if '2012' in year_list:
            a2012 = relation_dict[items]['2012'][:-1]
        else:
            a2012 = ''
        if '2011' in year_list:
            a2011 = relation_dict[items]['2011'][:-1]
        else:
            a2011 = ''
        if '2010' in year_list:
            a2010 = relation_dict[items]['2010'][:-1]
        else:
            a2010 = ''
        if '2009' in year_list:
            a2009 = relation_dict[items]['2009'][:-1]
        else:
            a2009 = ''
        if '2008' in year_list:
            a2008 = relation_dict[items]['2008'][:-1]
        else:
            a2008 = ''
        if '2007' in year_list:
            a2007 = relation_dict[items]['2007'][:-1]
        else:
            a2007 = ''
        if '2006' in year_list:
            a2006 = relation_dict[items]['2006'][:-1]
        else:
            a2006 = ''
        if '2005' in year_list:
            a2005 = relation_dict[items]['2005'][:-1]
        else:
            a2005 = ''
        new_id = int(id)
        item1 = int(items[0])
        item2 = int(items[1])
        total = int(total_dict[items])
        curs.execute(sql, (new_id,item1,item2,total,a2021,a2020,a2019,a2018,a2017,a2016,a2015,a2014,a2013,a2012,a2011,a2010,a2009,a2008,a2007,a2006,a2005))
        conn.commit()

        id += 1

    conn.close()
