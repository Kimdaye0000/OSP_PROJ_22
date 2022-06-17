import requests
from bs4 import BeautifulSoup
country = '모로코'
res = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='+country+'+여행+준비')
soup = BeautifulSoup(res.content, 'html.parser')

entry = soup.select("#nxTsOv div.item-2sM-R")#입국조건
home = soup.select("#nxTsOv div.item-PxYX-")#한국귀국시
check = soup.select("#nxTsOv div.cm_content_area li.item")#여행전체크하기
recommend = soup.select("#nxTsOv div.item")#추천여행기간

#입국조건
for i in entry:
    entry_txt = i.get_text().split("여부")	    
    print(f"{entry_txt[0]}여부 : {entry_txt[1]}  ")
print("\n")

#한국귀국시
for k in home:
    home_txt = k.get_text()
    print(home_txt)
print("\n")    

#여행전체크하기
for j in check:
    check_txt = j.get_text()
    print(check_txt)
print("\n")    

#추천여행기간   
for m in recommend:
    recommend_txt = m.get_text()
    print(recommend_txt)    
	 
