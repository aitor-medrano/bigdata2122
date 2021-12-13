# ETL con SQL / Python

<p align="right"><small>Tiempo estimado de lectura: XX minutos [21 de Febrero]</small></p>

## DataLake con SQL

Vamos a utilizar un *dataset* que contiene información sobre las ventas de un comercio. Los datos se pueden consultar en <https://archive.ics.uci.edu/ml/datasets/Online+Retail> y <https://archive.ics.uci.edu/ml/datasets/Online+Retail+II>.

En dichas páginas podemos ver como la estructura de los datos se compone de los siguientes campos:

* `InvoiceNo`: Número de factura compuesto de 6 digitos que se asigna a cada transacción. Si el código empieza por la letra c, indica una cancelación.
* `StockCode`: Código de producto, compuesto de 5 dígitos.
* `Description`: Nombre del producto.
* `Quantity`: Cantidad de cada producto que forma parte de la transacción.
* `InvoiceDate`: Fecha de la factura cuando se realizó la transacción, mediante un campo numérico.
* `UnitPrice`: Precio unitario.
* `CustomerID`: Número de cliente, compuesto de 5 dígitos.
* `Country`: Nombre del pais del cliente que realiza el pedido.

``` csv title="online_retail.csv"
Invoice;StockCode;Description;Quantity;InvoiceDate;Price;Customer ID;Country
489434;85048;15CM CHRISTMAS GLASS BALL 20 LIGHTS;12;01/12/2009 7:45;6,95;13085;United Kingdom
489434;79323P;PINK CHERRY LIGHTS;12;01/12/2009 7:45;6,75;13085;United Kingdom
489434;79323W; WHITE CHERRY LIGHTS;12;01/12/2009 7:45;6,75;13085;United Kingdom
```

Hemos cogido ambos archivos y los hemos unido generando un único archivo CSV, el cual puedes descargar desde [aquí](../recursos/online_retail_junto.csv).

Vamos a crear un *data lake* a partir de dichos datos. Realmente, vamos a cargarlos en una BD, en nuestro caso *MariaDB* mediante una instancia RDS, y una vez cargado los datos, vamos al limpiarlos.

Respecto a la estructura del *data lake*, hemos decidido crear casi todos los tipos de datos como caracteres para que no haya ningún problema de importación, ya que vamos a almacenar los datos en bruto. El único campo que vamos a ponerle un tipo es `Quantity`, ya que sí que esperamos que el dato sera numérico.

Así pues, creamos una tabla `datalake` con la siguiente estructura:

``` sql
CREATE TABLE datalake (
    InvoiceNo VARCHAR(12) NULL DEFAULT NULL,
    StockCode VARCHAR(12) NULL DEFAULT NULL,
    Description VARCHAR(100) NULL DEFAULT NULL,
    Quantity INT(5) NULL DEFAULT NULL,
    InvoiceDate VARCHAR(25) NULL DEFAULT NULL,
    UnitPrice VARCHAR(10) NULL DEFAULT NULL,
    CustomerID VARCHAR(10) NULL DEFAULT NULL,
    Country VARCHAR(100) NULL DEFAULT NULL
);
```

Sobre estos datos, ya sea mediante *HeidiSQL*, *DBeaver* o línea de comandos, importamos los datos del csv. En nuestro caso, nos hemos decantado por hacerlo desde dentro de *Cloud9*. Para ello, una vez subido el archivo de datos, nos conectamos a la base de datos mediante:

``` sql
mysql --host=sports.cm4za4bbxb45.us-east-1.rds.amazonaws.com  -u admin -padminadmin datalake
```

Cuando ya estamos dentro de *MariaDB*, utilizamos la instrucción `load data infile` para importar los datos (en nuestro caso se han importado 1067372 registros en menos de 9 segundos):

``` sql
LOAD DATA LOCAL INFILE 'online_retail_junto.csv' IGNORE INTO TABLE `datalake`.`datalake` CHARACTER SET utf8 FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (`InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`);
```

### Comenzamos la limpieza

Una vez cargado, vamos a empezar a realizar alguna labores de limpieza mediante SQL.

Antes de empezar, vamos a comprobar cuantos registros (1.067.372) contiene nuestro almacen:

``` sql
SELECT COUNT(*) as inicial FROM datalake;
```

A continuación, eliminamos:

