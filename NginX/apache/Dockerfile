FROM php:7.0-apache
LABEL Description = "Imagen para empezar un simple desarrollo PHP"

RUN mkdir /app
RUN chown -R www-data /app
RUN ln -s /app /var/www/html/app

#copiamos el vhost
COPY $PWD/example_vhost.conf /etc/apache2/sites-available/example_vhost.conf

#copiamos saludo.php
COPY saludo.php /var/www/html/app/saludo.php

RUN a2dissite 000-default
RUN a2ensite example_vhost
RUN a2enmod rewrite

WORKDIR /app
