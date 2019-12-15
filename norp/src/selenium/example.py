from selenium import webdriver
from time import sleep
import os


files_already_done = os.listdir('../images/')

embeddings = open('embeddings.txt','r').readlines()
embeddings = [x.strip('\n') for x in embeddings]
embeddings = [x for x in embeddings if not x == '']
print(len(embeddings))

def get_url_and_username(embedding):
  string = embedding.split(">A post shared by ")[1]
  string = string.split('instagram.com/')[1]
  string = string.split('/')[0]
  if 'embed.js' in string:
    string = embedding.split(">A post shared by")[1]
    string = string.split('@')[1]
    string = string.split(')')[0]
    string = string.split('<')[0]
  username = string
  url = embedding.split('data-instgrm-permalink="')[1].split('/?utm_source')[0]
  return url, username
  

for embedding in embeddings:
  print get_url_and_username(embedding)

def make_filename(username):
  return username + '_1'

def already_done(username):
  if make_filename(username) + '.png' in files_already_done:
    return True
  else:
    return False
  

browser = webdriver.Chrome()
browser.get('chrome://settings/')
browser.execute_script('chrome.settingsPrivate.setDefaultZoom(1);')

def take_screenshot(url, filename, close_login=False):
  browser.get(url)
  sleep(2)
  if close_login:
    browser.execute_script("document.querySelectorAll('button.dCJp8.afkep.xqRnw')[0].click();")
  sleep(5)
  os.system('screencapture -R200,300,500,600 ../images/' + filename + '.png')

counter = 0 
for i in range(len(embeddings)):
  close_login = False
  if counter == 0:
    close_login = True
  embedding = embeddings[i]
  url, username = get_url_and_username(embedding)
  if not already_done(username):
    print username
    take_screenshot(url, username + '_1', close_login=close_login)
    counter = counter + 1
browser.close()

