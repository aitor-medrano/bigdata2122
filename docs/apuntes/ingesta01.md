# Ingesta de Datos

## Introducción

Formalmente, la ingesta de datos es el proceso mediante el cual se introducen datos, de diferentes fuentes, estructura y/o características dentro de otro sistema de almacenamiento o procesamiento de datos. Un *pipeline* de datos consume datos de un punto de origen, los limpia y los escribe en un nuevo destino.

La ingesta de datos es un proceso muy importante porque la productividad de un equipo va directamente ligada a la calidad del proceso de ingesta de datos. Estos procesos deben ser flexibles y ágiles, ya que una vez puesta en marcha, los analistas y científicos de daots puedan contruir un *pipeline* de datos para mover los datos a la herramienta con la que trabajen.

Es sin duda, el primer paso que ha de tenerse en cuenta a la hora de diseñar una arquitectura Big Data, para lo cual, hay que tener muy claro, no solamente el tipo y fuente de datos, sino cual es el objetivo final y que se pretende conseguir con ellos. Por lo tanto, en este punto, hay que realizar un análisis detallado, porque es la base para determinar las tecnologías que compondrán nuestra arquitectura Big Data.

Dada la gran cantidad de datos que disponen las empresas, toda la información que generan desde diferentes fuentes se deben integrar en un único lugar, al que actualmente se le conoce como *data lake* asegurándose que los datos son compatibles entre sí. Gestionar tal volumen de datos puede llegar a ser un procedimiento complejo, normalmente dividido en procesos distintos y de relativamente larga duración.

## La ingesta por dentro

La ingesta extrae los datos desde la fuente donde se crean o almacenan originalmente y los carga en un destino o zona temporal. Un *pipeline* de datos sencillo puede que aplica uno más transformaciones ligeras para enriquecer o filtrar los datos antes de escribirlos en un destino, almacen de datos o cola de mensajería. Se pueden añadir nuevos *pipelines* para transformaciones más complejas como *joins*, agregacaiones u ordenaciones para analítica de datos, aplicaciones o sistema de informes.

<figure style="align: center;">
    <img src="../imagenes/etl/01dataIngestion.png">
    <figcaption>Ingesta de datos</figcaption>
</figure>

Las fuentes más comunes desde las que se obtienen los datos son:

* Servicios de mensajería como Apache Kafka
* Bases de datos relaciones, las cuales se acceden, por ejemplo, JDBC
* Servicios REST que vuelven los datos en formato JSON
* Servicios de almacenamiento distribuido como HDFS o S3.

Los destinos donde se almacenan los datos son:

* Servicios de mensajería como Apache Kafka
* Bases de datos relaciones
* Bases de datos NoSQL
* Servicios de almacenamiento distribuido como HDFS o S3.
* Plataformas de datos como Snowflake o Databricks.

## Pipeline de Datos

Un *pipeline* es una construcción lógica que representa un proceso dividido en fases. Los pipelines de datos se caracterizan por definir el conjunto de pasos o fases y las tecnologías involucradas en un proceso de movimiento o procesamiento de datos.

Las pipelines de datos son necesarios ya que no debemos analizar los datos en los mismos sistemas donde se crean. El proceso de analítica es costoso computacionalmente, por lo que se separa para evitar perjudicar el rendimiento del servicio. De esta forma, tenemos sistemas OLTP (como un CRM), encargados de capturar y crear datos, y sistemas OLAP (como un *Data Warehouse*), encargados de analizar los datos.

Los movimientos de datos entre estos sistemas involucran varias fases. Por ejemplo:

1. Recogemos los datos y los enviamos a un topic de Apache Kafka. Kafka actúa aquí como un buffer para el siguiente paso.

    <figure style="float: right;">
        <img src="../imagenes/etl/01pipeline.jpeg">
        <figcaption>Ejemplo de pipeline - aprenderbigdata.com</figcaption>
    </figure>

