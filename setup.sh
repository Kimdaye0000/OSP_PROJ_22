#!/bin/bash

# root diretory로 이동
cd

# 파이썬 실행환경 체크
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# 파이썬 모듈 설치 : requests, beautifulsoup4, elasticsearch
pip install requests beautifulsoup4 elasticsearch

# elasticsearch 확인 후 설치
ES_PATH="elasticsearch-8.2.0"
if [ ! -d $ES_PATH ]; then
    # elasticsearch 다운로드
    ES_GZ="elasticsearch-8.2.0-linux-x86_64.tar.gz"
    if [ ! -f $ES_GZ ]; then
        wget https://artifacts.elastic.co/downloads/elasticsearch/$ES_GZ
    fi
    tar xvzf $ES_GZ

    # elasticsearch 설정
    $ES_PATH/bin/elasticsearch -d -p es.pid
    while [ ! -f $ES_PATH/es.pid ]
    do
        sleep 1
    done
    read < $ES_PATH/es.pid PID
    kill $PID
fi
sed -i 's/xpack.security.enabled: true/xpack.security.enabled: false/' $ES_PATH/config/elasticsearch.yml

# (optional) 리눅스 부팅시 elasticsearch 자동 실행 설정