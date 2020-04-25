import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout

import random
import time

class MainGame(Widget):
    #initializing objects defined in .kv file as None to link it up
    hiscore = ObjectProperty(None)
    score = ObjectProperty(None)
    boardobject=ObjectProperty(None)
    time=ObjectProperty(None)

    def __init__(self, **kwargs):
        #super allows kwargs, allowing passing more arguements
        super().__init__(**kwargs)

        #Kivy way to allow keyboard inputs
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down = self._on_key_down) 
        
        #Initializing the gameboard
        newgame = self.new_game()
        self.gameboard = newgame[0]
        self.newtime = newgame[1]
        self.pop_board(self.gameboard)
        
        #Initializing time
        self.time.text = 'Time' +'\n'+str(int(round(time.time()-self.newtime,0))) +' s'
        #Auto-Refresh time value and updates time value every second, allowing for a 'stopwatch function'
        Clock.schedule_interval(self.update,1)

        #Initializing values of the scoreboards
        self.scoreboard = 0
        self.hiscoreboard=0
        self.score.text ='Score' +'\n'+str(self.scoreboard)
        self.hiscore.text = 'High Score' +'\n'+str(self.hiscoreboard)

        #To start background song when the game is opened
        self.sound = SoundLoader.load('music.mp3')
        self.sound.volume = 0.03
        self.sound.loop = True
        self.sound.play()

    #Method to refresh the time text shown
    def update(self, *args):
        self.time.text = 'Time' +'\n'+ str(int(round(time.time()-self.newtime,0))) + ' s'

    #Method creates a new array of arrays and randomly changes one of the elements to either 2 or 4 with an equal proba
    def new_game(self):
        board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        a = True
        i = random.randrange(0,4)
        x = random.randrange(0,4)
        board[i][x]=2*random.randrange(1,3)
        start_time = time.time()
        return board,start_time

    #Method that takes in an array(boards) of arrays(i) of numbers(j) and creates a label for each element(j) with different colors for each different value  
    def pop_board(self,boards):
        for i in boards:
            for j in i:
                if j==0:
                    boardtile=Label(text='')
                    self.boardobject.add_widget(boardtile)
                if j==2:
                    boardtile=Label(text=str(j),color=(70/255,194/255,120/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                if j==4:
                    boardtile=Label(text=str(j),color=(86/255, 191/255, 116/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                if j==8:
                    boardtile=Label(text=str(j),color=(102/255, 188/255, 113/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                if j==16:
                    boardtile=Label(text=str(j),color=(117/255, 185/255, 109/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                if j==32:
                    boardtile=Label(text=str(j),color=(133/255,182/255,106/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                if j==64:
                    boardtile=Label(text=str(j),color=(149/255,179/255,102/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                if j==128:
                    boardtile=Label(text=str(j),color=(165/255,176/255,99/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                if j==256:
                    boardtile=Label(text=str(j),color=(180/255,173/255,95/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                if j==512:
                    boardtile=Label(text=str(j),color=(196/255,170/255,2/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                if j==1024:
                    boardtile=Label(text=str(j),color=(212/255,167/255,88/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                if j==2048:
                    boardtile=Label(text=str(j),color=(255/255,251/255,189/255,1),font_size='36sp')
                    self.boardobject.add_widget(boardtile)
                    #Adds a label widget with a text j into the board object

    #code for the reset button to get a new clean board, a new score and a reset on the timer
    def reset(self):
        print("reset")
        self.boardobject.clear_widgets()                        #Clears all previous labels
        newgame = self.new_game()                               #Calls on new game method
        self.gameboard = newgame[0]                             #new game is a tuple where element 0 is a new board 
        self.newtime = newgame[1]                               #and element 1 is the starting time using time module
        self.time.text = 'Time' +'\n'+str(int(round(time.time()-self.newtime,0)))  +' s'  #sets the timer display to the new start time
        self.pop_board(self.gameboard)                          #calls on populat board method to create a new board based one the new board generated above
        if self.hiscoreboard<self.scoreboard:
            self.hiscoreboard = self.scoreboard
            self.hiscore.text = 'High Score' +'\n'+ str(self.hiscoreboard)
        self.scoreboard = 0
        self.score.text = 'Score' +'\n'+ str(self.scoreboard)

    #Method to constantly keep keyboard inputs open
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self._on_key_down)
        self._keyboard = None

    #Method to receive, process keyboard inputs(accepting {w,a,s,d,up,down,left,right} keys), check game state and update scoreboards
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        print(keycode) #for debugging purposes: keycode is just the code associated with every keyboard key with each having a unique number and calling keycode returning a tuple with (number, text)
        nextmove = self.checknextmove(keycode[0]) #Refers to the checknextmove function(using numerical portion of the keycode) to generate a new gameboard
        self.gameboard = nextmove[0] #Checknextmove method creates a tuple with format (new game board(a list), additional score)
        self.boardobject.clear_widgets() #removes all previous labels to return to a clean state
        self.pop_board(self.gameboard)  #repopulates gameboard with new labels representing new gameboard obtained from Checknextmove function
        
        #Updates current game score
        self.scoreboard +=nextmove[1] #updates score value
        self.score.text ='Score' +'\n'+ str(self.scoreboard) #updates score board
        
        #updates highscore if highscore is broken in current game playthrough
        if self.hiscoreboard<self.scoreboard: 
            self.hiscoreboard = self.scoreboard
            self.hiscore.text = 'High Score' +'\n'+ str(self.hiscoreboard)

        #checks board state to see if win/lose/ongoing at the end of each move
        state = self.check_state(self.gameboard) 
        if state == 'win': 
            print('You Won!')
            time_taken = str(int(round(time.time()-self.newtime,0)))
            popupwindow = Popup(title='Congratulations, 2048 achieved!',content=Label(text='You Won!'+'\n' + 'Your Score  ' +str(self.scoreboard)+'\n' + 'Total Time Taken  ' + time_taken),size_hint=(None,None),size=(500,300))
            
        elif state =='gameover':
            print('Game Over')
            time_taken = str(int(round(time.time()-self.newtime,0)))
            popupwindow = Popup(title='Game Over!',content=Label(text='No more moves!'+'\n' + 'Your Score  ' +str(self.scoreboard)+'\n' + 'Total Time Taken  ' + time_taken),size_hint=(None,None),size=(500,300))
            popupwindow.open()


    #Method to process keyboard inputs or in thie case usrinput whereby usrinput is a number representing any keyboard kkeys
    def checknextmove(self,usrinput):
        newgameboard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        addscore = 0
        print(usrinput)
        # up case accepts both up arrow button and w
        if usrinput == 273 or usrinput == 119:      #up button and w button respectively
            for columns in range(4):
                counter = 0
                for rows in range(4):
                    #checking column by column for a number from top to bottom
                    checkednumber = self.gameboard[rows][columns]
                    if checkednumber!=0: #if a number in the array is not equals 0, it has value and thus will be operated on
                        if counter == 0:
                            newgameboard[0][columns]=checkednumber
                        elif checkednumber == newgameboard[counter-1][columns]:
                            newgameboard[counter-1][columns] *=2
                            addscore+=newgameboard[counter-1][columns]
                            counter-=1
                        else:
                            newgameboard[counter][columns]=checkednumber
                        counter +=1
            print('up') #for debugging purposes
            if newgameboard != self.gameboard: #if up has been triggered but there is no change, just generate the same board again
                self.addnewnum(newgameboard)
            return newgameboard, addscore         

        # down case accepts both down arrow button and s
        if usrinput == 274 or usrinput == 115:      
            for columns in range(4):
                counter = 3
                for rows in range(3,-1,-1):
                    #checking column by column from bottom to top
                    checkednumber = self.gameboard[rows][columns]
                    if checkednumber!=0:
                        if counter == 3:
                            newgameboard[counter][columns]=checkednumber
                        elif checkednumber == newgameboard[counter+1][columns]:
                            newgameboard[counter+1][columns] *=2
                            addscore += newgameboard[counter+1][columns]
                            counter+=1
                        else:
                            newgameboard[counter][columns]=checkednumber
                        counter -=1
            print('down')
            if newgameboard != self.gameboard:
                self.addnewnum(newgameboard)
            return newgameboard, addscore 
    
        # right case accepts both d and right arrow
        if usrinput == 100 or usrinput == 275: 
            for rows in range(4):
                counter = 3
                for columns in range(3,-1,-1):
                    #checking row by row from right to left
                    checkednumber = self.gameboard[rows][columns]
                    if checkednumber!=0:
                        if counter == 3:
                            newgameboard[rows][counter]=checkednumber
                        elif checkednumber == newgameboard[rows][counter+1]:
                            newgameboard[rows][counter+1] *=2
                            addscore+=newgameboard[rows][counter+1]
                            counter+=1
                        else:
                            newgameboard[rows][counter]=checkednumber
                        counter -=1
            print('right')
            if newgameboard != self.gameboard:
                self.addnewnum(newgameboard)
            return newgameboard, addscore
        
        # left case accepts both a and left arrow
        if usrinput == 276 or usrinput == 97:     
            for rows in range(4):
                counter = 0
                for columns in range(4):
                    #checking row by row from left to right
                    checkednumber = self.gameboard[rows][columns]
                    if checkednumber!=0:
                        if counter == 0:
                            newgameboard[rows][counter]=checkednumber
                        elif checkednumber == newgameboard[rows][counter-1]:
                            newgameboard[rows][counter-1] *=2
                            addscore+=newgameboard[rows][counter-1]
                            counter-=1
                        else:
                            newgameboard[rows][counter]=checkednumber
                        counter +=1
            print('left')
            if newgameboard != self.gameboard:
                self.addnewnum(newgameboard)
            return newgameboard, addscore    
        else: # if none of the buttons that are accepted is inputted, dont exit the window, just return the same window
            return self.gameboard, addscore

    #Method to check state of board and determine the next state of the board
    def check_state(self,board):
        for i in range(4):
            for j in range(4):
                if board[i][j] == 2048: #If there is a tile with 2048 value, the person has won
                    return 'win'
                if board[i][j] == 0:    #else if there is no 2048, if there is a free tile, the game is not over, and is thus ongoing
                    return 'ongoing1'  #returns ongoing1 for debugging purposes

        #if above conditions are not met, check if there are same values side by side, allowing for a move and thus game is not over
        for i in range(3):
            for j in range(3):
                if board[i][j]==board[i][j+1] or board[i][j]==board[i+1][j]: 
                    return 'ongoing2'
            if board[3][i]==board[3][i+1] or board[i][3]==board[i+1][3]:
                return 'ongoing3'
        #if all above conditions are not met, then the game is over as there are no more moves left
        return 'gameover'            

    #method to add a new 2 or 4 with equal possibility in a random position on the board
    def addnewnum(self,board):
        i = random.randrange(0,4)
        x = random.randrange(0,4)
        while board[i][x]!=0:
            i = random.randrange(0,4)
            x = random.randrange(0,4)
        board[i][x]=2*random.randrange(1,3)

#Running app which runs a widget
class TwentyFourtyEightApp(App):
    def build(self):
        return MainGame()

#Running app    
if __name__ == '__main__':
    TwentyFourtyEightApp().run()