from flask import Flask
from flask_restful import Resource, Api
from flask import request
import os
import random
import mysql.connector
from elopy import *

app = Flask(__name__)
api = Api(app)

mysql_ip = os.environ['mysql_ip']

mydb=mysql.connector.connect(host=mysql_ip,user='root',password='mypassword')

mycursor = mydb.cursor(buffered=True)
mycursor.execute("USE blog_samples;")
sample_size = 5

def find_next_pair(index1, index2, last_index):
  if index2 < last_index:
    index2 = index2 + 1
    return index1, index2
  else:
    if index1 < last_index - 1:
      index1 = index1 + 1
      index2 = index1 + 1
      return index1, index2
    else:
      return None, None
      
def get_pairs(id_list):
  pairs = []
  index1 = 0
  index2 = 1
  last_index = len(id_list) - 1
  end = False
  while not end:
    pairs = pairs + [[id_list[index1], id_list[index2]]]
    index1, index2 = find_next_pair(index1=index1, index2=index2, last_index=last_index)
    if index1 == None and index2 == None:
      end = True
      return pairs

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
    return ''

class Record():
  @app.route("/record", methods=['GET'])
  def moose2():
    done = False
    i = 1
    while done == False:
      try:
        mycursor.execute('select sample' + str(i) + ' from tbl_images;')
        i = i + 1
      except:
        mycursor.execute('alter table tbl_images add column sample' + str(i) + ' int;')
        mycursor.execute('update tbl_images set sample' + str(i) + '=current_sample;')
        mycursor.execute('COMMIT;')
        done = True
        return 'moo'

class Query():
  @app.route("/query", methods=['GET'])
  def moose3():
    sample = request.args.get('sample')
    try:
      mycursor.execute('select sample' + sample + ' from tbl_images;')

    except:
      return 'No column ' + sample + '.'
    return str(list(mycursor))

class Elo():
  @app.route("/elo", methods=['GET'])
  def moose4():
    done = False
    all_pairs = []
    i = 1
    while done == False:
      try:
        mycursor.execute('select id from tbl_images where sample' + str(i) +' is not null order by sample' + str(i) + ' asc;')
        result = list(mycursor)
        result = [x[0] for x in result]
        pairs = get_pairs(result)
        all_pairs = all_pairs + pairs
        i = i + 1
      except:
        done = True
    all_pairs = random.sample(all_pairs, len(all_pairs))
    i = Implementation()    
    for j in range(1,201):
      i.addPlayer(str(j), rating = 1000)
    for pair in all_pairs:
      i.recordMatch(str(pair[0]), str(pair[1]), winner=str(pair[0]))
      print(i.getRatingList())
    try:
      mycursor.execute('select elo from tbl_images;')
    except:
      mycursor.execute('alter table tbl_images add column elo float(8,2);')
    for member in i.getRatingList():
      id = member[0]
      ranking = str(round(member[1], 2))
      mycursor.execute('update tbl_images set elo=' + ranking + ' where id=' + id + ';')
    return str(i.getRatingList())
    

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port = 89)
