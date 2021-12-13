# Flume / Sqoop

## Sqoop

*Apache Sqoop* (<https://sqoop.apache.org>) es una herramienta diseñada para transferir de forma eficiente datos crudos entre un cluster de Hadoop y un almacenamiento estructurado, como una base de datos relacional.

!!! caution "Sin continuidad"
    Desde Junio de 2021, el proyecto *Sqoop* ha dejado de mantenerse como proyecto de Apache y forma parte del *ático*. Aún así, creemos conveniente conocer su uso en el estado actual. Gran parte de las funcionalidad que ofrece *Sqoop* se pueden realizar mediante *Nifi* o *Spark*.

Un caso típico de uso es el de cargar los datos de un *data lake*  (ya sea en HDFS o en S3) con datos que importaremos desde una base de datos, como MariaDB, PosgreSQL o MongoDB.

Sqoop utiliza una arquitectura basada en conectores, con soporte para *plugins* que ofrecen la conectividad a los sistemas externos, como pueden ser Oracle o SqlServer. Internamente, Sqoop utiliza los algoritmos *MapReduce* para importar y exportar los datos.

Por defecto, todos los trabajos Sqoop ejecutan cuatro mapas de trabajo ¿?¿?¿

https://learning.oreilly.com/videos/master-big-data/9781839212734/9781839212734-video2_1/

!!! info "Instalación"
    Aunque en la máquina virtual con la que trabajamos ya tenemos tanto Hadoop como Sqoop instalados, podemos descargar la última versión desde <http://archive.apache.org/dist/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz>.

    Se recomienda seguir las instrucciones resumidas que tenemos en <https://www.tutorialspoint.com/sqoop/sqoop_installation.htm> o las de <https://riptutorial.com/sqoop>.

    Un par de aspectos que hemos tenido que modificar en nuestra máquina virtual son:

    * Copiar el [driver de MySQL](../recursos/mysql-connector-java-5.1.49-bin.jar) en `$SQOOP_HOME/lib`
    * Copiar la librería [commons-langs-2.6](https://repo1.maven.org/maven2/commons-lang/commons-lang/2.6/commons-lang-2.6.jar) en `$SQOOP_HOME/lib`

    Una vez configurado, podemos comprobar que funciona, por ejemplo, consultando las bases de datos que tenemos en MariaDB:

    ```
    sqoop list-databases --connect jdbc:mysql://localhost --username=iabd --password=iabd
    ```

### Importando datos

La sintaxis básica de Sqoop para importar datos en HDFS es la siguiente:

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

### Caso de uso 1 - Importando datos desde MariaDB

En el siguiente caso de uso vamos a importar datos que tenemos en una base de datos de MariaDB a HDFS.

!!! caution "Sqoop y las zonas horarias"
    Cuando se lanza SQOOP captura los *timestamps* de nuestra base de datos origen y las convierte a la hora del sistema servidor por lo que tenemos que especificar en nuestra base de datos la zona horaria.

    Para realizar estos ajustes simplemente editamos el fichero `mysqld.cnf` que se encuentra en `/etc/mysql/my.cnf/` y añadimos la siguiente propiedad para asignarle nuestra zona horaria:

    ``` conf
    [mariabd]
    default_time_zone = 'Europe/Madrid'
    ``` 

Primero, vamos a preparar nuestro entorno. Una vez conectados a MariaDB, creamos una base de datos que contenga una tabla con información sobre profesores:

``` sql
create database sqoopCaso1;
use sqoopCaso1;
CREATE TABLE profesores(
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    nombre CHAR(30) NOT NULL,
    edad INTEGER(30),
    materia CHAR(30),
    PRIMARY KEY (id) );
```

Insertamos datos en la tabla `profesores:`

``` sql
INSERT INTO profesores (nombre, edad, materia) VALUES ("Carlos", 24, "Matemáticas"),
("Pedro", 32, "Inglés"), ("Juan", 35, "Tecnología"), ("Jose", 48, "Matemáticas"),
("Paula", 24, "Informática"), ("Susana", 32, "Informática"), ("Lorena", 54, "Informática");
```

A continuación, arrancamos *HDFS* y *YARN*:

``` bash
start-dfs.sh
start-yarn.sh
```

Con el comando `sqoop list-tables` listamos todas las tablas de la base de datos `sqoopCaso1`:

``` bash
sqoop list-tables --connect jdbc:mysql://localhost/sqoopCaso1 --username=iabd --password=iabd
```

Y finalmente importamos los datos mediante el comando `sqoop import`:

``` bash
sqoop import --connect jdbc:mysql://localhost/sqoopCaso1 /
    --username=iabd --password=iabd /
    --table=profesores --driver=com.mysql.jdbc.Driver /
    --target-dir=/user/iabd/sqoop/profesores_hdfs /
    --fields-terminated-by=',' --lines-terminated-by '\n'
```

Si accedemos al interfaz gráfico de YARN (recuerda que puedes acceder a él mediante `http://localhost:9870`) podremos comprobar en el directorio `/user/iabd/sqoop` que ha creado el directorio que hemos especificado junto con los siguientes archivos:

FIXME: captura de pantalla

### Caso de uso 2 - Exportando datos a MariaDB

Ahora vamos a hacer el paso contrario, desde HDFS vamos a exportar los ficheros a  otra tabla. Así pues, primero vamos a crear la nueva tabla en una nueva base de datos (aunque podíamos haber reutilizado la base de datos):

``` sql
create database sqoopCaso2;
use sqoopCaso2;
CREATE TABLE profesores2(
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    nombre CHAR(30) NOT NULL,
    edad INTEGER(30),
    materia CHAR(30),
    PRIMARY KEY (id) );
```

Para exportar los datos de HDFS y cargarlos en esta nueva tabla lanzamos la siguiente orden:

``` bash
sqoop export --connect jdbc:mysql://localhost/sqoopCaso2?serverTimezone=Europe/Madrid --username=hadoop --password=hadoop --table=profesores2 --export-dir=/opt/hadoop/sqoop/profesores_hdfs
```

### Caso de uso 3 - Formatos Avro y Parquet

Sqoop permite trabajar con diferentes formatos, tanto Avro como Parquet.

Avro es un formato de almacenamiento basado en filas para Hadoop que se usa ampliamente como formato de serialización.

Para que funcione la serialización con Avro hay que copiar el fichero `.jar` que viene en el directorio de `Sqoop` para Avro como librería de Hadoop, mediante el siguiente comando:

``` bash
cp $SQOOP_HOME/lib/avro-1.8.1.jar $HADOOP_HOME/share/hadoop/common/lib/
rm $HADOOP_HOME/share/hadoop/common/lib/avro-1.7.7.jar
```

Ahora ya podemos lanzar realizar la importación mediante el siguiente comando:

``` bash
sqoop import --connect jdbc:mysql://localhost/ejemplo --username=hadoop --password=hadoop \
    --table=profesores --driver=com.mysql.jdbc.Driver --target-dir=/avro_hdfs \
    --as-avrodatafile
```

Si en vez de Avro, queremos importar los datos en formato Parquet:

``` bash
sqoop import --connect jdbc:mysql://localhost/ejemplo --username=hadoop --password=hadoop \
    --table=profesores --driver=com.mysql.jdbc.Driver --target-dir=/parquet_hdfs \
    --as-parquetdatafile
```

### Caso de uso 4 - Trabajando con datos comprimidos

Por defecto, podemos comprimir mediante el formato gzip:

``` bash
sqoop import --connect jdbc:mysql://localhost/ejemplo --username=hadoop --password=hadoop \
    --table=profesores --driver=com.mysql.jdbc.Driver --target-dir=/datos_gzip \
    --compress
```

Si en cambio queremos comprimirlo con formato Bzip y formato secuencial:

``` bash
sqoop import --connect jdbc:mysql://localhost/ejemplo --username=hadoop --password=hadoop \
    --table=profesores --driver=com.mysql.jdbc.Driver --target-dir=/datos_bzip \
    --compress --compression-codec bzip2
```

<!--
    --compression-codec org.apache.hadoop.io.compress.BZip2Codec --as-sequencefile 
-->

*Snappy* es una biblioteca de compresión y descompresión de datos rápida que se utiliza con frecuencia en proyectos Big Data.

``` bash
sqoop import --connect jdbc:mysql://localhost/ejemplo --username=hadoop --password=hadoop \
    --table=profesores --driver=com.mysql.jdbc.Driver --target-dir=/parquet_hdfs \
    --compress --compression-codec org.apache.hadoop.io.compress.SnappyCodec \
    --as-avrodatafile
```

### Caso de uso 5 - Importando con filtros

 sqoop import \
--connect jdbc:mysql://localhost/retail_db \ --username root --password cloudera \
--table customers \
--target-dir /user/cloudera/customer-name-m \
--where "customer_fname='Mary'"

Eligiendo las columnas

 sqoop import \
--connect jdbc:mysql://localhost/retail_db \ --username root --password cloudera \
--table customers \
--target-dir /user/cloudera/customer-selected \
--columns “customer_fname,customer_lname,customer_city’”

Mediante una consulta:

 sqoop import \
--connect jdbc:mysql://localhost/retail_db \
--username root --password cloudera \
--target-dir /user/cloudera/customer-queries \
--query "Select * from customers where customer_id > 100 AND $CONDITIONS" \
--split-by "customer_id"

### Caso de uso 6 - Importación incremental

 sqoop import \
--connect jdbc:mysql://localhost/retail_db \ --username root --password cloudera \ --target-dir /user/cloudera/orders-incremental \ --table orders \
--incremental append \
--check-column order_id \
--last-value 100003

### Caso de uso 7 - Trabajando con Hive

 sqoop import \
--connect "jdbc:mysql://localhost/retail_db" \ --username root \
--password cloudera \
--table customers \
--hive-import \ --create-hive-table \ --hive-database default \ --hive-table customer_mysql

 sqoop import \
--connect "jdbc:mysql://localhost/retail_db" \ --username root \
--password cloudera \
--table customers \
--fields-terminated-by '|' \
--hive-import \ --create-hive-table \ --hive-database default \ --hive-table customer_mysql_new

## Flume

Allá por el año 2010 Cloudera presentó Flume, programa para tratamiento e ingesta de datos masivo. Esto daba la posibilidad de crear desarrollos complejos que permitieran el tratamiento de datos masivos creados en Tiempo Real.

En Real Time se utiliza en la etapa de Obtención de Datos (para conectarnos a fuentes de datos Online).

Su arquitectura es sencilla, pues tiene tres componentes principales, muy configurables:

* Source: Fuente de origen de los datos
* Channel: la vía por donde se tratarán los datos
* Sink: persistencia/movimiento de los datos

Flume es sencilli apriori, el problema es cuando quieres utilizarlo para obtener datos de manera paralela (o multiplexada) y además te ves en la necesidad de crear tus propios Sinks, o tus propios interceptores. Entonces la cosa cambia y hay que dedicarle algo más de tiempo.

Muy recomendada como ayuda|compañero|alternativa a herramientas como Kettle.

Es un sistema confiable y distribuido para recopilar, agregar y mover datos masivos.
Algunas de sus características son:
Diseño flexible basado en flujos de datos de transmisión.
Resistente a fallos y robusto con múltiples conmutaciones por error y  mecanismos de recuperación.
Lleva datos desde origen a destino: incluidos HDFS y HBASE

Componentes:

* Evento:  Son las unidades de datos transportadas por el agente flume (array de bytes).
* Agente: Contenedor para alojar subcomponentes que permiten mover los eventos
* Source: Receptor de eventos
* Interceptor: Transformador de eventos
* Channel: Buffer de eventos
* Sink: Toma eventos del canal y los transmite hacia el siguiente componente

### Caso de uso 4 - Flume

https://programmerclick.com/article/36062177137/

``` conf title="seq_gen.conf"
#Nombramos a los componentes del agente
SeqGenAgent.sources = SeqSource
SeqGenAgent.channels = MemChannel
SeqGenAgent.sinks = HDFS

# Describimos el tipo de origen
SeqGenAgent.sources.SeqSource.type = seq

# Describimos el destino
SeqGenAgent.sinks.HDFS.type = hdfs
SeqGenAgent.sinks.HDFS.hdfs.path = hdfs://hadoop-VirtualBox:9000/user/hadoop/seqgen_data/
SeqGenAgent.sinks.HDFS.hdfs.filePrefix = log
SeqGenAgent.sinks.HDFS.hdfs.rollInterval = 0
SeqGenAgent.sinks.HDFS.hdfs.rollCount = 10000
SeqGenAgent.sinks.HDFS.hdfs.fileType = DataStream

# Describimos la configuración del canal
SeqGenAgent.channels.MemChannel.type = memory
SeqGenAgent.channels.MemChannel.capacity = 1000
SeqGenAgent.channels.MemChannel.transactionCapacity = 100

# Unimos el origen y el destino a través del canal
SeqGenAgent.sources.SeqSource.channels = MemChannel
SeqGenAgent.sinks.HDFS.channel = MemChannel
```

Ejecutamos el siguiente comando:

./bin/flume-ng agent --conf ./conf/ --conf-file
./conf/seq_gen.conf --name SeqGenAgent

Ahora vamos a crear otro ejemplo de generación de información. En el mismo directorio `$FLUME_HOME\conf`, creamos un nuevo fichero con el nombre netcat.conf y copiamos el siguiente código:

``` conf title="netcat.conf"
#Nombramos a los componentes del agente NetcatAgent.sources = Netcat NetcatAgent.channels = MemChannel NetcatAgent.sinks = HDFS
# Describimos el tipo de origen NetcatAgent.sources.Netcat.type = netcat NetcatAgent.sources.Netcat.bind = localhost NetcatAgent.sources.Netcat.port = 44444 NetcatAgent.sources.Netcat.channels = MemChannel
# Describimos el destino NetcatAgent.sinks.HDFS.type=hdfs
NetcatAgent.sinks.HDFS.hdfs.path=hdfs://hadoop- VirtualBox:9000/user/hadoop/net_data/
NetcatAgent.sinks.HDFS.hdfs.writeFormat=Text NetcatAgent.sinks.HDFS.hdfs.fileType=DataStream NetcatAgent.sinks.HDFS.channel=MemChannel
# Unimos el origen y el destino a través del canal NetcatAgent.channels.MemChannel.type = memory NetcatAgent.channels.MemChannel.capacity = 1000 NetcatAgent.channels.MemChannel.transactionCapacity = 100
```

Lanzamos al agente:

./bin/flume-ng agent --conf ./conf/ --conf-file
./conf/netcat.conf --name NetcatAgent - Dflume.root.logger=INFO,console

En una nueva pestaña introducimos el siguiente comando y escribimos
curl telnet

Nos vamos al navegador web de HDFS y comprobamos que se ha creado el fichero:
 http://localhost:9870/explorer.html#/user/hadoop/net_data

## Actividades

1.- Haciendo uso de Sqoop, carga los datos que tenemos en la base de datos *sports* que tenemos creada en RDS e importa los datos en HDFS.


## Referencias

* Página oficial de [Sqoop](https://sqoop.apache.org)
* [Sqoop User Guide](https://sqoop.apache.org/docs/1.4.7/SqoopUserGuide.html)
* [Sqoop Tutorial](https://www.tutorialspoint.com/sqoop/index.htm) en Tutorialspoint
