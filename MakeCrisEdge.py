import pymysql

def makeCrisEdge(host,user,password,dbname):
    connectn = pymysql.connect(host=host, user=user, password=password, db=dbname, charset='utf8mb4')
    cursorn = connectn.cursor()

    connect = pymysql.connect(host=host, user=user, password=password, db='medii', charset='utf8mb4')
    cursor = connect.cursor()

    cursorn.execute("select * from cris_edge;")
    cris= list(cursorn.fetchall())
    connectn.commit()

    cursor.execute("select * from Nodes;")
    doctor= list(cursor.fetchall())
    connect.commit()
    newcris=[]
    for cc in cris:
        newcc=[]
        for doc in doctor:
            if cc[0]==doc[1]+'|'+doc[6]:
                break
        newcc.append(doc[0])

        for doc in doctor:
            if cc[1]==doc[1]+'|'+doc[6]:
                break
        newcc.append(doc[0])
        newcc.append(cc[2])
        newcc.append(cc[3])
        newcris.append(newcc)
    print(newcris)
    try:
        cursor.execute('drop table if exists cris_edge;')
        cursor.execute("create table cris_edge (id int primary key, fromit int, toit int, cnt int, title mediumtext);")
        connect.commit()
    except:
        pass
    cid=0
    for cc in newcris:
        cid+=1
        cursor.execute("INSERT INTO cris_edge (id, fromit , toit , cnt , title) VALUES (%s,%s,%s,%s,%s);",(cid,cc[0],cc[1],cc[2],cc[3]))
        connect.commit()
