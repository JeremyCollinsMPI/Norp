mkdir -p mysql/data
docker run --rm --name mysql --env="MYSQL_ROOT_PASSWORD=mypassword" -v $PWD/mysql/my.cnf:/etc/mysql/my.cnf -v $PWD/mysql/data:/var/lib/mysql mysql 
