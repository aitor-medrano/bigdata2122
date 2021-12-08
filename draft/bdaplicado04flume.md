# Flume / Sqoop


## Sqoop

*Apache Sqoop* (<https://sqoop.apache.org>) es una herramienta diseñada para transferir de forma eficiente datos crudos entre un cluster de Hadoop y un almacenamiento estructurado, como una base de datos relacional.

!!! caution "Sin continuidad"
    Desde Junio de 2021, el proyecto *Sqoop* ha dejado de mantenerse como proyecto de Apache y forma parte del *ático*. Aún así, creemos conveniente conocer su uso en el estado actual. Gran parte de las funcionalidad que ofrece *Sqoop* se pueden realizar mediante *Nifi* o *Spark*.

Un caso típico de uso es el de cargar los datos de un *data lake*  (ya sea en HDFS o en S3) con datos que importaremos desde una base de datos, como MariaDB, PosgreSQL o MongoDB.

Sqoop utiliza una arquitectura basada en conectores, con soporte para *plugins* que ofrecen la conectividad a los sistemas externos, como pueden ser Oracle o SqlServer. Internamente, Sqoop utiliza los algoritmos *MapReduce* para importar y exportar los datos.

Por defecto, todos los trabajos Sqoop ejecutan cuatro mapas de trabajo ¿?¿?¿

### Importando datos

Por ejemplo, vamos a utilizar los datos que tenemos en la base de datos *sports* que tenemos cargada en RDS.

``` bash
sqoop import -connect jdbc:mysql://localhost/dbname -table <table_name> \
    --username <username> --password <password> -m 4
```

La importación se realiza en dos pasos:

1. Sqoop escanea la base de datos y colecta los metadatos de la tabla a importar.
2. Sqoop envia un *job* y transfiere los datos reales utilizando los metadatos necesarios.

Los datos importados se almacenan en carpetas de HDFS, pudiendo el usuario especificar otras carpetas, así como los caracteres separadores o de terminación de registro. Además, el usuario puede utilizar diferentes formatos, como son Avro, ORC, Parquet, ficheros secuenciales o de tipo texto, para almacenar los datos en HDFS.

https://learning.oreilly.com/library/view/modern-big-data/9781787122765/285db0b7-a800-4aa8-90f5-7613462d5ca6.xhtml



https://www.geeksforgeeks.org/overview-of-sqoop-in-hadoop/


## Flume

Allá por el año 2010 se Cloudera presentó Flume, programa para tratamiento e ingesta de datos masivo. Esto daba la posibilidad de crear desarrollos complejos que permitieran el tratamiento de datos masivos creados en Tiempo Real.

En Real Time se utiliza en la etapa de Obtención de Datos (para conectarnos a fuentes de datos Online).

Su arquitectura es sencilla, pues tiene tres componentes principales, muy configurables:

Source: Fuente de origen de los datos
Channel: la vía por donde se tratarán los datos
Sink: persistencia/movimiento de los datos

Flume es sencillito apriori, el problema es cuando quieres utilizarlo para obtener datos de manera paralela (o multiplexada) y además te ves en la necesidad de crear tus propios Sinks, o tus propios interceptores. Entonces la cosa cambia y hay que dedicarle algo más de tiempo.

Muy recomendada como ayuda|compañero|alternativa a herramientas como Kettle.

Es un sistema confiable y distribuido para recopilar, agregar y mover datos masivos.
Algunas de sus características son:
Diseño flexible basado en flujos de datos de transmisión.
Resistente a fallos y robusto con múltiples conmutaciones por error y  mecanismos de recuperación.
Lleva datos desde origen a destino: incluidos HDFS y HBASE

Componentes:
Evento:  Son las unidades de datos transportadas por el agente flume (array de bytes).
Agente: Contenedor para alojar subcomponentes que permiten mover los eventos
Source: Receptor de eventos
Interceptor: Transformador de eventos
Channel: Buffer de eventos
Sink: Toma eventos del canal y los transmite hacia el siguiente componente

## Referencias

* aaa
