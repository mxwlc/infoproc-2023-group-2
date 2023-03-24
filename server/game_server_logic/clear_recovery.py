# Run this script to clear the recovery database.
# It works by just deleting the table and then re-initialising it.

import boto3
from create_recovery import *
import time

def clear_recovery():

    try:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
        table = dynamodb.Table('Recovery')
        table.delete()
        print('Table deleted.')
    except:
        print('No table to delete.')
        return

    time.sleep(5)
    # Apparently, it takes time for dynamodb to recognise that a table has been deleted.
    # Trying to recreate the leaderboard immediately throws exception (dynamodb thinks the table still exists).

    try:
        create_recovery()
        print('Table re-initialised.')
    except:
        print('Unable to re-initialise table.')

if __name__ == '__main__':
    clear_recovery()