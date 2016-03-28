from tkinter import *
import board as game
import time
import threading
import queue
from tkinter import Scrollbar

class GuiPart:  
    
    def __init__(self, win, line, board, solutions):
        self.master = win
        self.line = line
        self.solutions = solutions
        self.user_points = 0
        self.board = board
        self.cpu_points = 0
        self.lock = threading.Lock()
        self.frame1 = Frame(win)
        #frame1.pack()
        self.make_buttons()
        self.make_timer()
        self.make_input()
        self.frame3 = Frame(win)
        #frame3.pack()
        self.make_ai()
        self.frame5 = Frame(win)
        #frame5.pack()
        self.make_user()
        self.frame1.grid(row = 1, column = 1)
        self.frame3.grid(row = 1, column = 2)
        self.frame5.grid(row = 1, column = 0)
        
        
    def make_user(self):
        self.userWords = Listbox(self.frame5, height= 18)
        self.user_score = Label(self.frame5, text= self.user_points)
        self.scroll2 = Scrollbar(self.frame5, orient= VERTICAL)
        self.userWords.config(yscrollcommand=self.scroll2.set)
        self.scroll2.config(command= self.userWords.yview)
        self.scroll2.grid(column= 2, sticky= N+S)  
        self.userWords.grid(row= 0)
        self.user_score.grid(row= 1)
    
    def make_ai(self):
        self.select = Listbox(self.frame3, height= 18)
        self.scroll = Scrollbar(self.frame3, orient=VERTICAL)
        self.select.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.select.yview)
        self.scroll.grid(column= 2, sticky= N+S) 
        self.cpu_score = Label(self.frame3, text= self.cpu_points)
        self.select.grid(row = 0)
        self.cpu_score.grid(row = 1)   
        
    def make_input(self):
        v = StringVar()
        self.e = Entry(self.frame1, textvariable =v)
        
        self.e.bind('<Return>', self.func)
        self.e.grid(row= 5, columnspan= 4)
        self.e.focus_set()        
    
    
    def make_timer(self):
        self.timeLeft = 180
        self.clock = Label(self.frame1, text= self.timeLeft)
        self.clock.grid(row= 0, columnspan= 4)
            
    def make_buttons(self):
        buttons = []
        for letter in self.board:
            value = ''
            if letter.lower() == 'q':
                value = 'Qu' 
            elif letter == ' ':
                continue
            else:
                value = letter
                
            but = Button(self.frame1, text = value, height= 3, width = 3)
            buttons.append(but)
            y = 1
            x = 0
            for button in buttons:
                button.grid(row = y, column = x)
                x += 1
                if x == 4:
                    x = 0
                    y += 1
    
    def func(self, event):
            with self.lock:
                value = self.e.get()
                try:
                    if value in self.solutions:
                        self.userWords.insert(END, value)
                        self.user_points += game.score_word(value, self.solutions)
                        self.solutions.remove(value)
                        self.user_score.config(text= self.user_points)
                except ValueError:
                    # all words have been found
                    pass
                self.e.delete(0, 'end')
                
    def processUpdate(self):
        with self.lock:
            while self.line.qsize():
                try:
                    msg = self.line.get(0)
                    self.select.insert(END, msg)
                    result = game.score_word(*msg, self.solutions)
                    self.cpu_points += result
                    self.cpu_score.config(text= self.cpu_points)
                    self.solutions.remove(*msg)
                except queue.Empty:
                    pass

    def countDown(self):
        self.clock.configure(text= self.timeLeft)
        self.timeLeft -= 1
        if self.timeLeft < 0:
            return False
        else:
            return True
            #self.master.after(1000, self.countDown())
    


class threadedClient:
    def __init__(self, master):
        self.master = master
        self.board = game.make_board()
        self.solutions = game.solver(self.board)
        self.line = queue.Queue()
        self.gui = GuiPart(master, self.line, self.board, self.solutions)
        self.running = 1
        self.exit_flag = threading.Event()
        self.thread1 = threading.Thread(target = self.aiThread1)
        self.thread2 = threading.Thread(target = self.clockThread2)
        self.thread1.start()
        self.thread2.start()
        self.gui.countDown()
        self.updateList()
        
    def updateList(self):
        self.gui.processUpdate()
        if not self.running:
            import sys
            sys.exit(1)
        self.master.after(100, self.updateList)
        
    def aiThread1(self):            
        DELAY = 10
        while not self.exit_flag.wait(timeout=DELAY):
            #time.sleep(10)
            import random
            try:
                rValue = random.sample(self.solutions, 1)
                self.line.put(rValue)
            except ValueError:
                #all values have been found
                pass
    
    def clockThread2(self):
        DELAY = 1
        while not self.exit_flag.wait(timeout=DELAY):
            if not self.gui.countDown():
                self.exit_flag.set()
            
            #time.sleep(1)
        
    
    def endApplication(self):
        self.running = 0
        self.exit_flag.set()
        self.thread1.join(timeout= None)
        self.thread2.join(timeout= None)
        
        
def main():
    win = Tk()
    ai = threadedClient(win)
    
    def on_closing():
        ai.endApplication()
        for word in ai.solutions:
            print(word, end= ' ')
        print()
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.wm_title("Boggle-ish")
    mainloop()
    ai.endApplication()

if __name__ == "__main__":
    main()  
    


