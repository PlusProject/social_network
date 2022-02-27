import pymysql
import pandas as pd

def CrisWithBelong(host,user,password):
    # mysql 연결
    conn = pymysql.connect(host=host, user=user, password=password, db='medii', charset='utf8mb4')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql1 = """SELECT * FROM medii.node_cris"""
    sql2 = """SELECT * FROM network.SN_paper"""

    curs.execute(sql1)
    rows_cris = curs.fetchall()
    cris = pd.DataFrame(rows_cris)
    cris = cris.fillna("")

    curs.execute(sql2)
    rows_paper = curs.fetchall()
    paper = pd.DataFrame(rows_paper)
    paper = paper.fillna("")

    cris_data = pd.DataFrame({'id':cris['id'],'label':cris['label'], 'title' :cris['title'],'shape':cris['shape'],'color':cris['color'],'size':cris['size']})
    paper_data = pd.DataFrame({'doctor1':paper['doctor1'], 'doctor2':paper['doctor2']})

    #node 색깔별로 병원명을 매치하기위한 table
    column = []
    for i in range(len(cris_data)):
        if cris_data.loc[i][4] == "#FFB169":
            column.append("계명대학교동산병원")
        if cris_data.loc[i][4] == "#FFA7B1":
            column.append("가톨릭대학교서울성모병원")
        if cris_data.loc[i][4] == "#FF6C7E":
            column.append("고려대학교안암병원")
        if cris_data.loc[i][4] == "#FBFF38":
            column.append("연세대학교세브란스병원")
        if cris_data.loc[i][4] == "#DDB1FF":
            column.append("분당서울대학교병원")
        if cris_data.loc[i][4] == "#C4C4C4":
            column.append("경상국립대학교병원")
        if cris_data.loc[i][4] == "#67F942":
            column.append("서울아산병원")
        if cris_data.loc[i][4] == "#4ED4FE":
            column.append("삼성서울병원")

    #table안에 병원이름을 포함한 node list 추가
    sql = "INSERT INTO medii.node_cris_belong (id,label,title,shape,color,size,belong) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    for i in range(len(cris_data)):
        curs.execute(sql, (cris_data.loc[i][0],cris_data.loc[i][1],cris_data.loc[i][2],cris_data.loc[i][3],cris_data.loc[i][4],cris_data.loc[i][5],column[i]))
        conn.commit()

    conn.close()
