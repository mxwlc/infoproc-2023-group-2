# This script tests the Leaderboard and Recovery tables in DynamoDB.

from clear_leaderboard import *
from create_leaderboard import *
from leaderboard_functions import *

from clear_recovery import *
from create_recovery import *
from recovery_functions import *

from decimal_encoder import *

import json
import time

def test_leaderboard():

    print('Testing leaderboard.')
    
    # Reset leaderboard to start
    clear_leaderboard()
    create_leaderboard()

    time.sleep(5) # Give DynamoDB time to create table

    # Test fetching leaderboard
    leaderboard = get_leaderboard()
    print('Leadboard after reset: ' + str(leaderboard))

    if leaderboard != []:
        print('Test failed.')
        return

    # Test adding new players
    update_leaderboard('one', 10)
    update_leaderboard('two', 20)
    update_leaderboard('three', 30)

    # Test updating leaderboard
    update_leaderboard('one', 20) # New highscore
    update_leaderboard('three', 25) # No change

    leaderboard = get_leaderboard()
    print('Leaderboard after update: ' + str(leaderboard))

    for entry in leaderboard:
        if entry['name'] == 'one' and entry['score'] != 20:
            print('Test failed.')
            return
        elif entry['name'] == 'two' and entry['score'] != 20:
            print('Test failed.')
            return
        elif entry['name'] == 'three' and entry['score'] != 30:
            print('Test failed.')
            return

    print('Test passed.')


def test_recovery():

    print('Testing recovery saves.')

    # Reset recovery saves to start
    clear_recovery()
    create_recovery()

    time.sleep(5) # Give DynamoDB time to create table

    # Create new game state
    game_state = {} # Create a dictionary with all necessary game data to be serialised to JSON.
    game_state['player_name'] = ['one', 'two']
    game_state['player_score'] = [10, 20]
    game_state['player_lives'] = [1, 2]
    game_state['player_x'] = [100, 200]
    game_state['player_bullet_x'] = [0, 100]
    game_state['player_bullet_y'] = [0, 200]
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    for i in range(44):
        enemyX.append(i)
        enemyY.append(43 - i)
        enemyX_change.append(i * 2)
        enemyY_change.append((43 - i) * 2)
    game_state['enemy_x'] = enemyX
    game_state['enemy_y'] = enemyY
    game_state['enemy_xvel'] = enemyX_change
    game_state['enemy_yvel'] = enemyY_change
    game_state['enemy_bullet_x'] = 50
    game_state['enemy_bullet_y'] = 500
    game_state['enemy_vel'] = 5
    game_state['bunker_health'] = [1, 2, 3, 5]
    print('Original recovery save: ' + str(game_state))

    # Add new recovery save
    new_recovery('alpha', game_state)

    # Fetch recovery save
    recovered_state = get_recovery('alpha')['game_state']
    print('Fetched recovery save: ' + str(recovered_state))

    if game_state == recovered_state:
        print('Test passed.')
    else:
        print('Test failed.')

if __name__ == '__main__':
    test_leaderboard()
    test_recovery()