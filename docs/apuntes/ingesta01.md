# Ingesta de Datos

17 Enero

## Ingesta de datos

Dada la gran cantidad de datos de que disponen las empresas, toda la información que generan desde diferentes fuentes se deben integrar en un único lugar, al que actualmente se le conoce como *data lake* asegurándose que los datos son compatibles entre sí. Gestionar tal volumen de datos puede llegar a ser un procedimiento complejo, normalmente dividido en procesos distintos y de relativamente larga duración. Para esta integración de datos diversos se suelen utilizar procesos ETL.

https://www.futurespace.es/ingesta-es-mas-que-una-mudanza-de-datos/

FIXME: Apuntes Teralco ... vairas diapositivas interesantes

## ETL

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

## Herramientas ETL

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

## AWS Athena

Athena es una herramienta *serverless* que permite agregar datos en S3 que provienen de fuentes dispares como bases de datos, un flujo de datos, contenido web desestructurado, etc..

Amazon Athena is an interactive query service that makes it easy for you to
analyze data directly in Amazon S3 using standard SQL. With a few actions in
the AWS Management Console, you can use Athena directly against data assets
stored in the data lake and begin using standard SQL to run ad hoc queries and
get results in a matter of seconds.
Athena is serverless, so there is no infrastructure to set up or manage, and you
only pay for the volume of data assets scanned during the queries you run.
Athena scales automatically—executing queries in parallel—so results are fast,
even with large datasets and complex queries. You can use Athena to process
unstructured, semi-structured, and structured data sets. Supported data asset
formats include CSV, JSON, or columnar data formats such as Apache Parquet
and Apache ORC. Athena integrates with Amazon QuickSight for easy
visualization. It can also be used with third-party reporting and business
intelligence tools by connecting these tools to Athena with a JDBC driver.

En este ejemplo, 

In this lab, you will practice using the AWS Management Console to create an Athena application, define a database in Athena, create a table, define columns and data types, and run both simple and complex queries.

Amazon Athena is an interactive query service that you can use to query data that is stored in Amazon S3. Athena stores data about the data sources that you must query in a database. You can store your queries for re-use, or you can share them with other users.

Athena is serverless, so there is no infrastructure to set up or manage, and you pay only for the queries you run. Athena scales automatically—running queries in parallel—so results are fast, even with large datasets and complex queries.

Amazon Athena is a fast, cost-effective, interactive query service that makes it easy to analyze petabytes of data in S3 with no data warehouses or clusters to manage.

1. Seleccionar el data set
Identificar en S3 donde están los datos. Athena permite consultar los datos CSV, TSV, JSON, Parquet y formato ORC.

2. Crear la tabla
Mediante el asistente de crear tbla o e
 
2Create a table
Use the Create Table Wizard or write your own DDL (Data Definition Language) statements using Hive. Learn more

 
3Query data
Run queries on your data. Amazon Athena supports ANSI SQL queries. Learn more


Your first task in this lab is to create the database by writing structured query language (SQL) statements to define the schema.

FIXME: mirar y hacer https://docs.aws.amazon.com/athena/latest/ug/getting-started.html

### AWS Glue

Es la herramienta ETL completamente administrador que ofrece Amazon Web Services.

Cuando el esquema de los datos es desconocido, *AWS Glue* permite inferirlo. Para ello, hemos de construir un rastreador (*crawler*) para descubrir su estructura.

. AWS Glue builds a catalog that contains metadata about the various data sources. AWS Glue is similar to Amazon Athena in that the actual data you analyze remains in the data source. The key difference is that you can build a crawler with AWS Glue to discover the schema.

### Creación

### Ejecución

Se puede ejecutar bajo demanda o planificar su ejecución de forma diaria, por horas, etc... Una vez lanzado, al cabo de un minuto, veremos que ha finalizado y en `Base de Datos --> Tablas` podremos ver la tabla que ha creado (en nuestro caso la tabla `csv`), junto con la estructura que ha inferido respecto a los datos cargados.

El siguiente paso es editar el esquema y ponerle nombres significativos a los campos:

Una vez los datos están cargados, ya podemos realizar consular con AWS Athena.

## Referencias

* [¿Qué es ETL?](https://www.talend.com/es/resources/what-is-etl/)
* [Building Big Data Storage Solutions (Data Lakes) for Maximum Flexibility](https://docs.aws.amazon.com/whitepapers/latest/building-data-lakes/building-data-lake-aws.html?did=wp_card&trk=wp_card)
