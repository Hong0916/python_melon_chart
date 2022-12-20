# -*- coding: utf-8 -*-

import pandas as pd
from konlpy.tag import Okt # class 
from collections import Counter

# 1985년부터 2021년까지 각 년도 TOP100 노래 데이터 가져오기
melon_fin = pd.read_csv('C:/Users/hsh97/Desktop/data/melon_fin.csv', encoding = 'utf-8')
melon_fin.info()
'''
RangeIndex: 3699 entries, 0 to 3698
Data columns (total 7 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   제목      3699 non-null   object
 1   가수      3699 non-null   object
 2   장르      3699 non-null   object
 3   가사      3621 non-null   object
 4   좋아요     3699 non-null   object
 5   년도      3699 non-null   int64 
 6   노래번호    3699 non-null   int64 
dtypes: int64(2), object(5)
'''
melon_fin.head()
'''
             제목    가수             장르  ...    좋아요    년도     노래번호
0  이젠 사랑할 수 있어요  해바라기         포크/블루스  ...    774  1985  2036556
1   어제, 오늘, 그리고   조용필           록/메탈  ...  1,631  1985    68142
2           희나리   구창모  발라드, 성인가요/트로트  ...  6,072  1985  3328252
3  아직도 어두운 밤인가봐   전영록             댄스  ...  1,054  1985    48478
4     모두가 사랑이예요  해바라기         포크/블루스  ...    510  1985   992352

[5 rows x 7 columns]
'''

# 가사가 없는 결측값 제거
melon_fin = melon_fin.dropna()
melon_fin.info()
'''
Int64Index: 3621 entries, 0 to 3698
Data columns (total 7 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   제목      3621 non-null   object
 1   가수      3621 non-null   object
 2   장르      3621 non-null   object
 3   가사      3621 non-null   object
 4   좋아요     3621 non-null   object
 5   년도      3621 non-null   int64 
 6   노래번호    3621 non-null   int64 
dtypes: int64(2), object(5)
'''

# 좋아요 같은 경우 숫자가 문자형으로 나타나있어 숫자형으로 변환
# ','가 있어서 문자형으로 인식하기 때문에 ','를 ''로 변환(없애는 것)후 타입 변환
melon_fin['좋아요'] = pd.to_numeric(melon_fin['좋아요'].str.replace(',', ''))
melon_fin.info()
'''
Int64Index: 3621 entries, 0 to 3698
Data columns (total 7 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   제목      3621 non-null   object
 1   가수      3621 non-null   object
 2   장르      3621 non-null   object
 3   가사      3621 non-null   object
 4   좋아요     3621 non-null   int64 
 5   년도      3621 non-null   int64 
 6   노래번호    3621 non-null   int64 
dtypes: int64(3), object(4)
'''


# 중복 노래 제거
melon_fin = melon_fin.drop_duplicates(['제목'])
melon_fin.info()
'''
Int64Index: 3099 entries, 0 to 3620
Data columns (total 8 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   제목      3099 non-null   object 
 1   가수      3099 non-null   object 
 2   장르      3099 non-null   object 
 3   가사      3099 non-null   object 
 4   좋아요     3099 non-null   int64  
 5   년도      3099 non-null   int64  
 6   노래번호    3099 non-null   int64  
 7   좋아요퍼센트  3099 non-null   float64
dtypes: float64(1), int64(3), object(4)
memory usage: 217.9+ KB
'''


# 인덱스 재설정
melon_fin = melon_fin.reset_index()
melon_fin = melon_fin.drop(['index'], axis = 1)
melon_fin.info()
melon_fin.head()
'''
RangeIndex: 3099 entries, 0 to 3098
Data columns (total 7 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   제목      3099 non-null   object
 1   가수      3099 non-null   object
 2   장르      3099 non-null   object
 3   가사      3099 non-null   object
 4   좋아요     3099 non-null   int64 
 5   년도      3099 non-null   int64 
 6   노래번호    3099 non-null   int64 
dtypes: int64(3), object(4)
memory usage: 169.6+ KB
'''
## 가사 대소문자 소문자로 모두 바꾸기
가사줄이기 = []
for i in melon_fin['가사']:
    a = i.lower()
    가사줄이기.append(a)