* los posibles registros con cabeceras (1):

    ``` sql
    DELETE FROM datalake WHERE UPPER(Country)='COUNTRY';
    ```

* los pedidos con cantidades negativas (22.950)

    ``` sql
    DELETE FROM datalake WHERE Quantity<=0;
    ```

* los pedidos con precio negativo o 0. Recuerda que era un campo de tipo `varchar` (2.768):

    ``` sql
    DELETE FROM datalake WHERE CAST(REPLACE(UnitPrice,',','.') AS DECIMAL(9,2))<=0;
    ```

* los pedidos cancelados (el número de factura comienza por `C`)

    ``` sql
    DELETE FROM datalake WHERE left(InvoiceNo,1)="C"
    ```
min 59

### Modelo transaccional

Vamos a crear un modelo transaccional a partir del *data lake*. Para ello, vamos a ir creando diferentes tablas para separar la información.


FIXME: Poner imagen del EER

Vamos a comenzar creando una tabla de `PAISES` con los paises de los clientes:

``` sql
DROP TABLE IF EXISTS PAISES;
CREATE TABLE PAISES AS SELECT DISTINCT UPPER(country) AS PAIS FROM datalake; 
ALTER TABLE PAISES ADD COLUMN IDPAIS INT PRIMARY KEY AUTO_INCREMENT FIRST ;
SELECT * FROM PAISES ORDER BY pais LIMIT 10;
```

A continuación creamos una tabla `CLIENTES`, distinguiendo a los clientes con que tenían el campo `CustomedID` vacío, que significa que han pagado al contado, respecto al resto de clientes. Tras crear la tabla y relacionarla con la de `PAISES`, la rellenamos con los datos.

``` sql
-- Comprobamos si los CustomerId son numéricos
SELECT DISTINCT CustomerID AS No_Numerico FROM datalake
    WHERE CAST(CAST(CustomerID AS UNSIGNED) AS CHAR)<>TRIM(CustomerID);

-- Comprobamos si tenemos clientes con CustomerId nulo.
SELECT COUNT(*) as nulos_contado FROM datalake where CustomerId = '';

DROP TABLE IF EXISTS CLIENTES;
CREATE TABLE CLIENTES (
    IDCLIENTE INT NOT NULL PRIMARY KEY,
    NOMBRE VARCHAR(100),
    IDPAIS INT NOT NULL DEFAULT 0
);
    
ALTER TABLE CLIENTES ADD CONSTRAINT CLIENTES_PAISES
    FOREIGN KEY (IDPAIS) REFERENCES PAISES(IDPAIS);

-- Al insertar los clientes, separamos los que tiene código 
-- (clientes normal que han pagado mediante la app)
-- respecto a los que son nulos
-- (que han pagado al contado y les asignamos el 0 como identificador)
INSERT INTO CLIENTES 
        SELECT DISTINCT CustomerID AS ID, '' AS NOMBRE, (SELECT IDPAIS FROM PAISES WHERE PAIS=UPPER(datalake.country))
            FROM datalake WHERE CustomerID <> ''
        UNION
        SELECT 0 AS ID, 'CONTADO' AS NOMBRE, (SELECT IDPAIS FROM PAISES WHERE PAIS=UPPER(datalake.country))
            FROM datalake WHERE CustomerID =''
ON DUPLICATE KEY UPDATE NOMBRE=NOMBRE; 

SELECT * FROM CLIENTES LIMIT 10000;
```

A continuación, vamos a crear la tabla de `PEDIDOS`:

``` sql
-- tabla de pedidos
-- examina si el codigo de pedido es numérico de forma homogénea
SELECT DISTINCT InvoiceNo AS no_numerico FROM datalake WHERE CAST(CAST(InvoiceNo AS UNSIGNED) AS CHAR)<>TRIM(InvoiceNo);

DROP TABLE IF EXISTS PEDIDOS;
CREATE TABLE PEDIDOS (
    IDPEDIDO VARCHAR(10) NOT NULL PRIMARY KEY,
    FECHAPEDIDO DATETIME NOT NULL,
    IDCLIENTE INT NOT NULL DEFAULT 0
);

ALTER TABLE PEDIDOS
        ADD CONSTRAINT PEDIDOS_CLIENTES FOREIGN KEY (IDCLIENTE) REFERENCES CLIENTES(IDCLIENTE);

-- En vez de on duplicate key se coge la fecha de inicio del pedido, por si es largo y cambia el minuto
-- y si un mismo pedido tuviera varios clientes, normalmente NULL y otro registrado, se coge el registrado 
INSERT INTO PEDIDOS
SELECT distinct InvoiceNo, MIN(STR_TO_DATE((InvoiceDate),'%d/%m/%Y %H:%i')) as FECHAPEDIDO,
        MAX(IF((CustomerID=''),0,CustomerID)) as IDCLIENTE 
        FROM datalake GROUP BY 1;

SELECT * FROM PEDIDOS LIMIT 10000;
```


