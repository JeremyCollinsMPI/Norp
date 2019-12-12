mysql_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql)
docker run --rm -it -p 80:80 -e mysql_ip=$mysql_ip --name norp jeremycollinsmpi/norp /bin/bash
