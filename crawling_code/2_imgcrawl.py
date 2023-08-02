'''
1. href.py 에서 얻은 하이퍼링크를 옮겨다니며 img 파일만 다운로드 받습니다
2. ./musinsa/img에 저장합니다.
'''
import requests
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import os
import pickle

#파일 불러 오기 (나중에 for 문으로 전체 년도와 성별에 대해서 하자)
common_path = './musinsa/img/'
if not os.path.exists(common_path):
    os.mkdir(common_path)
yearlist = list(range(2016,2018))
#yearlist.remove(2007)
gender = ['female','male']
def nosel(filename,sex,year):
    errorid=[]
    df=pd.read_csv('./musinsa/href/'+filename)
    idlist=df['id']
    hreflist=df['href']
    datapath = common_path + str(year) + sex
    #년도 성별 별로 저장할 폴더 생성 
    if not os.path.exists(datapath):
        os.mkdir(datapath)
    for id,href in zip(idlist,hreflist):
        response = requests.get(href)
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        snap=soup.find('div','snapImg')
        #아주 가끔씩 img 파일이 저장안되는 링크가 있다...
        #자기전에 돌려놨는데 멈춰있어서 너무 열받아서 try 구문 만듦
        #errorid에 저장안된 이미지 id를 리스트형식으로 저장하고 binary 파일로 저장한다.
        try:
            image_url = 'https:'+snap.select_one("img")["src"]
            image_url = image_url.replace("/n", "")
            print(image_url)
            datapath = common_path + str(year) + sex 
            image_name = datapath+'/'+str(id)+'.jpg'
            urllib.request.urlretrieve(image_url, image_name)
        except:
            print('error',id)
            errorid.append(id)
    errorname=str(year)+sex+'error.pkl'
    with open(errorname,"wb") as f:
        pickle.dump(errorid, f)
    return errorid

#성별 년도에 대한 loop 문
def main():
    for year in yearlist:
        for sex in gender:
            filename = sex + str(year) +'.csv'
            errorid=nosel(filename,sex,year)
            print(errorid)
    
main()
'''
#selenium 사용했던 코드
def imgcrawl(filename):
    df=pd.read_csv('./musinsa/href/'+filename)
    idlist=df['id']
    hreflist=df['href']
    for id,href in zip(idlist,hreflist):
        driver.get(href)
        html = driver.page_source
        soup = BeautifulSoup(html)
        snap=soup.find('div','snapImg')
        image_url = 'https:'+snap.select_one("img")["src"]
        print(image_url)
        datapath = common_path + year + sex 
        os.mkdir(datapath)
        image_name = './musinsa/img/2019male/'+str(id)+'.jpg'
        urllib.request.urlretrieve(image_url, image_name)
imgcrawl(filename)
'''