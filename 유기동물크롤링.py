# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 14:29:58 2022

@author: hsh97
"""

from selenium import webdriver # module 
import time # 화면 일시 정지 
from urllib.request import urlretrieve # server image -> local save
import os # dir 경로/생성/이동


# 1. driver 객체 생성 
path = r"C:\Users\hsh97\Desktop\ITWILL\6_Tensorflow\tools" # driver 경로 
driver = webdriver.Chrome(path + '/chromedriver.exe')

# 2. 대상 url 이동 
driver.get('https://www.animal.go.kr/front/awtis/public/publicList.do?totalCount=2139&pageSize=10&boardId=&desertionNo=&menuNo=1000000055&searchSDate=2022-06-02&searchEDate=2022-06-12&searchUprCd=&searchOrgCd=&searchCareRegNo=&searchUpKindCd=422400&searchKindCd=&searchSexCd=&searchState=&&page=1')  


# 3. 태그 수집
공고번호 = []
축종 = []
품종 = []
털색 = []
성별 = []
중성화_여부 = []
특징 = []
접수일시 = []
구조사유 = []
발생장소 = []
공고기간 = []
관할보호센터명 = []
보호장소 = []
전화번호 = []
관할기관 = []
담당자 = []
연락처 = []
특이사항 = []
img_url = []
img_url2 = []
start = '2022-06-15'
end = '2022-06-26'
jong = '422400'
# 개 : 417000, 고양이 : 422400


# 전체 페이지 수 알아내기! 
url = f"https://www.animal.go.kr/front/awtis/public/publicList.do?totalCount=2139&pageSize=10&boardId=&desertionNo=&menuNo=1000000055&searchSDate={start}&searchEDate={end}&searchUprCd=&searchOrgCd=&searchCareRegNo=&searchUpKindCd={jong}&searchKindCd=&searchSexCd=&searchState=&&page=1"
driver.get(url)
# 맨 마지막 페이지 버튼 클릭!
last_page = driver.find_element_by_xpath('//*[@id="searchList"]/ul/li[12]/a')
last_page.click()
time.sleep(2)
# 페이지 xpath 얻어내고 맨 마지막 페이지 번호 뜯어내기!
a = driver.find_elements_by_xpath('//*[@id="searchList"]/ul/li/a')
b = a[-1].text
b = int(b)
 
for n in range(1, b+1) :  
    url = f"https://www.animal.go.kr/front/awtis/public/publicList.do?totalCount=2139&pageSize=10&boardId=&desertionNo=&menuNo=1000000055&searchSDate={start}&searchEDate={end}&searchUprCd=&searchOrgCd=&searchCareRegNo=&searchUpKindCd={jong}&searchKindCd=&searchSexCd=&searchState=&&page={n}"
    driver.get(url) # page 번호 이동 
    time.sleep(1) # 1초 일시 정지 
    
    # 페이지당 동물 수 확인(마지막 페이지같은 경우엔 꼭 10장이 있는게 아니기 때문!)
    a = driver.find_elements_by_xpath('//*[@id="searchList"]/div[4]/ul[2]/li')
    
    # 이미지 url 수집
    images = driver.find_elements_by_css_selector("#searchList > div.boardList > ul:nth-child(2) > li > div.photo > div > a > img")

    for image in images :
        url = image.get_attribute('src')
        img_url.append(url)

            
    for i in range(1, len(a)+1): # 페이지 당 동물 수 만큼 크롤링 시작!
        
        # 첫 자세히보기 들어가기
        # //*[@id="searchList"]/div[4]/ul[2]/li[1]/div[1]/a
        # //*[@id="searchList"]/div[4]/ul[2]/li[2]/div[1]/a
        a_ele = driver.find_element_by_xpath('//*[@id="searchList"]/div[4]/ul[2]/li[%i]/div[1]/a'%i)
        a_ele.click() # 페이지 이동 
        time.sleep(2)
        
        # 공고번호 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[2]/td')
        for t in test : 
            공고번호.append(t.text)
    
        # 축종 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[3]/td')
        for t in test : 
            축종.append(t.text)
    
        # 품종 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[4]/td')
        for t in test : 
            품종.append(t.text)
    
        # 털색 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[5]/td')
        for t in test : 
            털색.append(t.text)
    
        # 성별 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[6]/td')
        for t in test : 
            성별.append(t.text)
    
        # 중성화_여부 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[7]/td')
        for t in test : 
            중성화_여부.append(t.text)
    
        # 특징 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[8]/td')
        for t in test : 
            특징.append(t.text)
    
        # 접수일시 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[10]/td')
        for t in test : 
            접수일시.append(t.text)
    
        # 구조사유 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[11]/td')
        for t in test : 
            구조사유.append(t.text)
    
        # 발생장소 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[12]/td')
        for t in test : 
            발생장소.append(t.text)
    
        # 공고기간 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[13]/td')
        for t in test : 
            공고기간.append(t.text)
    
        # 관할보호센터명 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[16]/td')
        for t in test : 
            관할보호센터명.append(t.text)
    
        # 보호장소 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[17]/td')
        for t in test : 
            보호장소.append(t.text)
    
        # 전화번호 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[18]/td')
        for t in test : 
            전화번호.append(t.text)
    
        # 관할기간 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[20]/td')
        for t in test : 
            관할기관.append(t.text)
    
        # 담당자 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[21]/td[1]')
        for t in test : 
            담당자.append(t.text)
    
        # 연락처 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[21]/td[2]/a')
        for t in test : 
            연락처.append(t.text)
    
        # 특이사항 수집
        test = driver.find_elements_by_xpath('//*[@id="publicForm"]/div/table/tbody/tr[22]/td')
        for t in test : 
            특이사항.append(t.text)
            
        # 큰 이미지 수집
        images_2 = driver.find_elements_by_css_selector("#slides > a > img")

        for image in images_2 :
            url = image.get_attribute('src')
            img_url2.append(url)

        # 뒤로가기!
        driver.back()


    # 페이지당 출력한 갯수 확인!
    print('공고번호 :', len(공고번호))
    print('축종 :', len(축종))
    print('품종 :', len(품종))
    print('털색 :', len(털색))
    print('성별 :', len(성별))
    print('중성화_여부 :', len(중성화_여부))
    print('특징 :', len(특징))
    print('접수일시 :', len(접수일시))
    print('구조사유 :', len(구조사유))
    print('발생장소 :', len(발생장소))
    print('공고기간 :', len(공고기간))
    print('관할보호센터명 :', len(관할보호센터명))
    print('보호장소 :', len(보호장소))
    print('전화번호 :', len(전화번호))
    print('관할기관 :', len(관할기관))
    print('담당자 :', len(담당자))
    print('연락처 :', len(연락처))
    print('특이사항 :', len(특이사항))
    print('url1 :', len(img_url))
    print('url2 :', len(img_url2))

# 닫아버리기!
driver.close()

# csv 파일로 저장해버리기!
import pandas as pd 

test1 = pd.DataFrame({'공고번호' : 공고번호, '축종' : 축종, '품종' : 품종, '털색' : 털색, '성별' : 성별, 
                      '중성화_여부' : 중성화_여부, '특징' : 특징, '접수일시' : 접수일시, '구조사유' : 구조사유, 
                      '발생장소' : 발생장소, '공고기간' : 공고기간, '관할보호센터명' : 관할보호센터명, 
                      '보호장소' : 보호장소, '전화번호' : 전화번호, '관할기관' : 관할기관, '담당자' : 담당자, 
                      '연락처' : 연락처, '특이사항' : 특이사항, 'url' : img_url, 'url2' : img_url2}, 
                       columns=['공고번호', '축종', '품종', '털색', '성별', '중성화_여부', '특징', '접수일시', 
                                '구조사유', '발생장소', '공고기간', '관할보호센터명', '보호장소', '전화번호', 
                                '관할기관', '담당자', '연락처', '특이사항', 'url', 'url2'])

# 2) csv file save
test1.to_csv('유기묘최종크롤링.csv',mode = "w", index=False, encoding='utf-8')


# 이미지 뽑아내서 저장해버리기!
pwd = r'C:\Users\hsh97\Desktop\fin_pro' # 저장 경로 
os.mkdir(pwd + '/' + '유기묘최종사진') # pwd 위치에 폴더 생성(폴더이름 변경하면됨) 
os.chdir(pwd+"/"+'유기묘최종사진') # 폴더 이동(현재경로/폴더로 저장)
        
# 7. image url -> image save
for i in range(len(img_url)) :
    try : # 예외처리 : server file 없음 예외처리 
        file_name = "cat"+str(i+1)+".jpg" # 사진이름에 넣을 이름 적으면됨 
        urlretrieve(img_url[i], filename=file_name)#(url, filepath)
        print(str(i+1) + '번째 image 저장')
    except :
        print('해당 url에 image 없음 : ', img_url[i])     