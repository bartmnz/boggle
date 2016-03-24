from tkinter import *
import board as game
import time
import threading
import queue

class GuiPart:  
    
    def __init__(self, win, line, endCommand, board, solutions):
        self.line = line
        self.solutions = solutions
        frame1 = Frame(win)
        frame1.pack()
        
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
        frame2.pack()
        v = StringVar()
        e = Entry(frame2, textvariable =v)
        def func(event):
            global e
            global solutions
            value = e.get()
            if value in self.solutions:
                print('good')
            e.delete(0, 'end')
            print(value)
        e.bind('<Return>', func)
        e.pack()
        
        frame3 = Frame(win)
        frame3.pack()
        scroll = Scrollbar(frame3, orient=VERTICAL)
        self.select = Listbox(frame3, height= 4)
        
        #elect.configure(anchor= CENTER)
        self.select.pack()
    def processUpdate(self):
        while self.line.qsize():
            try:
                msg = self.line.get(0)
                self.select.insert(END, msg)
            except queue.Empty:
                pass
        

    

class threadedClient:
    def __init__(self, master):
        self.master = master
        self.board = game.make_board()
        self.solutions = game.solver(self.board)
        self.line = queue.Queue()
        self.gui = GuiPart(master, self.line, self.endApplication, self.board, self.solutions)
        self.running = 1
        self.thread1 = threading.Thread(target = self.aiThread1)
        self.thread1.start()
        
        self.updateList()
        
    def updateList(self):
        self.gui.processUpdate()
        if not self.running:
            import sys
            sys.exit(1)
        self.master.after(100, self.updateList)
        
    def aiThread1(self):
        while self.running:
            time.sleep(2)
            import random
            rValue = random.sample(self.solutions, 1)
            self.line.put(rValue)
            
    def endApplication(self):
        self.running = 0
        
def main():
    win = Tk()
    ai = threadedClient(win)
    mainloop()

if __name__ == "__main__":
    main()  
    


