FROM python:3.7
# RUN apt-get update && apt-get install -y git \
ENV PYTHONUNBUFFERED 1
#     && apk add --update-cache --no-cache \
#     && apt-get install –y vim 
# 作業ディレクトリの作成
RUN mkdir /code
# RUN apt-get update && apt-get -y install vim

# 作業ディレクトリの設定
WORKDIR /code

# カレントディレクトリにある資産をコンテナ上の指定のディレクトリにコピーする
ADD . /code

RUN python -m pip install --upgrade pip
RUN pip install django
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 8000