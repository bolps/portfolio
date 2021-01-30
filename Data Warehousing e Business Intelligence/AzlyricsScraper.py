import re
import random
import argparse
import pandas as pd
from bs4 import BeautifulSoup
from langdetect import detect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from numpy import random

class AzlyricsScraper:
    def __init__(self, search, randomSample = -1, minSleep = 5, maxSleep = 20, headless=True):

        #IPERPARAMETRI SCRAPER (Selettori da aggiornare in caso di modifiche all'html del sito)
        self.BASEURL = "https://www.azlyrics.com/"
        self.SEL_SEARCHTEXT = "form-control"
        self.SEL_SEARCHBUTTON = "#search-collapse > form > div > span > button"
        self.SEL_SONGLINK = "listalbum-item"
        self.SEL_ARTIST = "body > div.container.main-page > div > div > div:nth-child(2) > table > tbody > tr > td > a > b"
        self.SEL_ALBUMSBUTTON = "body > div.container.main-page > div > div > div:nth-child(2) > table > tbody > tr > td > a"
        self.SEL_ALBUMLINK = "listalbum-item"
        self.SEL_LYRIC = "/html/body/div[2]/div/div[2]/div[5]"
        self.SEL_ALBUMNAME = "songinalbum_title"
        self.SEL_SONGYEAR = "songinalbum_title"
        self.SEL_AUTHOR = "/html/body/div[2]/div/div[2]/div[10]/small"

        #IPERPARAMETRI BROWSER
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--log-level=3")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36")

        # VARIABILI
        self.search = search
        self.randomSample = randomSample
        self.minSleep = minSleep
        self.maxSleep = maxSleep
        self.headless = headless
        self.warning = False
        self.artist = None
        self.links = []
        self.titles = []
        self.lyrics = []
        self.lang = []
        self.albums = []
        self.years = []
        self.authors = []

    # Salva il nome dell'artista e i link ai testi delle canzoni
    def getBasicInfo(self):
        if self.headless == True:
            driver = webdriver.Chrome(options=self.chrome_options)
        else:
            driver = webdriver.Chrome()
        driver.get(self.BASEURL)
        sleep(random.uniform(2,4))

        text = driver.find_element_by_class_name(self.SEL_SEARCHTEXT) #trovo il modulo input testo
        search_button = driver.find_element_by_css_selector(self.SEL_SEARCHBUTTON) #trovo il bottone
        text.send_keys(self.search) #scrivo la chiave di ricerca
        search_button.click()
        sleep(random.uniform(2,4))

        self.artist = driver.find_element_by_css_selector(self.SEL_ARTIST).text
        expand_artist = driver.find_element_by_css_selector(self.SEL_ALBUMSBUTTON)
        driver.execute_script("arguments[0].click();", expand_artist)
        sleep(random.uniform(2,4))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        songs = soup.find_all('div', attrs={'class':self.SEL_ALBUMLINK})

        if self.randomSample != -1:
            random.shuffle(songs)
            songs = songs[0:self.randomSample]

        for song in songs:
            title = song.find('a').get_text()
            href = song.find('a').get('href')
            self.titles.append(title)
            self.links.append("https://www.azlyrics.com/"+href[2:])

        driver.close()

    # Salva i testi dei brani e le informazioni addizionali (anno di rilascio, album, compositori, lingua)
    def getLyrics(self):
        if self.headless == True:
            driver = webdriver.Chrome(options=self.chrome_options)
        else:
            driver = webdriver.Chrome()
        try:
            for link in self.links:
                driver.get(link)

                try:
                    lyric = driver.find_element_by_xpath(self.SEL_LYRIC).text
                    self.lyrics.append(lyric)
                except:
                    self.lyrics.append(None)

                if lyric != None:
                    try:
                        self.lang.append(detect(lyric))
                    except:
                        self.lang.append(None)
                else:
                    self.lang.append(None)

                try:
                    album = driver.find_element_by_class_name(self.SEL_ALBUMNAME).text
                    album = re.search(r'\"(.+)\"', album).group(1)
                    album = album.strip('"')
                    self.albums.append(album)
                except:
                    self.albums.append(None)

                try:
                    year = driver.find_element_by_class_name(self.SEL_SONGYEAR).text
                    year = re.search((r'\((\d+)\)'), year).group(1)
                    self.years.append(year)
                except:
                    self.years.append(None)

                try:
                    author = driver.find_element_by_xpath(self.SEL_AUTHOR).text[11:]
                    self.authors.append(author)
                except:
                    self.authors.append(None)

                sleep(random.uniform(self.minSleep,self.maxSleep))
        except:
            self.lyrics.append(None)
            self.albums.append(None)
            self.years.append(None)
            self.authors.append(None)
            self.warning = True
        driver.close()

    def dumpCSV(self):
        df = pd.DataFrame()
        try:
            df["Artist"] = [self.artist] * len(self.titles)
            df["Year"] = self.years
            df["Album"] = self.albums
            df["Title"] = self.titles
            df["Authors"] = self.authors
            df["Lyric"] = self.lyrics
            df["Language"] = self.lang
            df["Links"] = self.links
        except:
            print("Attenzione, sono state salvate solo le informazioni base (titolo, artista, link).\nPer un dataset completo assicurati di aver eseguito prima del dump anche il metodo getLyrics()")
            df["Artist"] = [self.artist] * len(self.titles)
            df["Title"] = self.titles
            df["Links"] = self.links

        df.to_csv('{}-Lyrics.csv'.format(self.artist), index = False)

        if self.warning == True:
            print("Attenzione, il sito potrebbe aver bloccato lo scraping.\nI dati relativi ai testi sono stati salvati solo parzialmente.")


parser = argparse.ArgumentParser(description='*** AzlyricsScraper ***')
parser.add_argument("--artist", required=True, type=str, help="")
parser.add_argument("--sample", required=False, type=int, default=-1, help="")
parser.add_argument("--minsleep", required=False, type=int, default=5, help="")
parser.add_argument("--maxsleep", required=False, type=int, default=20, help="")
parser.add_argument("--headless", required=False, action="store_true", help="")
args = parser.parse_args()

scraperBeatles = AzlyricsScraper(args.artist, randomSample = args.sample, minSleep = args.minsleep, maxSleep = args.maxsleep, headless = args.headless)
scraperBeatles.getBasicInfo()
scraperBeatles.getLyrics()
scraperBeatles.dumpCSV()