``` sql
-- tabla de articulos
-- examina si el codigo de articulo es numérico de forma homogénea
    SELECT DISTINCT StockCode AS no_numerico FROM datalake WHERE CAST(CAST(StockCode AS UNSIGNED) AS CHAR)<>TRIM(StockCode);

-- revisa qué codigos de articulo no comienzan por numero
    SELECT DISTINCT StockCode, TRIM(Description) FROM datalake  where NOT StockCode REGEXP '^[0-9]' ORDER BY 1;

-- de ahí sacamos una limpieza fácil
    DELETE FROM datalake  where StockCode LIKE 'ADJUST%' OR StockCode LIKE 'AMAZON%' OR StockCode LIKE 'BANK%' OR StockCode LIKE 'TEST%' OR StockCode IN ('B','D','DOT','M','POST','S','C2') ;

-- revisa qué descripciones suenan parecidas en inglés y aparecen repetidas de forma incoherente (solución automática difícil)
    SELECT DISTINCT SOUNDEX(TRIM(Description)) as pronunciacion, 
            MAX(StockCode) as codigo, MAX(TRIM(Description)) AS Descripcion, MIN(TRIM(Description)) AS Otra_descripcion, COUNT(*) AS veces 
    FROM datalake 
    GROUP BY 1  
    HAVING COUNT(*)>1 AND MAX(TRIM(Description))<>MIN(TRIM(Description)) AND COUNT(DISTINCT StockCode)=1 ORDER BY 3;

-- revisa qué artículos tienen exactamente la misma descripción pero diferente código por si fueran en realidad el mismo artículo con dos códigos diferentes.
-- los que tienen desviación muy cercana a cero son sospechosos, los que la tienen de cero es prácticamente seguro que lo serán
-- SE OBSERVA QUE EN ALGUNOS CASOS ES LA LETRA EN MAYUSCULAS O MINUSCULAS, HAY QUE USAR UPPER
    SELECT description, COUNT(DISTINCT StockCode) veces, MIN(StockCode) AS minimo, MAX(StockCode) AS maximo, STD(CAST(REPLACE(UnitPrice,',','.') AS DECIMAL(9,2))) AS desviacion,
    MIN(CAST(REPLACE(UnitPrice,',','.') AS DECIMAL(9,2))) AS preciomin, MAX(CAST(REPLACE(UnitPrice,',','.') AS DECIMAL(9,2))) AS preciomax 
    FROM datalake 
    GROUP BY 1 
    HAVING COUNT(DISTINCT StockCode)>1 ORDER BY 1;

DROP TABLE IF EXISTS ARTICULOS;
CREATE TABLE ARTICULOS (
    IDARTICULO  VARCHAR(10) NOT NULL PRIMARY KEY,
    DESCRIPCION VARCHAR(100) NOT NULL 
);

-- Habrá algunas descripciones parecidas por un espacio, una coma...
INSERT INTO ARTICULOS
    SELECT DISTINCT UPPER(StockCode), TRIM(Description)  FROM datalake
ON DUPLICATE KEY UPDATE DESCRIPCION=Description; 

SELECT * FROM ARTICULOS LIMIT 10000;
```


