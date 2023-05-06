from tkinter import * 
import random


# Constant variables for setting
GAME_WIDTH = 700
GAME_HIGHT = 500
SPACE_SIZE = 20
BODY_PARTS = 2
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
Speed = 250


# Defining Classes

class Food:
    def __init__(self):
        x = random.randint(0,(GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0,(GAME_HIGHT/SPACE_SIZE)-1) * SPACE_SIZE
        self.coordiantes = [x,y]

        canvas.create_oval(x , y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag = 'food')

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.square = []

        for a in range(0,BODY_PARTS):
            self.coordinates.append([0,0])

        for x , y in self.coordinates:
            square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR,tag = 'snake')
            self.square.append(square)

def next_turn(snake: Snake, food: Food):

    x,y = snake.coordinates[0]

    if direction == 'right':
        x += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE

    snake.coordinates.insert(0,(x,y))
    square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill = SNAKE_COLOR)
    snake.square.insert(0,square)

    if x==food.coordiantes[0] and y==food.coordiantes[1]:
        global score, Speed
        score += 1
        canvas.delete('food')
        food = Food()
        Speed -= 5
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.square[-1])
        del snake.square[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(Speed,next_turn,snake,food)


def change_direction(new_direction):
    global direction

    if direction == 'right':
        if new_direction != 'right' and new_direction != 'left':
            direction = new_direction
    if direction == 'left':
        if new_direction != 'left' and new_direction != 'right':
            direction = new_direction
    if direction == 'up':
        if new_direction != 'up' and new_direction != 'down':
            direction = new_direction
    if direction == 'down':
        if new_direction != 'down' and new_direction != 'up':
            direction = new_direction

def check_collision(snake:Snake):
    x, y = snake.coordinates[0]
    if x<0 or x>=GAME_WIDTH:
        return True
    elif y<0 or y>=GAME_HIGHT:
        return True
    for body in snake.coordinates[1:]:
        if x == body[0] and y == body[1]:
            return True
        
    return False

def game_over():
    canvas.create_text(canvas.winfo_width()//2,canvas.winfo_height()//2,text="Game Over",fill='#FF0000',font=('consolas',70),tag='gameover')


# Settingup window with tkinter
window = Tk() #setting up main window
window.title("Snake Game") #window title
window.minsize(GAME_WIDTH,GAME_HIGHT) #window minimum size define in constants variables
window.resizable(False,False) #window can't be resized anymore
canvas = Canvas(window,bg=BACKGROUND_COLOR,height=GAME_HIGHT,width=GAME_WIDTH) #setting up a canvas on which actual game will run
canvas.pack() #packing up canvas in the main window
# Setting window to appear in middle of the screen 
window.update() #updating window so that new geomerty can be applied
screen_height = window.winfo_screenheight() #getting screen hight of the system
screen_width = window.winfo_screenwidth() #getting screen width of the system
win_width = window.winfo_width() #getting windows width 
win_height = window.winfo_height() #getting windows width
x = int((screen_width/2)-(win_width/2)) #getting middle x-axis on scrren (not 100% accurate)
y = int((screen_height/2)-(win_height/2)) #getting middle y-axis on scrren (not 100% accurate)
window.geometry(f"{win_width}x{win_height}+{x}+{y}") # setting up new geometry of the window

# Setting up some variables 
direction = 'right'
score = 0

# binding the controls
window.bind('<Left>', lambda event:change_direction('left'))
window.bind('<Right>', lambda event:change_direction('right'))
window.bind('<Up>', lambda event:change_direction('up'))
window.bind('<Down>', lambda event:change_direction('down'))

# Setting up classes
food = Food()
snake = Snake()
next_turn(snake,food)

window.mainloop() # running the window