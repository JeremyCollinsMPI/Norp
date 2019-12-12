mysql_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql)
docker run --rm -p 80:80 -e mysql_ip=$mysql_ip --name norp_page -v $PWD/norp/src:/var/www/html/ jeremycollinsmpi/norp:latest
# docker run -it --rm -p 80:80 -e mysql_ip=$mysql_ip --name norp_page -v $PWD/src:/var/www/html/ jeremycollinsmpi/norp:latest /bin/bash
