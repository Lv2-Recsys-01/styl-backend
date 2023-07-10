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

# GET /healthz

목적 : sys. health check.

[request]


[response(json)]
- 정상 response
```json
{
    "ok": true
}
```

# POST /login

[목적 및 기능]
- 목적 : 로그인
- guest인 경우에만 로그인 가능
- user_name, user_pwd 자리수 체크, user_pwd 맞는지 검증
- 로그인 성공 시
  - 비회원 상태에서 좋아요 목록 병합 (DB 수정)
  - 현재 비회원 세션 만료 시간 표시 (DB 수정)
  - 새 세션 id 생성, DB 추가
  - cookie의 session_id, user_id, user_name 변경

[request]
-   body params
    -   user_name
    -   user_pwd
-   cookie params
    -   user_id
    -   session_id

[response(json)]
-   user_id가 guest_user_id(=1)이 아니면 -> 이미 로그인 된 상태
    -   raise HTTPException(status_code=500, detail="로그아웃을 먼저 하십시오.")
-   user_name 4자리 미만 or 20자리 초과
    -   raise HTTPException(status_code=500, detail="아이디는 4자리 이상 20자리 이하의 숫자 or 영문자")
- user_pwd가 4자리 미만 or 20자리 초과
    -   raise HTTPException(status_code=500, detail="비밀번호는 4자리 이상 20자리 이하의 숫자 or 영문자")
-   user_name이 DB에 존재하지 않거나 user_pwd가 일치하지 않을때
    - raise HTTPException(status_code=500, detail="존재하지 않는 아이디이거나 잘못된 비밀번호입니다.")
-   정상 response
```json
{
    "ok": true,
    "user_name": user_name
}
```

# POST /logout

목적 : 로그아웃

[request]
-   cookie params
    -   user_id
    -   session_id

[response(json)]
-   정상 response
```json
{
    "ok": true,
}
```

# POST /singup

목적 : 회원가입 시키기 위함

[request]
-   body params
    -   user_name
    -   user_pwd
    -   confirm_pwd

[response(json)]
-   user_name 4자리 미만 or 20자리 초과
    -   raise HTTPException(status_code=500, detail="아이디는 4자리 이상 20자리 이하의 숫자 or 영문자")
-    user_pwd가 4자리 미만 or 20자리 초과
     - raise HTTPException(status_code=500, detail="비밀번호는 4자리 이상 20자리 이하의 숫자 or 영문자")
-   user_pwd와 confirm_pwd가 같지 않으면
    -   raise HTTPException(status_code=500, detail="비밀번호가 일치하지 않습니다")
-   user_name이 이미 DB에 존재
    -   raise HTTPException(status_code=500, detail="이미 존재하는 아이디입니다")
-   정상 response
```json
{
    "ok": true,
    "user_name": user_name
}
```

# GET /journey

목적 : 유저에게 코디 이미지를 보여줌

example)
최신순 가정  
GET /journey?pagesize=10&offset=0 (0번째 ~ 10번째)  
GET /journey?pagesize=10&offset=10 (10번째 ~ 20번째)

[request]
- query params
  - pagesize
  - offset
- cookie params
  - user_id
  - session_id

[response]
- 정상 response
```json
{
  "ok": true,
  "outfits_list": outfits_list,
  "pagesize": pagesize,
  "offset": offset,
  "is_last": is_last,
  "total_page_count": total_page_count
}
```

# POST /journey/{outfit_id}/click

목적 : 유저가 이미지를 클릭한 경우 DB에 반영

[request]
-   query params
    -   outfit_id
-   cookie params
    -   user_id
    -   session_id

[response(json)]
- 해당 outfit_id의 이미지가 존재하지 않을 때
  - raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")
-   정상 response
```json
{
    "ok": true
}
```

# POST /journey/{outfit_id}/like

목적 : 유저가 좋아요를 누른 경우 DB에 반영

[request]
-   query params
    -   outfit_id
-   cookie params
    -   user_id
    -   session_id

[response(json)]
-   성공 여부와 관련 없이 프론트에서는 optimistic하게 하트를 채워야 함.
- 해당 outfit_id의 이미지가 존재하지 않을 때
  - raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")
-   정상 response
```json
{
    "ok": true
}
```

# GET /collection

목적 : 유저가 좋아요 한 코디를 가져온다. my collections 페이지 렌더용

example)
최신순 가정  
GET /collection?pagesize=10&offset=0 (0번째 ~ 10번째)  
GET /collection?pagesize=10&offset=10 (10번째 ~ 20번째)

[request]
- query params
  - pagesize
  - offset
- cookie params
  - user_id
  - session_id

[response(json)]
- 좋아요한 이미지가 없을때
  - raise HTTPException(status_code=500, detail="좋아요한 사진이 없습니다.")
- 정상 response
```json
{
  "ok": True,
  "outfits_list": outfits_list,
  "pagesize": pagesize,
  "offset": offset,
  "is_last": is_last
}
```

# GET /journey/{outfit_id}

목적 : 단건의 이미지와 유사 이미지를 가져옵니다.

[request]
- query params
  - outfit_id
- cookie params
  - user_id
  - sesseion_id

[response(json)]
- 해당 outfit_id가 존재하지 않을때
  - raise HTTPException(status_code=500, detail="Outfit not found")
- 해당 outfit과 유사한 outfit이 존재하지 않을때
  - raise HTTPException(status_code=500, detail="Similar outfits not found")
- 정상 response
```json
{
  "ok": true,
  "outfit": outfit_out,
  "similar_outfits_list": similar_outfits_list
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
