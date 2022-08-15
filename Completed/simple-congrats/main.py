import turtle
import tkinter as tk

def run_turtle():
    turtle.title('Congratulations Hanae!')

    turtle.speed(5)

    # Background
    turtle.penup()
    turtle.goto(0, -300)
    turtle.pendown()
    turtle.color("green")
    turtle.begin_fill()
    turtle.circle(300)
    turtle.end_fill()

    # Lid on gift
    turtle.penup()
    turtle.goto(-180, 20)
    turtle.pendown()
    turtle.color("red")
    turtle.begin_fill()
    for i in range(2):
        turtle.forward(360)
        turtle.left(90)
        turtle.forward(60)
        turtle.left(90)
    turtle.end_fill()

    # Bottom of gift
    turtle.penup()
    turtle.goto(-160, 0)
    turtle.pendown()
    turtle.begin_fill()
    for i in range(2):
        turtle.forward(320)
        turtle.right(90)
        turtle.forward(210)
        turtle.right(90)
    turtle.end_fill()

    # Green line through middle of gift
    turtle.penup()
    turtle.goto(-10, 80)
    turtle.pendown()
    turtle.color("green")
    turtle.begin_fill()
    for i in range(2):
        turtle.forward(20)
        turtle.right(90)
        turtle.forward(290)
        turtle.right(90)
    turtle.end_fill()

    # Message
    turtle.penup()
    turtle.goto(-200, 170)
    turtle.pendown()
    turtle.color("red")
    message = "CONGRATULATIONS HANAE!"
    turtle.write(message.center(0), font=("Arial", 22, "bold"))

    turtle.hideturtle()
    turtle.done()


root = tk.Tk()
root.title("Hello Hanae!")

canvas1 = tk.Canvas(root, width=300, height=300)
canvas1.pack()


button1 = tk.Button(text='Click here for a surprise', command=run_turtle, bg='brown', fg='white')
canvas1.create_window(150, 150, window=button1)

root.mainloop()
