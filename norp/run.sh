mysql_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql)
docker run --rm -p 80:80 -e mysql_ip=$mysql_ip --name norp_page jeremycollinsmpi/norp 