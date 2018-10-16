import time
import os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

#Defines wheter or not the weather is nice
def weatherMood(weather):
	if weather == "Heavy rain." or weather == "Rain." or weather == "Kraftige regnbyger." or weather == "Kraftig regn.":
		print("red")
	elif weather == "Cloudy." or weather == "Lette regnbyger.":
		print("yellow")
	elif weather == "Partly cloudy." or weather == "Lettskyet." or weather == "Clear sky." or "Klarvær.":
		print("green")
	else:
		print("Unable to decide")

#Finds the weather for today
def findToday(page_soup):
	table_soup = page_soup.find("table", {"class":"yr-table yr-table-overview2 yr-popup-area"})
	todayWeather = table_soup.find("figcaption").get_text()
	print(todayWeather)
	weatherMood(todayWeather)

#Gets the HTML and writes it to a file
def getWebsite(url):
	
	page_html = uReq(url)
	page_soup = soup(page_html, "html.parser")
	findToday(page_soup)

#Gets the URL from the user and saves it to userpref.txt
def getURL():
	f = open("userpref.txt", "r")
	lines = f.readlines()
	if os.stat("userpref.txt").st_size == 0:
		url = input("Enter your link: ")
	else:
		url = lines[1]
	f = open("userpref.txt", "w")
	f.write("URL:\n" + url)
	f.close()
	getWebsite(url)

def newURL():
	f = open("userpref.txt", "w")
	url = input("What is your new URL?: ")
	f.write("URL:\n" + url)
	f.close()
	getWebsite(url)

def startScreen():
	print("What do you want to do?:\n1. Check weather\n2. Change location" )
	choice = input("");
	if choice == "1":
		getURL()
	elif choice == "2":
		newURL()
	else:
		print("Error")
		newURL()

startScreen()