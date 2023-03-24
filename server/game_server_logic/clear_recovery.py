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

    # Wait until the Recovery table no longer exists.
    while True:
        table_names = [table.name for table in dynamodb.tables.all()]
        if 'Recovery' not in table_names:
            break

    create_recovery()
    print('Table re-initialised.')


if __name__ == '__main__':
    clear_recovery()