# Redis-Sentinel
Se demostrará enñ funcionamiento de Redis-Sentinel mediante una prueba en caliente sobre una red de Redis.

## Red
La red está conformada por un Maestro, con siete Replicas, y ocho Sentinels. Cada Sentinel su comparte instancia de Redis con el Maestro o un esclavo.

```
       +----+
       | M1 |
       | S1 |
       +----+
          |
+----+    |    +----+
| R2 |----+----| R3 |
| S2 |    |    | S3 |
+----+    |    +----+
          |
+----+    |    +----+
| R4 |----+----| R5 |
| S4 |    |    | S5 |
+----+    |    +----+
          |
+----+    |    +----+
| R6 |----+----| R7 |
| S6 |    |    | S7 |
+----+    |    +----+
          |
       +----+
       | R8 |
       | S8 |
       +----+
```

Esta configuración se logra utilizando un contendor diferente para cada instancia de Redis.

### Set-Up
Para crear la red:
```
$ docker-compose build
```
Esto armará la red sin los Sentinels.
Para agregarlos:
```
$ ./start-sentinels
```

### Test
Ejecutar _test.py_ una vez levantado lo anterior.

Esto resultará en el cambio permanente del maestro.

### Reutilización
Para ejecutar la prueba nuevamente se deben detener y recomensar los contenerdores:
```
$ docker-compose down
$ docker-compose up
```
