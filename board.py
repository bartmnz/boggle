#!/usr/bin/python3


def score_word(s, word):
   
   if word in s:
       score= len(word)
       if score >= 8:
           return 11
       elif score == 7:
           return 5
       elif score == 6:
           return 3
       elif score == 5:
           return 2
       else:
           return 1 
   else:
       return 0
   

def make_board():
    #distribution for classic boggle game 1987~2008
    # found www.bananagrammer.com/2013/10/the-boggle-cube-redesign-and-its-effect.html
    dice = ['aaciot',
            'abilty',
            'abjmoq',
            'acdemp',
            'acelrs',
            'adenvz',
            'ahmors',
            'biforx',
            'denosw',
            'dknotu',
            'eefhiy',
            'egkluy',
            'egintv',
            'ehinps',
            'elpstu',
            'gilruw']
    
    import random
    import time
    random.seed(time.time())
    y = random.randint(0,len(dice))
    board = ''
    for x in range(0,16):
        if not x % 4 and x > 0:
            board += ' '
        if ( y > len(dice)-1):
            y = 0
        x = random.randint(0,5)
        value = dice[y]
        value = value[x]
        board += value
        y += 1
    return board


def solver(board):
    #http://stackoverflow.com/questions/746082/how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-solver
    grid = board.split()
    nrows, ncols = len(grid), len(grid[0])
    
    # A dictionary word that could be a solution must use only the grid's
    # letters and have length >= 3. (With a case-insensitive match.)
    import re
    
    alphabet = ''.join(set(''.join(grid)))
    if 'q' in alphabet:
        alphabet += 'u'
#         print(alphabet)
    bogglable = re.compile('[' + alphabet + ']{3,}$', re.I).match
    
    words = set(word.rstrip('\n') for word in open('/usr/share/dict/words') if bogglable(word))
    prefixes = set(word[:i] for word in words
                   for i in range(2, len(word)+1))
    
    
    
    def solve():
        for y, row in enumerate(grid):
            for x, letter in enumerate(row):
                if ( letter.lower() == 'q'):
                    letter +='u'
                for result in extending(letter, ((x, y),)):
                    yield result
    
    def extending(prefix, path):
        if prefix in words:
            yield (prefix, path)
        for (nx, ny) in neighbors(*path[-1]):
            if (nx, ny) not in path:
                prefix1 = prefix + grid[ny][nx]
                if grid[ny][nx].lower() == 'q':
                    prefix1 += 'u'
                if prefix1 in prefixes:
                    for result in extending(prefix1, path + ((nx, ny),)):
                        yield result
    
    def neighbors(x, y):
        for nx in range(max(0, x-1), min(x+2, ncols)):
            for ny in range(max(0, y-1), min(y+2, nrows)):
                yield (nx, ny)
    unique = []
    for solution in solve():
        unique.append(solution[0])
        #print (solution)
    unique = set(unique)
    return unique

    

    