``` sql
-- tabla de pedidos-articulos
-- verifica que el separador de precios es homogéneo a la ,
SELECT COUNT(*), 'Lleva .' FROM datalake WHERE INSTR(UnitPrice,'.') >0
UNION
SELECT COUNT(*), 'Lleva ,' FROM datalake WHERE INSTR(UnitPrice,',') >0;


DROP TABLE IF EXISTS PEDIDOS_ARTICULOS;
CREATE TABLE PEDIDOS_ARTICULOS(
    IDPEDIDO VARCHAR(10) NOT NULL,
    IDARTICULO VARCHAR(10) NOT NULL,
    CANTIDAD INT,
    PRECIOUNITARIO DECIMAL(9,2), 
    PRIMARY KEY(IDPEDIDO,IDARTICULO)
);
    
ALTER TABLE PEDIDOS_ARTICULOS
    ADD CONSTRAINT PEDIDOS_ARTICULOS_MM1 FOREIGN KEY (IDPEDIDO)   REFERENCES PEDIDOS(IDPEDIDO),
    ADD CONSTRAINT PEDIDOS_ARTICULOS_MM2 FOREIGN KEY (IDARTICULO) REFERENCES ARTICULOS(IDARTICULO);

-- si un pedido tiene varias líneas iguales con el mismo articulo se consolida y se hace la media de los precios por si son diferentes
INSERT INTO PEDIDOS_ARTICULOS
SELECT InvoiceNo, UPPER(StockCode), Quantity, CAST(REPLACE(UnitPrice,',','.') AS DECIMAL(9,2)) AS PRECIOUNITARIO from datalake
ON DUPLICATE KEY UPDATE PRECIOUNITARIO=CANTIDAD/(CANTIDAD+Quantity)*PRECIOUNITARIO + Quantity/(CANTIDAD+Quantity)* CAST(REPLACE(UnitPrice,',','.') AS DECIMAL(9,2))  , 
                        CANTIDAD=CANTIDAD+Quantity;

SELECT COUNT(*) FROM PEDIDOS_ARTICULOS;

SELECT * FROM PEDIDOS_ARTICULOS LIMIT 10000;
```


``` sql
-- modelo analítico RFM
-- ignoramos al cliente contado
CREATE TABLE RFM as
select cliente, 
       ntile(4) over (order by ultimopedido) as rfm_recency,
       ntile(4) over (order by totalpedidos) as rfm_frequency,
       ntile(4) over (order by gastomedio) as rfm_monetary
from 
(
SELECT c.IDCLIENTE AS cliente, 
       MAX(p.FECHAPEDIDO) as ultimopedido,
       COUNT(p.IDPEDIDO) as totalpedidos,
       AVG((SELECT SUM(pa.CANTIDAD*pa.PRECIOUNITARIO) as totalpedido FROM PEDIDOS_ARTICULOS pa WHERE pa.IDPEDIDO=p.IDPEDIDO)) as gastomedio
FROM CLIENTES c, PEDIDOS p
WHERE c.IDCLIENTE=p.IDCLIENTE AND c.IDCLIENTE>0 
group BY c.IDCLIENTE
) AS indicadores;


--Mejores clientes
DROP VIEW IF EXISTS mejores_clientes;
CREATE VIEW mejores_clientes AS
SELECT c.IDCLIENTE, p.PAIS FROM CLIENTES c, RFM r, PAISES p WHERE c.IDCLIENTE=r.cliente AND p.IDPAIS=c.IDPAIS AND rfm_recency=1 AND rfm_frequency=1 AND rfm_monetary=1 ;

SELECT * FROM mejores_clientes;
SELECT PAIS, COUNT(*) FROM mejores_clientes GROUP BY 1 ORDER BY 2 DESC; 



--Nuevos clientes con mucho gasto
DROP VIEW IF EXISTS nuevos_gastadores;
CREATE VIEW nuevos_gastadores as
SELECT c.IDCLIENTE, p.PAIS FROM CLIENTES c, RFM r, PAISES p WHERE c.IDCLIENTE=r.cliente AND p.IDPAIS=c.IDPAIS AND rfm_recency=1 AND rfm_frequency=4 AND rfm_monetary IN (1,2);


SELECT * FROM nuevos_gastadores;
SELECT PAIS, COUNT(*) FROM nuevos_gastadores GROUP BY 1 ORDER BY 2 DESC; 
 


--Muy gastadores con riesgo de abandono
DROP VIEW IF EXISTS gastadores_riesgoabandono;
CREATE VIEW gastadores_riesgoabandono as
SELECT c.IDCLIENTE, p.PAIS FROM CLIENTES c, RFM r, PAISES p WHERE c.IDCLIENTE=r.cliente AND p.IDPAIS=c.IDPAIS AND rfm_recency=4 AND rfm_frequency<3 AND rfm_monetary <3;


SELECT * FROM gastadores_riesgoabandono;
SELECT PAIS, COUNT(*) FROM gastadores_riesgoabandono GROUP BY 1 ORDER BY 2 DESC; 
```


