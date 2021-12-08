
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

En el siguiente supuesto, vamos a crear una aplicación *Athena*, definiremos una base de datos, crearemos una tabla con sus columnas y tipos de datos, y ejecutaremos consultas sencillas y compuestas.

Amazon Athena es un servicio de consulta interactivo que se puede utilizar para extraer información de datos almacenados en S3. Athena almacena metadatos sobre las fuentes de datos, así como las consultas para poder reutilizarlas o compartirlas con otros usuarios.

Athena is serverless, so there is no infrastructure to set up or manage, and you pay only for the queries you run. Athena scales automatically—running queries in parallel—so results are fast, even with large datasets and complex queries.

Amazon Athena is a fast, cost-effective, interactive query service that makes it easy to analyze petabytes of data in S3 with no data warehouses or clusters to manage.

1. Seleccionar el *data set*, identificando en S3 donde están los datos. Athena permite consultar los datos CSV, TSV, JSON, Parquet y formato ORC.
2. Crear la tabla, mediante el asistente de crear tabla o utilizanos la sintaxis DDL de Hive.
3. Consultar los datos, mediante SQL.

Antes de empezar con *Athena*, necesitamos crear un *bucket* donde almacenar los resultados de nuestras consultas. Así pues, vamos a crear un *bucket* que llamaremos *severo2122athena*.

Una vez creado, ya podemos acceder a Athena, y en la pestaña de *Settings* indicar el bucket donde vamos a guardar los resultados:

<figure style="align: center;">
    <img src="../imagenes/etl/01athenaSettings.png">
    <figcaption>Athena - Configuración inicial</figcaption>
</figure>

A continuación, entramos al *Query editor*, y a lado de la sección *Tables and vies*, desplegamos el menú *Create* y creamos una tabla a partir de datos S3:

<figure style="align: center;">
    <img src="../imagenes/etl/01athenaCreateTable0.png">
    <figcaption>Athena - Opción para crear la tabla a partir de S3</figcaption>
</figure>

En la siguiente pantalla, crearemos la tabla `yellow` en una nueva base de datos que denominamos `taxidata` y le indicamos que coja los datos S3 de `s3://aws-tc-largeobjects/CUR-TF-200-ACBDFO-1/Lab2/yellow/`. El formato de los datos es `CSV`. El siguiente paso es mediante `Bulk add columns` indicar los nombre y tipos de las columnas:

``` sql
vendor string,
pickup timestamp,
dropoff timestamp,
count int,
distance int,
ratecode string,
storeflag string,
pulocid string,
dolocid string,
paytype string,
fare decimal,
extra decimal,
mta_tax decimal,
tip decimal,
tolls decimal,
surcharge decimal,
total decimal
```

Finalmente, veremos a modo de resumen una instrucción `create table` similar a la siguiente y ya podemos pulsar sobre *Create table*:

``` sql
CREATE EXTERNAL TABLE IF NOT EXISTS `taxidata`.`yellow` (
`vendor` string,
`pickup` timestamp,
`dropoff` timestamp,
`count` int,
`distance` int,
`ratecode` string,
`storeflag` string
`pulocid` string,
`dolocid` string,
`paytype` string,
`fare` decimal,
`extra` decimal,
`mta_tax` decimal,
`tip` decimal,
`tolls` decimal,
`surcharge` decimal,
`total` decimal
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
'serialization.format' = ',',
'field.delim' = ','
) LOCATION 's3://aws-tc-largeobjects/CUR-TF-200-ACBDFO-1/Lab2/yellow/'
TBLPROPERTIES ('has_encrypted_data'='false');



FIXME: mirar y hacer https://docs.aws.amazon.com/athena/latest/ug/getting-started.html


### AWS Glue

Es la herramienta ETL completamente administrado que ofrece Amazon Web Services.

Cuando el esquema de los datos es desconocido, *AWS Glue* permite inferirlo. Para ello, hemos de construir un rastreador (*crawler*) para descubrir su estructura.

. AWS Glue builds a catalog that contains metadata about the various data sources. AWS Glue is similar to Amazon Athena in that the actual data you analyze remains in the data source. The key difference is that you can build a crawler with AWS Glue to discover the schema.

### Creación

### Ejecución

Se puede ejecutar bajo demanda o planificar su ejecución de forma diaria, por horas, etc... Una vez lanzado, al cabo de un minuto, veremos que ha finalizado y en `Base de Datos --> Tablas` podremos ver la tabla que ha creado (en nuestro caso la tabla `csv`), junto con la estructura que ha inferido respecto a los datos cargados.

El siguiente paso es editar el esquema y ponerle nombres significativos a los campos:

Una vez los datos están cargados, ya podemos realizar consular con AWS Athena.
