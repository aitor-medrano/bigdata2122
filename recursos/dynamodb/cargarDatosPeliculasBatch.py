import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla = dynamodb.Table('SeveroPeliculas3')

with open("datosPeliculas.json") as ficheroJSON:
    peliculas = json.load(ficheroJSON, parse_float=decimal.Decimal)

with tabla.batch_writer() as batch:
    for pelicula in peliculas:
        contenido = {
            'year': pelicula['year'],
            'title': pelicula['title'],
            'info': pelicula['info'],
        }
        batch.put_item(Item=contenido)
# Al terminar el bucle, es cuando se sale del with y envía los datos batch