## AWS CLI

Para poder acceder a los recursos de AWS, necesitamos preparar nuestro entorno de trabajo.

Recuerda que necesitas copiar las credenciales de acceso en `~/.aws/credentials` tal como vimos en XXXXX.


## AWS desde Python

Para acceder a AWS, Amazon ofrece la librería Boto3. Para poder utilizarla, la instalaremos mediante

``` console
pip install boto3
```

!!! warning "Cloud 9"
    Aunque hayamos decidido utilizar Cloud9, también debemos instalar la librería boto3.

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

### Cargando datos en DynamoDB

Vamos a cargar un listado de películas en *DynamoDB*. El primer paso es elegir las claves de particionado y ordenación. El archivo [datosPeliculas.json](../recursos/dynamodb/datosPeliculas.json) contiene el siguiente contenido:

``` json
[
    {
        "year": 2013,
        "title": "Rush",
        "info": {
            "directors": ["Ron Howard"],
            "release_date": "2013-09-02T00:00:00Z",
            "rating": 8.3,
            "genres": [
                "Action",
                "Biography",
                "Drama",
                "Sport"
            ],
            "image_url": "http://ia.media-imdb.com/images/M/MV5BMTQyMDE0MTY0OV5BMl5BanBnXkFtZTcwMjI2OTI0OQ@@._V1_SX400_.jpg",
            "plot": "A re-creation of the merciless 1970s rivalry between Formula One rivals James Hunt and Niki Lauda.",
            "rank": 2,
            "running_time_secs": 7380,
            "actors": [
                "Daniel Bruhl",
                "Chris Hemsworth",
                "Olivia Wilde"
            ]
        }
    },
]
```

Como los años de las películas permiten particionar de manera más o menos equilibrada los datos, en la mejor candidata para clave de particionado. Como sí que habrá varias películas en el mismo año, elegimos el título como clave de ordenación, provocando que los documentos tengan una clave compuesta.

Así pues, vamos a nombrar nuestra tabla como `SeveroPeliculas` y ponemos como clave de partición el atributo `year` de tipo númerico, y como clave de ordenación `title` de tipo cadena.

<figure style="align: center;">
    <img src="../imagenes/etl/05ddCrearTabla.png">
    <figcaption>Creación de la tabla SeveroPeliculas</figcaption>
</figure>

Una vez creada la tabla, vamos a ver como podemos cargar los datos. Haciendo uso de la librería *boto3* vamos a crear el archivo [cargarDatosPeliculas.py](../recursos/dynamodb/cargarDatosPeliculas.py):

``` python title="cargarDatosPeliculas.py"
import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # (1)

tabla = dynamodb.Table('SeveroPeliculas')

with open("datosPeliculas.json") as ficheroJSON:
    peliculas = json.load(ficheroJSON, parse_float=decimal.Decimal)
    for pelicula in peliculas:
        year = int(movie['year'])
        title = movie['title']
        info = movie['info']

        print("Añadida película:", year, title)

        tabla.put_item(
            Item={
                'year': year,
                'title': title,
                'info': info,
            }
        )
```

1. Nos conectamos a la región e indicamos que vamos a utilizar el servicio de DynamoDB

Si lo ejecutamos desde nuestro ordenador, nos aparecerá por la consola cada una de las películas insertadas.


!!! caution "Float y boto3"
    AWS SDK for Python, specifically aimed towards DynamoDB is that Float types are not supported and that you should use Decimal types instead.

Ejemplo cloud9 y DynamoDB con Python
https://aws-dojo.com/excercises/excercise29/


Cargar datos de CSV y cargar en DynamoDB
Consultar de RDS e insertar en DDB (Sqoop?)

## Funciones Lambda

## Python

Faker, libreria para crear datos falsos

https://learning.oreilly.com/library/view/data-engineering-with/9781839214189/B15739_03_ePub_AM.xhtml#_idParaDest-40

## Referencias

* Python, Boto3, and AWS S3: Demystified: <https://realpython.com/python-boto3-aws-s3/>
* [DynamoDB mediante Python](https://highlandsolutions.com/blog/hands-on-examples-for-working-with-dynamodb-boto3-and-python)
