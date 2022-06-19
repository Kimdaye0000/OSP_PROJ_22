#!/usr/bin/python3
#-*- coding: utf-8 -*-

from elasticsearch import Elasticsearch

# Index가 있는지 확인
def checkIndex(es: Elasticsearch, index: str):
    return es.indices.exists(index=index)

# Index에 데이터 삽입
def insertToIndex(es: Elasticsearch, index: str, id: str, document: dict):
    es.index(index=index, id=id, document=document)

# Index 삭제
def deleteIndex(es: Elasticsearch, index: str):
    if checkIndex(es, index):
        es.indices.delete(index=index)

# Index에서 데이터 검색
def searchFromIndex(es: Elasticsearch, index: str, body: dict):
    es_result = es.search(index=index, body=body)
    if es_result['hits']['total']['value'] > 0:
        return es_result['hits']['hits'][0]['_source']
    else:
        return None