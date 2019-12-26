import mysql.connector
import os

mysql_ip = os.environ['mysql_ip']

mydb=mysql.connector.connect(host=mysql_ip,user='root',password='mypassword')

mycursor = mydb.cursor(buffered=True)

mycursor.execute("CREATE DATABASE IF NOT EXISTS blog_samples;")
mycursor.execute("USE blog_samples;")

string = "INSERT INTO tbl_images (id, image_name, image_path, image_order, date) VALUES "
images = os.listdir('images')
images = [x for x in images if not x == '.DS_Store']


def already_in_table(image, table):
  string = "select image_name from " + table + " where image_name = '" + image + "' ;"
  mycursor.execute(string)
  result = list(mycursor)
  if len(result) > 0:
    return True
  else:
    return False


orders = range(1, len(images)+1)
images_to_add = []
last_id = 0
table = 'tbl_images'
for i in range(0, len(images)):
  image = images[i]
  if not already_in_table(image, table):
    images_to_add.append(image)
  else:
    last_id = last_id + 1

for i in range(len(images_to_add)):
  image = images_to_add[i]
  to_add = '(' + str(last_id+1) + ", '" + image + "', '" + 'images/' + image + "', " + str(orders[last_id]) + ", '2018-09-16 10:46:21')" 
  if i < len(images_to_add) - 1:
    to_add = to_add + ','
  else:
    to_add = to_add + ';'
  string = string + to_add
  last_id = last_id + 1
print(string)
if not len(images_to_add) == 0:
  mycursor.execute(string)

string = "ALTER TABLE `tbl_images` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;"
mycursor.execute(string)



string = '''
CREATE TABLE if not exists `all_images` (
  `id` int(11) NOT NULL,
  `image_name` varchar(200) NOT NULL,
  `image_path` varchar(150) NOT NULL,
  `image_order` int(7) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `person` varchar(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
mycursor.execute(string)


all_embeddings_done = open('selenium/all_embeddings_done.txt', 'r').readlines()
all_embeddings_done = [x.strip('\n') for x in all_embeddings_done]
all_embeddings_done = [x for x in all_embeddings_done if not x == '']

last_image_orders = {}
def find_last_image_order(person):
  try: 
    return last_image_orders[person]
    print('matey')
  except:
    string = 'select max(image_order) from all_images where person="' + person + '";'
    print(string)
    mycursor.execute(string)
    to_return = list(mycursor)[0][0]
    if to_return == None:
      to_return = 0
    print('********')
    mycursor.execute('select * from all_images where person="' + person + '";')
    print(list(mycursor))
    return to_return 

def find_last_id():
  mycursor.execute('select max(id) from all_images;')
  to_return = list(mycursor)[0][0]
  if to_return == None:
    to_return = 0
  return to_return

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


last_id = find_last_id()



embeddings_to_add = open('selenium/all_embeddings.txt', 'r').readlines()
embeddings_to_add = [x.strip('\n') for x in embeddings_to_add]
embeddings_to_add = [x for x in embeddings_to_add if not x == '']
embeddings_to_add = [x for x in embeddings_to_add if not x in all_embeddings_done]

string = "INSERT INTO all_images (id, image_name, image_path, image_order, date, person) VALUES "

for i in range(len(embeddings_to_add)):
  embedding = embeddings_to_add[i]
  url, person = get_url_and_username(embedding)
  url = url + "/media/?size=l"
  last_image_order = find_last_image_order(person)
  to_add = '(' + str(last_id+1) + ", '" + person + '_' + str(last_image_order+1) + "', '" + url + "', " + str(last_image_order+1) + ", '2018-09-16 10:46:21', '" + person + "')"
  last_image_orders[person] = find_last_image_order(person)+1
  if i < len(embeddings_to_add) - 1:
    to_add = to_add + ','
  else:
    to_add = to_add + ';'
  string = string + to_add
  last_id = last_id + 1

print(string)
  
if not len(embeddings_to_add) == 0:
  mycursor.execute(string)



string = "COMMIT;"
mycursor.execute(string)

print('fine')

all_embeddings_done = all_embeddings_done + embeddings_to_add
all_embeddings_done_file = open('selenium/all_embeddings_done.txt', 'w')
all_embeddings_done_file.write('\n'.join(all_embeddings_done))


'''
you have a list of embeddings
you see which ones you need to add
then for each of those, you need to tind the person, then find the last number, the last id, then make the image name by person + '_' + the last number + 1 


'''


# string='drop table all_images;'
# mycursor.execute(string)





'''
the version which uses the directory all_images
'''

# all_images = os.listdir('all_images')
# all_images = [x for x in all_images if not x== '.DS_Store']
# table = 'all_images'
# 
# def get_username(filename):
#   s = filename.split('_')
#   return '_'.join(s[0:len(s)-1])
#  
# images_to_add = [] 
# for image in all_images:
#   if not already_in_table(image, table):
#     images_to_add.append(image)
# 
# last_image_orders = {}
# def find_last_image_order(person):
#   try: 
#     return last_image_orders[person]
#     print('matey')
#   except:
#     string = 'select max(image_order) from all_images where person="' + person + '";'
#     print(string)
#     mycursor.execute(string)
#     to_return = list(mycursor)[0][0]
#     if to_return == None:
#       to_return = 0
#     print('********')
#     mycursor.execute('select * from all_images where person="' + person + '";')
#     print(list(mycursor))
#     return to_return 
# 
# print(images_to_add)
# 
# string = "INSERT INTO all_images (id, image_name, image_path, image_order, date, person) VALUES "
# 
# def find_last_id():
#   mycursor.execute('select max(id) from all_images;')
#   to_return = list(mycursor)[0][0]
#   if to_return == None:
#     to_return = 0
#   return to_return
# 
# last_id = find_last_id()
# 
# 
# for i in range(len(images_to_add)):
#   image = images_to_add[i]
#   person = get_username(image)
#   to_add = '(' + str(last_id+1) + ", '" + image + "', '" + 'all_images/' + image + "', " + str(find_last_image_order(person)+1) + ", '2018-09-16 10:46:21', '" + person + "')"
#   last_image_orders[person] = find_last_image_order(person)+1
#   if i < len(images_to_add) - 1:
#     to_add = to_add + ','
#   else:
#     to_add = to_add + ';'
#   string = string + to_add
#   last_id = last_id + 1
# 
# print(string)
# if not len(images_to_add) == 0:
#   mycursor.execute(string)
# 
# 
# '''
# plan:
# if an image is already in the table, then you ignore it
# if not, you can find the id by taking last_id which is len(all_images) and then adding 1
# image order is most complicated
# if it is a new image, then you look at the maximum of the image orders of the ones for that person
# then you make image_order for that image be set to that maximum image order + 1
# '''
# 
# 
# 
# string = "COMMIT;"
# mycursor.execute(string)
# 
# print('fine')
# 
# string='drop table all_images;'
# mycursor.execute(string)
# print('fine')