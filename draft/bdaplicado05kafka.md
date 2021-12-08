# Kafka

https://www.theninjacto.xyz/Instalacion-Configuracion-Kafka-Manager/

Kafka, sin ir más lejos, es un proyecto de intermediación de mensajes de código abierto desarrollado por la Apache Software Foundation y escrito en Scala. Entre sus características principales, podremos realizar:

Publicación y suscribción de flujos de registros (Bastante similar a una cola de mensajes o un sistema de mensajería).
Almacenar flujos de registros tolerante a fallos (Sistema de Buffer con un periodo de retención de mensajes).
Procesar flujos de registros a medida que ocurren.




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

Kafka con Docker:
https://www.theninjacto.xyz/Instalacion-Configuracion-Kafka-Manager/


https://learning.oreilly.com/videos/apache-kafka-a-z/9781801077569/
Apache Kafka A-Z with Hands-On Learning

TIME TO COMPLETE:
9h 36m


Transient Storage

Sencillamente es un servicio de commit log, particionado, replicado y distribuido.

En su arquitectura encontramos que disponemos de un modelo Productor/Consumidor, cuyos mensajes se pueden categorizar en algo llamado topics y que funciona como si fuera un cluster.

Se suele utilizar como gestor de colas.

Se utiliza en la etapa de Almacenamiento de Datos.

### Kafka Connect

https://learning.oreilly.com/library/view/modern-big-data/9781787122765/30e977be-ef98-4cc6-a771-d15030ad19c9.xhtml



## Nifi +  Kafka

Aunque Kafka lo estudiaremos en profundidad más adelante, vamos a ver como leer datos en streaming desde una *topic* para luego ingestar los datos en Elasticsearch.


Ejemplo con Kafka
Split Text + ExtractText + PutKafka
https://www.youtube.com/watch?v=2w14d16wR8Y

### Caso de uso

Mediante Nifi, unir Kafka Connect, Kafka, HDFS

Nifi + Kafka
https://www.youtube.com/watch?time_continue=1588&v=nWEna1mE4KY&feature=emb_logo

## Amazon Kinesis

Amazon Kinesis facilita la recopilación, el procesamiento y el análisis de datos de streaming en tiempo real para obtener datos de manera oportuna y reaccionar rápidamente ante información nueva. Amazon Kinesis ofrece capacidades clave para procesar de manera rentable datos de streaming a cualquier escala, además de la flexibilidad para elegir las herramientas más adecuadas para los requisitos de su aplicación. Con Amazon Kinesis, puede incorporar datos en tiempo real, como videos, audios, registros de aplicaciones, secuencias de clics de sitios web y datos de telemetría de IoT para aprendizaje automático, análisis y otras aplicaciones. Amazon Kinesis le permite procesar y analizar datos a medida que se reciben y responder instantáneamente en vez de tener que esperar a que los datos se recopilen antes de que el procesamiento pueda comenzar.


Nifi + Zookeeper
https://www.theninjacto.xyz/Running-cluster-Apache-Nifi-Docker/

## Referencias

* aaa

https://www.theninjacto.xyz/tags/apache-kafka/
