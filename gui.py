from tkinter import *
import board as game
import time
import threading
import queue

class GuiPart:  
    
    def __init__(self, win, line, endCommand, board, solutions):
        self.master = win
        self.line = line
        self.solutions = solutions
        self.user_points = 0
        self.cpu_points = 0
        self.lock = threading.Lock()
        frame1 = Frame(win)
        #frame1.pack()
        
        buttons = []
        for letter in board:
            value = ''
            if letter.lower() == 'q':
                value = 'Qu' 
            elif letter == ' ':
                continue
            else:
                value = letter
                
            but = Button(frame1, text = value, height= 3, width = 3)
            buttons.append(but)
        y = 1
        x = 0
        for button in buttons:
            button.grid(row = y, column = x)
            x += 1
            if x == 4:
                x = 0
                y += 1
        
        self.timeLeft = 180
        self.clock = Label(frame1, text= self.timeLeft)
        self.clock.grid(row= 0, columnspan= 4)
        
        
        
        #frame2 = Frame(win)
        #frame2.pack()
        v = StringVar()
        self.e = Entry(frame1, textvariable =v)
        def func(event):
            with self.lock:
                value = self.e.get()
                if value in self.solutions:
                    self.userWords.insert(END, value)
                    self.user_points += game.score_word(value, self.solutions)
                    self.solutions.remove(value)
                    self.user_score.config(text= self.user_points)
                self.e.delete(0, 'end')
            
            #print(value)
        self.e.bind('<Return>', func)
        self.e.grid(row= 5, columnspan= 4)
        self.e.focus_set()
        
        frame3 = Frame(win)
        #frame3.pack()
        scroll = Scrollbar(frame3, orient=VERTICAL)
        self.select = Listbox(frame3, height= 18)
        
        self.cpu_score = Label(frame3, text= self.cpu_points)
        self.select.grid(row = 0)
        self.cpu_score.grid(row = 1)
        
        #elect.configure(anchor= CENTER)
        #self.select.pack()
     
        frame5 = Frame(win)
        #frame5.pack()
        self.userWords = Listbox(frame5, height= 18)
        self.user_score = Label(frame5, text= self.user_points)
        self.userWords.grid(row= 0)
        self.user_score.grid(row= 1)
        
        #self.userWords.pack()
        frame1.grid(row = 1, column = 1)
        #frame2.grid(row = 2, column = 1)
        frame3.grid(row = 1, column = 2)
        #frame4.grid(row = 0, column = 1)
        frame5.grid(row = 1, column = 0)
        
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
            #self.master.after(1000, self.countDown())
    


class threadedClient:
    def __init__(self, master):
        self.master = master
        self.board = game.make_board()
        self.solutions = game.solver(self.board)
        self.line = queue.Queue()
        self.gui = GuiPart(master, self.line, self.endApplication, self.board, self.solutions)
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
            rValue = random.sample(self.solutions, 1)
            self.line.put(rValue)
    
    def clockThread2(self):
        DELAY = 1
        while not self.exit_flag.wait(timeout=DELAY):
            self.gui.countDown()
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
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.wm_title("Boggle-ish")
    mainloop()
    ai.endApplication()

if __name__ == "__main__":
    main()  
    


