# styl-backend

```bash
conda create -n backend python=3.10.4 -y
conda activate backend
pip install -r requirements.txt
```

## docker

```bash
# single container
docker build --platform=linux/amd64 -t stylback .
docker run -it -p 8000:8000 stylback

# docker compose
docker compose up
docker compose build --no-cache # 패키지 설치했는데도 인식 하지 못하면.
```

<<<<<<< HEAD
1. 쿠키와 세션
- 쿠키
  - 클라이언트 로컬에 저장되는 key:value 형태 데이터
  - request하면 자동으로 서버에 전송
  - 서버에서 쿠키 생성/업데이트해서 response 가능
  - 유효시간 있음
- 세션
  - 쿠키 기반
  - 클라이언트가 아니라 서버에서 관리
  - 동작 방식
    클라이언트가 서버 처음 접속시 세션 id 발급 ->
    db에 세션 id 저장 ->
    서버는 세션 id에 해당하는 쿠키 생성해서 response ->
    이후 서버가 request 받으면 쿠키에 포함된 세션 id로 클라이언트 식별

2. 쿠키/세션 필요한 이유
- 로그인 안 한 유저의 로그 수집
  - 로그인 안 하고 사용하다 로그인 하면 병합 필요
- 세션 단위로 로그 수집

3. 우리 서비스에서 사용하는 지점
- 최초 접속
  - 세션id 없으면 로그인 페이지로 리다이렉트
    - 프론트/백 어디서 처리?
  - 로그아웃하면 세션id 삭제하고 로그인 페이지로 보냄
  - 로그인 된 상태(유저id != guest id)에서 접속시 journey 페이지로 리다이렉트
- 로그인 페이지
  - 비회원 '로그인 없이 시작'
    - 세션id 생성
    - 미리 생성해 놓은 비회원용(guest) id를 유저id에 배정
    - 유저id, 세션id 같이 db에 저장
  - 회원 로그인 성공
    - 좋아요 목록 병합
      - 현재 세션id 확인 (없으면 pass)
      - db의 like 테이블에 현재 세션id 기준으로 좋아요 목록이 있는지 확인
      - 해당 좋아요 목록의 유저id를 변경 (guest id -> 실제 유저id)
    - 세션id 생성
    - 유저id, 세션id 같이 db에 저장
  - "XXX"님 환영합니다 이런 메세지 띄울거면 login id도 저장
- 유저 로그(클릭/좋아요 등)
  - 세션id, 유저id를 pk로 db에 저장(like, click 테이블)
- 좋아요 불러오기
  - 현재 세션id, 유저id를 기준으로 like 테이블에서 불러옴

4. 기타 문제들
- 쿠키 수집 거부하는 브라우저면 어떻게?
=======
# GET /healthz

목적 : sys. health check.

[request]
query params :

-   유저 식별자

[response(json)]

```json
{
    "ok": true
}
```

# POST /login

목적 : 로그인 시키기 위함

[request]
query params :

-   유저 식별자 (기존에 사용하던 유저라면 fake 식별자가 넘어옴)

body params :

-   id
-   password

[response(json)]

```json
{
"ok": true
"user_id": user_id
}
```

# POST /singin

목적 : 회원가입 시키기 위함

[request]
query params :

-   유저 식별자

body params :

-   id
-   password
-   confirm password

[response(json)]

```json
{
"ok": true
"user_id": user_id
}
```

<!-- # POST /logout

목적 : 로그아웃
query params : 없음
body params : 없음
로그아웃을 프론트 단에서 유저 식별자 지우면 됨. -->

# POST /heart

목적 : 좋아요를 누른 경우 DB에 반영하기 위함

[request]

query params :

-   유저 식별자

body params :

-   outfit id

[response(json)]

-   성공 여부와 관련 없이 프론트에서는 optimistic하게 하트를 채워야 함.

```json
{
    "ok": true
}
```

# GET /heart

목적 : 유저가 좋아요 한 코디를 가져온다. my collections 페이지 렌더용

[request]
query params :

-   유저 식별자
-   pagesize : 한번에 가져올 이미지의 개수
-   offset: 어디서부터

example)
최신순 가정
GET /heart?userid=1&pagesize=10&offset=0 (0번째 ~ 10번째)
GET /heart?userid=1&pagesize=10&offset=10 (10번째 ~ 20번째)

[response(json)]

```json
{
    "outfits": [{
        Outfit properties,
        }
    ],
    "pagesize": pagesize,
    "offset": offset,
    "is_last": boolean,
}
```

# PUT /heart

목적 : 유저가 하트를 취소 했을 때. hard delete가 아니고 soft delete하자(is_deleted = True) 같은 식임.
[request]
query params :

-   유저 식별자

body params :

-   outfit id

[response(json)]

```json
{
    "ok": true
}
```

# GET /images

목적 : 해당 유저가 journey 페이지에 접근했을 때 여러 이미지를 옵니다. 추천할만한 이미지를 불러와야 함.
[request]
query params :

-   유저 식별자
-   pagesize : 한번에 가져올 이미지의 개수
-   offset: 어디서부터

[response(json)]

```json
{
    "outfits": [{
        Outfit properties,
        is_liked, // 넣어줘야 함.
        }
    ],
    "pagesize": pagesize,
    "offset": offset,
    "is_last": boolean,
}
```

# GET /image

[request]
목적 : 단건의 이미지를 가져옵니다.

query params :

-   유저 식별자
-   outfit id

[response(json)]

```json
{
    "outfit": {
        Outfit properties,
        is_liked, // 넣어줘야 함.
    },
    similar_outfits: [
        {
            outfit_id,
            img_url,
        }
    ],
    "pagesize": pagesize,
    "offset": offset,
    "is_last": boolean,
}
```

# POST /shared

목적 : 공유 버튼을 눌렀을 때 해당 행동을 기록하기 위함

[request]
query params :

-   유저 식별자

body params :

-   outfit id

[response(json)]

```json
{
    "ok": true
}
```

# POST /similar

목적 : 유사 아이템 클릭시 기록

[request]
query params :

-   유저 식별자

body params :

-   base outfit id: 들어온 페이지의 코디 id
-   clicked outfit id: 밑에 유사한 코디를 클릭했을 때

[response(json)]

```json
{
    "ok": true
}
```

# 기타

-   auth 체크는 미들웨어로 작성해서 request 객체에 append해서 넘겨주길 바람
-   모든 요청의 query param에 유저 식별자 넣기
-   outfit id는 코디의 식별자를 의미함
-   timestamp는 서버에서 찍어주세요

# 미들웨어를 거친 후의 로직

-   미들웨어에서 로그인 여부 및 로그인했다면 어떤 유저인지 확인 -> request.user dict에 키, 값 추가
-   해당 유저의 db pk를 통해서 sqlalchemy를 통해서 join 등을 통해 여러 테이블을 연산하여 결과값을 만들어냄
-   response로 보내줌.
>>>>>>> origin/master
