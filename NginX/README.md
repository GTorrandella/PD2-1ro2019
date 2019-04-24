# Ejemplo Docker - UNDAV

## Dockerfile
Antes que nada, veamos como quedó el archivo

    FROM php:7.0-apache
    LABEL Description = "Imagen para empezar un simple desarrollo PHP"

    RUN mkdir /app
    RUN chown -R www-data /app
    RUN ln -s /app /var/www/html/app

    #copiamos el vhost
    COPY $PWD/example_vhost.conf /etc/apache2/sites-available/example_vhost.conf

    RUN a2dissite 000-default
    RUN a2ensite example_vhost
    RUN a2enmod rewrite

    WORKDIR /app

## Desarmandolo

Y vamos viendo de a poco, qué significa cada palabra reservada.

#### FROM
Volviendo a la analogía del apunte, esto sería de quién *hereda* esta imágen. En este caso, todo lo que haremos estará montado sobre una imágen php7:apache. ¿Qué significa? Que hay alguien que hizo una imágen con php7, con un Apache instalado y la subió al registro público de Docker, [hub.docker.com](hub.docker.com)

#### RUN
Esto nos permite correr un comando dentro de la imágen. Si corremos un contenedor de la imágen que generamos, vamos a ver que habrá un directorio "/app" ya creado

#### COPY
Copiamos un archivo de nuestra máquina local, a la imágen.

#### WORKDIR
Establecemos cuál es el directorio de trabajo para las operaciones subsiguientes. También es donde nos encontramos cuando entramos al contenedor.

## Construyamos la imágen y corramos un contenedor

Con el comando build construimos la imágen. El -t indica que tag le queremos poner.

`docker build -t undav_app:latest .`

Una vez que la imágen ya está construida, ya podemos correr un container de esa imágen.

`docker run -v $PWD:/app -p 80:80 --name undav undav_app:latest`

¿Y todas esas opciones?
Suponiendo que ya está todo, ¿cómo veo la página de saludo.php en mi browser?


## Referencias

* [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