2. Mediante una tecnología de procesamiento, que puede ser streaming o batch, leemos los datos del buffer. Por ejemplo, mediante *Spark* realizmaos la analítica sobre estos datos.
3. Almacenamos el resultado en una base de datos NoSQL como *Amazon DynamoDB* o un sistema de almacenamiento distribuidos como *Amazon S3*.

Aunque a menudo se intercambian los términos de *pipeline* de datos y ETL no significan lo mismo. Las ETLs son un caso particular de pipeline de datos que involucran las fases de extracción, transformación y carga de datos. Las pipelines de datos son cualquier proceso que involucre el movimiento de datos entre sistemas.




## ETL


Una ETL, entendida esta como un proceso que lleva la información de un punto A a un punto B puede realizarse con muchísimas herramientas, scripts, Python. Pero cuando nos metemos con Big Data no servirá cualquier tipo de herramienta, deberemos tener herramientas:
Flexible y soporten formatos variados (Json,csv,etc)
Escalable y tolerante a fallos.
Con conectores a múltiples fuentes y destinos de datos.

https://www.talend.com/es/resources/what-is-etl/

https://www.informatica.com/resources/articles/what-is-etl.html

https://www.informatica.com/blogs/etl-vs-elt-whats-the-difference.html


Los procesos ETL, siglas de extracción, transformación y carga (*load*), permiten a las organizaciones recopilar en un único lugar todos los datos de los que pueden disponer. Ya hemos comentado que estos datos provienen de diversas fuentes, por lo que es necesario acceder a ellos, y formatearlos para poder ser capaces de integrarlos. Además, es muy recomendable asegurar la calidad de los datos y su veracidad, para así evitar la creación de errores en los datos.

Una vez los datos están unificados en un *data lake*, otro tipo de herramientas de análisis permitirán su estudio para apoyar procesos de negocio.

Dada la gran variedad de posibilidades existentes para representar la realidad en un dato, junto con la gran cantidad de datos almacenados en las diferentes fuentes de origen, los procesos ETL consumen una gran cantidad de los recursos asignados a un proyecto.

### Extracción

Esta fase de un proceso ETL es la encargada de recopilar los datos de los sistemas originales y transportarlos al sistema donde se almacenarán, de manera general suele tratarse de un entorno de Data Warehouse o almacén de datos. Los formatos de las fuentes de datos pueden encontrarse en diferentes formatos, desde ficheros planos hasta bases de datos relacionales entre otros formatos distintos.
Una parte de la extracción es la de analizar que los datos sean los que se esperaban, verificando que siguen el formato que se esperaba. En caso contrario, esos datos se rechazan.

La primera característica deseable de un proceso de extracción es que debe ser un proceso rápido, ligero, causar el menor impacto posible, ser trasparente para los sistemas operacionales e independiente de las infraestructuras.

La segunda característica es que debe reducir al mínimo el impacto que se generase en el sistema origen de la información. No se puede poner en riesgo el sistema original, generalmente operacional, ni perder ni modificar sus datos; ya que si colapsase esto podría afectar el uso normal del sistema y generar pérdidas a nivel operacional.

Así pues, la extracción convierte los datos a un formato preparado para iniciar el proceso de transformación

### Transformación

En esta fase se espera realizar los cambios necesarios en los datos de manera que estos tengan el formato y contenido esperado.

En concreto, la transformación puede comprender:

* Cambios de codificación
* Eliminar datos duplicados
* Cruzar diferentes fuentes de datos para obtener una fuente diferente
* Agregar información en función de alguna variable
* Tomar parte de los datos para cargarlos
* Transformar información para generar códigos, claves, identificadores…
* Generar información
* Estructurar mejor la información
* Generar indicadores que faciliten el procesamiento y entendimiento

Respecto a sus características, debe transformar los datos para mejorarlos, incrementar su calidad, integrarlos con otros sistemas, normalizarlos, eliminar duplicidades o ambigüedades. Además, no debe crear información, duplicar, eliminar información relevante, ser errónea o impredecible.

