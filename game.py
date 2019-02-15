
from tkinter import *
import time
import random

def game():
    def close():
        root.destroy()

    def playagain():
        close()
        game()

        
    class Ball:
        def __init__(self,canvas,paddle,score,color):
            self.canvas=canvas
            self.paddle=paddle
            self.score=score
            self.id=canvas.create_oval(10,10,25,25,fill=color)
            self.canvas.move(self.id,245,100)

            starts = [-3, -2, -1, 1, 2, 3]
            random.shuffle(starts)
            self.x = starts[0]
            self.y = -3

            self.canvas_height=self.canvas.winfo_height()       # height of canvas
            self.canvas_width = self.canvas.winfo_width()
            self.hit_bottom=False

        def hit_paddle(self,pos):
            paddle_position=self.canvas.coords(self.paddle.id)              #checks the contact between ball and paddle
            if pos[2]>=paddle_position[0] and pos[0]<=paddle_position[2]:
                if pos[3]>=paddle_position[1] and pos[3]<=paddle_position[3]:
                    self.score.increase()
                    return True
            return False

        def draw(self):
            self.canvas.move(self.id,self.x,self.y)
            pos=self.canvas.coords(self.id)             #position of ball (tuple) 

            if pos[1]<=0:
                self.y=3
            if pos[3]>=self.canvas_height:              # ball bounces up and down
                self.hit_bottom=True
            if self.hit_paddle(pos):
                self.y=-3
            if pos[0]<=0:
                self.x=3
            if pos[2]>=self.canvas_width:
                self.x=-3
                #print(pos)

    class Paddle:
        def __init__(self,canvas,color):
            self.canvas=canvas
            self.id=canvas.create_rectangle(0,0,100,10,fill=color)
            self.canvas.move(self.id,200,300)
            self.x=0
            self.canvas_width=self.canvas.winfo_width()

            self.started=False
            self.canvas.bind_all('<KeyPress-Up>',self.start_game)
            self.canvas.bind_all('<KeyPress-Left>',self.move_left)
            self.canvas.bind_all('<KeyPress-Right>',self.move_right)

                    
        def move_left(self,evt):
            self.x=-3
            pos=self.canvas.coords(self.id)
            if pos[0]<=0:
                self.x=0

        def move_right(self,evt):
            self.x=3
            pos=self.canvas.coords(self.id)
            if pos[2]>= self.canvas_width:
                self.x=0

        def start_game(self,evt):
            self.started=True



        def draw(self):
            self.canvas.move(self.id,self.x,0)
                
            pos=self.canvas.coords(self.id)
            if pos[0]<=0:
                self.x=0
            elif pos[2]>= self.canvas_width:
                self.x=0

    class Score:
        def __init__(self,canvas,color):
            self.score=0
            self.canvas=canvas
            self.id=canvas.create_text(250,10,text='Score:'+str(self.score),fill=color,font=('Helvetica',20))
        def increase(self):
            self.score+=5
            self.canvas.itemconfig(self.id,text='Score:'+str(self.score))
     
    root=Tk()
    root.title("Bounce")
    root.resizable(0,0)
    root.wm_attributes("-topmost",1)    
        
    canvas=Canvas(root,width=500,height=400,bg='black')
    canvas.pack()
    root.update()


    score=Score(canvas,'yellow')
    paddle=Paddle(canvas,'red')
    ball=Ball(canvas,paddle,score,'blue')
    game_over_text = canvas.create_text(250, 200, text='GAME OVER',fill='yellow',state='hidden')

    quit_qame=Button(root,text='Quit',bg='Black',fg='White',command=close).pack(side='right')
    play_again=Button(root,text='Play again',bg='Black',fg='White',command=playagain).pack(side='right')

    while 1:
        if ball.hit_bottom==False and paddle.started==True:
            ball.draw()
            paddle.draw()
        if ball.hit_bottom == True:
            time.sleep(0.1)
            canvas.itemconfig(game_over_text, state='normal')
            break
        root.update_idletasks()
        root.update()
        time.sleep(0.01)

game()
