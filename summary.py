from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import re
import os
directory =  r"your_directory"
roi = 'no info on the website'
s = Service("PATH_TO_CHROMDRIVER")
driver = webdriver.Chrome(service=s)
driver.get('https://www.shortform.com/app/login')
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, '[type=email]').send_keys('your_login')
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '[type=password]').send_keys('your_password')
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
            with open(file_path, "a", encoding="utf-8") as txtfile:
                current_time = datetime.now(pytz.timezone('Europe/Berlin'))
                berlin = current_time.strftime('%Y-%m-%d %H:%M:%S %Z')
                txtfile.write(f'Berlin time: {berlin}\n\n')
                while True:
                    driver.get(link)
                    WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.title-section__title')))
                    time.sleep(3)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    for s in soup.find(class_='book-reading__content-editor content-editor font-medium line-medium margin-medium').find_all(['p', 'h2', 'h3', 'h4', 'h5', 'li']):
                        txtfile.write(s.text.strip() + '\n\n')
                    if soup.find('p', class_='book-reading-nav__name book-reading-nav__next-name').text == ' Go to home page ':
                        break
                    else:
                        link = 'https://www.shortform.com' + soup.find('a', class_='book-reading-nav__next-box')['href']
                        txtfile.write(f'Link of the next section: {link}\n\n')