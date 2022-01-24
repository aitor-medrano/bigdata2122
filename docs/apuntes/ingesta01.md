# Ingesta de Datos

## Introducción

Formalmente, la ingesta de datos es el proceso mediante el cual se introducen datos, desde diferentes fuentes, estructura y/o características dentro de otro sistema de almacenamiento o procesamiento de datos.

<figure style="float: right;">
    <img src="../imagenes/etl/01ingesta.png">
    <figcaption>Ingesta de datos</figcaption>
</figure>

La ingesta de datos es un proceso muy importante porque la productividad de un equipo va directamente ligada a la calidad del proceso de ingesta de datos. Estos procesos deben ser flexibles y ágiles, ya que una vez puesta en marcha, los analistas y científicos de datos puedan construir un *pipeline* de datos para mover los datos a la herramienta con la que trabajen. Entendemos como *pipeline* de datos un proceso que consume datos desde un punto de origen, los limpia y los escribe en un nuevo destino.

Es sin duda, el primer paso que ha de tenerse en cuenta a la hora de diseñar una arquitectura Big Data, para lo cual, hay que tener muy claro, no solamente el tipo y fuente de datos, sino cual es el objetivo final y qué se pretende conseguir con ellos. Por lo tanto, en este punto, hay que realizar un análisis detallado, porque es la base para determinar las tecnologías que compondrán nuestra arquitectura Big Data.

Dada la gran cantidad de datos que disponen las empresas, toda la información que generan desde diferentes fuentes se deben integrar en un único lugar, al que actualmente se le conoce como *data lake* asegurándose que los datos son compatibles entre sí. Gestionar tal volumen de datos puede llegar a ser un procedimiento complejo, normalmente dividido en procesos distintos y de relativamente larga duración.

## Pipeline de datos

Un *pipeline* es una construcción lógica que representa un proceso dividido en fases. Los pipelines de datos se caracterizan por definir el conjunto de pasos o fases y las tecnologías involucradas en un proceso de movimiento o procesamiento de datos.

Las pipelines de datos son necesarios ya que no debemos analizar los datos en los mismos sistemas donde se crean (principalmente para evitar problemas de rendimiento). El proceso de analítica es costoso computacionalmente, por lo que se separa para evitar perjudicar el rendimiento del servicio. De esta forma, tenemos sistemas OLTP (como un CRM), encargados de capturar y crear datos, y de forma separada, sistemas OLAP (como un *Data Warehouse*), encargados de analizar los datos.

Los movimientos de datos entre estos sistemas involucran varias fases. Por ejemplo:

1. Recogemos los datos y los enviamos a un topic de Apache Kafka. Kafka actúa aquí como un buffer para el siguiente paso.

    <figure style="align: center;">
        <img src="../imagenes/etl/01pipeline.jpeg">
        <figcaption>Ejemplo de pipeline - aprenderbigdata.com</figcaption>
    </figure>

2. Mediante una tecnología de procesamiento, que puede ser streaming o batch, leemos los datos del buffer. Por ejemplo, mediante *Spark* realizamos la analítica sobre estos datos (haciendo cálculos, filtrados, agrupaciones de datos, etc...).
3. Almacenamos el resultado en una base de datos NoSQL como *Amazon DynamoDB* o un sistema de almacenamiento distribuido como *Amazon S3*.

Aunque a menudo se intercambian los términos de *pipeline* de datos y ETL, no significan lo mismo. Las ETLs son un caso particular de pipeline de datos que involucran las fases de extracción, transformación y carga de datos. Las pipelines de datos son cualquier proceso que involucre el movimiento de datos entre sistemas.

## ETL

Una ETL, entendida como un proceso que lleva la información de un punto A a un punto B, puede realizarse mediante diversas herramientas, scripts, Python, etc... Pero cuando nos metemos con Big Data no servirá cualquier tipo de herramienta, ya que necesitamos que sean:

* Flexibles y soporten formatos variados (JSON, CSV, etc...)
* Escalables y tolerante a fallos.
* Dispongan de conectores a múltiples fuentes y destinos de datos.

Los procesos ETL, siglas de **e**xtracción, **t**ransformación y carga (***l****oad*), permiten a las organizaciones recopilar en un único lugar todos los datos de los que pueden disponer. Ya hemos comentado que estos datos provienen de diversas fuentes, por lo que es necesario acceder a ellos, y formatearlos para poder ser capaces de integrarlos. Además, es muy recomendable asegurar la calidad de los datos y su veracidad, para así evitar la creación de errores en los datos.

<figure style="align: center;">
    <img src="../imagenes/etl/01etl.png">
    <figcaption>Extracción, Transformación y Carga (load)</figcaption>
</figure>

