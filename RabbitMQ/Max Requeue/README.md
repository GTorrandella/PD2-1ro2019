# Ejemplo Maximos Reencolamientos con Rabbit - UNDAV

## Funcionamiento

### Producer
Mandará 4 mensajes al Exchange "example", con la Routing Key "example.maxRequeue".
Todos los mensajes poseen el header 'x-requeue-count', fijado en 2.
El primero de los mensajes estará roto, lo que provocará su reencolamiento.

### Consumer
Trabajará los mensajes de la cola "maxRequeue".
En caso de que alguno este mal ("rompa"), tomará la decisión de reencolarlo según el header 'x-requeue-count'.
Si 'x-requeue-count' es major a 0, reencolará el mensaje con su 'x-requeue-count' disminuido en uno.
Caso contrario, mandará un nack, enviando el mensaje al Dead Letter exchange.
