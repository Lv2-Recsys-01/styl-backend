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

# 프로덕션 빌드
docker compose -f docker-compose.prod.yaml up -d
docker compose -f docker-compose.prod.yaml build --no-cache
```

# GET /healthz

목적 : sys. health check.

[request]

[response(json)]

-   정상 response

```json
{
    "ok": true
}
```

# POST /login

[목적 및 기능]

-   목적 : 로그인
-   guest인 경우에만 로그인 가능
-   user_name, user_pwd 자리수 체크, user_pwd 맞는지 검증
-   로그인 성공 시
    -   비회원 상태에서 좋아요 목록 병합 (DB의 Like 테이블 수정)
    -   현재 비회원 세션 만료 시간 표시 (DB의 UserSession 테이블 수정)
    -   새 세션 id 생성, DB의 UserSession 테이블에 추가
    -   cookie의 session_id, user_id, user_name 변경

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
-   user_pwd가 4자리 미만 or 20자리 초과
    -   raise HTTPException(status_code=500, detail="비밀번호는 4자리 이상 20자리 이하의 숫자 or 영문자")
-   user_name이 DB에 존재하지 않거나 user_pwd가 일치하지 않을때
    -   raise HTTPException(status_code=500, detail="존재하지 않는 아이디이거나 잘못된 비밀번호입니다.")
-   정상 response

```json
{
    "ok": true,
    "user_name": user_name
}
```

# POST /logout

[목적 및 기능]

-   목적 : 로그아웃
-   DB의 UserSession 테이블 수정
    -   expired_at 업데이트
-   쿠키의 user_id, session_id, user_name 삭제

[request]

-   cookie params
    -   user_id
    -   session_id

[response(json)]

-   정상 response

```json
{
    "ok": true
}
```

# POST /singup

[목적 및 기능]

-   목적 : 회원가입
-   user_name, user_pwd 자리수 확인
-   user_pwd, confirm_pwd 같은지 확인
-   DB의 User 테이블에 존재하는 user_name인지 확인
-   검증 통과하면 DB의 User 테이블에 추가

[request]

-   body params
    -   user_name
    -   user_pwd
    -   confirm_pwd

[response(json)]

-   user_name 4자리 미만 or 20자리 초과
    -   raise HTTPException(status_code=500, detail="아이디는 4자리 이상 20자리 이하의 숫자 or 영문자")
-   user_pwd가 4자리 미만 or 20자리 초과
    -   raise HTTPException(status_code=500, detail="비밀번호는 4자리 이상 20자리 이하의 숫자 or 영문자")
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

[목적 및 기능]

-   유저에게 코디 이미지를 보여줌
-   한 페이지당 offset부터 pagesize 개수만큼 보여줌
    -   /journey?pagesize=10&offset=0 (0번째 ~ 10번째)
    -   /journey?pagesize=10&offset=10 (10번째 ~ 20번째)
-   DB의 Outfit 테이블에서 가져올 이미지 목록 불러옴
    -   이 개수가 pagesize보다 작으면 is_last = True
-   유저가 좋아요 누른 outfit_id 집합 생성
-   각 outfit마다 유저가 좋아요 눌렀는지 확인
-   이미지마다 DB의 Outfit 테이블에서 가져온 메타정보 + 좋아요 여부 합쳐서 outfits_list로 목록 생성

[request]

-   query params
    -   pagesize
    -   offset
-   cookie params
    -   user_id
    -   session_id

[response]

-   정상 response

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

[목적 및 기능]

-   목적 : 유저가 이미지를 클릭한 경우 DB에 반영
-   outfit_id가 존재하지 않으면 에러 반환
-   DB의 Click 테이블에 클릭 로그 저장

[request]

-   query params
    -   outfit_id
-   cookie params
    -   user_id
    -   session_id

[response(json)]

-   해당 outfit_id의 이미지가 존재하지 않을 때
    -   raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")
-   정상 response

```json
{
    "ok": true
}
```

# POST /journey/{outfit_id}/like

[목적 및 기능]

-   목적 : 유저가 좋아요를 누르거나 취소한 경우 DB에 반영
-   outfit_id가 존재하지 않으면 에러 반환
-   이전에 유저가 좋아요 누른적 있는지 DB의 Like 테이블에서 확인
-   없으면 DB에 추가
-   있으면 is_deleted 바꿔줌(True면 False로, False면 True로)

[request]

-   query params
    -   outfit_id
-   cookie params
    -   user_id
    -   session_id

[response(json)]

-   성공 여부와 관련 없이 프론트에서는 optimistic하게 하트를 채워야 함.
-   해당 outfit_id의 이미지가 존재하지 않을 때
    -   raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")
-   정상 response

```json
{
    "ok": true
}
```

# GET /collection

[목적 및 기능]

-   목적 : 유저가 좋아요 한 코디 이미지 가져옴
-   한 페이지당 offset부터 pagesize 개수만큼 보여줌
    -   /collection?pagesize=10&offset=0 (0번째 ~ 10번째)
    -   /collection?pagesize=10&offset=10 (10번째 ~ 20번째)
-   DB의 Like 테이블에서 outfit_id 목록 가져옴
-   목록 길이가 pagesize보다 작으면 is_last = True
-   좋아요 목록이 없으면 에러 반환
-   이미지마다 DB의 Outfit 테이블에서 가져온 메타정보 + 좋아요 여부(모두 True) 합쳐서 outfits_list로 목록 생성

[request]

-   query params
    -   pagesize
    -   offset
-   cookie params
    -   user_id
    -   session_id

[response(json)]

-   좋아요한 이미지가 없을때
    -   raise HTTPException(status_code=500, detail="좋아요한 사진이 없습니다.")
-   정상 response

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

[목적 및 기능]

-   목적 : 이미지 하나의 상세 정보와 유사 이미지를 가져옴
-   해당 outfit_id의 이미지가 없으면 에러 반환
-   DB의 Outfit 테이블에서 가져온 메타정보 + 좋아요 여부 합쳐서 outfit 생성
-   DB의 Similar 테이블에서 유사 이미지의 outfit_id 목록 가져옴
    -   해당 목록에서 outfit_id의 이미지가 없으면 에러 반환
-   개별 유사 이미지마다 DB의 Outfit 테이블에서 가져온 메타정보 + 좋아요 여부 합쳐서 similar_outfits_list 목록 생성

[request]

-   query params
    -   outfit_id
-   cookie params
    -   user_id
    -   sesseion_id

[response(json)]

-   해당 outfit_id가 존재하지 않을때
    -   raise HTTPException(status_code=500, detail="Outfit not found")
-   해당 outfit과 유사한 outfit이 존재하지 않을때
    -   raise HTTPException(status_code=500, detail="Similar outfits not found")
-   유사 이미지의 outfit_id가 존재하지 않을 때
    -   raise HTTPException(status_code=500, detail="Id for this similar outfit not found")
-   정상 response

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
