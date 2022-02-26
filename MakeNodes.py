import pymysql

def makeNodes(host,user,password,dbname):
    connect = pymysql.connect(host=host, user=user, password=password, db=dbname, charset='utf8mb4')
    cursor = connect.cursor()

    connectn = pymysql.connect(host=host, user=user, password=password, db='medii', charset='utf8mb4')
    cursorn = connectn.cursor()

    cursor.execute("select * from SN_paper;")
    papers= list(cursor.fetchall())
    connect.commit()

    cursor.execute("select * from SN_paper_cnt;")
    paper_cnts= list(cursor.fetchall())
    connect.commit()

    nodes={}
    edges=[]
    maxed=papers[0][3]
    mined=papers[len(papers)-1][3]
    mined=50
    for paper in papers:
        doc1=paper[1]
        cnt=0
        dis=''
        if doc1 not in nodes:
            for pc in paper_cnts:
                if pc[1]==doc1:
                    cnt=pc[2]
                    if pc[3]==None:
                        dis='None'
                    else:
                        dis=pc[3]
                    break
            nodes[doc1]=[cnt,dis,len(nodes)+1]

        doc2=paper[2]
        cnt=0
        dis=''
        if doc2 not in nodes:
            for pc in paper_cnts:
                if pc[1]==doc2:
                    cnt=pc[2]
                    if pc[3]==None:
                        dis='None'
                    else:
                        dis=pc[3]
                    break
            nodes[doc2]=[cnt,dis,len(nodes)+1]
        fr=nodes.get(doc1)[2]
        to=nodes.get(doc2)[2]
        edges.append([fr,to,(paper[3]-mined+1)/(maxed-mined+1)*10])
    maxcnt=paper_cnts[0][2]
    try:
        cursorn.execute("if exists drop table Nodes;")
        cursorn.execute("create table Nodes (id int primary key, label mediumtext, disease mediumtext, color mediumtext, paper_cnt int, clinical_cnt int,belong mediumtext, borderWidth int);")
        connectn.commit()
    except:
        pass
    nodes=sorted(nodes.items(),key=lambda x:x[1],reverse=True)
    for node in nodes:
        size=node[1][0]
        dis=node[1][1]
        nid=node[1][2]
        name=node[0].split('|')[0]
        belong=node[0].split('|')[1]
        if '삼성' in belong:
            color='#4ED4FE'
        elif '아산' in belong:
            color='#67F942'
        elif '세브란스' in belong:
            color='#FBFF38'
        elif '서울대' in belong:
            color='#DDB1FF'
        elif '가톨릭' in belong:
            color='#FFA7B1'
        elif '계명대' in belong:
            color='#FFB169'
        elif '고려' in belong:
            color='#FF6C7E'
        else: 
            color='#C4C4C4'
        cursorn.execute("INSERT INTO Nodes (id , label, disease, color, paper_cnt, belong, clinical_cnt) VALUES (%s,%s,%s,%s,%s,%s,0);",(nid,name,dis,color,size,belong))
        connectn.commit()