Una vez los datos están unificados en un *data lake*, otro tipo de herramientas de análisis permitirán su estudio para apoyar procesos de negocio.

Dada la gran variedad de posibilidades existentes para representar la realidad en un dato, junto con la gran cantidad de datos almacenados en las diferentes fuentes de origen, los procesos ETL consumen una gran cantidad de los recursos asignados a un proyecto.

### Extracción

Encargada de recopilar los datos de los sistemas originales y transportarlos al sistema donde se almacenarán, de manera general suele tratarse de un entorno de Data Warehouse o almacén de datos. Las fuentes de datos pueden encontrarse en diferentes formatos, desde ficheros planos hasta bases de datos relacionales, pasando por mensajes de redes sociales como *Twitter* o *Redddit*.

Un paso que forma parte de la extracción es la de analizar que los datos sean veraces, que contiene la información que se espera, verificando que siguen el formato que se esperaba. En caso contrario, esos datos se rechazan.

La primera característica deseable de un proceso de extracción es que debe ser un proceso rápido, ligero, causar el menor impacto posible, ser transparente para los sistemas operacionales e independiente de las infraestructuras.

La segunda característica es que debe reducir al mínimo el impacto que se genera en el sistema origen de la información. No se puede poner en riesgo el sistema original, generalmente operacional, ni perder ni modificar sus datos; ya que si colapsase esto podría afectar el uso normal del sistema y generar pérdidas a nivel operacional.

Así pues, la extracción convierte los datos a un formato preparado para iniciar el proceso de transformación.

### Transformación

En esta fase se espera realizar los cambios necesarios en los datos de manera que estos tengan el formato y contenido esperado.

En concreto, la transformación puede comprender:

* Cambios de codificación.
* Eliminar datos duplicados.
* Cruzar diferentes fuentes de datos para obtener una fuente diferente.
* Agregar información en función de alguna variable.
* Tomar parte de los datos para cargarlos.
* Transformar información para generar códigos, claves, identificadores…
* Generar información.
* Estructurar mejor la información.
* Generar indicadores que faciliten el procesamiento y entendimiento.

Respecto a sus características, debe transformar los datos para mejorarlos, incrementar su calidad, integrarlos con otros sistemas, normalizarlos, eliminar duplicidades o ambigüedades. Además, no debe crear información, duplicar, eliminar información relevante, ser errónea o impredecible.

Una vez transformados, los datos ya estarán listos para su carga.

### Carga

Fase encargada de almacenar los datos en el destino, un *data warehouse* o en cualquier tipo de base de datos. Por tanto la fase de carga interactúa de manera directa con el sistema destino, y debe adaptarse al mismo con el fin de cargar los datos de manera satisfactoria.

La carga debe realizarse buscando minimizar el tiempo de la transacción.

Cada BBDD puede tener un sistema ideal de carga basado en:

* SQL (Oracle, SQL Server, Redshift, Postgres, Teradata, Greenplum, …)
* Ficheros (Postgres, Redshift, ...)
* Cargadores Propios (HDFS, S3, ...)

Para mejorar la carga debemos tener en cuenta la:

* Gestiones de índices
* Gestión de claves de distribución y particionado
* Tamaño de las transacciones y commit’s

## ELT

ELT cambia el orden de las siglas y se basa en extraer, cargar y transformar. Es un técnica de ingestión de datos donde los datos que se obtienen desde múltiples fuentes se colocan sin transformar directamente en un *data lake* o almacenamiento de objetos en la nube. Desde ahí, los datos se pueden transformar dependiendo de los diferentes objetivos de negocio.

En principio un proceso ELT necesita menos ingenieros de datos necesarios. Con la separación de la extracción y la transformación, ELT permite que los analistas y científicos de datos realicen las transformaciones, ya sea con SQL o mediante Python. De esta manera, más departamentos se involucran en obtener y mejorar los datos.

Una de las principales razones de que ELT cueste menos de implementar es que permite una mayor generalización de la información que se almacena. Los ingenieros de datos generan un *data lake* con los datos obtenidos de las fuentes de datos más populares, dejando que la transformación la realicen los expertos en el negocio. Esto también implica que los datos estén disponibles antes, ya que mediante un proceso ETL los datos no están disponibles para los usuarios hasta que se han transformado, lo que suele implicar un largo proceso de trabajo.

En resumen, el mercado se está moviendo desde un desarrollo centralizado mediante ETL a uno más orientado a servicios como ELT, que permite automatizar la carga del *data lake* y la posterior codificación de los flujos de datos.

## Herramientas ETL

Las caracteristicas de las herramientas ETL son:

* Permiten conectividad con diferentes sistemas y tipos de datos
    * Excel, BBDD transaccionales, XML, ficheros CSV / JSON, Teradata, HDFS, Hive, S3, ...
    * Peticiones HTTP, servicios REST...
    * APIs de aplicaciones de terceros, logs…

