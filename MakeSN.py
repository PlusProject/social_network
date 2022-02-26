from ast import operator
import pandas as pd
import pymysql
import operator

def makeSocialNetwork(host,user,password,dbname):
    connect = pymysql.connect(host=host, user=user, password=password, db=dbname, charset='utf8mb4')
    cursor = connect.cursor()

    cursor.execute("select * from CoOccurence;")
    scholar= list(cursor.fetchall())
    connect.commit()
    group=[]
    for sc in scholar:
        group.append(sc[3].split(','))
    count={}
    for gr in group:
        for i, a in enumerate(gr):
            for b in gr[i+1:]:
                if a>b: x,y=b,a
                else: x,y=a,b
                count[x,y]=count.get((x,y),0)+1
    count= sorted(count.items(), key=operator.itemgetter(1),reverse=True)
    try:
        cursor.execute("drop table if EXISTS SN_paper;")
        cursor.execute("create table SN_paper (id int primary key, doctor1 mediumtext, doctor2 mediumtext, together int);")
        connect.commit()
    except:
        pass
    ch=0
    for c in count:
        ch+=1
        cursor.execute("INSERT INTO SN_paper (id,doctor1, doctor2, together) VALUES (%s,%s,%s,%s);",(ch,c[0][0],c[0][1],c[1]))
        connect.commit()
    df=pd.DataFrame(list(count),columns=['items', 'num'])
    df=df[df['num']>=0].sort_values(by='num', ascending=False)
    df=df.reset_index(drop=True)
    print(df)

    cursor.execute("select * from scholarwithname;")
    scholar= list(cursor.fetchall())
    connect.commit()
    doctor=[]
    for sc in scholar:
        check=0
        for doc in doctor:
            if sc[0]==doc[0]and sc[1]==doc[1]:
                doc[2]+=1
                check=1
                break
        if check==0:
            d=[]
            d.append(sc[0])
            d.append(sc[1])
            d.append(1)
            doctor.append(d)
    for doc in doctor:
        doc[0]=doc[0]+'|'+doc[1]
        doc[1]=doc[2]
        del doc[2]
    print(len(doctor))
    delete=[]
    for didx in range(len(doctor)):
        doc=doctor[didx]
        check=0
        for fa in df.values:
            if doc[0]in fa[0]:
                check=1
                break
        if check==0:
            delete.append(didx)
    delete.sort(reverse=True)
    for d in delete:
        del doctor[d]
    print(len(doctor))
    doctor.sort(key= lambda x: x[1],reverse=True)
    print(doctor)

    try:
        cursor.execute("drop table if EXISTS SN_paper_cnt;")
        cursor.execute("create table SN_paper_cnt (id int primary key, doctor mediumtext, paper_count int, disease varchar(10));")
        connect.commit()
    except:
        pass
    ch=0
    for doc in doctor:
        ch+=1
        cursor.execute("INSERT INTO SN_paper_cnt (id, doctor, paper_count) VALUES (%s,%s,%s);",(ch,doc[0],doc[1]))
        connect.commit()
