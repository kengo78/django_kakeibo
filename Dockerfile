FROM python:3.7
ENV PYTHONUNBUFFERED 1
#     && apk add --update-cache --no-cache \
#     && apt-get install –y vim 
# 作業ディレクトリの作成
RUN mkdir /code
# RUN apt-get update && apt-get -y install vim

# 作業ディレクトリの設定
WORKDIR /code

# カレントディレクトリにある資産をコンテナ上の指定のディレクトリにコピーする
COPY requirements.txt /code/

RUN python -m pip install --upgrade pip
RUN pip install django
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8000