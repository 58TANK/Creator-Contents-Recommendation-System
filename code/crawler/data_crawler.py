from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.youtube.com/channel/UCAJ-meoCh1TrPZ7La3UpPrw/videos?view=0&sort=dd&flow=grid/')
time.sleep(4)

body = driver.find_element_by_tag_name("body")
num_of_pagedowns = 3

while num_of_pagedowns:
  body.send_keys(Keys.PAGE_DOWN)
  time.sleep(1.5)
  num_of_pagedowns -= 1
  try:
    driver.find_elements_by_xpath("""//*[@id="feed-main-what_to_watch"]/button""").click()
  except:
    None

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
titles = soup.find_all('h3')

for title in titles:
  test = title.select('a')
  print(test[0]['href'])
  driver.get('https://www.youtube.com/' + test[0]['href'])
  time.sleep(3)

driver.close()