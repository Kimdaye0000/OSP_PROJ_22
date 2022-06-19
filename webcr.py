import requests
from bs4 import BeautifulSoup

#외교부해외안전여행_안전공지
notice = requests.get('https://www.0404.go.kr/dev/newest_list.mofa')
sp = BeautifulSoup(notice.content, 'html.parser')

#제목
title = sp.select("#content.Content h3.Ctit")

#제목 출력
for t in title:
    title_txt = t.get_text()
    print(title_txt)    

#공지
notice_19 = sp.select("#content.Content td.subject b")

#공지출력
for n in notice_19:
    notice19_txt = n.get_text()
    print(notice19_txt)    
print("\n")

#여행 관련 정보
country = ''
while(1):
	country = input('나라를 한국어로 입력해주세요 : ')
	if(country.encode().isalpha()==False):
		break		
print("\n")

res = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='+country+'+여행+준비')
soup = BeautifulSoup(res.content, 'html.parser')

#입국조건
entry = soup.select("#nxTsOv div.item-2sM-R")
#한국귀국시
home = soup.select("#nxTsOv div.item-PxYX-")
#여행전체크하기
check = soup.select("#nxTsOv div.cm_content_area li.item")
#추천여행기간
recommend = soup.select("#nxTsOv div.item")

#입국조건 출력
for e in entry:
	entry_txt = e.get_text().split("여부")	    
	print(f"{entry_txt[0]}여부 : {entry_txt[1]}  ")
print("\n")

#한국귀국시 출력
for h in home:
	home_txt = h.get_text()
	print(home_txt)
print("\n")    
	
#여행전체크하기 출력
for c in check:
	check_txt = c.get_text()
	print(check_txt)
print("\n")    

#추천여행기간 출력   
for r in recommend:
	recommend_txt = r.get_text()
	print(recommend_txt)    
	 	
