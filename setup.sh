#!/usr/bin/bash

# home 경로로 이동
cd

# 파이썬 실행환경 체크
update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# 파이썬 모듈 설치 : requests, beautifulsoup4, elasticsearch
pip install requests beautifulsoup4 elasticsearch

# elasticsearch 다운로드
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.2.0-linux-x86_64.tar.gz
tar xvzf elasticsearch-8.2.0-linux-x86_64.tar.gz

# (optional) 리눅스 부팅시 elasticsearch 자동 실행 설정