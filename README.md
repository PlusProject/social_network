# Social Network

## Node
1. MakeCoOccur.py 실행  
> scholar와 scholarwithname -> CoOccurence  
> 각 논문마다 공동작가 표시  
2. MakeSN.py, UpdateSN.py 실행  
> doctor_scholar + CoOccurence -> SocialNetwork(SN_paper, SN_paper_cnt)  
> 의료진 간의 공동작업 수, 각 의료진의 논문 작성수 + 대표 질병코드 표시  
3. MakeNodes.py, (cris 정보 추가하는 파이썬 코드) 실행  
> SocialNetwork + (임상시험 정보 추가에 필요한 테이블 이름) -> Nodes  
> 논문 또는 임상시험 공동작업 활동을 한 의료진들의 노드화  

## Edge
### 논문
1. MakePaperYearEdge.py 실행  
> 전체 의료진 및 개별 의료진 추천에 사용  
> 년도별 논문 작성수 및 의료진 간의 대표 질병코드 표시  
> CoOccurence -> SN_paper_edge_year  
2. MakePaperYearDiseaseEdge.py 실행
> 추천 후 의료진 추천에 사용  
> 년도 별 각 질병코드의 논문 수 표시
> (scholar_year 만들 때 필요한 테이블) -> scholar_year

### 임상시험
1. MakeCrisEdge.py 실행
> 의료진 간의 질병코드 및 임상시험 수 표시  
> (cris_edge 만들 때 필요한 테이블) -> cris_edge
