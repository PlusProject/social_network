import pymysql

def makeNetworkCrisEdge(host,user,password,dbname):
    connectn = pymysql.connect(host=host, user=user, password=password, db=dbname, charset='utf8mb4')
    cursorn = connectn.cursor()

    connect = pymysql.connect(host=host, user=user, password=password, db='medii', charset='utf8mb4')
    cursor = connect.cursor()
    
    cursor.execute("select * from node_cris_belong;")
    cris= list(cursor.fetchall())
    connect.commit()
    
    cursor.execute("select * from node_cris_cnt;")
    criscnt= list(cursor.fetchall())
    connect.commit()
    newcris=[]
    for cc in criscnt:
        newcc=[]
        for cr in cris:
            if cc[1]==cr[0]:
                break
        newcc.append(cr[1]+'|'+cr[6])
    
        for cr in cris:
            if cc[2]==cr[0]:
                break
        newcc.append(cr[1]+'|'+cr[6])
        newcc.append(round(cc[3]/10*11))
        newcc.append(cc[4])
        newcris.append(newcc)
    try:
        cursorn.execute('drop table if exists cris_edge;')
        cursorn.execute("create table cris_edge ( fromit mediumtext, toit mediumtext, cnt int, title mediumtext);")
        connectn.commit()
    except:
        pass
    for cc in newcris:
        cursorn.execute("INSERT INTO cris_edge ( fromit , toit , cnt , title) VALUES (%s,%s,%s,%s);",(cc[0],cc[1],cc[2],cc[3]))
        connectn.commit()
