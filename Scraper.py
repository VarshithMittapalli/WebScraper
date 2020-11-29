import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time

class Scraper:

    def __init__(self, url):
        self.url = url

    def open_browser(self):
        driver = webdriver.Chrome("E:\\python\\Drivers\\chromedriver_win32\\chromedriver.exe")  #full path of your downloaded webdriver
        driver.get(self.url)
        driver.find_element_by_class_name('_34RNph').click()
        time.sleep(3)
        driver.quit()

    def product_url(self):
        self.url += Scraper.keyword()
        return self.url

    #This method takes the keyword by voice recognization for url
    def keyword(self):
        print("Tell What's in your mind ?")
        self.cmd = ''
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        self.cmd = r.recognize_google(audio)
        self.cmd = str(self.cmd).lower()
        print(f'Searching for....... : {self.cmd}')
        return self.cmd

    #Scrapes the required data
    def product_list(self):
        res = requests.get(Scraper.product_url()).content
        soup = BeautifulSoup(res, 'html.parser')

        self.items = soup.find_all('div', class_='_4rR01T')
        self.costs = soup.find_all('div', class_='_30jeq3 _1_WHN1')
        self.rating = soup.find_all('div', class_='_3LWZlK')
        print('Connecting to flipkart.com ')

    #Creates the csv file of the products in the respective folder
    def create_csv(self):
        while len(self.items) == 0:
            engine = pyttsx3.init()
            engine.say("Data not found for your search")
            print("Data not found for your search")
            engine.say("plz.. try again")
            print("plz.. try again")
            engine.runAndWait()
            self.url = self.url[:34]
            Scraper.open_browser()
            Scraper.product_list()
        else:
            csv_file = open("SearchProducts.csv", 'wt', newline='', encoding='utf-8')
            try:
                writer = csv.writer(csv_file)
                writer.writerow(('PRODUCT', 'COST', 'RATING'))
                for i in range(0, len(self.items)):
                    writer.writerow((self.items[i].text, self.costs[i].text, self.rating[i].text))
            finally:
                csv_file.close()
            engine = pyttsx3.init()
            engine.say("your Products file is created")
            print("your Products file is created")
            engine.say("GO and check your folder......")
            print("GO and check your folder......")
            engine.runAndWait()

if __name__ == '__main__':
    url = "https://www.flipkart.com/search?q="
    Scraper = Scraper(url)
    Scraper.product_list()
    Scraper.open_browser()
    Scraper.create_csv()
