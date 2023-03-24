import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from decimal import Decimal

def new_recovery(identifier, game_state, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    table = dynamodb.Table('Recovery')
    table.put_item(
        Item = {
            'recovery' : 1,
            'identifier' : identifier,
            'game_state' : game_state
        }
    )

# def new_recovery(identifier, player1_score, player2_score, player1_pos, player2_pos, player1_bullet_x,
#                  player1_bullet_y, player2_bullet_x, player2_bullet_y, enemy_x, enemy_y, enemy_xvel,
#                  enemy_yvel, enemy_bullet_x, enemy_bullet_y, dynamodb=None):
#     if not dynamodb:
#         dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
#     table = dynamodb.Table('Recovery')
#     table.put_item(
#         Item = {
#             'recovery' : 1,
#             'identifier' : identifier,
#             'player1_score' : player1_score,
#             'player2_score' : player2_score,
#             'player1_pos' : player1_pos,
#             'player2_pos' : player2_pos,
#             'player1_bullet_x' : player1_bullet_x,
#             'player1_bullet_y' : player1_bullet_y,
#             'player2_bullet_x' : player2_bullet_x,
#             'player2_bullet_y' : player2_bullet_y,
#             'enemy_x' : enemy_x,
#             'enemy_y' : enemy_y,
#             'enemy_xvel' : enemy_xvel,
#             'enemy_yvel' : enemy_yvel,
#             'enemy_bullet_x' : enemy_bullet_x,
#             'enemy_bullet_y' : enemy_bullet_y
#         }
#     )

# Gets a recovery save with a given identifier from the database.
def get_recovery(identifier, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    table = dynamodb.Table('Recovery')
    item = None
    try:
        response = table.get_item(Key = {'recovery' : 1, 'identifier' : identifier})
        item = response['Item']
    except:
        pass
    return item