# coding=utf-8
import time
import os
import RPi.GPIO as GPIO
from bs4 import BeautifulSoup as soup
from urllib import urlopen as uReq

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.IN)

GPIO.setup(4, GPIO.OUT) #Red
GPIO.setup(3, GPIO.OUT) #Yellow
GPIO.setup(2, GPIO.OUT) #Green

#Starts Light Blinking
def blink(color):
	print("Starting " + color + "Blink")
	for x in range (0, 10):
		print(x)
		if color == "RED":
			GPIO.output(4, GPIO.HIGH)
		elif color == "YELLOW":
			GPIO.output(3, GPIO.HIGH)
		elif color == "GREEN":
			GPIO.output(2, GPIO.HIGH)
		else:
			return
		print("Turning off lights")
		time.sleep(1)
		GPIO.output(2, GPIO.LOW)
		GPIO.output(3, GPIO.LOW)
		GPIO.output(4, GPIO.LOW)
		time.sleep(1)

def badWeather(weather):
	print("red")
	weatherOs= "say " + "Hello! Todays weather is forecasted to be: " + weather + "It is time to get depressed"
        os.system(weatherOs)
	blink("RED")
	time.sleep(6)

def mehWeather(weather):
	print("Yellow")
	weatherOs= "say " + "Hello! Todays weather is forecasted to be: " + weather
	os.system(weatherOs)
	blink("YELLOW")
	time.sleep(3)

def goodWeather(weather):
	print("Green")
	print(weather) 
        weatherOs= "say " + "Hello! Todays weather is forecasted to be: " + weather
	os.system(weatherOs)
	blink("GREEN")
	time.sleep(6)

#Defines wheter or not the weather is nice
def weatherMood(weather):
	if weather == "Heavy rain." or weather == "Rain." or weather == "Kraftige regnbyger." or weather == "Kraftig regn." or weather == "Rain showers.":
		badWeather(weather)
	elif weather == "Cloudy." or weather == "Lette regnbyger." or weather == "Lett regn.":
		mehWeather(weather)
	elif weather == "Partly cloudy." or weather == "Lettskyet." or weather == "Clear sky." or "Klarvær.":
		goodWeather(weather)

	else:
		print("Unable to decide")
		os.system("Oh, Something went wrong with the weather recognition")

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
		GPIO.output(2, GPIO.LOW)
                GPIO.output(3, GPIO.LOW)
                GPIO.output(4, GPIO.LOW)
	time.sleep(1)
while True:
	checkButton()

