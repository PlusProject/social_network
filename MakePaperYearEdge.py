import pymysql

def makePYE(host,user,password,dbname):
    connect = pymysql.connect(host=host, user=user, password=password, db=dbname, charset='utf8mb4')
    cursor = connect.cursor()

    connectn = pymysql.connect(host=host, user=user, password=password, db='medii', charset='utf8mb4')
    cursorn = connectn.cursor()
    
    cursor.execute("select * from CoOccurence;")
    scholar= list(cursor.fetchall())
    connect.commit()
    
    cursorn.execute("select * from Nodes;")
    doctor= list(cursorn.fetchall())
    connectn.commit()
    
    group=[]
    for sc in scholar:
        group.append(sc[3].split(','))
    count={}
    for gidx,gr in enumerate(group):
        for i, a in enumerate(gr):
            for b in gr[i+1:]:
                if a>b: x,y=b,a
                else: x,y=a,b
                if (x,y) in count:
                    co=count.get((x,y))
                    co[int(scholar[gidx][2])]=co.get(int(scholar[gidx][2]),0)+1
                    dis=co['disease']
                    if scholar[gidx][4] in dis.keys():
                        dis[scholar[gidx][4]]+=1
                    else:
                        dis[scholar[gidx][4]]=1
                    co['disease']=dis
                    co['total']+=1
                    count[(x,y)]=co
                else:
                    co={}
                    co['total']=1
                    co['disease']={scholar[gidx][4]:1}
                    co[int(scholar[gidx][2])]=1
                    count[(x,y)]=co
    count= sorted(count.items(), key=lambda x: x[1]['total'],reverse=True)
    
    try:
        cursorn.execute('drop table if exists SN_paper_edge_year;')
        cursorn.execute("create table SN_paper_edge_year (id int primary key, fromit int, toit int, disease mediumtext , together int,y2021 int, y2020 int, y2019 int, y2018 int, y2017 int, y2016 int, y2015 int, y2014 int, y2013 int, y2012 int, y2011 int, y2010 int, y2009 int, y2008 int, y2007 int, y2006 int, to2005 int);")
        connectn.commit()
    except:
        pass
    ch=0
    for c in count:
        ch+=1
        toget=c[1]
        to2005=0
        dis=toget['disease']
        dis= sorted(dis.items(), key=lambda x: x[1],reverse=True)
        if dis[0][0]==None:
            try:
                dis=dis[1][0]
            except:
                dis=None
        else:
            dis=dis[0][0]
        for i in range(1972,2006):
            to2005+=toget.get(i,0)
        for doc in doctor:
            if doc[1] in c[0][0] and doc[6] in c[0][0]:
                doc1=doc[0]
                break
        for doc in doctor:
            if doc[1] in c[0][1] and doc[6] in c[0][1]:
                doc2=doc[0]
                break
        cursorn.execute("INSERT INTO SN_paper_edge_year (id, fromit, toit, disease, together, y2021, y2020, y2019, y2018, y2017, y2016, y2015, y2014, y2013, y2012, y2011, y2010, y2009, y2008, y2007, y2006, to2005) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(ch,doc1,doc2,dis,c[1].get('total'),c[1].get(2021,0),c[1].get(2020,0),c[1].get(2019,0),c[1].get(2018,0),c[1].get(2017,0),c[1].get(2016,0),c[1].get(2015,0),c[1].get(2014,0),c[1].get(2013,0),c[1].get(2012,0),c[1].get(2011,0),c[1].get(2010,0),c[1].get(2009,0),c[1].get(2008,0),c[1].get(2007,0),c[1].get(2006,0),to2005))
        connectn.commit()
