import requests
from bs4 import BeautifulSoup
country = '모로코'
res = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='+country+'+여행+준비')
soup = BeautifulSoup(res.content, 'html.parser')

mydata = soup.select("#nxTsOv div.item-2sM-R")#입국조건
mydata1 = soup.select("#nxTsOv div.item-PxYX-")#한국귀국시
mydata2 = soup.select("#nxTsOv div.cm_content_area li.item")#여행전체크하기
mydata4 = soup.select("#nxTsOv div.item")#추천여행기간

#입국조건
for i in mydata:
    clear_txt = i.get_text().split("여부")	    
    print(f"{clear_txt[0]}여부 : {clear_txt[1]}  ")
print("\n")

#한국귀국시
for k in mydata1:
    clear1_txt = k.get_text()
    print(clear1_txt)
print("\n")    

#여행전체크하기
for j in mydata2:
    clear2_txt = j.get_text()
    print(clear2_txt)
print("\n")    

#추천여행기간   
for m in mydata4:
    clear4_txt = m.get_text()
    print(clear4_txt)    
	 
