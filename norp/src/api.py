from flask import Flask
from flask_restful import Resource, Api
import os
import random
import mysql.connector


app = Flask(__name__)
api = Api(app)

mysql_ip = os.environ['mysql_ip']

mydb=mysql.connector.connect(host=mysql_ip,user='root',password='mypassword')

mycursor = mydb.cursor(buffered=True)
mycursor.execute("USE blog_samples;")
sample_size = 10

class RandomSample():
  @app.route("/random", methods=['GET'])
  def moose1():
    mycursor.execute("USE blog_samples;")
    mycursor.execute('select id from tbl_images;')
    ids = list(mycursor)
    ids = [x[0] for x in ids]
    sample = random.sample(ids, sample_size)
    mycursor.execute('update tbl_images set current_sample=NULL;')
    for i in range(sample_size):
      mycursor.execute("update tbl_images set current_sample=" + str(i) + " where id=" + str(sample[i]) + ';')
    mycursor.execute('COMMIT;')
    return 'success'

class Record():
  @app.route("/record", methods=['GET'])
  def moose2():
    try:
      mycursor.execute('select sample1 from tbl_images;')
      mycursor.execute('update tbl_images set sample1=current_sample;')
      mycursor.execute('COMMIT;')
      return 'success'
    except:
      mycursor.execute('alter table tbl_images add column sample1 int;')
      mycursor.execute('update tbl_images set sample1=current_sample;')
      mycursor.execute('COMMIT;')
      return 'success'

class Query():
  @app.route("/query", methods=['GET'])
  def moose3():
    mycursor.execute('select sample1 from tbl_images where sample1 is not null;')
    return str(list(mycursor))





if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port = 89)
