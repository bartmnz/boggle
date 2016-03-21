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