* Permiten la planificación mediante *batch*, *eventos* o en *streaming*.

* Capacidad para transformar los datos:
    * Transformaciones simples: tipos de datos, cadenas, codificaciones, cálculos simples.
    * Transformaciones intermedias: agregaciones, lookups.
    * Transformaciones complejas: algoritmos de IA, segmentación, integración de código de terceros, integración con otros lenguajes.

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
    <img src="../imagenes/etl/01herramientasETL.png">
    <figcaption>Herramientas ETL</figcaption>
</figure>

## La ingesta por dentro

La ingesta extrae los datos desde la fuente donde se crean o almacenan originalmente y los carga en un destino o zona temporal. Un *pipeline* de datos sencillo puede que tenga que aplicar uno más transformaciones ligeras para enriquecer o filtrar los datos antes de escribirlos en un destino, almacén de datos o cola de mensajería. Se pueden añadir nuevos *pipelines* para transformaciones más complejas como *joins*, agregaciones u ordenaciones para analítica de datos, aplicaciones o sistema de informes.

<figure style="align: center;">
    <img src="../imagenes/etl/01dataIngestion.png">
    <figcaption>La ingesta de datos - StreamSets</figcaption>
</figure>

Las fuentes más comunes desde las que se obtienen los datos son:

* servicios de mensajería como Apache Kafka, los cuales han obtenido datos desde fuentes externas, como pueden ser dispositivos IOT o contenido obtenido directamente de las redes sociales.
* bases de datos relaciones, las cuales se acceden, por ejemplo, mediante JDBC.
* servicios REST que vuelven los datos en formato JSON.
* servicios de almacenamiento distribuido como HDFS o S3.

Los destinos donde se almacenan los datos son:

* servicios de mensajería como Apache Kafka
* bases de datos relaciones
* bases de datos NoSQL
* servicios de almacenamiento distribuido como HDFS o S3.
* plataformas de datos como Snowflake o Databricks.

### Batch vs Streaming

