# Kafka

Es una plataforma para la transmisión de eventos
Implementa un sistema distribuido formado Servidores y Clientes que se comunican a través de TCP.
Servidores: Importan y exportan datos continuamente como flujos de eventos.
Clientes: Permiten escribir aplicaciones distribuidas y microservicios que leen, escriben y procesan flujos de eventos en paralelo.

Evento: registra el hecho de que algo ha sucedido.
Tiene una clave, un valor y una marca
Los eventos se organizan de forma duradera en temas (similar a una carpeta de archivos)
Los temas están divididos, distribuidos en varios depósitos. Los eventos con la misma clave, se escriben en la misma partición.
Productores: aplicaciones clientes que publican (escriben) eventos en Kaffa.
Consumidores: los que leen estos eventos.

Apache Kafka Fundamentals LiveLessons

https://learning.oreilly.com/videos/apache-kafka-fundamentals/9780134833682/

TIME TO COMPLETE:
3h 49m



https://learning.oreilly.com/videos/apache-kafka-a-z/9781801077569/
Apache Kafka A-Z with Hands-On Learning

TIME TO COMPLETE:
9h 36m


Transient Storage

Sencillamente es un servicio de commit log, particionado, replicado y distribuido.

En su arquitectura encontramos que disponemos de un modelo Productor/Consumidor, cuyos mensajes se pueden categorizar en algo llamado topics y que funciona como si fuera un cluster.

Se suele utilizar como gestor de colas.

Se utiliza en la etapa de Almacenamiento de Datos.


## Amazon Kinesis

Amazon Kinesis facilita la recopilación, el procesamiento y el análisis de datos de streaming en tiempo real para obtener datos de manera oportuna y reaccionar rápidamente ante información nueva. Amazon Kinesis ofrece capacidades clave para procesar de manera rentable datos de streaming a cualquier escala, además de la flexibilidad para elegir las herramientas más adecuadas para los requisitos de su aplicación. Con Amazon Kinesis, puede incorporar datos en tiempo real, como videos, audios, registros de aplicaciones, secuencias de clics de sitios web y datos de telemetría de IoT para aprendizaje automático, análisis y otras aplicaciones. Amazon Kinesis le permite procesar y analizar datos a medida que se reciben y responder instantáneamente en vez de tener que esperar a que los datos se recopilen antes de que el procesamiento pueda comenzar.

## Referencias

* aaa
