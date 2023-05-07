"""
This game is created by a college student of IMCA from parul university for his project in 2nd semister.
Made with the help of youtube but the code is rewriten to help further development of game easily.
Project Scope:
> Displaying score
> Difficulty selector
> User database
> PVP support 

Discord tag: Fammy player#9600
Instagram ID: abhishek_airan_

If this code helps you make me know :)
"""

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


# class for main to be executed
class GameFram(Frame):
    def __init__(self, master: Tk):
        super().__init__(master=master)

        # Setting up some variables which will control the snake 
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
        self.food = self.Food(self.canvas) # food
        self.snake = self.Snake(self.canvas) # snake
        # turning on game 
        self.next_turn(self.snake,self.food)



    # Defining Classes

    class Food: # class for food
        def __init__(self,canvas:Canvas):
            # getting random coordinates to place the food
            x = int(random.randint(0,(GAME_WIDTH//SPACE_SIZE)-1)) * SPACE_SIZE # x coordinate for food
            y = int(random.randint(0,(GAME_HIGHT//SPACE_SIZE)-1)) * SPACE_SIZE # y coordinate for food
            self.coordiantes = [x,y] # adding this coordinate in list to use them later too

            canvas.create_oval(x , y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag = 'food') # creating food

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
            x += SPACE_SIZE
        elif self.direction == 'left':
            x -= SPACE_SIZE
        elif self.direction == 'up':
            y -= SPACE_SIZE
        elif self.direction == 'down':
            y += SPACE_SIZE

        snake.coordinates.insert(0,(x,y)) # setting the new coords of the head
        square = self.canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill = SNAKE_COLOR) # creating the new head
        snake.square.insert(0,square) # adding new head coords to the list

        # checking if snake eats the food
        if x==food.coordiantes[0] and y==food.coordiantes[1]:
            # if eats the food then...
            self.score += 1 # increase the score
            self.canvas.delete('food') # delete the food
            food = self.Food(self.canvas) # create a new food on canvas
            self.speed -= 5 # increasing speed
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
        if x<0 or x>=GAME_WIDTH: # if head hits the right or left walls 
            return True 
        elif y<0 or y>=GAME_HIGHT: # if head hits the upper or lower walls 
            return True
        # if head hits snake another body part
        for body in snake.coordinates[1:]: 
            if x == body[0] and y == body[1]: 
                return True
        # if head does not collide
        return False

    # function to end game (this just show the game over text)
    def game_over(self):
        self.canvas.create_text(self.canvas.winfo_width()//2,self.canvas.winfo_height()//2,text="Game Over",fill='#FF0000',font=('consolas',70),tag='gameover')


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

game_fram = GameFram(window) #showing game canvas

window.mainloop() # running the window