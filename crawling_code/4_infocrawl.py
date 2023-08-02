'''
add_s3url에서 얻은 scv파일에다가 메타데이터 추가해서 저장
메타데이터 크롤링 musinsa data에
'''
import requests
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import os
from collections import defaultdict

if not os.path.exists('./musinsa/data'):
    os.mkdir('./musinsa/data')
filename='female2019.csv'
common_path = './musinsa/img/'
yearlist = list(range(2014,2024))
#yearlist.remove(2007)
gender = ['female','male']
cattext = ['이름(나이)','촬영일','게시일','촬영지역','직업','스타일','조회/추천/댓글']
def get_tags(tbody):
    tags = tbody.find('ul','article-tag-list list')
    tag_spans=tags.select('span')
    taglist=[]
    for tag in tag_spans:
        taglist.append(tag.text)
    return taglist
def extract_name(total):
    print(total)
    idx=total.index('(')
    return total[0:idx]
def extract_age(total):
    print(total)
    idx=total.index('(')
    return total[idx+1:-1]

def get_infos(filename,sex,year):
    metadata = defaultdict(list)
    df=pd.read_csv('./musinsa/imgurl/'+filename)
    idlist=df['id']
    hreflist=df['href']
    #test할때사용
    #idlist=idlist[530:-1]
    #hreflist=hreflist[530:-1]
    datapath = common_path + str(year) + sex
    if not os.path.exists(datapath):
        os.mkdir(datapath)
    for id,href in zip(idlist,hreflist):
        response = requests.get(href)
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        #코멘트 추출
        comment=soup.find('p','comment').get_text()
        comment=comment.strip()
        metadata['repoter'].append(comment)
        #나머지 정보
        info=soup.find('div','snapInfo')
        tbody=info.select_one('tbody')
        #trs=[이름,촬영일,게시일,촬영지역,직업,스타일,관련브랜드,조회추천댓글,태그]
        #tag먼저 빼내기
        tags=get_tags(tbody)
        metadata['tag'].append(tags)
        #brand
        brans = tbody.find_all('a','brand')
        brandlist=[]
        if brans == None:
            brandlist.append('None')
        else:
            for bran in brans:
                brandlist.append(bran.text)
        metadata['브랜드'].append(brandlist)
        #나머지들
        spans=tbody.select('span')
        checklist=[]
        for span in spans:
            try:
                checklist.append(span.text)
            except:
                continue
        for category in cattext:
            i=checklist.index(category)
            metadata[category].append(checklist[i+1])
        print(href)
    df2=pd.DataFrame(metadata)
    df2.insert(0,'name',df2['이름(나이)'].apply(extract_name))
    df2.insert(1,'age',df2['이름(나이)'].apply(extract_age))
    df2=df2.drop(['이름(나이)'],axis=1)
    print(df2.head())

    new = pd.concat([df, df2], axis=1)
    col_list=['id','href','imgurl','name','age','reporter','tags','brand','date','upload','region','job','style','hype']
    new.columns=col_list
    print(new.head())
    savefile = f'./musinsa/data/{year}_{sex}.csv'
    new.to_csv(savefile,index=False,encoding="utf-8-sig")

def main():
    for year in yearlist:
        for sex in gender:
            filename = str(year)+sex +'.csv'
            get_infos(filename,sex,year)
main()