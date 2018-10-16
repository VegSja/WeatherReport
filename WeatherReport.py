# coding=utf-8
import time
import os
import RPi.GPIO as GPIO
from bs4 import BeautifulSoup as soup
from urllib import urlopen as uReq

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.IN)

#Defines wheter or not the weather is nice
def weatherMood(weather):
	osWeather = "say'Good morning! Today's weather is forecasted to be: '" + "say" + weather
	if weather == "Heavy rain." or weather == "Rain." or weather == "Kraftige regnbyger." or weather == "Kraftig regn.":
		print("red")
		os.system(osWeather)
	elif weather == "Cloudy." or weather == "Lette regnbyger.":
		print("yellow")
		os.system(osWeather)
	elif weather == "Partly cloudy." or weather == "Lettskyet." or weather == "Clear sky." or "Klarvær.":
		print("green")
		os.system(osWeather)
	else:
		print("Unable to decide")
		os.system("Oh, Something went wrong")

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

def checkButton():
	if(GPIO.input(10)):
		print("Button Pressed")
		getURL()
	else:
		os.system('clear')
		print ("Waiting for buttonpress")
	time.sleep(1)
while True:
	checkButton()

