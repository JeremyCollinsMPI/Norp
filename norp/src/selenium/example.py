from selenium import webdriver
from time import sleep
import os

browser = webdriver.Chrome()
browser.get('chrome://settings/')
browser.execute_script('chrome.settingsPrivate.setDefaultZoom(1);')


urls = open('urls.txt','r').readlines()
urls = [x.strip('\n') for x in urls]
urls = [x for x in urls if not x == '']
def take_screenshot(url, filename, close_login=False):
  browser.get(url)
  if close_login:
    browser.execute_script("document.querySelectorAll('button.dCJp8.afkep.xqRnw')[0].click();")
  sleep(5)
  os.system('screencapture -R200,300,500,600 ../images/' + filename + '.png')
  
for i in range(len(urls)):
  close_login = False
  if i == 0:
    close_login = True
  url = urls[i]
  take_screenshot(url, str(i), close_login=close_login)
browser.close()

