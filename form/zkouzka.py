### import ptřebných knihoven #######
# from pickletools import int4
from bs4 import BeautifulSoup
import requests
import smtplib
import schedule
import time

def email_sender(messsg):
	server =smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login('sokolim@stredniskola.cz', 'Dunajovice49')
	server.sendmail("sokolim@stredniskola.cz", "ragnarsokolik@gmail.com",messsg )

predchozi = 0



  
def kontrola():
	headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}
	 
	htmls = requests.get("https://jiho.ceskereality.cz/pronajem/byty/cast-ceske-budejovice-1/", headers=headers )
	htmls = htmls.text
	b = BeautifulSoup(  htmls, "lxml")
	pocet_nemovitosti = b.find("span", class_ = "number").text
	l = b.findAll("div", class_ ="div_nemovitost suda")
	return pocet_nemovitosti, l
	
  
schedule.every(5).seconds.do(kontrola)
  
while True:
	
	schedule.run_pending()
	vystup  = kontrola()
	data = vystup[1]
	

	if vystup !=predchozi:
		a ="ahoj tady jsou nové nabytky"
		email_sender(a.encode("utf-8"))
	else:
		print("ahoj")
	
	predchozi = vystup
	
		
		

	
	time.sleep(5)




  

  

  

  

