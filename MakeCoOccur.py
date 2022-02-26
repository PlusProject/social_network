import pymysql

def makeCoOccurence(host,user,password,dbname):
    connect = pymysql.connect(host=host, user=user, password=password, db=dbname, charset='utf8mb4')
    cursor = connect.cursor()
    
    cursor.execute("select * from scholarwithname;")
    scholarwithname= list(cursor.fetchall())
    connect.commit()

    cursor.execute("select * from scholar;")
    scholar= list(cursor.fetchall())
    connect.commit()
    new=[]
    for sc in scholar:
        s=[]
        s.append(sc[0])
        s.append(sc[3])
        s.append(sc[1])
        auth=''
        for swn in scholarwithname:
            if sc[0]==swn[2] and sc[3]==swn[5]:
                if auth=='':
                    auth=swn[0]+'|'+swn[1]
                else:
                    auth+=','+swn[0]+'|'+swn[1]
        s.append(auth)
        s.append(sc[len(sc)-1])
        new.append(s)
    print(new)
    try:
        cursor.execute("drop table if EXISTS CoOccurence;")
        cursor.execute("create table CoOccurence (title mediumtext, journal mediumtext, year int, authors mediumtext, disease mediumtext);")
        connect.commit()
    except:
        pass
    for cooc in new:
        cursor.execute("INSERT INTO CoOccurence (title , journal , year , authors , disease) VALUES (%s,%s,%s,%s,%s);",(cooc[0],cooc[1],cooc[2],cooc[3],cooc[4]))
        connect.commit()
