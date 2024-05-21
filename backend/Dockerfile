# 기본 이미지로 Python 3.10 사용
FROM python:3.10

# 현재 디렉터리의 모든 파일을 컨테이너의 /backend 디렉터리로 복사
COPY . /backend

# 작업 디렉터리 설정
WORKDIR /backend

# pip 업그레이드 및 의존성 설치
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install libgl1-mesa-glx -y

# 컨테이너를 실행할 때 사용될 명령 설정 (예시로 gunicorn을 사용하여 FastAPI 서버 실행)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


