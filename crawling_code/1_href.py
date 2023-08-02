'''
href.py
1. 같은 년도 같은 성별의 코디 링크들을 . 하나의 csv 파일로 정리합니다.
2. id 번호를 생성합니다.
'''
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import csv
import pandas as pd
import time

#무신사/href(하이퍼링크) 폴더 만들기
if not os.path.exists('./musinsa'):
        os.mkdir('./musinsa')
if not os.path.exists('./musinsa/href'):
        os.mkdir('./musinsa/href')

browser = webdriver.Chrome()
browser.maximize_window()
url = 'https://www.musinsa.com/mz/streetsnap'
browser.get(url)
#페이지 개수 찾기
pagingNumber = browser.find_element(By.CLASS_NAME, 'totalPagingNum')
totalpage=int(pagingNumber.text.replace(",",""))

yearlist = list(range(2020,2021))
#yearlist.remove(2007)
gender = ['female','male']

# 현재 페이지에 있는 모든 하이퍼 링크 저장
def get_href_in_page(hreflist):
    boxlist = browser.find_element(By.CLASS_NAME, 'snap-article-list.article-list.list.enlarged')
    lilist = boxlist.find_elements(By.TAG_NAME, 'li') #len(lilist)=60 한 페이지당 60장 (확인)
    for li in lilist:
        small_img = li.find_element(By.CLASS_NAME, 'articleImg')
        aTag = small_img.find_element(By.TAG_NAME, 'a')
        og_href = aTag.get_attribute('href')
        href=og_href.split('?')
        hreflist.append(href[0])
    return hreflist

# 맨 마지막 숫자(id) 추출 함수
def extract_last_number(url):
    return url.split('/')[-1]


def main():
    for year in yearlist:
        for sex in gender:
            hreflist = []
            yurl = 'https://www.musinsa.com/mz/streetsnap?_y='+str(year)
            browser.get(yurl)
            time.sleep(2)
            #남성여성 클릭
            if sex=='male':
                btn_apply = browser.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[2]/div[3]/button[2]')
                btn_apply.click()
            else:
                btn_apply = browser.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[2]/div[3]/button[3]')
                btn_apply.click()
            #totalpage
            pagingNumber = browser.find_element(By.CLASS_NAME, 'totalPagingNum') #페이지 찾기
            totalpage=int(pagingNumber.text.replace(",",""))
            #각 페이지별로 href 크롤링
            for page in range(1,totalpage+1):
                url = f'https://www.musinsa.com/mz/streetsnap?_y={year}&_mon=&p={page}#listStart'
                browser.get(url)
                try:
                    get_href_in_page(hreflist)
                except:
                    print('error at',page,sex,year)
                    pass
            #저장
            datapath='./musinsa/href/'
            filename=datapath+sex+str(year)+'.csv'
            dflist = pd.DataFrame(hreflist,columns=['href'])
            dflist.insert(0,'id',dflist['href'].apply(extract_last_number))
            if not os.path.exists(datapath):
                os.mkdir(datapath)
            dflist.to_csv(filename,index=False)
            print('info',sex,year,len(dflist))
main()
'''
# 먼저 상위 클래스를 찾자
# 띄어쓰기가 있으면 붙이고 대신 . (list_box box->list-box.box)
boxlist = browser.find_element(By.CLASS_NAME, 'snap-article-list.article-list.list.enlarged')
lilist = boxlist.find_elements(By.TAG_NAME, 'li') #len(lilist)=60 한 페이지당 60장 (확인)
'''