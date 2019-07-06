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

## Explicación del proceso

### Funcionamiento durante la partición de red
Aunque en el test se pone a dormir al maestro por 45 segudos, esto representa una partición de red donde el maestro queda completamente aislado de los esclavos.
Debido a ello, aunque el maestro continua funcionando con normalidad, va a rechazar todas las escrituras, ya que está configurado para que solamente pueda escribir cuando tiene al menos 2 esclavos conectados.

Del otro lado de la partición, los esclavos intentarán reconectarse con el maestro.
Luego de 30 segundos, los sentinelas empezarán a detectar al maestro como caído, marcandoló como _sdown_, y avisarán al resto de que detectaron al maestro caido.
Cuando cada sentinela reciba mensajes de otros 2 sentinelas (el valor de _quorum_) de que el maestro está caido, elevará la situación interna a _odown_, e intentará empezar el proceso de failover. 

### Failover
El proceso de failover es la elección de un nuevo maestro cuando el actual se desconecta por cualquier motivo.
Comienza una vez que al menos la mitad de los sentinelas detectan al maestro como _odown_, 4 en este caso.

Una vez que comienza el failover, los sentinelas eligirán a uno de ellos que conducirá el resto del proceso.
Este eligirá un esclavo como nuevo maestro, según los siguientes criterios:
  1. El esclavo debe ser confiable. Eso quiere decir que el esclavo se debe haber desconectado del antiguo maestro hace menos de diez veces el tiempo de desconección (30s * 10) más los segundos desde que el sentinela a cargo dispuso el estado _sdown_ del maestro.
```
(down-after-milliseconds * 10) + milliseconds_since_master_is_in_SDOWN_state
```
  2. Los esclavos de mayor prioridad, estando esta declarada en el archivo de configuración de cada esclavo. Para este test todos los esclavos poseen la misma prioridad, 100.
  3. Los esclavos que posean las replicaciones más actualizadas, o sea, que su _replication offset_ sea lo más cercano al maestro.
  4. Por último, aquel esclavo de mayor ID de proceso.

La selección prosigue paso a paso hasta que quede un solo esclavo que sea posible seleccionar.
El último paso es para evitar un "desempate" aleatorio, brindandole un algoritmo determinista al proceso, de manera que ante las mismas condiciones iniciales siempre se elija al mismo esclavo.

Este esclavo será configurado como nuevo maestro. Hecho eso, se avisará del cambio a los demás esclavos y todos los clientes, y se degradará al antiguo maestro a esclavo.

En el caso de este test: ningún esclavo quedará eliminado por el primer criterio; la prioridad es la misma en todos; el _replicatión offset_ también será el mismo, ya que no hay escrituras durante en test como está planteado; el ID del proceso depende del orden de creación de cada uno de los contenedores. Debido a esto no hay un control sobre cual de los esclavos se convertirá en el proximo maestro.

### Finalizada/reparada la partición de red
Una vez finalizada la partición, una vez que el antiguo maestro se despierta del _sleep_ de 45s en este test, los setinelas reconfigurán al ex-maestro como un esclavo más. 
De haber recibido escrituras, algo imposible en este test, durante el tiempo de partición, estas se perderian al replicar el nuevo maestro. 
En caso de querer conservar estas escrituras se debe utilizar un sistema por afuera de Redis, ya que este no ofrece ningún servicio como este.

### Consistencia y disponibilidad en cada partición
Esta configuración prioriza la consistencia de la información por sobre la disponibilidad, ya que ninguna partición aceptará escrituras durante la misma. Los redis de ambas particiones continuarán respondiendo consultas que no requieran escrituras.

En caso de que el maestro no requiriera esclavos conectados para escribir, este seguiria recibiendo escrituras, que se perderían en caso de un failover. Este tipo de configuración prioriza la disponibilidad por sobre la consistencia.
