docker run --rm --name mysql --env="MYSQL_ROOT_PASSWORD=mypassword" -v $PWD/my.cnf:/etc/mysql/my.cnf mysql 
# docker run -it --rm --name mysql --env="MYSQL_ROOT_PASSWORD=mypassword" -v $PWD/my.cnf:/etc/mysql/my.cnf mysql /bin/bash
