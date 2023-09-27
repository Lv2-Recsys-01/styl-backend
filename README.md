<a name="readme-top"></a>

<div align="center">

![header](https://capsule-render.vercel.app/api?&height=150&type=transparent&text=Journey&fontSize=120&fontColor=be3455&fontAlign=50&desc=개인화%20코디%20추천%20서비스&descAlign=64&descAlignY=95)

![header](https://capsule-render.vercel.app/api?&height=70&type=transparent&text=-%20Team%20Style%20Bible%20-&fontSize=30&fontColor=36618C&fontAlign=50)

<img src = ./docs/journey-logo.png width =1000/>

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
    <li><a href="#프로젝트-구조">프로젝트 구조</a></li>
    <li><a href="#랩업-리포트-및-발표-영상">랩업 리포트 및 발표 영상</a></li>
    <li><a href="#팀원-소개">팀원 소개</a></li>
  </ol>
</details>
<br>

<!-- 프로젝트 개요 -->

## 프로젝트 개요

‘Journey’는 수많은 사진 속에서 자신만의 패션을 찾아가는 AI 코디 추천 서비스입니다.

[서비스 링크](https://stylesjourney.com) (서비스는 2023년 8월부로 종료되었습니다.)
<br>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 시연 영상
<p align="center">
  <a href="https://youtu.be/uY6cEJMjPDs target="_blank">
    <img src="https://img.shields.io/badge/YouTube-team_video-red?&style=for-the-badge&logo=youtube" />
  </a>
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 아키텍처
### 프로젝트 아키텍처
<div align="center">
<img src = "./docs/architecture.png" width=800/>
</div>

### Airflow Pipeline
<div align="center">
<img src = "./docs/ops.png" width =800 />
</div>

### ERD
<div align="center">
<img src = "./docs/ERD.png" width =1000 />
</div>
<br>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 추천 로직

### 유사한 코디 추천 로직 (Similar Style)

<br>
<div align="center">
<img src = "./docs/similar.png" width=800/>
</div>
<br>

수집한 코디의 메타 데이터 중에서 reporter 데이터를 활용하여 형태소 분석을 수행했습니다.

TF-IDF와 벡터화를 사용하여 코디 정보를 벡터로 표현하고, 코사인 유사도를 계산하여 유사한 코디 리스트를 생성했습니다.

<br>

### 개인화 코디 추천 로직 (Journey)

<div align="center">
<img src = "./docs/model2.png" width=800/>
</div>
<br> 

개인화 코디 추천 서비스에는 Contents based와 MAB + Content-based 모델을 적용했습니다.

AB 테스트를 위해 랜덤하게 하나의 모델을 적용하여 사용자에게 서빙했습니다. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 프로젝트 구조

총 4개의 repo를 만들어 작업하였고 backend repo에 통합하여 서비스를 배포했습니다.

docker를 사용하여 로컬에서 실제 서비스와 같은 환경을 구축하여 개발을 진행했습니다.

-   [styl-frontend](https://github.com/Lv2-Recsys-01/styl-frontend)

-   [styl-backend](/docs/README.md)

-   [styl-ml](https://github.com/Lv2-Recsys-01/styl-ml)

-   [styl-airflow](https://github.com/Lv2-Recsys-01/styl-airflow)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 랩업 리포트 및 발표 영상
- [랩업 리포트](./docs/wrapup.pdf)

- [발표 영상](https://www.youtube.com/watch?v=M98BRk6CqNE&t=152s)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 팀원 소개

<table><tbody><tr>
<td align="center">
    <img width="100%" src="./docs/동호.png"/>
    <div><a href="https://github.com/CIOI">곽동호</a></div>
    <div>Data, Modeling</div>
</td>
<td align="center">
        <img width="100%" src="./docs/수훈.png"/>
        <div><a href="https://github.com/DarrenKwonDev">권수훈</a></div>
        <div>PM, BE, FE, Ops</div>
    </td>
<td align="center">
        <img width="100%" src="./docs/상우.png"/>
        <div><a href="https://github.com/sangwu99">박상우</a></div>
        <div>BE, Modeling</div>
    </td>
</tr>
<tr>
<td align="center">
        <img width="100%" src="./docs/민호.png"/>
        <div><a href="https://github.com/RonaldFisher9999">이민호</a></div>
        <div>BE, BA, Modeling, AB Test</div>
    </td>
<td align="center">
        <img width="100%" src="./docs/준원.png"/>
        <div><a href="https://github.com/junwon-0313">이준원</a></div>
        <div>FE, BA, Modeling</div>
    </td>
<td align="center">
        <img width="100%" src="./docs/한정.png"/>
        <div><a href="https://github.com/leehanjeong">이한정</a></div>
        <div>DE, BE, Ops</div>
    </td>
</tr>
</tbody></table>
<br>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<br>
