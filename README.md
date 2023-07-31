<a name="readme-top"></a>

<div align="center">  

![header](https://capsule-render.vercel.app/api?&height=150&type=transparent&text=Journey&fontSize=120&fontColor=be3455&fontAlign=50&desc=개인화%20코디%20추천%20서비스&descAlign=64&descAlignY=95)

![header](https://capsule-render.vercel.app/api?&height=70&type=transparent&text=-%20Team%20Style%20Bible%20-&fontSize=30&fontColor=36618C&fontAlign=50)

<img src = ./docs/journey-logo.png width =400 height=200 />

<br><br>
  
  <p align="center"><strong>Skills</strong>
    <br />

---
<br>

<p align="center">
    <img src = "https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB" alt="react badge"/>
    <img src = "https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt ="fastapi badge"/>
    <img src="https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white" alt='aws badge'/>
    <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt='postgres badge'/>
    <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt='docker badge' />
    <br>
    <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas badge"/>
    <img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white" alt="numpy badge"/>
    <img src="https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikitlearn badge">
    <img src="https://img.shields.io/badge/apache%20airflow-%23017CEE.svg?&style=for-the-badge&logo=apache%20airflow&logoColor=white" alt="airflow badge"/>
</p>
  
<br><br>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#프로젝트-개요">프로젝트 개요</a></li>
    <li><a href="#시연-영상">시연 영상</a></li>
    <li><a href="#아키텍처">아키텍처</a></li>
    <li><a href="#추천-로직">추천 로직</a></li>
    <li><a href="#유저-로그-분석">유저 로그 분석</a></li>
    <li><a href="#프로젝트-구조">프로젝트 구조</a></li>
    <li><a href="#타임라인">로드맵</a></li>
  </ol>
</details>
<br>

<!-- 프로젝트 개요 -->
## 프로젝트 개요
‘Journey’는 수많은 사진 속에서 자신만의 패션을 찾아가는 AI 코디 추천 서비스입니다.

[서비스 링크](https://stylesjourney.com) (23년 8월 중순까지 서비스 운영 예정입니다.)
<br>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 시연 영상

<img src = './docs/demonstration.gif' width= 500 alt= 'vedio'/>
<br>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 아키텍처
<img src = "./docs/architecture.png" width=500/>

### Front End
- React

### Back End
- FastAPI

### Data

- Entity Relationship Diagram

<img src = "./docs/ERD.png" width =500 />

<br>

- 무신사 스트릿 스냅 이미지 크롤링
- 선정 이유: 다양한 메타 데이터, 다양한 스타일, 비상업성, 무보정, 비슷한 구도

### Ops
<img src = "./docs/ops.png" width =500 />

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 추천 로직

### 유사한 코디 추천
<img src = "./docs/similar.png" width=500/>


### 개인화 코디 추천

1. MAB

<img src = "./docs/model1.png" width=500/>

2. Contents based 

<img src = "./docs/model2.png" width=500/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 유저 로그 분석

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 프로젝트 구조

    📦STYL
    ┣ 📂client
    ┣ 📂docs
    ┣ 📂logging
    ┣ 📂scripts
    ┣ 📂src
    ┃ ┣ 📂router
    ┃ ┗ 📜backend
    ┣ 📜Dockerfile
    ┣ 📜nginx.conf
    ┗ 📜README.md

  총 4개의 repo를 만들어 작업하였고 backend repo에 통합하여 서비스를 배포하였습니다.

  docker를 사용하여 로컬에서 실제 서비스와 같은 환경을 구축하여 개발을 진행했습니다.

- [styl-frontend](https://github.com/Lv2-Recsys-01/styl-frontend)

- [styl-backend](/docs/README.md)

- [styl-ml](https://github.com/Lv2-Recsys-01/styl-ml)

- [styl-airflow](https://github.com/Lv2-Recsys-01/styl-airflow)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 타임라인

<img src = "./docs/timeline.png" width=500/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 팀원소개

:sunglasses:[곽동호](https://github.com/CIOI): Data Engineering, Modeling

:moneybag:[권수훈](https://github.com/DarrenKwonDev): PM, BE, FE, Ops

:smile_cat:[박상우](https://github.com/sangwu99): BE, Modeling

:smile:[이민호](https://github.com/RonaldFisher9999): Data Engineering, BE, Modeling, AB Test

:relaxed:[이준원](https://github.com/junwon-0313?tab=repositories): FE, Modeling

:stuck_out_tongue_winking_eye:[이한정](https://github.com/leehanjeong): Data Engineering, BE, Ops

<br>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<br>
