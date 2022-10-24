from os import stat_result
import click
import random
import copy
import numpy as np
import keyboard
import json

print('\nWelcom to 2048!\n\nTo merge left - press \'a\' or  < ,\n   merge up -         \'w\' or  ^ ,\n   merge right -      \'d\' or  > ,\n   merge down -       \'s\' or  v .\n\nTo quit the game - press \'Esc\'\nTo restart the game - press \'0\'')

def randomize(state):
    coordinates = [(x,y) for x in range(state['rows']) for y in range(state['columns'])]
    x, y = random.choice(coordinates)
    while not state['matrix'][x][y] == 0:
        x, y = random.choice(coordinates)
    state['matrix'][x][y] = random.choice([2, 4])
    
    return state
    
def new_board(state):
    for i in range(state['rows']):
        state['matrix'].append([0]*state['columns']) 
    for j in range (2):
        randomize(state)   
    return state

def show_state(state):
    if state['w_cell'] < len(str(state['maxium_nuber'])):
        state['w_cell'] = len(str(state['maxium_nuber']))
    hor_line = ('+' + '-' *state['w_cell']) * state['columns'] + '+\n'
    line_with_gaps = ('|' + '%s') * state['columns'] + '|\n'
    table = (hor_line + line_with_gaps * state['h_cell']) * state['rows']  + hor_line
    #print('\n' * 50)
    board_for_print = []
    row = []
    for i in state['matrix']:
        for j in i:
            if j == 0:
                j = ' '
            row.append(j)
        board_for_print.append(row)
        row = []
            
    #print('\n' * 5)
    print(table % tuple((str(cell).center(state['w_cell'], ' ') for row in board_for_print for cell in row)))
    print(f"Your score: {state['score']}\nBest score: {state['best_score']}")
    
def remove_zeros(state):
    for row in state['matrix']:
        i = 0
        while i < len(row):
            if row[i] == 0:
                row.pop(i)
            else:
                i += 1
    return state

def agregation(state):
    for row in state['matrix']:
        for i in range(len(row)-1):
            if row[i] == row[i+1]:
                row [i] *= 2
                row[i+1] = 0
                state['score'] += row [i]
                
                if state['maxium_nuber'] < row [i]:
                    state['maxium_nuber'] = row [i]
    return state

def add_zeros(state, before):
    if before % 2 != 0:
        columns = state['rows']
    else:
        columns = state['columns']
    for row in state['matrix']:
        dif = columns - len(row)
        for i in range(dif):
            row.append(0)
    return(state)

def rotate_matrix(state):
    rot_data = copy.deepcopy(state['matrix'])
    m = len(rot_data)
    n = len(rot_data[0])
    rev_data = rot_data[::-1]
    rot_data = [[rev_data[j][i] for j in range(m)] for i in range(n)]
    state['matrix'] = rot_data
    return state

def step(state, cmd):
    n_turns = { # main direction is left
        'a': (0, 0),
        'left': (0, 0),
        's': (1, 3),
        'down': (1, 3),
        'd': (2, 2),
        'right':(2, 2),
        'w': (3, 1),
        'up' :(3, 1),
    }
    
    before, after = n_turns[cmd]
        
    
    
    for i in range(before):
        rotate_matrix(state)
    remove_zeros(state)
    agregation(state)
    remove_zeros(state)
    add_zeros(state, before)
    for j in range(after):
        rotate_matrix(state)
    #print(state)

def event(state, cmd):
    
    if cmd == 'esc':
        state['is_finished'] = True
        
    elif cmd == '0':
        restart_game(state)

    elif cmd in 'wasd' or cmd =='up' or cmd == 'right' or cmd == 'left' or cmd == 'down':
        step(state, cmd)
        randomize(state)
        show_state(state)

    else:
        print('\n\n\n\n\n\nInvalid input! Try another key.')
        show_state(state)

def won(state):
    for row in state['matrix']:
        if 2048 in row:
            state['is_finished'] = True
            state['won'] = True

def loss(state):
    state['is_finished'] = True
    for row in state['matrix']:
        if 0 in row:
            state['is_finished'] = False
        
        
def best_score(state):
    if state['best_score'] < state['score']:
        state['best_score'] = state['score']
    return state

def save_results(state):
    
    with open('old_game.json', 'w') as file:
        json.dump(state, file)
    

def prin_result(state):
    print('\n' * 3)
    if state['won'] == True:
        print('Congretulations! You won!\n')
    print("Gaim is over!")

def restart_game(state):
    best_score(state)
    state['score'] = 0
    state['matrix'] = []
    new_board(state)
    print('You restarted the game')
    show_state(state)



@click.command()
@click.option('--game', default='new', help='To start last game type \'last\'')
@click.option('--rows', default=4, help='Amont of rows of the table')
@click.option('--columns', default=4, help='Amont of columns of the table')
@click.option('--w_cell', default=4, help='Width of tbe cell of the table')
@click.option('--h_cell', default=1, help='Height of tbe cell of the table')
def run(game, rows, columns, w_cell, h_cell, *args, **kwargs):
    
    state = {}
    state['game'] = game
    state['rows'] = rows
    state['columns'] = columns
    state['w_cell'] = w_cell
    state['h_cell'] = h_cell
    state['score'] = 0
    state['best_score'] = 0 # read best score from some file
    state['is_finished'] = False
    state['maxium_nuber'] = 9
    state['won'] = False
    state['matrix'] = []
    

  
    try:
        with open('old_game.json', 'r') as file:
            l_game = json.load(file)
    except FileNotFoundError:
        new_board(state)
        with open('old_game.json', 'w') as file:
            json.dump(state, file)
        l_game = state
    else:
        with open('old_game.json', 'r') as file:
            l_game = json.load(file)
            
        
   
    if  state['game'].lower() == 'last':
        state = l_game
        randomize(state)
    else:
        state['matrix'] = []
        state['best_score'] = l_game['best_score']
        new_board(state)
        
    
    
    state['is_finished'] = False
    show_state(state)
    n = 1
   

    while True:
        
        if n == 1:
            print('Press a key')
            n -= 1
        key = keyboard.read_event()
        if key.event_type != 'up': continue
        cmd = key.name
        n = 1
        #print(cmd)
        event(state, cmd)
        if cmd != 'esc':
            loss(state)
        won(state)
        if state['is_finished'] == True:
            best_score(state)
            prin_result(state)
            save_results(state)
            exit(0)


if __name__ == '__main__':
    run()