El movimiento de datos entre los orígenes y los destinos se puede hacer, tal como vimos en la sesión de [Arquitecturas de Big Data](arquitecturas01.md#tipos-de-arquitecturas), mediante un proceso:

* *Batch*: el proceso se ejecuta de forma periódica (normalmente en intervalos fijos) a partir de unos datos *estáticos*. Muy eficiente para grandes volúmenes de datos, y donde la latencia (del orden de minutos) no es el factor más importante. Algunas de las herramientas utilizadas son *Apache Sqoop*, trabajos en *MapReduce* o de *Spark jobs*, etc...
* *Streaming*: también conocido como en tiempo real, donde los datos se leen, modifican y cargan tan pronto como llegan a la capa de ingesta (la latencia es crítica). Algunas de las herramientas utilizadas son *Apache Storm*, *Spark Streaming*, *Apache Nifi*, *Apache Kafka*, etc...

### Arquitectura

Si nos basamos en la [arquitectura por capas](arquitecturas01.md#arquitectura-por-capas), podemos ver como la capa de ingesta es la primera de la arquitectura por capas, la cual recoge los datos que provienen de fuentes diversas. Los datos se categorizan y priorizan, facilitando el flujo de éstos en posteriores capas:

<figure style="align: center;">
    <img src="../imagenes/arq/01arquitecturasCapas.png">
    <figcaption>Arquitectura por capas (xenonstack.com)</figcaption>
</figure>

En el primer paso de la ingesta es el paso más pesado, por tiempo y cantidad de recursos necesarios. Es normal realizar la ingesta de flujos de datos desde cientos a miles de fuentes de datos, los cuales se obtiene a velocidades variables y en diferentes formatos.

Para ello, es necesario:

* Priorizar las fuentes de datos
* Validar de forma individual cada fichero
* Enrutar cada elemento a su destino correcto.

Resumiendo, los cuatro parámetros en los que debemos centrar nuestros esfuerzos son:

1. Velocidad de los datos: cómo fluyen los datos entre máquinas, interacción con usuario y redes sociales, si el flujo es continuo o masivo.
2. Tamaño de los datos: la ingesta de múltiples fuentes puede incrementarse con el tiempo.
3. Frecuencia de los datos: ¿Batch o en Streaming?
4. Formato de los datos: estructurado (tablas), desestructurado (imágenes, audios, vídeos, ...), o semi-estructurado (JSON).

## Herramientas de Ingesta de datos

Las herramientas de ingesta de datos para ecosistemas Big Data se clasifican en los siguientes bloques:

<figure style="float: right;">
    <img src="../imagenes/etl/01ingestaTools.png">
    <figcaption>Herramientas de ingesta de datos</figcaption>
</figure>

* [*Apache Sqoop*](https://sqoop.apache.org): permite la transferencia bidireccional de datos entre *Hadoop/Hive/HBase* y una bases de datos SQL (datos estructurados). Aunque principalmente se interactura mediante comandos, proporciona una API Java.
* [*Apache Flume*](https://flume.apache.org): sistema de ingesta de datos semiestructurados o no estructurados sobre HDFS o HBase mediante una arquitectura basada en flujos de datos en streaming.
* [*Apache Nifi*](https://nifi.apache.org): herramienta que facilita un interfaz gráfico que permite cargar datos de diferentes fuentes (tanto *batch* como *streaming*), los pasa por un flujo de procesos (mediante grafos dirigidos) para su tratamiento y transformación, y los vuelca en otra fuente.
* [*Elastic Logstash*](https://www.elastic.co/es/logstash/): Pensada inicialmente para la ingesta de logs en *Elasticsearch*, admite entradas y salidas de diferentes tipos (incluso AWS).
* [*AWS Glue*](https://aws.amazon.com/es/glue): servicios gestionado para realizar tareas ETL desde la consola de AWS. Facilita el descubrimiento de datos y esquemas. También se utiliza como almacenamiento de servicios como *Amazon Athena* o *AWS Data Pipeline*.

Por otro lado existen sistemas de mensajería con funciones propias de ingesta, tales como:

* *Apache Kafka*: sistema de intermediación de mensajes basado en el modelo publicador/suscriptor.
* *RabbitMQ*: sistema de colas de mensajes (MQ) que actúa de middleware entre productores y consumidores.
* *Amazon Kinesis*: homólogo de Kafka para la infraestructura Amazon Web Services.
* *Microsoft Azure Event Hubs*: homólogo de Kafka para la infraestructura Microsoft Azure.
* *Google Pub/Sub*: homólogo de Kafka para la infraestructura Google Cloud.

## Consideraciones

A la hora de analizar cual sería la tecnología y arquitectura adecuada para realizar la ingesta de datos en un sistema Big Data, hemos de tener en cuenta los siguientes factores:

* Origen y formato de los datos
    * ¿Cual va a ser el origen u orígenes de los datos?
    * ¿Provienen de sistemas externos o internos?
    * ¿Serán datos estructurados o datos sin estructura?
    * ¿Cuál es el volumen de los datos? Volumen diario, y plantear como sería la primera carga de datos.
    * ¿Existe la posibilidad de que más adelante se incorporen nuevas fuentes de datos?
* Latencia/Disponibilidad
    * Ventana temporal que debe pasar desde que los datos se ingestan hasta que puedan ser utilizables, desde horas/días (mediante procesos *batch*) o ser *real-time* (mediante *streaming*)
* Actualizaciones
    * ¿Las fuentes origen se modifican habitualmente?
    * ¿Podemos almacenar toda la información y guardar un histórico de cambios?
    * ¿Modificamos la información que tenemos? ¿mediante *updates*, o *deletes + insert*?
* Transformaciones
    * ¿Son necesarias durante la ingesta?
    * ¿Aportan latencia al sistema? ¿Afecta al rendimiento?
    * ¿Tiene consecuencias que la información sea transformada y no sea la original?
* Destino de los datos
    * ¿Será necesario enviar los datos a más de un destino, por ejemplo, S3 y DynamoDB?
    * ¿Cómo se van a utilizar los datos en el destino? ¿cómo serán las consultas? ¿es necesario particionar los datos? ¿serán búsquedas aleatorias o no? ¿Utilizaremos *Hive* / *Pig* / *DynamoDB*?
    * ¿Qué procesos de transformación se van a realizar una vez ingestados los datos?
    * ¿Cual es la frecuencia y actualización de los datos origen?
* Estudio de los datos
    * Calidad de los datos ¿son fiables? ¿existen duplicados?
    * Seguridad de los datos. Si tenemos datos sensibles o confidenciales, ¿los enmascaramos o decidimos no realizar su ingesta?

## Actividades

1. Completa el cuestionario disponible en *Aules* (dentro del apartado *Big Data Aplicado*).

## Referencias

* [Ingesta, es más que una mudanza de datos](https://www.futurespace.es/ingesta-es-mas-que-una-mudanza-de-datos/)
* [¿Qué es ETL?](https://www.talend.com/es/resources/what-is-etl/)
* [Building Big Data Storage Solutions (Data Lakes) for Maximum Flexibility](https://docs.aws.amazon.com/whitepapers/latest/building-data-lakes/building-data-lake-aws.html?did=wp_card&trk=wp_card)

<!--
https://streamsets.com/learn/data-ingestion/
https://streamsets.com/learn/etl-or-elt/
https://aprenderbigdata.com/pipeline-de-datos/
-->
