"""
This game is created by a college student of IMCA course from parul university for his project in 2nd sem.
Made with the help of youtube but the code is rewriten to help further development of game easily.
Project Scope:
> Displaying score
> Better Graphics
> User database
> PVP support 

Discord tag: Fammy player#9600
Instagram ID: abhishek_airan_

If this code helps you make me know :)
"""

from tkinter import *
import sys 
import os
import random


#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")



# Constant variables for setting
GAME_WIDTH = 700
GAME_HIGHT = 500
SPACE_SIZE = 20
BODY_PARTS = 2
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


# class for functions which will control the flow of data
def beasy(window: Tk):
    for item in window.winfo_children():
        item.destroy()
    game_fram = GameFram(window)

def bmedium(window: Tk):
    for item in window.winfo_children():
        item.destroy()
    game_fram = GameFram(window,1)
    
def bhard(window: Tk):
    for item in window.winfo_children():
        item.destroy()
    game_fram = GameFram(window,2)

def bretry(window: Tk):
    for item in window.winfo_children():
        item.destroy()
    game_fram = GameFram(window)

def bmenu(window: Tk):
    for item in window.winfo_children():
        item.destroy()
    game_fram = MenuUI(window)


# class for main menu where player can select difficulty
class MenuUI(Frame):
    def __init__(self,window:Tk):
        super().__init__(master = window,background='#333333',width=GAME_WIDTH,height=GAME_HIGHT)
        window.configure(background='#333333')
        
        # frame for buttons 
        window.columnconfigure(0,weight=1,uniform='a')
        window.columnconfigure(1,weight=1,uniform='a')
        window.columnconfigure(2,weight=1,uniform='a')
        window.rowconfigure(0,weight=1,uniform='a')
        window.rowconfigure(1,weight=1,uniform='a')
        window.rowconfigure(2,weight=1,uniform='a')

        # buttons
        self.easyB = Button(window,text="Easy",background='#555555',fg='#00ff00',padx=50,pady=50,font='arial 15',command= lambda: beasy(window))
        self.easyB.grid(column=0,row=1,sticky='e')
        self.mediumB = Button(window,text="Medium",background='#555555',fg='yellow',padx=50,pady=50,font='arial 15', command= lambda: bmedium(window))
        self.mediumB.grid(column=1,row=1)
        self.hardB = Button(window,text='Hard',background='#555555',fg='red',padx=50,pady=50,font='arial 15', command=lambda: bhard(window))
        self.hardB.grid(column=2,row=1,sticky='w')
        self.label = Label(window,text="Select Game Diffculty",background='#333333',font='arial 20',fg='cyan')
        self.label.grid(row=0,column=0,columnspan=3)



