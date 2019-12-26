from selenium import webdriver
from time import sleep
import os

files_already_done = os.listdir('../all_images/')

embeddings = open('all_embeddings.txt','r').readlines()
embeddings = [x.strip('\n') for x in embeddings]
embeddings = [x for x in embeddings if not x == '']
print(len(embeddings))

urls_already_done = open('urls_already_done.txt', 'r').readlines()
urls_already_done = [x.strip('\n') for x in urls_already_done]

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
  

browser = webdriver.Chrome()
browser.get('chrome://settings/')
browser.execute_script('chrome.settingsPrivate.setDefaultZoom(1);')

def take_screenshot(url, filename, close_login=False):
  browser.get(url)
  sleep(2)
  if close_login:
    browser.execute_script("document.querySelectorAll('button.dCJp8.afkep.xqRnw')[0].click();")
  sleep(5)
  os.system('screencapture -R200,300,500,600 ../all_images/' + filename + '.png')


def get_username_and_number(filename):
  filename = filename.split('.png')[0]
  s = filename.split('_')
  return '_'.join(s[0:len(s)-1]), int(s[-1])

last_user_numbers = {}

for image in files_already_done:
  try:
    username, number = get_username_and_number(image)
    try:
      x = last_user_numbers[username]
      if x < number:
        last_user_numbers[username] = number
    except:
      last_user_numbers[username] = number
  except:
    pass

counter = 0 
for i in range(len(embeddings)):
  close_login = False
  if counter == 0:
    close_login = True
  embedding = embeddings[i]
  url, username = get_url_and_username(embedding)
  if not url in urls_already_done:
    print username
    try:
      last_user_number = last_user_numbers[username]
    except:
      last_user_number = 0
    take_screenshot(url, username + '_' + str(last_user_number+1), close_login=close_login)
    counter = counter + 1
    urls_already_done.append(url)
    last_user_numbers[username] = last_user_number+1
browser.close()

urls_already_done_file = open('urls_already_done.txt', 'w')
urls_already_done_file.write('\n'.join(urls_already_done))

'''
you can see which images are already in all_images
for each person you can get the maximum number which is at the end of the filename
you set last_user_numbers[$person] to that number
you take an embedding, find the username, and then look up its latest number in last_user_numbers
you save the image as person + latest_number + 1
then you update last_user_numbers[$person] to latest number + 1


for each person you can get the maximum number which is at the end of the filename
- how do you do this most efficiently?
you have the filenames;
for each filename, you find the person, and you find the number.
if person is not in last_user_numbers, add it
if it is, then see if last_user_numbers[person] is less than the new number
if it is, then update it with the new number

how do you do already_done?
you are checking whether the embedding has already had a screenshot
so you want to just write urls to a document and check them

'''



