# Run this script to clear the leaderboard.
# It works by just deleting the table and then re-initialising it.

import boto3
from create_leaderboard import *
import time

def clear_leaderboard():

    try:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
        table = dynamodb.Table('Leaderboard')
        table.delete()
        print('Table deleted.')
    except:
        print('No table to delete.')
        return

    # Wait until the Leaderboard table no longer exists.
    while True:
        table_names = [table.name for table in dynamodb.tables.all()]
        if 'Leaderboard' not in table_names:
            break

    create_leaderboard()
    print('Table re-initialised.')


if __name__ == '__main__':
    clear_leaderboard()