Una vez transformados los datos, ya estarán listos para su carga.

### Carga

Fase encargada de almacenar los datos en el destino, un Data Warehouse o en cualquier tipo de base de datos. Por tanto la fase de carga interactúa de manera directa con el sistema destino, y debe adaptarse al mismo con el fin de cargar los datos de manera satisfactoria.

La carga ha de realizarse buscando minimizar el tiempo de la transacción

Cada BBDD puede tener un sistema ideal de carga basado en:

* SQL (Oracle, SQL Server, Redshift, Postgres, Teradata, Greenplum, …)
* Ficheros (Postgres, Redshift)
* Cargadores Propios (HDFS, Teradata, Greenplum)

Se pueden realizar acciones para mejorar estos procesos:

* Gestiones de índices
* Gestión de claves de distribución y particionado
* Tamaño de las transacciones y commit’s

https://www.informatica.com/blogs/etl-vs-elt-whats-the-difference.html


https://www.franciscojavierpulido.com/2013/11/paradigmas-bigdata-el-procesamiento.html

### Herramientas ETL

Las caracteristicas de las herramientas ETL son:

* Permiten conectividad con diferentes sistemas y tipos de datos
    * Excel, BBDD Transaccionales, XML, Access, Teradata, HDFS, Hive, CRM
    * APIs de Aplicaciones de terceros, Logs…

* Permiten la planificación y ejecución de lógica
    * Planificación por Batch
    * Planificación por eventos
    * Planificación en tiempo real

* Capacidad para transformar los datos
    * Transformaciones Simples: Tipos de datos, cadenas, codificaciones, cálculos simples
    * Transformaciones Intermedias: Agregaciones, lookups,  
    * Transformaciones Complejas: Algoritmos de IA, Segmentación, Integración de código de terceros, Integración con otros lenguajes

* Metadatos y gestión de errores
    * Permiten tener información del funcionamiento de todo el proceso
    * Permiten el control de errores y establecer politicas al respecto

Las soluciones más empleadas son:

