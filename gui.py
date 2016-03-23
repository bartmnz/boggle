from Tkinter import *

win = Tk()
frame1 = Frame(win)
frame1.pack()

buttons = []
for x in range(0,16):
    b1 = Button(frame1, text = x, height= 3, width = 3)
    buttons.append(b1)
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
e.pack()

frame3 = Frame(win)
frame3.pack()
scroll = Scrollbar(frame3, orient=Vertical)
select = Listbox()

mainloop()  
    


