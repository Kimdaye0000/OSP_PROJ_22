#!/usr/bin/python3
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def crawl(country: str):
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

    for key, value in countryInfoDocument.items():
        if value:
            print(key, value)

    '''searchPopularDoc = { # Naver 검색어 트렌드 문서화
        "period" : periodList,
        "ratio" : ratioList,
    }'''

    return countryInfoDocument

if __name__ == '__main__':
    country = '모로코'
    print(crawl(country))