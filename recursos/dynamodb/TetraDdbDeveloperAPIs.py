import boto3
import pprint
import json
import decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')

table = dynamodb.Table('TetraMovies')

#############################################################
# INSERT an Item into "TetraMovies" Table
#############################################################

# title = "Interstellar"
# year = 2015
#
# response = table.put_item(
#    Item={
#         'year': year,
#         'title': title,
#         'info': {
#             'plot':"Inter Galactic Travel by a man to save his family",
#             'rating': decimal.Decimal(9.5)
#         }
#     }
# )
#
# print("PutItem succeeded:")
# pprint.pprint(response)


#############################################################
# READ a single Item from "TetraMovies" Table
#############################################################

# title = "Interstellar"
# year = 2015
#
# try:
#     response = table.get_item(
#         Key={
#             'year': year,
#             'title': title
#         },
#         ProjectionExpression="title,info.rating"
#     )
# except ClientError as e:
#     print(e.response['Error']['Message'])
# else:
#     item = response['Item']
#     print("GetItem succeeded:")
#     pprint.pprint(response['Item'])

#############################################################
# QUERY to get a range of item from "TetraMovies" table
#############################################################

# print("Movies from 1985")
#
# response = table.query(
#     KeyConditionExpression=Key('year').eq(1985),
#     ProjectionExpression="title,info.actors[1],info.image_url"
# )
#
# pprint.pprint(response['Items'])

# for i in response['Items']:
#     print(i['year'], ":", i['title'])


#############################################################
# QUERY to get a single item from "TetraMovies" table
#############################################################

# print("Movies from 1992 - titles A-L, with genres and lead actor")

# response = table.query(
#     ProjectionExpression="#yr, title, info.genres, info.actors[0]",
#     ExpressionAttributeNames={ "#yr": "year" }, # Expression Attribute Names for Projection Expression only.
#     # KeyConditionExpression=Key('year').eq(1992) & Key('title').between('A', 'L')
#     KeyConditionExpression=Key('year').eq(1992) & Key('title').eq('Home Alone 2: Lost in New York')
# )
#
# pprint.pprint(response['Items'])
#
#
# for i in response[u'Items']:
#     pprint.pprint(i)
#     print()

#############################################################
# SCAN the entire table
#############################################################
#
year_range = Key('year').between(1950, 1959)
project = "#yr, title, info.rating"
# Expression Attribute Names for Projection Expression only.
expr = { "#yr": "year", }


response = table.scan(
    FilterExpression=Key('year').between(1950, 1959),
    ProjectionExpression=project,
    ExpressionAttributeNames=expr
    )

pprint.pprint(response['Items'])
# # for i in response['Items']:
# #     pprint.pprint(i)

# while 'LastEvaluatedKey' in response:
#     response = table.scan(
#         ProjectionExpression=project,
#         FilterExpression=year_range,
#         ExpressionAttributeNames= ean,
#         ExclusiveStartKey=response['LastEvaluatedKey']
#         )
#
#     for i in response['Items']:
#         pprint.pprint(i)

