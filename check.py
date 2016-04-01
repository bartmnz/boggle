#!usr/bin/env python3
 #http://stackoverflow.com/questions/26659142/cat-grep-and-cut-translated-to-python
import sys
 
def check_dictionary(word):
   f=open("./words2.txt") 
   s = set(word.strip() for word in f)
   if word in s:
       print("here")
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

if __name__ == "__main__":
    word = sys.argv[1:]
    print(word)
    stuff = valid_sub_string(*sys.argv[1:])
    if stuff: 
        print ("works")
        


# class myThread(threading.Thread):
#     def __init__(self, solutions):
#         threading.Thread.__init__(self)
#         #self.threadID = threadID
#         #self.name = name
#         self.solutions = solutions #list(solutions)
#     def run(self):
#         import random
#         import time
#         end = time.time()+60
#         while (time.time() < end):
#             time.sleep(10)
#             choice = random.sample(self.solutions, 1)
#             print()
#             print (*choice)
#             self.solutions.remove(*choice)

# class userInput(threading.Thread):
#     def __init__(self, solutions):
#         threading.Thread.__init__(self)
#         self.solutions = solutions
#     def run(self):
#         import time
#         end = time.time()+60
#         while (time.time() < end):
#             guess = input('guess:')
#             if guess in solutions:
#                 print ('good!')
#             else:
#                 print( 'nope')

# if __name__ == "__main__":
#     board = make_board()
#     solutions = solver(board)
#    
#     #try:
#     for s in solutions:
#         print(s, end = ' ')
#     print()
#     thread1 = myThread( solutions)
#     thread2 = userInput( solutions)
#     thread1.start()
#     thread2.start()
    #except:
    #   print("didn't work")
    
  
  

# class Path(object):
#     def __init__(self, path, current_word):
#         self.path = path
#         self.word = current_word
#     def append(self, letter, pos):
#         self.word += letter
#         self.path.append(pos)
#     def used_before(self, pos):
#         for place in self.path:
#             if place == pos:
#                 return True
#         return False
#     def index(self):
#         return self.path[len(self.path)-1]
#     def nom(self):
#         return self.word
#     def otherNom(self):
#         return self.path

# def find_all(board,s):
#     results = []
#     for x in range(0,len(board)):
#         test = Path([x], board[x])
#         results.append(expand(test, board,s))
#     return results

# def expand(word, board,s):
#     possibilities = []
#     results = []
#     spot = word.index()
#     # build next level by comparing all adjacent spots
#     to_check = [spot+1, spot -1, spot+ 3, spot -3, spot +4, spot -4, spot +5, spot-5]
#     for spot in to_check:
#         try:
#             if not word.used_before(spot):
#                 if valid_sub_string(word.nom() + board[spot]):
#                     next_path = Path(word.otherNom(), word.nom())
#                     next_path.append(board[spot], spot)
#                     possibilities.append(next_path)
#                     if check_dictionary(next_path.nom(),s):
#                         results.append(next_path.nom())
#         except IndexError:
#             continue
#     #recursive call for all remaining possibilities
#     for thing in possibilities:
#         results.append(expand(thing, board))
#     return results

# def valid_sub_string(word):
#     import re
#     pattern = re.compile('\A' + word, re.IGNORECASE)
#     with open("./words2.txt") as inFile:
#         for line in inFile:
#             result = re.search(pattern, line)
#             if result :
#                 print ( "found it")
#                 return True
#     return False

  