# class for main to be executed
class GameFram(Frame):
    def __init__(self, master: Tk,difficulty: int = 0):
        super().__init__(master=master)

        # Setting up some variables which will control the snake 
        self.difficulty = difficulty
        self.direction = 'right'
        self.score = 0
        self.speed = 250

        #adding canvas to the frame
        self.canvas = Canvas(window,bg=BACKGROUND_COLOR,height=GAME_HIGHT,width=GAME_WIDTH) #setting up a canvas on which actual game will run
        self.canvas.pack() #packing up canvas in the main window

        # binding the controls
        window.bind('<Left>', lambda event:self.change_direction('left')) # Left arrow key ⬅️
        window.bind('<Right>', lambda event:self.change_direction('right')) # right arrow key ➡️
        window.bind('<Up>', lambda event:self.change_direction('up')) # up arrow key ⬆️
        window.bind('<Down>', lambda event:self.change_direction('down')) # down arrow key ⬇️
        window.bind('<a>', lambda event:self.change_direction('left')) # 'a' key for left navigation
        window.bind('<d>', lambda event:self.change_direction('right')) # 'd' key for right navigation
        window.bind('<w>', lambda event:self.change_direction('up')) # 'w' key for up navigation 
        window.bind('<s>', lambda event:self.change_direction('down')) # 's' key for down navigation

        # Setting up food and snake
        if self.difficulty==0: self.food = self.Food(self.canvas,3) # food
        elif self.difficulty == 1: self.food = self.Food(self.canvas)
        else: self.food = self.Food(self.canvas)
        self.snake = self.Snake(self.canvas) # snake
        # turning on game 
        self.next_turn(self.snake,self.food)



    # Defining Classes

    class Food: # class for food
        def __init__(self,canvas:Canvas,count: int = 1):
            self.canvas = canvas
            self.count = count
            self.currentFood = 0
            self.coordiantes = []
            self.create_food()

        def create_food(self):
            # getting random coordinates to place the food
            while self.currentFood<self.count:
                x = int(random.randint(0,(GAME_WIDTH//SPACE_SIZE)-1)) * SPACE_SIZE # x coordinate for food
                y = int(random.randint(0,(GAME_HIGHT//SPACE_SIZE)-1)) * SPACE_SIZE # y coordinate for food
                self.coordiantes.append((x,y)) # adding this coordinate in list to use them later too
                self.canvas.create_oval(x , y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag = f'food({x},{y})') # creating food
                self.currentFood += 1


    class Snake: # snake class
        def __init__(self,canvas:Canvas):
            self.body_size = BODY_PARTS # number of initial body parts snake will have at the start if the game
            # coordinates of each snake's body part
            self.coordinates = [] 
            self.square = []

            # creating the initials coordinates of the snake
            for a in range(0,BODY_PARTS):
                self.coordinates.append([0,0])

            # creating the actual snake on the canvas
            for x , y in self.coordinates:
                square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR,tag = 'snake')
                self.square.append(square)

    # function to change the snake direction
    def next_turn(self,snake: Snake, food: Food):

        x,y = snake.coordinates[0] # getting snake head coordinates

        # setting up the coords for making the next body on canvas
        if self.direction == 'right':
            if self.difficulty == 0 or self.difficulty==1:
                if x==GAME_WIDTH-SPACE_SIZE:
                    x = 0
                else:
                    x+=SPACE_SIZE
            else: 
                x += SPACE_SIZE
        elif self.direction == 'left':
            if self.difficulty == 0 or self.difficulty == 1:
                if x==0:
                    x = GAME_WIDTH-SPACE_SIZE
                else:
                    x -= SPACE_SIZE
            else:
                x -= SPACE_SIZE
        elif self.direction == 'up':
            if self.difficulty == 0 or self.difficulty == 1:
                if y == 0:
                    y = GAME_HIGHT-SPACE_SIZE
                else:
                    y -= SPACE_SIZE
            else:
                y -= SPACE_SIZE
        elif self.direction == 'down':
            if self.difficulty == 0 or self.difficulty==1:
                if y == GAME_HIGHT-SPACE_SIZE:
                    y = 0
                else:
                    y += SPACE_SIZE
            else:
                y += SPACE_SIZE
        snake.coordinates.insert(0,(x,y)) # setting the new coords of the head
        square = self.canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill = SNAKE_COLOR) # creating the new head
        snake.square.insert(0,square) # adding new head coords to the list

        # checking if snake eats the food
        if (x,y) in food.coordiantes:
            # if eats the food then...
            self.score += 1 # increase the score
            self.canvas.delete(f'food({x},{y})') # delete the food
            food.coordiantes.remove((x,y))
            food.currentFood -= 1
            food.create_food() # create a new food on canvas
            if self.difficulty==0: self.speed -= 2 # increasing speed on easy difficulty
            if self.difficulty==1: self.speed -= 5 # increasing speed on medium difficulty
            if self.difficulty==2: self.speed -= 8 # increasing speed on hard difficulty
        else:
            # if snake don't eat the food...
            del snake.coordinates[-1] # delete the snake last body part's coordinates from list
            self.canvas.delete(snake.square[-1]) # delete the snake last body part form the canvas
            del snake.square[-1] # delete the snake last body part from list

        # check if snake collided from walls or itself
        if self.check_collision(snake): 
            # if collied then end game
            self.game_over()
        else:
            # if not the continue the next turn
            window.after(self.speed,self.next_turn,snake,food)

    # function to change direction of the snake when key is pressed
    def change_direction(self,new_direction):
        if self.direction == 'right':
            if new_direction != 'right' and new_direction != 'left':
                self.direction = new_direction
        if self.direction == 'left':
            if new_direction != 'left' and new_direction != 'right':
                self.direction = new_direction
        if self.direction == 'up':
            if new_direction != 'up' and new_direction != 'down':
                self.direction = new_direction
        if self.direction == 'down':
            if new_direction != 'down' and new_direction != 'up':
                self.direction = new_direction

    # function to check if snake collied from itself or walls
    def check_collision(self,snake:Snake):
        x, y = snake.coordinates[0] # getting snake head coordinates
        for body in snake.coordinates[1:]:
            if x == body[0] and y == body[1]:
                return True
        if self.difficulty == 0 or self.difficulty == 1:
            return False
        else:
            if x<0 or x>=GAME_WIDTH: # if head hits the right or left walls 
                return True 
            elif y<0 or y>=GAME_HIGHT: # if head hits the upper or lower walls
                return True
        # if head hits snake another body part
        # if head does not collide
        return False

    # function to end game (this just show the game over text)
    def game_over(self):
        self.canvas.create_text(self.canvas.winfo_width()//2,self.canvas.winfo_height()//2-50,text=f"Your Score:{self.score}",fill='#FF0000',font=('consolas',60),tag='gameover')
        self.canvas.create_text(self.canvas.winfo_width()//2,self.canvas.winfo_height()//2+50,text=f"Game Over",fill='#FF0000',font=('consolas',70),tag='gameover')
        self.retryB = Button(window,text="Retry",font='arial 16',background='#555555',fg='#00ff59',padx=20,pady=5,command=lambda: bretry(window))
        self.menuB = Button(window,text="Menu",font='arial 16',background='#555555',fg='#00ff59',padx=20,pady=5,command=lambda: bmenu(window))
        self.retryB.place(x=350,y=380)
        self.menuB.place(x=250,y=380)


# Setting window with tkinter
window = Tk() #setting up main window
window.title("Snake Game") #window title
window.minsize(700,500) #window minimum size define in constants variables
window.resizable(False,False) #window can't be resized anymore

# Setting window to appear in middle of the screen 
window.update() #updating window so that new geomerty can be applied
screen_height = window.winfo_screenheight() #getting screen hight of the system
screen_width = window.winfo_screenwidth() #getting screen width of the system
win_width = window.winfo_width() #getting windows width 
win_height = window.winfo_height() #getting windows width
x = int((screen_width/2)-(win_width/2)) #getting middle x-axis on scrren (not 100% accurate)
y = int((screen_height/2)-(win_height/2)) #getting middle y-axis on scrren (not 100% accurate)
window.geometry(f"{win_width}x{win_height}+{x}+{y}") # setting up new geometry of the window
game_fram = MenuUI(window) #showing main menu
# window.overrideredirect(True)
window.mainloop() # running the window