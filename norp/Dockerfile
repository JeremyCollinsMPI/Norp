FROM php:5.6-apache
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli
RUN apt-get update
RUN apt-get install -y mysql-server mysql-client mysql-common
COPY config/php.ini /usr/local/etc/php/
