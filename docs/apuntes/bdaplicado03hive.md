# Hive

Apache Hive (<https://hive.apache.org/>) es una tecnología distribuida diseñada y construida sobre un cúster de *Hadoop*. Permite leer, escribir y gestionar grandes dataset (con escala de petabytes) que residen en HDFS haciendo uso de un lenguaje dialecto de SQL, conocido como *HiveSQL*, lo que simplifica mucho el desarrollo y la gestión de Hadoop.

FIXME: poner logo

El proyecto comenzó en el 2008 por Facebook para conseguir que la interacción con Hadoop fuera similar a la que se realiza con un *datawarehouse*  tradicional. La tecnología Hadoop es altamente escalable, aunque hay que destacar su dificultad de uso y que está orientado únicamente a operaciones *batch*, con lo que no soporta el acceso aleatorio ni está optimizado para ficheros pequeños.

Si volvemos a ver como casa Hive dentro del ecosistema de Hadoop
Relación de Hive con Hadoop y otras herramientas,

Aunque en principio estaba diseñado para el procesamiento por lotes ahora se integra con frameworks de tiempo real como Tez y Spark.

Dicho de otro modo, Hive es una fachada construida sobre Hadoop que permite acceder a los datos almacenados en HDFS de forma muy sencilla sin necesidad de conocer *Java*, *Map Reduc*e u otras tecnologías.

Hive impone una estructura sobre los datos almacenados en HDFS. Esta estructura se conoce como Schema, y Hive la almacena en su propia base de datos (*metastore*). Gracias a ella, optimiza de forma automática el plan de ejecución y usa particionado de tablas en determinadas consultas. También soporta diferentes formatos de ficheros, codificaciones y fuentes de datos como HBase.



. Hive permite evitar la complejidad de escribir trabajos Tez basados en DAG (directed acyclic graphs) o programas MapReduce en un lenguaje de programación inferior como es Java.

Hive amplía el paradigma de SQL incluyendo formatos de serialización. También puede personalizar el procesamiento de consultas creando un esquema de tabla acorde con sus datos, sin tocar los datos. Aunque SQL solo es compatible con tipos de valor primitivos (como fechas, números y cadenas), los valores de las tablas de Hive son elementos estructurados, por ejemplo, objetos JSON, cualquier tipo de datos definido por el usuario o cualquier función escrita en Java.





Una consulta típica en Hive ejecuta en varios data nodes en paralelo, con trabajos MapReduce asociados. Estas operaciones son de tipo batch, por lo que la latencia es más alta que en otros tipos de bases de datos. Además, hay que considerar el retardo producido por la inicialización de los trabajos, sobre todo en el caso de consultar pequeños datasets.

 Structure can be projected onto data already in storage. A command line tool and JDBC driver are provided to connect users to Hive.

Hive incorpora Beeline, un cliente basado en JDBC para hacer consultas por línea de comandos contra el componente *HiveServer*, sin necesitar las dependencias de Hive. Por otro lado, también incorpora Hive CLI, un cliente basado en *Apache Thrift*, que usa los mismos drivers que Hive.

Hive como Data Warehouse
Cuando se empezaba a generalizar el procesamiento de datos de negocio masivos, se usaban las mismas bases de datos para procesar las transacciones y para hacer consultas analíticas. Sin embargo, las organizaciones pronto empezaron a separar las consultas analíticas a una base de datos distinta llamada Data Warehouse.

Esta base de datos contiene copias de solo lectura de todos los datos en los sistemas transaccionales y operacionales (OLTP). Los datos se extraen periódicamente de las bases de datos OLTP, se transforman y se limpian para adaptarlos esquemas que facilitan la analítica y se insertan en el Data Warehouse (OLAP). Este es el proceso conocido como ETL.

El modelo OLTP (Online Transaction Processing) requiere operaciones transaccionales. Es una categoría de procesamiento basada en tareas transaccionales, generalmente consisten en actualizar, insertar o eliminar pequeños conjuntos de datos. Para mantener su integridad, estas bases de datos deben cumplir las propiedades ACID, que garantizan la Atomicidad, Consistencia, Aislamiento y Durabilidad de las transacciones.

Por otra parte, aunque Hive está más cerca de ser una base de datos tipo OLAP (Online Analytical Processing), tampoco satisface la parte en línea o la rapidez de respuesta, como hace Apache Kylin. Estas herramientas típicamente están optimizadas para consultar grandes conjuntos de datos o todos los registros disponibles.


## Estructura de datos en Hive

Hive proporciona una estructura basada en tablas sobre HDFS. Soporta tres tipos de estructuras: Tablas, particiones y buckets. Las tablas se corresponden con directorios de HDFS, las particiones son las divisiones de las tablas y los buckets son las divisiones de las particiones.

Hive permite crear tablas externas, similares a las tablas en una Base de datos, pero a la que se les proporciona una ubicación. En este caso, cuando se elimina la tabla externa, los datos continúan en HDFS.

Las particiones en Hive consisten en dividir las tablas en varios subdirectorios. Esta estructura permite aumentar el rendimiento de las consultas en el caso de usar filtros con cláusula WHERE.

Otro concepto importante en Hive son los Buckets. Son particiones hasheadas, en las que los datos se distribuyen en función de su valor hash. Los Buckets pueden acelerar las operaciones de tipo JOIN si las claves de particionado y de JOIN coinciden. Debido a los beneficios de las particiones, se deben considerar siempre que puedan optimizar el rendimiento de las consultas realizadas.

ENTIDAD	EJEMPLO	UBICACIÓN
base de datos	testdb	$WH/testdb.db
tabla	T	$WH[/testdb.db]/T
partición	fecha=’01012020′	$WH[/testdb.db]/T/fecha=01012020
bucket column	userid	$WH[/testdb.db]/T/fecha=01012020/000000_0
…
$WH[/testdb.db]/T/fecha=01012020/000032_0
Hive también permite una operación de sampling sobre una tabla, por la que se obtienen valores aleatorios o una “muestra” sobre la que realizar analítica o transformaciones sin tener que tratar el dataset completo, que en ocasiones es inviable.

La política del esquema es schema-on-read, de forma que solo se obliga en las operaciones de lectura. Esta propiedad permite a Hive ser más flexible en la lectura de los datos: un mismo dato se puede ajustar a varios esquemas, uno en cada lectura. Los sistemas RDBMS tienen una política schema-on-write, que obliga a las escrituras a cumplir un esquema. En este caso acelera las lecturas.

### Componentes
 
En Hive 3 se deja de soportar MapReduce. *Apache Tez* lo reemplaza como el motor de ejecución por defecto. Tez es un framework de procesamiento que mejora el rendimiento y ejecuta sobre Hadoop Yarn, que encola y planifica los trabajos en el clúster. Además de Tez, Hive también puede usar Apache Spark como motor de ejecución.

### Hive Server

HiveServer 2 (HS2) es la última versión del servicio. Se compone de una interfaz que permite a clientes externos ejecutar consultas contra Apache Hive y obtener los resultados. Está basado en Thrift RPC y soporta clientes concurrentes.

A este servidor nos conectaremos mediante Beeline (Beeline CLI) herramienta en modo comando.

### Hive Metastore 

Es el repositorio central para los metatados de Hive, y se almacena una base de datos relacional como MySQL, PostgreSQL o Apache Derby (embebida). Mantiene los metadatos, las tablas y sus tipos mediante *Hive DDL* (*Data Definition Language*). Además, el sistema se puede configurar para que también almacene estadísticas de las operaciones y registros de autorización para optimizar las consultas.

En las últimas versiones de Hive, este componente se puede desplegar de forma remota e independiente, para no compartir la misma JVM con *HiveServer*. Dentro del *metastore* podemos encontrar el *Hive Catalog* (*HCatalog*), que permite acceder a sus metadatos, actuando como una API. Al poder desplegarse de forma aislada e independiente, permite que otras aplicaciones hagan uso del Schema sin tener que desplegar el motor de consultas de Hive.

Así pues, al *metastore* podremos acceder mediante HiveCLI, o a traves del Hive Server, por ejemplo con Beeline.

Arquitectura de alto nivel Hive
Arquitectura de Apache Hive

 
Hive LLAP
Hive LLAP (Low Latency Analytical Processing) fue añadido como motor a Hive 2.0. Requiere Tez como motor de ejecución y aporta funcionalidades de caché de datos y metadatos en memoria, acelerando mucho algunos tipos de consulta. Es especialmente significativo en consultas repetitivas para las que ofrecer tiempos de respuesta menores al segundo.

LLAP se compone de un conjunto de demonios que ejecutan partes de consultas Hive. Las tareas de los ejecutores, por tanto, se encuentran dentro de los demonios y no en los contenedores. En este caso, la sesión Tez tendrá solamente un contenedor, que corresponde al coordinador de consultas.

Esquema de Arquitectura en Hive LLAP
Esquema de Arquitectura en Hive LLAP
Hive LLAP tiene en cuenta las transacciones ACID y tiene una política de desalojo de caché personalizable y optimizada para operaciones analíticas. También soporta federación de consultas en HDFS, almacenamiento de objetos e integración con tecnologías de streaming y de tiempo real como Apache Kafka y Apache Druid.

Es una tecnología similar a Apache Impala pensada para cargas big data. Hive LLAP es ideal en entornos empresariales de Data Warehouse, en los que nos podemos encontrar consultas repetitivas pero muy pesadas en su primera ejecución, con transformaciones complejas y joins sobre grandes cantidades de datos.

Ventajas
Reduce la complejidad de la programación MapReduce al usar HQL como lenguaje de consulta (dialecto de SQL).
Está orientado a aplicaciones de tipo Data Warehouse, con datos estáticos, poco cambiantes y sin requisitos de tiempos de respuesta rápidos.
Permite a los usuarios despreocuparse de en qué formato y dónde se almacenan los datos.
Incorpora Beeline: una herramienta por línea de comandos para realizar consultas con HQL.
Desventajas
Hive no es la mejor opción para consultas en tiempo real o de tipo OLTP (Online Transaction Processing).
Hive no está diseñado para usarse con actualizaciones de valores al nivel de registro.
Soporte SQL limitado: no existen sub-queries.


Los tipos de datos de las tablas son muy similares a los de SQL (TINYIN, INT, FLOAT, BOOLEAN, TIMESTAMP, ... ) así como también tiene soporte para tipos de datos complejos, como ARRAY (conjunto de datos del mismo tipo), MAP( conjunto de pares clave/valor) o STRUCT (conjunto de valores de distinto tipo).



Ejemplo de consulta en Apache Hive



A continuación vamos a escribir un ejemplo de consultas en Apache Hive. Para empezar podemos crear una base de datos:

CREATE DATABASE mydb;
USE mydb;
La sintaxis para crear una tabla es la siguiente:

CREATE TABLE IF NOT EXISTS mydb.pagina (
  view_time INT,
  user_id BIGINT,
  page_url STRING,
  ip STRING
PARTITIONED BY (dt STRING)
CLUSTERED BY (user_id) INTO 32 BUCKETS
ROW FORMAT DELIMITED
  FIELDS TERMINATED BY '\t'
STORED AS ORC;
Con ello, hemos creado una tabla llamada pagina con 4 columnas. Se ha especificado una partición y la columna user_id se usará para el bucket. El formato indica ORC (Binario).

Para insertar datos podemos cargarlos de un fichero o bien insertar los valores desde la propia consulta:

LOAD DATA LOCAL INPATH '/tmp/pagina_2020-01-01.txt'
  OVERWRITE INTO TABLE mydb.pagina
  PARTITION (dt='2020-01-01');

INSERT INTO TABLE mydb.pagina partition(dt='2020-01-01')
  values (1,1,'s1','t1');
Especificando LOCAL, indicamos que el fichero se encuentra en el sistema de ficheros local. Por defecto, interpretará que el fichero se encuentra en HDFS.

## Referencias

* [Tutorial de Hive](https://www.tutorialspoint.com/hive/index.htm) de TutorialsPoint.
* [Tutorial de Pih](https://www.tutorialspoint.com/apache_pig/index.htm) de TutorialsPoint.

## Actividades
