from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import re
import os
directory =  r"your_directory" #directory where all the txt files are located
dir =  r"audio_directory" #directory where you want to save the audio files
roi = 'no info on the website'
s = Service("PATH_TO_CHROMEDRIVER")
driver = webdriver.Chrome(service=s)
driver.get('https://www.shortform.com/app/login')
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, '[type=email]').send_keys('YOUR_EMAIL')
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '[type=password]').send_keys('YOUR_PASSWORD')
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '[type=submit]').click()
time.sleep(5)
for file_name in os.listdir(directory):
    if file_name.endswith(".txt"):
        file_path = os.path.join(directory, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            contents = file.read()
            link = re.findall(r"https://www.shortform.com/app/book/\S+", contents)[0]
            print(link)
            file_pat = os.path.join(dir, os.path.splitext(file_name)[0] + ".mp3")
            driver.get(link)
            WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.title-section__title')))
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, '.control__btn.player-btn[title=Listen]').click()
            WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.player__content')))
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            mp3 = soup.select_one('audio[src]')['src']
            respon = requests.get(mp3)
            with open(file_pat, 'wb') as f:
                f.write(respon.content)
            
            