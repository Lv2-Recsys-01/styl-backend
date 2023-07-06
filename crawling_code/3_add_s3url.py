'''
기존 href 에서 얻은 csv 파일에 3s imgurl column을 추가
'''
import pandas as pd
import os

if not os.path.exists('./musinsa/imgurl'):
    os.mkdir('./musinsa/imgurl')

def s3url(id,sex,year):
    result=f"https://codidatabucket.s3.ap-northeast-2.amazonaws.com/img/{year}{sex}/{id}.jpg"
    return result

for i in range(2005,2024):
    for sex in ['male','female']:
        name = f"{sex}{i}.csv"
        full = f'./musinsa/href/{name}'
        try:
            df=pd.read_csv(full)
            print('check1')
            df.insert(2,'imgurl',df['id'].apply(s3url,args=(sex,i)))
            savepoint = f'./musinsa/imgurl/{i}{sex}.csv'
            df.to_csv(savepoint,index=False)
        except:
            print('error')
            continue