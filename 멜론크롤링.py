# -*- coding: utf-8 -*-

from selenium import webdriver # 크롤링 
import time # 화면 일시 정지 
import pandas as pd # 데이터 프레임

###########################################
## 노래 번호 추출
###########################################

# driver 객체 생성 
path = r"C:\Users\hsh97\Desktop\ITWILL\6_Tensorflow\tools" # driver 경로 
driver = webdriver.Chrome(path + '/chromedriver.exe')

# 태그 수집
number = [] # 곡번호 기입칸
year = [] # 년도 기입칸
# 추출할 년도 리스트
Date = [list(range(1985, 1990)), list(range(1990, 2000)), list(range(2000, 2010)), list(range(2010, 2020)),
        list(range(2020, 2022))]

# 노래 번호 크롤링
for D in Date:
    for i in D:        
        a = str(i) # 년도 기입
        # 해당 년도로 주소 이동
        driver.get("https://www.melon.com/chart/age/index.htm?chartType=YE&chartGenre=KPOP&chartDate=" + a)
        time.sleep(2) # 1초 일시 정지 
        songTagList = driver.find_elements_by_class_name('input_check') # 추출할 노래번호 위치
        num = [] # 노래번호 위치
        for i in songTagList:
            num.append(i.get_attribute('value')) # 노래 번호 추출 후 num에 기입
        num = num[-108:-8] # 필요한 부분의 번호만 추출
        for i in num:
            number.append(i) # 곡번호 리스트에 기입
        a = [a]*len(num) # 해당 년도를 곡번호 갯수에 맞게 생성
        year.append(a) # 년도 리스트에 기입
        time.sleep(2) # 1초 일시 정지 
driver.close() # 드라이버 닫기

# 년도 리스트 재정렬
years = []
for i in year:
    for q in i:
        years.append(q)
len(years)
'''
year = year*100
year.sort()
year[0:100]
'''

# 데이터 프레임 생성
test1 = pd.DataFrame({'년도' : years, '노래번호' : number}, columns=['년도', '노래번호'])
test1.info()

# 데이터 전처리
print (test1.loc[test1['노래번호'] == 'on'])
test1.loc[test1['년도'] == '1994']

test2 = test1.drop(test1.index[800])
print (test2.loc[test1['노래번호'] == 'on'])

# 노래번호 csv 파일 생성
test2.to_csv('melon_num.csv',mode = "w", index=False, encoding='utf-8')


test2 = pd.read_csv('C:/Users/hsh97/Desktop/data/melon_num.csv', encoding='utf-8')

test2.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3699 entries, 0 to 3698
Data columns (total 2 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   년도      3699 non-null   int64
 1   노래번호    3699 non-null   int64
dtypes: int64(2)
memory usage: 57.9 KB
'''

###########################################
## 노래 가사, 가수, 제목, 장르, 좋아요 수 크롤링
###########################################

# driver 객체 생성 
path = r"C:\Users\hsh97\Desktop\ITWILL\6_Tensorflow\tools" # driver 경로 
driver = webdriver.Chrome(path + '/chromedriver.exe')


# 태그 수집
title = [] # 제목
artist = [] # 가수
genre = [] # 장르
lyric = [] # 가사
like = [] # 좋아요 수

for s in test2['노래번호'] :  
    url = f"https://www.melon.com/song/detail.htm?songId={s}"
    driver.get(url) # page 번호 이동 
    time.sleep(3) # 3초 일시 정지 

    # 제목 수집
    test_a = driver.find_elements_by_xpath('//*[@id="downloadfrm"]/div/div/div[2]/div[1]/div[1]')
    for t in test_a : 
        title.append(t.text)
    time.sleep(1)
    # 가수 수집
    test_b = driver.find_elements_by_xpath('//*[@id="downloadfrm"]/div/div/div[2]/div[1]/div[2]')
    for t in test_b : 
        artist.append(t.text)
    time.sleep(1)
    # 장르 수집
    test_c = driver.find_elements_by_xpath('//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[3]')
    for t in test_c : 
        genre.append(t.text)
    time.sleep(1)    
    # 가사 수집
    test_d = driver.find_elements_by_xpath('//*[@id="d_video_summary"]')
    for t in test_d : 
        lyric.append(t.text)
    time.sleep(1)    
    # 좋아요 수 수집
    test_e = driver.find_elements_by_xpath('//*[@id="d_like_count"]')
    for t in test_e : 
        like.append(t.text)
    time.sleep(1)
    
    # 가사가 없을 땐 'NA' 기입
    if len(title) != len(lyric):
        lyric.append('NA')


    # 페이지당 출력한 갯수 확인
    print('제목 :', len(title))
    print('가수 :', len(artist))
    print('장르 :', len(genre))
    print('가사 :', len(lyric))
    print('좋아요 수 :', len(like))

#del artist[0]
#del genre[0]

# 드라이버 종료
driver.close()



# 데이터프레임 생성
test3 = pd.DataFrame({'제목' : title, '가수' : artist, '장르' : genre, '가사' : lyric, '좋아요' : like}, 
                       columns=['제목', '가수', '장르', '가사', '좋아요'])

# csv 파일로 저장
test3.to_csv('3698개.csv',mode = "w", index=False, encoding='utf-8')

print (len(test3.loc[test3['가사'] == 'NA']))


# 노래번호 csv 파일과 노래 데이터 csv 파일 합치기
melon_num = pd.read_csv('C:/Users/hsh97/Desktop/data/melon_num.csv', encoding='utf-8')
melon_num.info()
melon_chart = pd.read_csv('C:/Users/hsh97/Desktop/data/3698개.csv', encoding='utf-8')
melon_chart.info()
print (len(melon_chart.loc[melon_chart['가사'] == 'NaN']))
melon_chart.tail()
melon_num.tail()
melon_fin = pd.concat([melon_chart, melon_num], axis = 1)
print(melon_fin.info())
melon_fin.tail()
melon_fin.to_csv('melon_fin.csv', mode = 'w', index = False, encoding = 'utf-8')