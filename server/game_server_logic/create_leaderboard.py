# Run this script to set up the leaderboard.
# It only needs to be run once on the EC2 instance. However, it can be run multiple
# times with no negative effect if that is more convenient.

# The leaderboard has only one partition, which is leaderboard=1.
# In this partition the sort key is the name of the player, and the value is their score.

import boto3

def create_leaderboard():

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')

    table = dynamodb.create_table(
        TableName = 'Leaderboard',
        KeySchema = [
            {
                'AttributeName' : 'leaderboard',
                'KeyType' : 'HASH' # Partition key
            },
            {
                'AttributeName' : 'name',
                'KeyType' : 'RANGE' # Sort key
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName' : 'leaderboard',
                'AttributeType' : 'N'
            },
            {
                'AttributeName' : 'name',
                'AttributeType' : 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

if __name__ == '__main__':
    create_leaderboard()