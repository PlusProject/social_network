import pymysql

def updateSocialNetwork(host,user,password,dbname):
    connect = pymysql.connect(host=host, user=user, password=password, db=dbname, charset='utf8mb4')
    cursor = connect.cursor()
    
    connectn = pymysql.connect(host=host, user=user, password=password, db='Taehyun', charset='utf8mb4')
    cursorn = connectn.cursor()

    cursorn.execute("select * from doctor_top;")
    doctor= list(cursorn.fetchall())
    connectn.commit()
    
    cursor.execute("select * from SN_paper_cnt;")
    papercnt= list(cursor.fetchall())
    connect.commit()

    dc=len(papercnt)
    for paper in papercnt:
        ch=0
        for doc in doctor:
            if doc[3] in paper[1] and doc[4] in paper[1]:
                ch=1
                break
        if ch!=0:
            cursor.execute("UPDATE SN_paper_cnt SET disease=%s where doctor = %s;",(doc[2],paper[1]))
            connect.commit()
