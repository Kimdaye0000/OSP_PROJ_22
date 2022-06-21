#!/usr/bin/python
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import datetime

def crawlCountryInfo(country: str):
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=' + country + '+여행+준비'
    res = requests.get(url)
    if res.status_code != 200:
        return None
    soup = BeautifulSoup(res.content, 'html.parser')

    #입국조건
    inboundData = soup.select("#nxTsOv div.item-2sM-R")
    #한국귀국시
    quarantineInfo = soup.select("#nxTsOv div.item-PxYX-")
    #여행전체크하기
    travelTip = soup.select("#nxTsOv div.cm_content_area li.item")
    #추천여행기간
    recomDate = soup.select("#nxTsOv div.item")

    if not(inboundData and quarantineInfo and travelTip and recomDate):
        return None

    isEntPass, isVaccineReq, isQurantAtDest = 'NoData', 'NoData', 'NoData'
    for i,text in enumerate(inboundData): # 현재 입국가능여부, 백신필수여부, 현지격리여부
        idx = text.get_text().find('여부') + 2
        if(i == 0):
            isEntPass = text.get_text()[idx:]
        elif(i == 1):
            isVaccineReq = text.get_text()[idx:]
        else:
            isQurantAtDest = text.get_text()[idx:]

    vaccinatedPerson, unvaccinatedPerson = 'NoData', 'NoData'
    for i,text in enumerate(quarantineInfo): # 백신접종여부에 따른 격리여부
        idx = text.get_text().find('후') + 2
        if(i == 0):
            vaccinatedPerson = text.get_text()[idx:]
        else:
            unvaccinatedPerson = text.get_text()[idx:]

    flightTime,visaNecessity,currency,voltage,weather,language,timeDiff,tippingCul,livingExp = 'NoData','NoData','NoData','NoData','NoData','NoData','NoData','NoData','NoData',
    # 데이터값이 없는경우 구분을 위한 초기화

    for text in travelTip: # 각종 정보 
        text = text.get_text()
        if("항공" in text):
            flightTime = text[4:]
        elif("비자" in text):
            visaNecessity = text[2:]
        elif("환율" in text):
            currency = text[2:]
        elif("전압" in text):
            voltage = text[2:]
        elif("날씨" in text):
            weather = text[2:]
        elif("언어" in text):
            language = text[2:]
        elif("시차" in text):
            timeDiff = text[2:]
        elif("팁" in text):
            tippingCul = text[3:]
        elif("물가" in text):
            livingExp = text[2:]

    recomDateToGo = recomDate[1].get_text()[4:] # 추천 여행일자

    countryInfoDocument = { # ES 문서화
        "Country" : country,
        "PossibleToVisit" : isEntPass,
        "Vaccination" : isVaccineReq,
        "QurantineInfo" : isQurantAtDest,
        "VaccineStatus_Not" : unvaccinatedPerson,
        "VaccineStatus_OK" : vaccinatedPerson,
        "FlightTime" : flightTime,
        "Visa" : visaNecessity,
        "ExchangeRate" : currency,
        "Voltage" : voltage,
        "Weather" : weather,
        "Language" : language,
        "TimeDifference": timeDiff,
        "TippingCulture" : tippingCul,
        "LivingCost" : livingExp
    }

    return countryInfoDocument

def crawlSearchPopularity(country: str):
    # datetime 모듈에서 날짜 가져오기
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    
    #naverAPI id, secret(나중에 가릴 것)
    client_id = "HaWOrcasRaKjXojoFXFs"
    client_secret = "sTTbLrJsi9"
    header_parm = { "X-Naver-Client-Id" : client_id, "X-Naver-Client-Secret" : client_secret }
    naver_datalab = "https://openapi.naver.com/v1/datalab/search"

    keywordsG = [ { "groupName" : country + "여행", "keywords" : [ country + "여행" ] } ]
    enddate = "%d-%02d-%02d" % (year, month, day)
    postdata = { "startDate" : "2022-01-02", "endDate" : enddate, "timeUnit" : "month", "keywordGroups" : keywordsG}

    res = requests.post(naver_datalab, headers=header_parm, json=postdata)
    #입력 키워드는 여행국가명+여행, 데이터는 한달단위로 받아옴 필요시 수정가능

    if (res.status_code == 200):
        data = res.json()
        periodList = [i['period'] for i in data['results'][0]['data']] # 몇 월 데이터인지
        ratioList = [int(i['ratio']) for i in data['results'][0]['data']]   # 최고 검색달이 100으로 기준잡히고 나머지 상대적 표현

        searchPopularDoc = { # Naver 검색어 트렌드 문서화
            "period" : periodList,
            "ratio" : ratioList,
        }

        return searchPopularDoc
    else:
        return None

if __name__ == '__main__':
    country = '한국'
    print(crawlCountryInfo(country))
    print(crawlSearchPopularity(country))