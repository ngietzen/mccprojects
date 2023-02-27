#########################################################
# main.py
# ITCC 2100 - AWS DynamoDB Utility Functions
# By Nikolaus Gietzen
# 02/02/2023
#########################################################

# import our libraries
import logging
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from botocore.exceptions import WaiterError

# test data for the put functions
same_primary_list = [
    {
        'item_name': 'Scrabble',
        'item_price': '9.99'
    },
    {
        'item_name': 'Scrabble',
        'item_price': '12.99'
    },
    {
        'item_name': 'Scrabble',
        'item_price': '19.99'
    },
]

same_secondary_list = [
    {
        'item_name': 'Monopoly',
        'item_price': '19.99'
    },
    {
        'item_name': 'Life',
        'item_price': '12.99'
    },
    {
        'item_name': 'Chess',
        'item_price': '19.99'
    },
]


# this is the main function
def main():
    # setup logging
    logging.basicConfig(filename='s3.log', level=logging.DEBUG)

    # while the user hasn't quit, show our menu and ask for a function
    selection = ''

    while selection != 'q':
        show_menu()
        selection = input('Please enter a function to run 1-7, or q to quit: ')

        # if 1 create table
        if selection == '1':
            table_name = input('Please enter the name of the table to create: ')
            primary_key = input('Please enter the primary key: ')
            secondary_key = input('Please enter the secondary key: ')
            if create_table(table_name, primary_key, secondary_key):
                print('Created table: ' + table_name)
                pause()

        # if 2 wait for a table
        elif selection == '2':
            table_name = input('Please enter the name of the table to wait for: ')
            if wait_for_table(table_name):
                print('The table ' + table_name + ' exists and is active!')
                pause()
            else:
                print('The table ' + table_name + ' still does not exist!')
                pause()

        # if 3 put the 3 test items with the same primary key
        if selection == '3':
            table_name = input('Please enter the name of the table to add the test items to: ')
            primary_key = input('Please enter the primary key: ')
            secondary_key = input('Please enter the secondary key: ')
            if put_same_primary(table_name, primary_key, secondary_key):
                print("Items put successfully!")
                pause()

        # if 4 put the 3 test items with the same secondary key
        if selection == '4':
            table_name = input('Please enter the name of the table to add the test items to: ')
            primary_key = input('Please enter the primary key: ')
            secondary_key = input('Please enter the secondary key: ')
            if put_same_secondary(table_name, primary_key, secondary_key):
                print("Items put successfully!")
                pause()

        # if 5 get one item from the database
        if selection == '5':
            table_name = input('Please enter the name of the table to get the item from: ')
            primary_key = input('Please enter the primary key: ')
            pk_value = input('Please enter the pk value: ')
            secondary_key = input('Please enter the secondary key: ')
            sk_value = input('Please enter the sk value: ')
            if get_item(table_name, primary_key, pk_value, secondary_key, sk_value):
                pause()

        # if 6 delete one item from the database
        if selection == '6':
            table_name = input('Please enter the name of the table to delete the item from: ')
            primary_key = input('Please enter the primary key: ')
            pk_value = input('Please enter the pk value: ')
            secondary_key = input('Please enter the secondary key: ')
            sk_value = input('Please enter the sk value: ')
            if delete_item(table_name, primary_key, pk_value, secondary_key, sk_value):
                print("Item " + pk_value + " : " + sk_value + " deleted successfully!")
                pause()

        # if 7 delete table
        if selection == '7':
            table_name = input('Please enter the name of the table to delete: ')
            if delete_table(table_name):
                print('Deleted table: ' + table_name)
                pause()

        # if 8 query a table
        if selection == '8':
            table_name = input('Please enter the name of the table to query: ')
            key = input('Please enter the key to query: ')
            value = input('Please enter the value to query: ')
            if query_item(table_name, key, value):
                pause()


# show_menu prints the menu display
def show_menu():
    print('************************************')
    print('*   Nik\'s AWS DynamoDB Utilities   *')
    print('************************************')
    print('1. Create A Table')
    print('2. Wait For A Table')
    print('3. Put 3 Items (Same Primary Key)')
    print('4. Put 3 Items (Same Secondary Key)')
    print('5. Get An Item')
    print('6. Delete An Item')
    print('7. Delete A Table')
    print('8. BONUS: Query')


