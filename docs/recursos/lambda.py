def lambda_handler(event, context):
    """ Suma dos números """

    a = event["a"]
    b = event["b"]

    suma = a+b
    print(f"La suma de a:{a} y b:{b} es {suma}")

    return {
      "total" : suma
    }
