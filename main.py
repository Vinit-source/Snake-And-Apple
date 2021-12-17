# Author: aqeelanwar
# Created: 12 June,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

# Trainer: Vinit Gore
# Edited: 17 Dec, 2021
# Email: vinitgore@gmail.com

from tkinter import *   # Tkinter is the package for creating simple Graphical User Interfaces (GUIs)
import random   # python package to generate random numbers
import time     # python package to measure time
import numpy as np  # Numpy package is used to handle linear algebraic operations easily
from PIL import ImageTk,Image   # PIL package used to process images

# Define useful parameters
'''
These variables act like settings for your Snake game. 
Changing these variables will change the behaviour of the game.
'''
size_of_board = 600 # Size of the complete board
rows = 10           # Number of rows on the board
cols = 10           # Number of columns on the board
DELAY = 200         # Speed of the snake (and every step in the program)
snake_initial_length = 3    # Initial length of the snake
RED_COLOR = "#EE4035"       # Red color value in hexadecimal format (#000000 to #FFFFFF)
BLUE_COLOR = "#0492CF"      # Blue color value in hexadecimal format (#000000 to #FFFFFF)
Green_color = "#7BC043"     # Green color value in hexadecimal format (#000000 to #FFFFFF)

BLUE_COLOR_LIGHT = '#67B0CF'    # Light Blue color value in hexadecimal format (#000000 to #FFFFFF)
RED_COLOR_LIGHT = '#EE7E77' # Light Red color value in hexadecimal format (#000000 to #FFFFFF)


