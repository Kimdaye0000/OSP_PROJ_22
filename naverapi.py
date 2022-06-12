import requests
import pprint
import datetime

year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day

nation = "일본" # 나중에 사용자 입력으로 수정

client_id = " "
client_secret = " " # 깃허브에 오픈되기 때문에 가려놉니다 필요시 디스코드에 올려드릴테니 확인해보세요
header_parm= {"X-Naver-Client-Id":client_id, "X-Naver-Client-Secret":client_secret} 
naver_datalab = "https://openapi.naver.com/v1/datalab/search"
keywordsG = [{"groupName":f"{nation}여행","keywords":[f"{nation}여행"]}]
enddate = f"{year}-0{month}-{day}"


res = requests.post(naver_datalab,headers=header_parm, json={"startDate":"2022-01-02", "endDate":enddate, "timeUnit":"month", "keywordGroups":keywordsG})
#입력 키워드는 여행국가명+여행, 데이터는 한달단위로 받아옴 필요시 수정가능


if(res.status_code==200):
    data = res.json()
    pprint.pp(data) 
    periodList = [i['period'] for i in data['results'][0]['data']] # 몇 월 데이터인지
    ratioList = [int(i['ratio']) for i in data['results'][0]['data']]   # 최고 검색달이 100으로 기준잡히고 나머지 상대적 표현
    print(periodList)
    print(ratioList)

else:
    print("Error Code:" + res.status_code)