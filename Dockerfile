FROM python:3.10

LABEL maintainer="darrenkwondev46@gmail.com"

WORKDIR /app

# deps install cache
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# copy source
COPY ./src /app/src

# EXPOSE와 별도로 명령어 실행시 포트 명시 해야함.
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