class SnakeAndApple:
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()  # create an object of Tkinter window
        self.window.title("Snake-and-Apple")    # title of the window
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)    # create a canvas on the window having size of board as height and width
        self.canvas.pack()  # fills the canvas in the window.
        # Input from user in form of clicks and keyboard
        self.window.bind("<Key>", self.key_input)  # Keyboard input by user calls key_input function 
        self.window.bind("<Button-1>", self.mouse_input)    # Button-1 means left-click. mouse_input function called when left click by user
        self.play_again()   # function defined below
        self.begin = False  # boolean value that becomes True when game starts

    def initialize_board(self):
        '''
        Initializes the board i.e. initialize apple and board and draw the rows and columns of the board
        '''
        self.board = []     # empty list that will store all cell positions on the board
        self.apple_obj = [] # initialize apple object*
        self.old_apple_cell = []    # stores previous apple cells*

        # add each cell value to the board
        for i in range(rows):
            for j in range(cols):
                self.board.append((i, j))
        # draw row lines
        for i in range(rows):
            self.canvas.create_line(
                i * size_of_board / rows, 0, i * size_of_board / rows, size_of_board,
            )
        # draw column lines
        for i in range(cols):
            self.canvas.create_line(
                0, i * size_of_board / cols, size_of_board, i * size_of_board / cols,
            )

    def initialize_snake(self):
        '''
        Initialize snake object. Define its behaviour. Grow it till initial length.
        '''
        self.snake = [] # empty list to store positions of the entire snake
        self.crashed = False # when snake crashes a wall (i.e. edges of the board), this variable becomes true
        self.snake_heading = "Right"    # initial direction of the snake
        self.last_key = self.snake_heading  # value that stores last key entered. Initially same as initial direction.
        # these actions are not available to play during the game.
        self.forbidden_actions = {}
        self.forbidden_actions["Right"] = "Left"
        self.forbidden_actions["Left"] = "Right"
        self.forbidden_actions["Up"] = "Down"
        self.forbidden_actions["Down"] = "Up"
        self.snake_objects = []
        # Grow till initial length
        for i in range(snake_initial_length):
            self.snake.append((i, 0))

    def play_again(self):
        '''
        This function is called when the user wants to play again.
        '''
        self.canvas.delete("all")   # library function to clear the window
        self.initialize_board()     # initialize board 
        self.initialize_snake()     # initialize snake 
        self.place_apple()          # initialize apple 
        self.display_snake(mode="complete") # 
        self.begin_time = time.time()   # save the begin time value

    def mainloop(self):
        '''
        This function is the main loop. The game will keep running continuously because of the while loop below.
        '''
        while True:                     # run infinitely
            self.window.update()        # update runs the input methods bound to the window
            if self.begin:              # game running case
                if not self.crashed:
                    self.window.after(DELAY, self.update_snake(self.last_key))  # DELAY has number of seconds used to set the delay of every window update. Snake is updated everytime after DELAY seconds
                else:                   # game over case
                    self.begin = False
                    self.display_gameover()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------
    def display_gameover(self):
        '''
        Display gameover.
        '''
        score = len(self.snake) 
        self.canvas.delete("all")
        score_text = "Scores \n"
        # Display the string above
        self.canvas.create_text(
            size_of_board / 2,
            3 * size_of_board / 8,
            font="cmr 40 bold",
            fill=Green_color,
            text=score_text,
        )
        score_text = str(score)
        # Display score
        self.canvas.create_text(
            size_of_board / 2,
            1 * size_of_board / 2,
            font="cmr 50 bold",
            fill=BLUE_COLOR,
            text=score_text,
        )
        time_spent = str(np.round(time.time() - self.begin_time, 1)) + 'sec'    # time duration of the game calculated by subtracting current time and begin time.

        # Display time_spent
        self.canvas.create_text(
            size_of_board / 2,
            3 * size_of_board / 4,
            font="cmr 20 bold",
            fill=BLUE_COLOR,
            text=time_spent,
        )
        score_text = "Click to play again \n"
        # Display the string above
        self.canvas.create_text(
            size_of_board / 2,
            15 * size_of_board / 16,
            font="cmr 20 bold",
            fill="gray",
            text=score_text,
        )

    def place_apple(self):
        '''
        Place apple randomly anywhere except at the cells occupied by snake
        '''
        unoccupied_cels = set(self.board) - set(self.snake) # find cells on the board unoccupied by snake
        self.apple_cell = random.choice(list(unoccupied_cels))  # randomly choose any one of the unoccupied cells
        row_h = int(size_of_board / rows)   # row-height
        col_w = int(size_of_board / cols)   # column-width
        x1 = self.apple_cell[0] * row_h     # x value of the bottom-left corner of the apple
        y1 = self.apple_cell[1] * col_w     # y value of the bottom-left corner of the apple
        x2 = x1 + row_h                     # x value of the top-right corner of the apple
        y2 = y1 + col_w                     # y value of the top-right corner of the apple
        
        # draw rectangle using the coordinates of the bottom-left and top-right corner cartesian values
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=RED_COLOR_LIGHT, outline=BLUE_COLOR,   # rectangle color: red, border color: blue
        )

    def display_snake(self, mode=""):
        # Remove tail from display if it exists
        if self.snake_objects != []:
            self.canvas.delete(self.snake_objects.pop(0))
        if mode == "complete":
            for i, cell in enumerate(self.snake):
                # print(cell)
                row_h = int(size_of_board / rows)
                col_w = int(size_of_board / cols)
                x1 = cell[0] * row_h
                y1 = cell[1] * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                self.snake_objects.append(
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=BLUE_COLOR, outline=BLUE_COLOR,
                    )
                )
        else:
            # only update head
            cell = self.snake[-1]
            row_h = int(size_of_board / rows)
            col_w = int(size_of_board / cols)
            x1 = cell[0] * row_h
            y1 = cell[1] * col_w
            x2 = x1 + row_h
            y2 = y1 + col_w
            self.snake_objects.append(
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=BLUE_COLOR, outline=RED_COLOR,
                )
            )
            if self.snake[0] == self.old_apple_cell:
                self.snake.insert(0, self.old_apple_cell)
                self.old_apple_cell = []
                tail = self.snake[0]
                row_h = int(size_of_board / rows)
                col_w = int(size_of_board / cols)
                x1 = tail[0] * row_h
                y1 = tail[1] * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                self.snake_objects.insert(
                    0,
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=BLUE_COLOR, outline=RED_COLOR
                    ),
                )
            self.window.update()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------
    def update_snake(self, key):
        # Check if it hit the wall or its own body
        tail = self.snake[0]
        head = self.snake[-1] 
        if tail != self.old_apple_cell:  # delete one cell from tail of snake to move it ahead by one position
            self.snake.pop(0)
        # add one cell from head to move it ahead
        if key == "Left":   
            self.snake.append((head[0] - 1, head[1]))
        elif key == "Right":
            self.snake.append((head[0] + 1, head[1]))
        elif key == "Up":
            self.snake.append((head[0], head[1] - 1))
        elif key == "Down":
            self.snake.append((head[0], head[1] + 1))

        head = self.snake[-1]
        # Hit the wall / Hit on body
        if (
                head[0] > cols - 1
                or head[0] < 0
                or head[1] > rows - 1
                or head[1] < 0
                or len(set(self.snake)) != len(self.snake)
        ):
            self.crashed = True
        # Got the apple
        elif self.apple_cell == head:
            self.old_apple_cell = self.apple_cell
            self.canvas.delete(self.apple_obj)
            self.place_apple()
            self.display_snake()
        
        else:
            self.snake_heading = key
            self.display_snake()

    def check_if_key_valid(self, key):
        '''
        Check if the key entered from the keyboard is valid or not.
        '''
        valid_keys = ["Up", "Down", "Left", "Right"]    # only these keys should change the behavior of the snake
        # key should be among the valid keys and should not be a forbidden action
        if key in valid_keys and self.forbidden_actions[self.snake_heading] != key:
            return True
        else:
            return False

    def mouse_input(self, event):
        '''
        Function called when mouse left-click is pressed.
        '''
        self.play_again()

    def key_input(self, event):
        '''
        Function called when keyboard input is pressed.
        '''
        if not self.crashed:
            key_pressed = event.keysym
            # Check if the pressed key is a valid key
            if self.check_if_key_valid(key_pressed):
                print(key_pressed)
                self.begin = True
                self.last_key = key_pressed

game_instance = SnakeAndApple() # create a game instance. __init__() function is called here.
game_instance.mainloop()    # main loop runs the game.