# pause just lets the user press any key to continue
def pause():
    input('Press any key to continue...')


# create_table creates a DynamoDB table
def create_table(table_name, primary_key, secondary_key):
    try:
        db_client = boto3.client('dynamodb')
        db_client.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': primary_key,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': secondary_key,
                    'AttributeType': 'S'
                },
            ],
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': primary_key,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': secondary_key,
                    'KeyType': 'RANGE'
                },
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'string',
                    'KeySchema': [
                        {
                            'AttributeName': secondary_key,
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': primary_key,
                            'KeyType': 'RANGE'
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
            ],
            BillingMode='PROVISIONED',
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except ClientError as e:
        logging.error(e)
        return False

    return True


# wait_for_table waits for a table to exist for 5 seconds 5 times or returns that it still doesn't exist
def wait_for_table(table_name):
    try:
        db_client = boto3.client('dynamodb')
        waiter = db_client.get_waiter('table_exists')
        try:
            waiter.wait(
                TableName=table_name,
                WaiterConfig={
                    'Delay': 5,
                    'MaxAttempts': 5
                }
            )
        except WaiterError as e:
            logging.error(e)
            return False
    except ClientError as e:
        logging.error(e)
        return False

    return True


# put_same_primary puts the 3 test items with the same primary key
def put_same_primary(table_name, primary_key, secondary_key):
    try:
        db_resource = boto3.resource('dynamodb')
        table = db_resource.Table(table_name)

        with table.batch_writer() as batch:
            for test_item in same_primary_list:
                item = {
                    primary_key: test_item['item_name'],
                    secondary_key: test_item['item_price']
                }
                print("Putting " + item[primary_key] + " : " + item[secondary_key])
                batch.put_item(Item=item)

    except ClientError as e:
        logging.error(e)
        return False

    return True


# put_same_secondary puts the 3 test items with the same secondary key
def put_same_secondary(table_name, primary_key, secondary_key):
    try:
        db_resource = boto3.resource('dynamodb')
        table = db_resource.Table(table_name)

        with table.batch_writer() as batch:
            for test_item in same_secondary_list:
                item = {
                    primary_key: test_item['item_name'],
                    secondary_key: test_item['item_price']
                }
                print("Putting " + item[primary_key] + " : " + item[secondary_key])
                batch.put_item(Item=item)

    except ClientError as e:
        logging.error(e)
        return False

    return True


# get_item gets one item
def get_item(table_name, primary_key, pk_value, secondary_key, sk_value):
    try:
        db_client = boto3.client('dynamodb')

        response = db_client.get_item(TableName=table_name,
                                      Key={
                                          primary_key: {"S": pk_value},
                                          secondary_key: {"S": sk_value}
                                      }
                                      )
        data = response['Item']
        print(data)

    except ClientError as e:
        logging.error(e)
        return False

    return True


# delete_item deletes one item
def delete_item(table_name, primary_key, pk_value, secondary_key, sk_value):
    try:
        db_client = boto3.client('dynamodb')

        db_client.delete_item(TableName=table_name,
                              Key={
                                  primary_key: {"S": pk_value},
                                  secondary_key: {"S": sk_value}
                              }
                              )

    except ClientError as e:
        logging.error(e)
        return False

    return True


# delete_table deletes a table
def delete_table(table_name):
    try:
        db_client = boto3.client('dynamodb')
        db_client.delete_table(TableName=table_name)

    except ClientError as e:
        logging.error(e)
        return False

    return True


# query_item queries a table index for a key that matches value
def query_item(table_name, key, value):
    try:
        db = boto3.resource('dynamodb')
        table = db.Table(table_name)
        response = table.query(
            IndexName='string',
            KeyConditionExpression=Key(key).eq(value)
        )

        for item in response['Items']:
            print(item)

    except ClientError as e:
        logging.error(e)
        return False

    return True


if __name__ == '__main__':
    main()
