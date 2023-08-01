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
docker compose restart client # client만 재시작(nginx 설정을 자주 바꾸게 됨.)

# 프로덕션 빌드
docker compose -f docker-compose.prod.yaml up -d
docker compose -f docker-compose.prod.yaml restart client
docker compose -f docker-compose.prod.yaml build --no-cache
```
