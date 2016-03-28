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
        y = 0
        x = 0
        for button in buttons:
            button.grid(row = y, column = x)
            x += 1
            if x == 4:
                x = 0
                y += 1
        
        
        frame2 = Frame(win)
        #frame2.pack()
        v = StringVar()
        self.e = Entry(frame2, textvariable =v)
        def func(event):
            value = self.e.get()
            if value in self.solutions:
                self.userWords.insert(END, value)
            self.e.delete(0, 'end')
            print(value)
        self.e.bind('<Return>', func)
        self.e.pack()
        self.e.focus_set()
        
        frame3 = Frame(win)
        #frame3.pack()
        scroll = Scrollbar(frame3, orient=VERTICAL)
        self.select = Listbox(frame3, height= 18)
        
        #elect.configure(anchor= CENTER)
        self.select.pack()
        
        frame4 = Frame(win)
        #frame4.pack()
        self.timeLeft = 180
        self.clock = Label(frame4, text= self.timeLeft)
        self.clock.pack()
        
        frame5 = Frame(win)
        #frame5.pack()
        self.userWords = Listbox(frame5, height= 18)
        self.userWords.pack()
        frame1.grid(row = 1, column = 1)
        frame2.grid(row = 2, column = 1)
        frame3.grid(row = 1, column = 2)
        frame4.grid(row = 0, column = 1)
        frame5.grid(row = 1, column = 0)
        
    def processUpdate(self):
        while self.line.qsize():
            try:
                msg = self.line.get(0)
                self.select.insert(END, msg)
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
    


