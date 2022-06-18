from elasticsearch import Elasticsearch

def indexChecker(name):
    if es.indices.exists(index=name):
        es.indices.delete(index=name)

def insertToES(index, id, document):
    es.index(index=index ,id=id,document=document )

def infoFromES(searchCountry:str , searchIdx:str): # index값과 나라이름을 입력하면 해당 값을 dict로 반환합니다.
    retResult = es.search(index=searchIdx, body={"query": {
            "bool": {
            "filter": [
                {
                "match_phrase": {
                    "Country":searchCountry
                }
                }
            ]
            }
        }})
    return retResult['hits']['hits'][0]['_source']


es_host ="http://localhost:9200"

inboundData = mydata # 변수 시인성 확대
quarantineInfo = mydata1
travelTip = mydata2
recomDate = mydata4


for i,text in enumerate(inboundData): # 현재 입국가능여부, 백신필수여부, 현지격리여부
    idx = text.get_text().find('여부') + 2
    if( i == 0):
        isEntPass = text.get_text()[idx:]
    elif(i == 1):
        isVaccineReq = text.get_text()[idx:]
    else:
        isQurantAtDest = text.get_text()[idx:]
# print(isEntPass)
# print(isVaccineReq)
# print(isQurantAtDest)
# print()

for i,text in enumerate(quarantineInfo): # 백신접종여부에 따른 격리여부
    idx = text.get_text().find('후') + 2
    if(i == 0):
        vaccinatedPerson = text.get_text()[idx:]
    else:
        unvaccinatedPerson = text.get_text()[idx:]
# print(vaccinatedPerson)
# print(unvaccinatedPerson)
# print()

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
    
# print(flightTime,visaNecessity,currency,voltage,weather,language,timeDiff,tippingCul,livingExp)
# print()

recomDateToGo = recomDate[1].get_text()[4:] # 추천 여행일자
# print(recomDateToGo)

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

searchPopularDoc = { # Naver 검색어 트렌드 문서화
    "period" : periodList,
    "ratio" : ratioList,
}

es = Elasticsearch(es_host)
indexChecker("countryinfo")
indexChecker("searchpopularity")

es.indices.create(index="countryinfo")
es.indices.create(index='searchpopularity')
insertToES('countryinfo', country,countryInfoDocument)
insertToES('searchpopularity',country,searchPopularDoc)
