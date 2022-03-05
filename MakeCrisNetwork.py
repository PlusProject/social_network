import pymysql
import pandas as pd

# 임상시험에 참여한 의사들 간의 관계성을 찾기 위한 함수
def makeCrisNetwork(host,user,password,dbname):
    conn = pymysql.connect(host=host, user= user, password=password, db=dbname, charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql1 = """SELECT * FROM medii.cris_dataset"""
    sql2 = """SELECT * FROM doctor.doctor"""

    curs.execute(sql1)
    rows_cris = curs.fetchall()
    cris = pd.DataFrame(rows_cris)
    cris = cris.fillna("")

    curs.execute(sql2)
    rows_doc = curs.fetchall()
    doc = pd.DataFrame(rows_doc)
    doc = doc.fillna("")

    cris_data = pd.DataFrame({'title':cris['brief_title_kor'],'chief_name':cris['chief_name_kor'],'chief_belong':cris['chief_belong_kor'],'charge_name':cris['charge_name_kor'],'charge_belong':cris['charge_belong_kor'],'rm_name':cris['rm_name_kor'],'rm_belong':cris['rm_belong_kor']})
    cris_disease_code = pd.DataFrame({'code':cris['disease_code']})
    doc_data = pd.DataFrame({'name':doc['name_kor'],'belong':doc['belong'],'major':doc['major']})

    doc_list = []
    cris_list = []
    cris_doc_list = []

    cris_title_doc = {} # 임상시험명 - 참여한 의사 list
    cris_code = {}

    # 병원 명칭 통일
    df = pd.read_csv('hospital_name.csv')

    hospital = []
    hos_cris = []

    for i in range(len(df)):
        hospital.append(df.loc[i][0])
        hos_cris.append(df.loc[i][1])

    for i in range(len(doc_data)):
        if doc_data.loc[i][1] in hospital:
            doc_data.loc[i][1] = hos_cris[hospital.index(doc_data.loc[i][1])]

    for i in range(len(cris_data)):
        for j in range(1,4):
            cris_data.loc[i][j*2] = cris_data.loc[i][j*2].split('병원')[0]

    for i in range(len(doc_data)):
        doc_data.loc[i][1] = doc_data.loc[i][1].split('병원')[0]

    for i in range(len(doc_data)):
        doc_list.append(doc_data.loc[i][0] + "|" + doc_data.loc[i][1])

    doc_list = list(set(doc_list))

    for i in range(len(cris_data)):
        for j in range(1,4):
            cris_list.append(cris_data.loc[i][j * 2 - 1] + "|" + cris_data.loc[i][j * 2])

    cris_list = list(set(cris_list))

    # 같은 임상시험에 참여한 의사들 묶는 작업
    for item in cris_list:
        if item in doc_list:
            cris_doc_list.append(item)

    for i in range(len(cris_data)):
        if cris_data.loc[i][0] not in cris_title_doc:
            cris_title_doc[cris_data.loc[i][0]] = []

    for i in range(len(cris_data)):
        for j in range(1,4):
            if (cris_data.loc[i][j * 2 - 1] + "|" + cris_data.loc[i][j * 2]) in cris_doc_list:
                if (cris_data.loc[i][j * 2 - 1] + "|" + cris_data.loc[i][j * 2]) not in cris_title_doc[cris_data.loc[i][0]]:
                    cris_title_doc[cris_data.loc[i][0]].append(cris_data.loc[i][j * 2 - 1] + "|" + cris_data.loc[i][j * 2])

    for i in range(len(cris_data)):
      cris_code[cris_data.loc[i][0]]=cris_disease_code.loc[i][0]

    null_title = []

    for item in cris_title_doc:
      if len(cris_title_doc[item]) == 0:
        null_title.append(item)

    for item in null_title:
      del cris_title_doc[item]

    title_list = list(cris_title_doc.values())

    doc_cnt = {} # 의사별 참여한 임상시험 개수 list
    doc_code = {} # 의사별 질병코드를 묶어 놓은 dictionary

    for key, value in cris_title_doc.items():
        for items in title_list:
            items = tuple(items)
            doc_code[items] = []

    for key, value in cris_title_doc.items():
        for items in title_list:
            if items == value:
                items = tuple(items)
                doc_code[items].append(cris_code[key])

    for item in doc_code:
        doc_code[item] = list(set(doc_code[item]))

    null_code = []

    for item in doc_code:
        if len(item) == 1:
            null_code.append(item)
        if '' in doc_code[item][:]:
            doc_code[item].remove('')
            doc_code[item].append("null")

    for item in null_code:
      del doc_code[item]

    for item in doc_code:
        if len(doc_code[item][:])>1 and "null" in doc_code[item][:]:
            doc_code[item].remove("null")

    for item in doc_code:
        if len(doc_code[item]) > 1:
            str = ''
            for items in doc_code[item]:
                str += items
                str += ' '
            doc_code[item].clear()
            doc_code[item].append(str)


    print(doc_code)

    for item in cris_doc_list:
        doc_cnt[item] = 0

    for item in cris_doc_list:
        for j in range(len(cris_title_doc)):
            if item in title_list[j]:
                doc_cnt[item] += 1

    cris_relation = {} # 의사 이름, 횟수 연관 List (dict type)

    for item in cris_doc_list:
        cris_relation[item] = {}

    value_list = list(cris_title_doc.values())

    for item in value_list:
        item = tuple(set(item))

    for item in cris_doc_list:
        for j in range(len(value_list)):
            if item in value_list[j]:
                value_list[j] = tuple(value_list[j])
                if value_list[j] not in cris_relation[item]:
                    cris_relation[item][value_list[j]] = 1
                else:
                    cris_relation[item][value_list[j]] += 1

    new_list = list(cris_relation.values())

    # cris_relation dictionary 에서 value 값만 처리
    cris_relation_list = []

    for item in new_list:
        for i in range(len(list(item.keys()))):
            cris_relation_list.append(list(item.keys())[i])

    cris_relation_list = list(set(cris_relation_list))

    relation_list = []
    for item in cris_relation_list:
        relation_list.append(list(item))

    for item in relation_list[:]:
        if len(item) == 1:
            relation_list.remove(item)

    tmp = []
    for item in relation_list:
        tmp.append(tuple(item))

    new_relation = {}

    for items in new_list:
        for item in items:
            if item in tmp:
                new_relation[item] = items[item]

    relation_doc = []
    for item in new_relation:
        relation_doc.append(item[0])
        relation_doc.append(item[1])

    relation_doc = list(set(relation_doc))
    cnt = 0
    for item in new_relation:
        if item in doc_code:
            cnt+=1
    print(cnt)
    for item in relation_doc:
        print(item)
        print(doc_cnt[item])
        

    # db table 에 값 넣어주기
    sql_cnt = "INS기RT INTO network.SN_cris_cnt (doctor, count) VALUES (%s, %s)"
    
    for item in relation_doc:
        curs.execute(sql_cnt, (item, doc_cnt[item]))
        conn.commit()

    sql_doc = "INSERT INTO network.SN_cris (doctor1, doctor2, together, disease_code) VALUES (%s, %s, %s, %s)"

    for item in new_relation:
        curs.execute(sql_doc, (item[0],item[1],new_relation[item],doc_code[item]))
        conn.commit()

    conn.close()