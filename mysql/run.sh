docker run --rm --name mysql --env="MYSQL_ROOT_PASSWORD=mypassword" -v $PWD/my.cnf:/etc/mysql/my.cnf -v $PWD/data:/var/lib/mysql mysql 
