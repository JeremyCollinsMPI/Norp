mysql_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql)
python_url=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' create-sql)
docker run --rm -e mysql_ip=$mysql_ip -v $PWD/norp/src:/src python:latest python /src/create_db_php.py
docker run --rm -e python_url=$python_url -v $PWD/norp/src:/src python:latest python /src/create_index_php.py
docker run --rm -p 80:80 --name norp_page -v $PWD/norp/src:/var/www/html/ jeremycollinsmpi/norp:latest
# docker run -it --rm -p 80:80 -e mysql_ip=$mysql_ip --name norp_page -v $PWD/src:/var/www/html/ jeremycollinsmpi/norp:latest /bin/bash
