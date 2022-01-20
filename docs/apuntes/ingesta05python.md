# Python y AWS

<p align="right"><small>Tiempo estimado de lectura: XX minutos [21 de Febrero]</small></p>

En esta sesión vamos a ver como acceder a los diversos servicios de AWS relacionados con el Big Data, y mediante diferentes casos de uso, crear diferentes flujos de datos.

Para los siguientes casos de uso, realizaremos los 5 primeros desde nuestro sistema local y el caso final haciendo uso de Cloud 9.

Para autenticarnos en AWS desde nuestro sistema local, recuerda que necesitas copiar las credenciales de acceso en `~/.aws/credentials` o mediante las [variables de entorno](nube02aws.md#variablesEntorno).

## boto3

Para acceder a AWS desde Python, Amazon ofrece el [SDK Boto3](https://aws.amazon.com/es/sdk-for-python/). Para poder utilizarlo, la instalaremos mediante

``` console
pip install boto3
```

Podéis consultar toda la información relativa a Boto3 en su documentación oficial en
<https://boto3.amazonaws.com/v1/documentation/api/latest/index.html>

Existen dos posibilidades para acceder a AWS mediante *Boto3*:

* Recursos: representan un interfaz orientado a objetos de AWS. Más información en https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html
* Clientes: ofrecen un interfaz de bajo nivel que se mapena con el API de cada servicio. Los clientes se generan a partir de la definición JSON del servicio. Más información en <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/clients.html>

https://www.learnaws.org/2021/02/24/boto3-resource-client/

## Caso de uso 1: Leer datos desde S3

http://ramondario.com/processing-nyc-taxi-data-part-1-downloading.html


## Caso de uso 2: Cargar datos en DynamoDB

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

## Creando datos falsos con Faker

Si necesitamos escribir muchos datos, es muy útil emplear una librería como [Faker](https://faker.readthedocs.io/en/master/) para generar los datos.

Primero hemos de instalarla mediante pip:

``` bash
pip3 install faker
```

Vamos a realizar un ejemplo para mostrar algunos datos aleatorios y comprobar su funcionamiento:

=== "Código"

    ``` python title="holaFaker.py"
    from faker import Faker

    fake = Faker()
    fake = Faker('es_ES')   # cambiamos el locale a español

    print("Nombre:", fake.name())
    print("Dirección:", fake.address())
    print("Nombre de hombre:", fake.first_name_male())
    print("Número de teléfono:", fake.phone_number())
    print("Color:", fake.color_name())
    print("Fecha:", fake.date())
    print("Email:", fake.email())
    print("Frase de 10 palabras", fake.sentence(nb_words=10))

    ```

=== "Resultado"

    ``` output
    Nombre: Dani Pla Chico
    Dirección: Cuesta de Emiliano Milla 66
    Albacete, 83227
    Nombre de hombre: Matías
    Número de teléfono: +34 818 779 827
    Color: Salmón oscuro
    Fecha: 1984-09-29
    Email: btome@example.net
    Frase de 10 palabras Perferendis saepe consequatur saepe sapiente est impedit eaque omnis temporibus excepturi repellat ducimus.
    ```

Los diferentes grupos de datos que genera se agrupan en *Providers*: de dirección, fechas, relacionados con internet, bancarios, códigos de barra, isbn, etc... Se recomienda consultar la documentación en <https://faker.readthedocs.io/en/master/providers.html>.

!!! caution "Locale ES"
    Al trabajar con el idioma en español, puede que algunos métodos no funcionen (más que no funcionar, posiblemente tengan otro nombre). Es recomendable comprobar las opciones disponibles en <https://faker.readthedocs.io/en/master/locales/es_ES.html>

### Generando CSV

Vamos a generar un CSV con datos de 1000 personas. Primero creamos un lista con los encabezados y los escribimos en el fichero, para posteriormente, línea a línea, generar los datos de cada persona:

=== "Código"

    ``` python title="generaCSV.py"
    from faker import Faker
    import csv

    output = open('datosFaker.csv', 'w')

    fake = Faker('es_ES')   # cambiamos el locale a español
    header = ['nombre', 'edad', 'calle', 'ciudad',
            'provincia', 'cp', 'longitud', 'latitud']
    mywriter = csv.writer(output)
    mywriter.writerow(header)

    for r in range(1000):
        mywriter.writerow([fake.name(),
                        fake.random_int(min=18, max=80, step=1),
                        fake.street_address(),
                        fake.city(),
                        fake.state(),
                        fake.postcode(),
                        fake.longitude(),
                        fake.latitude()])
    output.close()
    ```

=== "Resultado"

    ``` csv title="datosFaker.csv"
    nombre,edad,calle,ciudad,provincia,cp,longitud,latitud
    Jenaro Verdú Suarez,26,Urbanización Mohamed Vallés 122,Sevilla,Guipúzcoa,73198,2.657719,-69.679293
    Eugenio Calzada Revilla,57,Camino Vanesa Amor 36 Piso 9 ,Huesca,Álava,75590,34.041399,-52.924628
    Flavio del Lumbreras,76,Avenida de Beatriz Amaya 92,Ciudad,Murcia,86420,58.248903,-17.924926
    ```

### Generando JSON

Y a continuación repetimos el mismo ejemplo, pero ahora generando un documento JSON. La principal diferencia es que primero vamos a rellenar un diccionario con toda la información, y luego persistimos el diccionario:

=== "Código"

    ``` python title="generaJSON.py"
    from faker import Faker
    import json

    fake = Faker('es_ES')   # cambiamos el locale a español

    # Preparamos los datos
    datos = {}
    datos['registros'] = []

    for x in range(1000):
        persona = {"datos": fake.name(),
                "edad": fake.random_int(min=18, max=80, step=1),
                "calle": fake.street_address(),
                "ciudad": fake.city(),
                "provincia": fake.state(),
                "cp": fake.postcode(),
                "longitud": float(fake.longitude()),
                "latitud": float(fake.latitude())}
        datos['registros'].append(persona)

    # Los metemos en el fichero
    output = open('datosFaker.json', 'w')
    json.dump(datos, output)
    ```

=== "Resultado"

    ``` json title="datosFaker.json"
    {
        "registros": [
            {
                "datos": "Merche Moreno Roman",
                "edad": 51,
                "calle": "Paseo Amelia Folch 967",
                "ciudad": "Segovia",
                "provincia": "M\u00e1laga",
                "cp": "71721",
                "longitud": 84.603801,
                "latitud": 58.941349
            },
            {
                "datos": "Miguel Abascal Sanz",
                "edad": 21,
    ```



## Caso de uso 3 - Consultar datos en DynamoDB

## Caso de uso 4 - De S3 a DynamoDB

En este caso, vamos a coger datos de películas de un dataset público disponible en https://www.kaggle.com/rounakbanik/the-movies-dataset?select=movies_metadata.csv

Una vez descargado movies_metadata.csv, vamos a cargar la información en S3 dentro del bucket .

A partir de ahí, veamos como vamos a recuperar el archivo, parsear el fichero CSV, e insertar los datos de las películas en DynamoDB.



## Caso de uso 5 - De RDS a DynamoDB

Vamos a utilizar la instancia de base de datos iabd que tenemos en RDS con la base de datos `retail_db`.

Para acceder a la base de datos desde Python necesitamos instalar la librería correspondiente:

``` bash
pip3 install mariadb
pip3 install mysql-connector-python
```

<https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/>

Todo el código a continuacion se basa en MariaDB como sistema gestor de base de datos. Si queremos conectarnos, debemos indicar los datos de conexion:

``` python
import mariadb
import sys

try:
    conn = mariadb.connect(
        user="admin",
        password="adminadmin",
        host="iabd.cllw9xnmy9av.us-east-1.rds.amazonaws.com",
        port=3306,
        database="retail_db"
    )
except mariadb.Error as e:
    print(f"Error conectando a MariaD: {e}")
    sys.exit(1)

# Obtenemos el cursor
cur = conn.cursor()
```

Una vez nos hemos conectado y tenemos abierto un cursor, ya podemos hacer consultas y recuperar datos.

Por ejemplo, para recuperar toda la información de los clientes almacenada en la tabla `customers`:

``` python
sql = "select * from customers"
cur.execute(sql)
resultado = cur.fetchAll()

# Cerramos el cursor y la conexión
cur.close()
conn.close()

# Mostramos el resultado
print(resultado)
```

Vamos a realizar otro ejemplo sencillo que recupere el nombre, apellido y email de los clientes 

## Caso de uso 6 - AWS Lambda

En este caso de uso, vamos a realizar los casos de uso 4 y 5 mediante AWS Lambda, de manera que accedamos a S3, RDS y DynamoDB mediante funciones serverless.

Para este ejercicio, vamos a trabajar con Cloud9 el cual facilita el trabajo con AWS Lambda. 

Ejemplo cloud9 y DynamoDB con Python
https://aws-dojo.com/excercises/excercise29/


## Actividades

## Referencias

* Python, Boto3, and AWS S3: Demystified: <https://realpython.com/python-boto3-aws-s3/>
* [DynamoDB mediante Python](https://highlandsolutions.com/blog/hands-on-examples-for-working-with-dynamodb-boto3-and-python)
