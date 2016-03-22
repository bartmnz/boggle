#!usr/bin/python3

import threading

exitFlag = 0

def check_dictionary(word, s):
   
   if word in s:
       print(word)
   return word in s
   
def valid_sub_string(word):
    import re
    pattern = re.compile('\A' + word, re.IGNORECASE)
    with open("./words2.txt") as inFile:
        for line in inFile:
            result = re.search(pattern, line)
            if result :
                print ( "found it")
                return True
    return False

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
    board = ''
    for x in range(0,16):
        if not x % 4 and x > 0:
            board += ' '
        if ( y > len(dice)-1):
            y = 0
        x = random.randint(0,5)
        value = dice[y]
        value = value[x]
        # if value == 'q':
        #     value = 'qu'
        if y == len(dice) -1:
            value = value.upper()
        board += value
        y += 1
    count = 0 
    for letter in board:
        if letter.lower() == 'q':
            print ( 'Qu', end = '  ' )
        else:
            print(letter + " ", end="  ")
        
        if count == 4:
            print()
            count = -1
        count += 1
    return board

class Path(object):
    def __init__(self, path, current_word):
        self.path = path
        self.word = current_word
    def append(self, letter, pos):
        self.word += letter
        self.path.append(pos)
    def used_before(self, pos):
        for place in self.path:
            if place == pos:
                return True
        return False
    def index(self):
        return self.path[len(self.path)-1]
    def nom(self):
        return self.word
    def otherNom(self):
        return self.path

def find_all(board,s):
    results = []
    for x in range(0,len(board)):
        test = Path([x], board[x])
        results.append(expand(test, board,s))
    return results

def expand(word, board,s):
    possibilities = []
    results = []
    spot = word.index()
    # build next level by comparing all adjacent spots
    to_check = [spot+1, spot -1, spot+ 3, spot -3, spot +4, spot -4, spot +5, spot-5]
    for spot in to_check:
        try:
            if not word.used_before(spot):
                if valid_sub_string(word.nom() + board[spot]):
                    next_path = Path(word.otherNom(), word.nom())
                    next_path.append(board[spot], spot)
                    possibilities.append(next_path)
                    if check_dictionary(next_path.nom(),s):
                        results.append(next_path.nom())
        except IndexError:
            continue
    #recursive call for all remaining possibilities
    for thing in possibilities:
        results.append(expand(thing, board))
    return results
    


def solver(board):
    #http://stackoverflow.com/questions/746082/how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-solver
    grid = board.split()
    nrows, ncols = len(grid), len(grid[0])
    
    # A dictionary word that could be a solution must use only the grid's
    # letters and have length >= 3. (With a case-insensitive match.)
    import re
    alphabet = ''.join(set(''.join(grid)))
    bogglable = re.compile('[' + alphabet + ']{3,}$', re.I).match
    
    words = set(word.rstrip('\n') for word in open('./words2.txt') if bogglable(word))
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
                    #print(prefix1)
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

class myThread(threading.Thread):
    def __init__(self, solutions):
        threading.Thread.__init__(self)
        #self.threadID = threadID
        #self.name = name
        self.solutions = solutions #list(solutions)
    def run(self):
        import random
        import time
        end = time.time()+60
        while (time.time() < end):
            time.sleep(10)
            choice = random.sample(self.solutions, 1)
            print()
            print (*choice)
            self.solutions.remove(*choice)

class userInput(threading.Thread):
    def __init__(self, solutions):
        threading.Thread.__init__(self)
        self.solutions = solutions
    def run(self):
        import time
        end = time.time()+60
        while (time.time() < end):
            guess = input('guess:')
            if guess in solutions:
                print ('good!')
            else:
                print( 'nope')

if __name__ == "__main__":
    board = make_board()
    solutions = solver(board)
   
    #try:
    for s in solutions:
        print(s, end = ' ')
    print()
    thread1 = myThread( solutions)
    thread2 = userInput( solutions)
    thread1.start()
    thread2.start()
    #except:
    #   print("didn't work")
    
    
    

    