len(가사줄이기)
melon_fin['가사'] = 가사줄이기


##############################
### Okt
### 가사 키워드 추출
##############################
okt = Okt() # 객체 생성 

# 단어 추출 : 명사, 영문 

# 단어 사이에 ", "를 포함시키는 함수
def listToString(str_list):
    result = ""
    for s in str_list:
        result += s + ", "
    return result.strip()

키워드 = []

for i in range(0, int(len(melon_fin))):
    nouns = []                                          
    for word, wclass in okt.pos(melon_fin['가사'][i]) :   
        if wclass == 'Noun' or wclass == 'Alpha' :
            nouns.append(word)
    
    counter = Counter(nouns)
    counter = dict(counter)
    x = {key: value for key, value in counter.items()}
    x = list(x)
    x = listToString(x)
    키워드.append(x)

키워드[1]

melon_fin['키워드'] = 키워드
melon_fin.head()
melon_fin.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3621 entries, 0 to 3620
Data columns (total 8 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   제목      3621 non-null   object
 1   가수      3621 non-null   object
 2   장르      3621 non-null   object
 3   가사      3621 non-null   object
 4   좋아요     3621 non-null   int64 
 5   년도      3621 non-null   int64 
 6   노래번호    3621 non-null   int64 
 7   키워드     3621 non-null   object
dtypes: int64(3), object(5)
memory usage: 226.4+ KB
'''


###########################################################
## 좋아요 수 비율로 나타내기
###########################################################

좋아요퍼센트 = []
for i in range(1985,2022):
    x = melon_fin[(melon_fin['년도'] == i)]
    for a in range(0, int(len(x['좋아요']))):
        y = x['좋아요'][x.index[a]] / x['좋아요'].sum()*100
        y = round(y, 3)
        좋아요퍼센트.append(y)
    
melon_fin['좋아요퍼센트'] = 좋아요퍼센트

melon_fin.info()

###########################################################
## 함수 작성
###########################################################
def melon_find (lyric, artist, genre, year):
    if lyric != 'NA':
        A = melon_fin[melon_fin['키워드'].str.contains(lyric.lower())]
        if artist != 'NA':
            B = A[A['가수'].str.contains(artist)]
            if genre != 'NA':
                C = B[B['장르'].str.contains(genre)]
                if year != 'NA':
                    D = C[C['년도'] >= year-2]
                    D = D[D['년도'] <= year+2]
                else :
                    D = C
            else :
                if year != 'NA':
                    D = B[B['년도'] >= year-2]
                    D = D[D['년도'] <= year+2]
                else : 
                    D = B
        else :
            if genre != 'NA':
                C = A[A['장르'].str.contains(genre)]
                if year != 'NA':
                    D = C[C['년도'] >= year-2]
                    D = D[D['년도'] <= year+2]
                else:
                    D = C
            else :
                if year != 'NA':
                    D = A[A['년도'] >= year-2]
                    D = D[D['년도'] <= year+2]
                else:
                    D = A
    else:
        if artist != 'NA':
            B = melon_fin[melon_fin['가수'].str.contains(artist)]
            if genre != 'NA':
                C = B[B['장르'].str.contains(genre)]
                if year != 'NA':
                    D = C[C['년도'] >= year-2]
                    D = D[D['년도'] <= year+2]
                else:
                    D = C
            else:
                if year != 'NA':
                    D = B[B['년도'] >= year-2]
                    D = D[D['년도'] <= year+2]
                else:
                    D = B
        else:
            if genre != 'NA':
                C = melon_fin[melon_fin['장르'].str.contains(genre)]
                if year != 'NA':
                    D = C[C['년도'] >= year-2]
                    D = D[D['년도'] <= year+2]
                else:
                    D = C
            else:
                if year != 'NA':
                    D = melon_fin[melon_fin['년도'] >= year-2]
                    D = D[D['년도'] <= year+2]
    D = D.sort_values('좋아요퍼센트', ascending = False)
    D = D[['제목', '가수', '장르', '년도', '좋아요']]
    print(D.head())

# melon_find('키워드', '가수', '장르', '년도')
melon_find('고백', '아이유', 'NA', 'NA')


