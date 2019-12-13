import os
file = open('/src/db_template.php','r').read()
mysql_ip = os.environ['mysql_ip']
print(mysql_ip)
output = file.replace('MYSQL_IP', "'" + mysql_ip + "'")
output_file = open('/src/db.php', 'w')
output_file.write(output)