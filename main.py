import tkinter as tk
import random
from random import randrange



count = 0
points = 0

# def set_random_color(i):
#     color = random.choice(colours)
#     canvas.itemconfig(i, fill=color)

def update_point():
    global points
    points += 1
    canvas.itemconfig(scorer, text=str(points))

def destroy_brick():
    global movement
    coord_ball = canvas.coords(ball)
    #print(coord_ball)
    item_list = canvas.find_overlapping(coord_ball[0],coord_ball[1],coord_ball[2],coord_ball[3])
    # print(item_list)
    for i in item_list:
        if i in bricks:
            color = canvas.itemcget(i, "fill")
            if color == "yellow":
                bricks.remove(i)
                canvas.delete(i)
                movement = [movement[0]*-1, movement[1]*-1]
                update_point()
            else:
                randomcolor = random.choice(colours)
                canvas.itemconfig(i, fill = randomcolor)
                movement = [movement[0]*-1, movement[1]*-1]


def ball_move():
    global ball, movement, desk
    canvas.move(ball, movement[0], movement[1])
    destroy_brick()
    pos = canvas.coords(ball)
    desk_pos = canvas.coords(desk)
    overlap = canvas.find_overlapping(desk_pos[0], desk_pos[1], desk_pos[2], desk_pos[3])
    if pos[2] >= width:     # prava hranica
        # movement = [-1, 1]
        movement = [movement[0] * -1, movement[1]]
        # faker(0)
    elif pos[3] >= height:  # spodna hranica
        canvas.delete('all')
        text = canvas.create_text(width//2, height//2, text='YOU LOST', fill = "white")
    elif pos[0] <= 0:       # lava hranica
        # movement = [1, -1]
        movement = [movement[0] * -1, movement[1]]
        # faker(0)
    elif pos[1] <= 0:       # vrchna hranica
        # movement = [1, 1]
        movement = [movement[0], movement[1] * -1]
        # faker(1)
    elif ball in overlap:
        # movement = [-1, -1]
        # faker(1)
        movement = bounce(pos, desk_pos)
    canvas.after(4, ball_move)


def faker(a):   # nepotrebny lebo uhol sa meni pri odraze od rectanglu
    global movement
    d = randrange(-1, 2)
    movement[a] += d


# def move_left(e):
#     canvas.move(desk, -4, 0)


# def move_right(e):
#     canvas.move(desk, 4, 0)


def mover(e):
    global x
    x2 = e.x
    if x != 0:
        mouse = x2-x
        canvas.move(desk, mouse, 0)
        x= e.x


def bounce(ball_pos, rec_pos):
    ball_pos = (ball_pos[0] + ball_pos[2])//2
    rec_middle = (rec_pos[0] + rec_pos[2])//2
    ball_to_rec = ball_pos - rec_middle
    return [ball_to_rec//(rec_w//3), -1]    # rec_w//3 => vector x je 0-3


def starter(e):
    global x, y
    zoz = canvas.find_overlapping(e.x, e.y, e.x+1, e.y+1)
    if desk in zoz:
        x = e.x
        y = e.y
        ball_move()
        canvas.delete(start_text)

def prepare_bricks():
    root.wm_attributes('-transparentcolor', '#ab23ff')
    for y in range(brick_count_y):
        for x in range(brick_count_x):
            bricks.append(canvas.create_rectangle(x* brick_w, y * brick_h,x*brick_w+brick_w,y * brick_h + brick_h,fill = colours[y%len(colours)], width = 5,outline = 'white'))



colours = ['red','green','lime','turquoise', 'aquamarine', 'yellow', 'magenta']
randomcolor = random.choice(colours)
root = tk.Tk()
width = 500
height = 500
ws = 10
rec_w = 25
brick_w = 50
brick_h = 10
brick_count_x = 10
brick_count_y = 6
bricks = []
canvas = tk.Canvas(root, width= width, height= height, bg= 'black')
canvas.pack()
movement = [0,1]
ball = canvas.create_oval(width//2 - ws, height//2 - ws, width//2 + ws, height//2 + ws, fill = 'red')
desk = canvas.create_rectangle(width//2 - rec_w, height - 30, width//2 + rec_w, height - 20, fill= 'yellow')
start_text = canvas.create_text(width//2, height//2 - 50, text='KLICK ON RECTANGLE TO START\nplay on fullscreen\nuse mouse to move', fill = "white")
scorer = canvas.create_text(width-50, height - 400 , text='0', font=('Arial', 40, 'bold'), fill='white')

# def checkkey(e):
#     print("stlacil som")
#     print(e.char)




prepare_bricks()
# treba najst bind na sipky
canvas.bind('<Button-1>', starter)
canvas.bind('<Motion>',mover)
# canvas.focus_set()
#root.bind('<Key>',checkkey)
# canvas.bind('d',move_right)
# root.bind('<Up>',checkkey)

root.mainloop()
