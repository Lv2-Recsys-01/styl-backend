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
