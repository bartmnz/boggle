#!usr/bin/python3
def make_board():
    dice = ['aaafrs',
            'aaeeee',
            'aafirs',
            'adennn',
            'aeeeem',
            'aeegmu',
            'aegmnn',
            'afirsy',
            'bjkqxz',
            'ccenst',
            'ceiilt',
            'ceilpt',
            'ceipst',
            'ddhnot',
            'dhhlor',
            'dhlnor',
            'dhlnor', #(duplicate)
            'eiiitt',
            'emottt',
            'ensssu',
            'fiprsy',
            'gorrvw',
            'iprrry',
            'nootuw',
            'ooottu',
            'iklmqu']
    
    import random
    import time
    random.seed(time.time())
    y = random.randint(0,len(dice))
    board = []
    for x in range(0,16):
        if ( y > len(dice)-1):
            y = 0
        x = random.randint(0,5)
        value = dice[y]
        value = value[x]
        if value == 'q':
            value = 'qu'
        if y == len(dice) -1:
            value = value.upper()
        board.append(value)
        y += 1
    count = 0 
    for letter in board:
        print(letter + " ", end=" ")
        if count == 3:
            print()
            count = -1
        count += 1
        
        
        
if __name__ == "__main__":
    make_board()