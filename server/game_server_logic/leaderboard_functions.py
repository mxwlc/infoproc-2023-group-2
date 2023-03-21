import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from decimal import Decimal

# Adds a new player and their score to the leaderboard.
def new_player(name, score, dynamodb):
    table = dynamodb.Table('Leaderboard')
    table.put_item(
        Item = {
            'leaderboard' : 1,
            'name' : name,
            'score' : score
        }
    )    

# Gets the entry associated with a player's name from the leaderboard.
# If no entry exists for this player, return None.
def get_player(name, dynamodb):
    table = dynamodb.Table('Leaderboard')
    item = None
    try:
        response = table.get_item(Key = {'leaderboard' : 1, 'name' : name})
        item = response['Item']
    except:
        pass
    return item

# Updates the score of an existing player if their new score is higher than their old score.
# The old score must have been fetched previously and is provided in repsonse.
def update_score(name, score, response, dynamodb):
    if score > response['score']:
        table = dynamodb.Table('Leaderboard')
        table.update_item(
            Key = {
                'leaderboard' : 1,
                'name' : name
            },
            UpdateExpression = 'set score=:s',
            ExpressionAttributeValues = {
                ':s' : Decimal(score)
            },
            ReturnValues = 'UPDATED_NEW'
        )
    # Do nothing if the old score was higher.

# Update leaderboard with new score. 3 cases to consider:
# 1. Player does not exist in leaderboard yet, so add them.
# 2. Player does exist in leaderboard, but their old score was higher.
# 3. Player does exist in leaderboard, and their new score is higher.
def update_leaderboard(name, score):
    print('name: ' + name + ' score: ' + str(score))
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    response = get_player(name, dynamodb)
    if response == None:
        new_player(name, score, dynamodb)
    else:
        update_score(name, score, response, dynamodb)

def get_leaderboard():
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    
    table = dynamodb.Table('Leaderboard')
    response = table.query(
        KeyConditionExpression = Key('leaderboard').eq(1) # The default leaderboard has ID 1.
    )
    return response['Items']