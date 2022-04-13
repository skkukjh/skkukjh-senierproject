from tkinter import *
import random

window = Tk()

window.title("Shape Placement")
window.geometry("768x640+100+100")
window.resizable(False, False)

imageObj1 = []
imageObj2 = []

for i in range(18):
    figure = [None, "rect", "circle", "tri"]
    color = [None, "red", "orange", "yellow", "green", "blue", "violet", "white", "black"]
    f = figure[random.randrange(0,4)]
    if f == None:
        f = "none"
    c = color[random.randrange(0,9)]
    if c == None:
        c = "none"
    files = "images/"+f+"_"+c+".png"
    print(files)
    if i < 9:
        imageObj1.append(PhotoImage(file=files))
        label=Label(window, image=imageObj1[i])
        label.place(x=48+96*(i%3), y=48+96*(i//3))
    else:
        imageObj2.append(PhotoImage(file=files))
        label=Label(window, image=imageObj2[i-9])
        label.place(x=48+96*((i%3)+4), y=48+96*((i-9)//3))

    textinput = Entry(window, width=64)
    textinput.place(x=80, y=360)

    btn = Button(window, height=1, width=10, text="입력", command=newInput)
    btn.place(x=600, y=356)

window.mainloop()

