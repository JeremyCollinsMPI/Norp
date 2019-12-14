import mysql.connector
import os

mysql_ip = os.environ['mysql_ip']

mydb=mysql.connector.connect(host=mysql_ip,user='root',password='mypassword')

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS blog_samples;")
mycursor.execute("USE blog_samples;")
mycursor.execute("DROP TABLE IF EXISTS tbl_images;")
string = '''
CREATE TABLE `tbl_images` (
  `id` int(11) NOT NULL,
  `image_name` varchar(200) NOT NULL,
  `image_path` varchar(50) NOT NULL,
  `image_order` int(7) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
mycursor.execute(string)
string = "INSERT INTO tbl_images (id, image_name, image_path, image_order, date) VALUES "
images = os.listdir('images')
images = [x for x in images if not x == '.DS_Store']
print(images)
orders = range(1, len(images)+1)
for i in range(0, len(images)):
  image = images[i]
  to_add = '(' + str(i+1) + ", '" + image + "', '" + 'images/' + image + "', " + str(orders[i]) + ", '2018-09-16 10:46:21')" 
  if i < len(images) - 1:
    to_add = to_add + ','
  else:
    to_add = to_add + ';'
  string = string + to_add
print(string)
mycursor.execute(string)
# mycursor.execute('COMMIT;')

string = "ALTER TABLE `tbl_images` ADD PRIMARY KEY (`id`);"
mycursor.execute(string)
string = "ALTER TABLE `tbl_images` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;"
mycursor.execute(string)
string = "COMMIT;"
mycursor.execute(string)

string = "SELECT * FROM tbl_images;"
x  = mycursor.execute(string)
print(x)

