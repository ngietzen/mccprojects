##################################
# lambdaDemo.py
# Based on login.py from class module
# ITCC2100
# Nikolaus Gietzen
# 02/26/2023
##################################

import logging
import boto3
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENDPOINT = "arn:aws:dynamodb:us-east-1:546288284345:table/inventory"
TABLE_NAME = "inventory"


###############################################################################
# Put a DynamoDb Item.
###############################################################################
def log_in_out(product_id, product_type, login):

    time_stamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    try:
        db_client = boto3.client("dynamodb")
        db_client.put_item(
            Item={
                "productID": {
                    "S": product_id,
                },
                "productType": {
                    "S": product_type,
                },
                "login": {
                    "BOOL": login,
                },
                "timestamp": {
                    "S": time_stamp,
                },
            },
            ReturnConsumedCapacity="TOTAL",
            TableName=TABLE_NAME,
        )
        return True
    except Exception as e:
        logging.error(e)
        return False


###############################################################################
# Entrance to the lambda function.
###############################################################################
def lambda_handler(event, context):

    # This is new info....

    logger.info(event)
    logger.info(context)

    product_id = "rrgame123456"
    product_type = "Age of Steam"
    if log_in_out(product_id, product_type, True):
        return {"statusCode": 200, "body": "Successfully logged in!"}

    return {"statusCode": 400, "body": "Error logging in!"}


# # For debugging only
# if __name__ == "__main__":
#     print(lambda_handler(None, None))
