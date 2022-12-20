# -*- coding: utf-8 -*-

import pandas as pd # 데이터프레임
from konlpy.tag import Okt # 단어 사전 
from collections import Counter # 단어 중복 제거를 위해 사용
from sklearn.feature_extraction.text import TfidfVectorizer # 자연어 벡터화
from sklearn.metrics.pairwise import cosine_similarity # 코싸인 유사도

# 데이터 프레임 불러오기
melon_fin = pd.read_csv('C:/Users/hsh97/Desktop/data/melon_fin.csv', encoding = 'utf-8')
melon_fin.info()
'''
<class 'pandas.core.frame.DataFrame'>
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
memory usage: 202.4+ KB
'''

# 가사가 없는 결측값 제거
melon_fin = melon_fin.dropna()

# '좋아요' 열을 숫자형으로 변환(','를 빈칸으로 변환)
melon_fin['좋아요'] = pd.to_numeric(melon_fin['좋아요'].str.replace(',', ''))

# 중복 노래 제거
melon_fin = melon_fin.drop_duplicates(['제목'])

# 인덱스 재설정
melon_fin = melon_fin.reset_index()
melon_fin = melon_fin.drop(['index'], axis = 1)
## 가사 대소문자를 소문자로 모두 바꾸기
가사변환 = []
for i in melon_fin['가사']:
    a = i.lower()
    가사변환.append(a)
melon_fin['가사'] = 가사변환
melon_fin.info()
'''
<class 'pandas.core.frame.DataFrame'>
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
memory usage: 202.4+ KB
'''


# 명사 분류하기
okt = Okt()

# 단어끼리 이어 붙일 때 ', '를 붙이기
def listToString(str_list):
    result = ""
    for s in str_list:
        result += s + ", "
    return result.strip()

# 가사 단어를 키워드로 변환
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

melon_fin['키워드'] = 키워드
melon_fin.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3099 entries, 0 to 3098
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
 7   키워드     3099 non-null   object
dtypes: int64(3), object(5)
memory usage: 193.8+ KB
'''

# 자연어 처리 함수
transformer = TfidfVectorizer()
# 노래 가사의 키워드 자연어 처리
tfidf_matrix = transformer.fit_transform(melon_fin['키워드'])
print(tfidf_matrix.shape) #(3099, 11425)

# 코싸인 유사도로 유사값끼리 정리
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print(cosine_sim.shape) #(3099, 3099)


print(melon_fin['제목'][:5])
'''
0    이젠 사랑할 수 있어요
1     어제, 오늘, 그리고
2             희나리
3    아직도 어두운 밤인가봐
4       모두가 사랑이예요
Name: 제목, dtype: object
'''
indices = pd.Series(melon_fin.index, index=melon_fin['제목'])
print(indices.head())
'''
제목
이젠 사랑할 수 있어요    0
어제, 오늘, 그리고     1
희나리             2
아직도 어두운 밤인가봐    3
모두가 사랑이예요       4
dtype: int64
'''

# 예시로 '벚꽃 엔딩'
title = '벚꽃 엔딩'

# 선택한 음악의 타이틀로부터 해당되는 인덱스를 받아옵니다. 이제 선택한 음악을 가지고 연산할 수 있습니다.
idx = indices[title]
print(idx) #2308

# 모든 음악에 대해서 해당 음악의 유사도를 구합니다.
sim_scores = cosine_sim[idx]
print(sim_scores[:5]) #[0.03874383 0.02605509 0.01512985 0.07314379 0.00627342]
sim_scores = list(enumerate(sim_scores))
print(sim_scores[:5]) #[(0, 0.038743830479830224), (1, 0.026055091772365053), (2, 0.01512985219608747), (3, 0.07314379486142673), (4, 0.00627341935602596)]
# 유사도에 따라 음악들을 정렬합니다.
sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
print(sim_scores[:5]) #[(2308, 1.0), (2900, 0.21362647581452868), (200, 0.20745160272915314), (494, 0.18804513835275907), (924, 0.18071635243924952)]

# 가장 유사한 5개의 음악를 받아옵니다.
sim_scores = sim_scores[1:6]
print(sim_scores) #[(2900, 0.21362647581452868), (200, 0.20745160272915314), (494, 0.18804513835275907), (924, 0.18071635243924952), (1466, 0.18071635243924952)]
# 가장 유사한 5개의 음악의 인덱스를 받아옵니다.
movie_indices = [i[0] for i in sim_scores]
print(movie_indices) #[2900, 200, 494, 924, 1466]
print(melon_fin['제목'].iloc[movie_indices])
'''
2900        나만, 봄
200         세월 가면
494     모두가 잊혀질때면
924         어떤가요?
1466         어떤가요
Name: 제목, dtype: object
'''


# 최종 결과물

def sing_title(title):
    # 들었을 때 비슷하기 위해 같은 장르에서만 찾기
    mel = melon_fin[melon_fin['제목'] == title]
    mel = mel['장르']
    mel = list(mel)
    mel = ' '.join(s for s in mel)
    mel = melon_fin[melon_fin['장르'] == mel]
    mel = mel.reset_index()
    mel = mel.drop(['index'], axis = 1)
    transformer = TfidfVectorizer()
    tfidf_matrix = transformer.fit_transform(mel['키워드'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(mel.index, index=mel['제목'])
    idx = indices[title]
    sim_scores = cosine_sim[idx]
    sim_scores = list(enumerate(sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    print(mel['제목'].iloc[movie_indices])


# sing_title('노래제목')
sing_title('희나리')
'''
3    어떻게 얘기할까요
1       아득히 먼곳
2        영동부르스
Name: 제목, dtype: object
'''

sing_title('소녀')
'''
169                                      마음에 쓰는 편지
377    영원한 사랑 (With London Metropolitan Orchestra)
200                                      모두가 잊혀질때면
293                                              햄
110                                     시를 위한 시(詩)
Name: 제목, dtype: object
'''

sing_title('인연')
'''
850       보고싶은 날엔..
561       I Believe
40              괜찮아
451    다시 돌아온 그대 위해
333       기억 속의 멜로디
Name: 제목, dtype: object
'''
