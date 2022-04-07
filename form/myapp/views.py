#importy potřebných knihoven


from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import smtplib
import schedule
import time
from . forms import formular
from typing import List



def email_sender( adresat, messsg):
	server =smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login('sokolim@stredniskola.cz', '******') #můj cvičný email  pro log
	server.sendmail("sokolim@stredniskola.cz", adresat,messsg )#funkce pro odeslání emailu






  #funkce pro kontrolu změny  počtu nabídek 
def kontrola():
	headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}
	
	htmls = requests.get("https://jiho.ceskereality.cz/pronajem/byty/cast-ceske-budejovice-1/", headers=headers )
	htmls = htmls.text
	b = BeautifulSoup(  htmls, "lxml")
	pocet_nemovitosti = b.find("span", class_ = "number").text
	return pocet_nemovitosti


def contact(request): # spracovani formulare
	predchozi = 0
	if request.method =="POST":
		form = formular(request.POST)
		if form.is_valid():
			
			text = form.cleaned_data["email"] # ukládám zadany email
			l = kontrola()
			email_sender(text, l.encode("utf-8")) # na začátku chci aby na vybraný mail přišel aktualní počet nabídek který se může měnit

			schedule.every(200).seconds.do(kontrola) # každách dvěstě sekund proběhne refresh 
			while True:
				schedule.run_pending()
				vystup  = kontrola() #ukládám danou hodnotu
	
				if vystup !=predchozi: #pokud se nerovná té předchozí tak posílám email 
					a ="ahoj tady jsou nové nabytky" + str(vystup) 
					email_sender(text, a.encode("utf-8"))
	
				predchozi = vystup
				time.sleep(5)


			

	form = formular()
	return  render(request,"form.html", {"form": form })




  




