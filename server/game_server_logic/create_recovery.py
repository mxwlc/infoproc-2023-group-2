# Run this script to set up the game recovery DB.
# There is only one partition, which is recovery = 1.
# In this partition the sort key is an identifier associated with the game state, which is stored by the server.

import boto3

def create_recovery():

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')

    table = dynamodb.create_table(
        TableName = 'Recovery',
        KeySchema = [
            {
                'AttributeName' : 'recovery',
                'KeyType' : 'HASH' # Partition key
            },
            {
                'AttributeName' : 'identifier',
                'KeyType' : 'RANGE' # Sort key
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName' : 'recovery',
                'AttributeType' : 'N'
            },
            {
                'AttributeName' : 'identifier',
                'AttributeType' : 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    # Wait until the Recovery table has been created.
    # while True:
    #     try:
    #         if table.table_status == 'ACTIVE':
    #             break
    #     except:
    #         pass


if __name__ == '__main__':
    create_recovery()