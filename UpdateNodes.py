import pymysql
import pandas as pd

def updateNodes(host,user,password):
    # mysql 연결
    conn = pymysql.connect(host=host, user=user, password=password, db='medii', charset='utf8mb4')
    curs = conn.cursor()

    sql1 = """SELECT * FROM medii.Nodes"""
    sql2 = """SELECT * FROM medii.cris_dataset_new"""

    curs.execute(sql1)
    rows_cris = curs.fetchall()
    cris = pd.DataFrame(rows_cris)
    cris = cris.fillna("")

    cris_data = pd.DataFrame({'id':cris['id'],'label':cris['label'],'belong':cris['belong'],'clinical_cnt':cris['clinical_cnt']})

    curs.execute(sql2)
    rows = curs.fetchall()
    cris2 = pd.DataFrame(rows)
    cris2 = cris2.fillna("")

    new_data = pd.DataFrame({'name':cris2['name'],'belong':cris2['belong'],'count':cris2['count']})

    df = pd.read_csv('total_name.csv')

    sql = "INSERT INTO medii.Nodes (id,label,disease,color,paper_cnt,clinical_cnt,belong) VALUES (%s, %s, %s, %s,%s,%s,%s)"
    #cris에만 해당하는 의사들에 대한 id, 이름, 질병코드, 병원색, 임상시험 및 논문 개수, 소속 병원 table에 추가

    for i in range(452,458):
        id = i + 47
        label = df.loc[i][0]
        disease = df.loc[i][4]
        paper_cnt = 0
        clinical_cnt = df.loc[i][6]
        belong = df.loc[i][3]

        #기존에 지정해둔 색과 소속병원을 맞춰서 입력
        if '삼성' in df.loc[i][3]:
            color = '#4ED4FE'
        elif '아산' in df.loc[i][3]:
            color = '#67F942'
        elif '세브란스' in df.loc[i][3]:
            color = '#FBFF38'
        elif '서울대' in df.loc[i][3]:
            color = '#DDB1FF'
        elif '가톨릭' in df.loc[i][3]:
            color = '#FFA7B1'
        elif '계명대' in df.loc[i][3]:
            color = '#FFB169'
        elif '고려' in df.loc[i][3]:
            color = '#FF6C7E'
        else:
            color = '#C4C4C4'

        curs.execute(sql, (str(id), str(label),str(disease),str(color),str(paper_cnt),str(clinical_cnt),str(belong)))
        conn.commit()