* [Pentaho Data Integration (PDI)](https://www.hitachivantara.com/en-us/products/data-management-analytics/lumada-data-integration.html)
* [Oracle Data Integrator](https://www.oracle.com/es/middleware/technologies/data-integrator.html)
* [Talend Open Studio](https://www.talend.com/products/talend-open-studio/)
* [Mulesoft](https://www.mulesoft.com)
* [Informatica Data Integration](https://www.informatica.com/products/data-integration.html)

<figure style="align: center;">
    <img src="../imagenes/etl/herramientasETL.png">
    <figcaption>Herramientas ETL</figcaption>
</figure>

## Arquitectura de Ingesta de datos

https://ezdatamunch.com/what-is-data-ingestion/

## Herramientas de Ingesta de datos

Las herramientas de ingesta de datos para ecosistemas Big Data se clasifican en los siguientes bloques:

* *Apache Nifi*: herramienta ETL que se encarga de cargar datos de diferentes fuentes, los pasa por un flujo de procesos para su tratamiento, y los vuelca en otra fuente.
* *Apache Sqoop*: transferencia bidireccional de datos entre *Hadoop* y una bases de datos SQL (datos estructurados)
* *Apache Flume*: sistema de ingesta de datos semiestructurados o no estructurados en streaming sobre HDFS o HBase.

Por otro lado existen sistemas de mensajería con funciones propias de ingesta, tales como:

* *Apache Kafka*: sistema de intermediación de mensajes basado en el modelo publicador/suscriptor.
* *RabbitMQ*: sistema colas de mensajes (MQ) que actúa de middleware entre productores y consumidores.
* *Amazon Kinesis*: homólogo de Kafka para la infraestructura Amazon Web Services.
* *Microsoft Azure Event Hubs*: homólogo de Kafka para la infraestructura Microsoft Azure.
* *Google Pub/Sub*: homólogo de Kafka para la infraestructura Google Cloud.


This stage of the data processing pipeline has some overlap with the Collection stage. Data can be collected by or ingested into AWS services in various ways. The following two managed AWS services—which can be used for ingestion—are included in this course.

AWS Glue (Enlaces a un sitio externo.): AWS Glue is a fully managed extract, transform, and load (ETL) service that makes it easy for customers to prepare and load their data for analytics. ETL jobs can be created with a few clicks in the AWS Management Console. AWS Glue can discover data and store the inferred schema in the AWS Glue Data Catalog, which can then be available for ETL. AWS Glue can also act as a remote metadata store for various AWS services like Amazon Athena, AWS Data Pipeline, etc.
AWS Data Pipeline (Enlaces a un sitio externo.): Data Pipeline is a managed service that can be used to move data between various data sources in the AWS Cloud, like Amazon S3, Amazon RDS, DynamoDB, Amazon Redshift, and Amazon EMR. It can reduce the complexities of handling data pipelines, and reliably move data from source to destination in a cost-effective way.

## Consideraciones

A la hora de analizar cual sería la tecnología y arquitectura adecuada para realizar la ingesta de datos en un sistema Big Data, hemos de tener en cuenta los siguientes factores:

* Origen y formato de los datos
    * ¿Cual va a ser el origen u orígenes de los datos?
    * ¿Provienen de sistemas externos o internos?
    * ¿Serán datos estructurados o datos sin estructura?
    * ¿Cuál es el volumen de los datos? Volumen diario, y plantear como sería la primera carga de datos.
    * ¿Existe la posibilidad de que más adelante se incorporen nuevas fuentes de datos?
* Latencia/Disponibilidad
    * Ventana temporal que debe pasar desde que los datos se ingestan hasta que puedan ser utilizables, desde horas/dias (mediante procesos *batch) o ser *real-time* (mediante *streaming*)
* Actualizaciones
    * ¿Las fuentes origen se modifican habitualmente?
    * ¿Podemos almacenar toda la información y guardar un histórico de cambios?  * ¿Modificamos la información que tenemos? ¿mediante *updates*, o *deletes +insert*?
* Transformaciones
    * ¿Son necesarias durante la ingesta?
    * ¿Aportan latencia al sistema? ¿Afecta al rendimiento?
    * ¿Tiene consecuencias que la información sea transformada y no sea la original?
* Destino de los datos
    * ¿Será necesario enviar los datos a más de un destino, por ejemplo, S3 y Cassandra?
    * ¿Cómo se van a utilizar los datos en el destino? ¿cómo serán las consultas? ¿es necesario particionar los datos? ¿serán búsquedas aleatorias o no? ¿Utilizaremos *Hive* / *Pig* / *Cassandra*?
    * ¿Qué procesos de transformación de datos se van a realizar una vez ingestados los datos?
    * ¿Cual es la frecuencia y actualización de los datos origen?
* Estudio de los datos
    * Calidad de los datos ¿son fiables? ¿existen duplicados?
    * Seguridad de los datos. Si tenemos datos sensibles o confidenciales, ¿los enmascaramos o decidimos no realizar su ingesta?

## Referencias

* [Ingesta, es más que una mudanza de datos](https://www.futurespace.es/ingesta-es-mas-que-una-mudanza-de-datos/)
* [¿Qué es ETL?](https://www.talend.com/es/resources/what-is-etl/)
* [Building Big Data Storage Solutions (Data Lakes) for Maximum Flexibility](https://docs.aws.amazon.com/whitepapers/latest/building-data-lakes/building-data-lake-aws.html?did=wp_card&trk=wp_card)

17 Enero



https://www.xenonstack.com/blog/big-data-ingestion
https://streamsets.com/learn/data-ingestion/
https://ezdatamunch.com/what-is-data-ingestion/

https://streamsets.com/learn/etl-or-elt/


https://aprenderbigdata.com/pipeline-de-datos/

https://www.xenonstack.com/blog/big-data-ingestion
https://www.xenonstack.com/blog/data-pipeline