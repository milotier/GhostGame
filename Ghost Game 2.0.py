from tkinter import *
from random import randint
import pickle

class MainMenu:
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def show(self):
        self.canvas = Canvas(self.game_controller.window, height = 150, width = 520,)
        self.canvas.pack()
        self.which_gamemode = Label(self.canvas, text = 'Welcome to the Ghost Game. First choose a game mode: easy, medium or hard?')
        self.which_gamemode.place(x = 1, y = 1)
        self.easy_mode = Button(self.canvas, text = 'easy', command = self.set_easy)
        self.medium_mode = Button(self.canvas, text = 'medium', command = self.set_medium)
        self.hard_mode = Button(self.canvas, text = 'hard', command = self.set_hard)
        Button(self.canvas, text = 'quit', command = self.quit_game).place(x = 240, y = 80, width = 75)
        self.easy_mode.place(x = 85, y = 50, width = 75)
        self.medium_mode.place(x = 240, y = 50, width = 75)
        self.hard_mode.place(x = 390, y = 50, width = 75)

    def quit_game(self):
        self.game_controller.window.destroy()

    def set_easy(self):
        self.canvas.destroy()
        self.game_controller.game_mode("easy")
        
    def set_medium(self):
        self.canvas.destroy()
        self.game_controller.game_mode("medium")
        
    def set_hard(self):
        self.canvas.destroy()
        self.game_controller.game_mode("hard")

class Game:
    def __init__(self, game_controller):
        self.game_controller = game_controller
        self.score = 0

    def reset_score(self):
        self.score = 0
        self.play()
    
    def set_game_mode(self, game_mode):
        self.game_mode = game_mode
        
    def play(self):
        self.canvas = Canvas(self.game_controller.window, height = 150, width = 520)
        self.canvas.pack()
        Label(self.canvas, text = "Behind one of the doors is a ghost!").place(x = 150, y = 1)
        Label(self.canvas, text = "Which one will you choose?").place(x = 175, y = 20)

        if self.game_mode == "easy":
            self.door_quantity = 5
        elif self.game_mode == "medium":
            self.door_quantity = 4
        else:
            self.door_quantity = 3

        self.door_buttons = []
        for door_num in range(1, self.door_quantity + 1):
            door_func = lambda num = door_num: self.door_choice(num)
            button = Button(self.canvas, text = 'door ' + str(door_num), command = door_func)
            button.place(x = 350 / self.door_quantity * door_num, y = 55)
            self.door_buttons.append(button)
       
    def door_choice(self, door_num):
        for button in self.door_buttons:
            button.config(state = DISABLED)
        
        self.ghost_door = randint(1, self.door_quantity)
        if self.ghost_door == door_num:
            Label(self.canvas, text = 'Ghost!').place(x = 235, y = 80)
            label = Label(self.canvas, text = 'Run away!')
            label.place(x = 225, y = 100)
            label.after(2000, self.to_game_over)
 
        else:
            Label(self.canvas, text = "No Ghost!").place(x = 225, y = 80)
            label = Label(self.canvas, text = 'You enter the next room.')
            label.place(x = 185, y = 100)
            label.after(2000, self.next_room)

    def next_room(self):   
        self.score += 1
        self.canvas.destroy()
        self.play()

    def to_game_over(self):
        self.canvas.destroy()
        self.game_controller.player_score(self.score)


class Game_Over:
    def __init__(self, game_controller):
        self.game_controller = game_controller
        self.player_list = []

    def to_main_menu(self):
        self.canvas.destroy()
        self.game_controller.run()

    def retry(self):
        self.canvas.destroy()
        self.game_controller.retry()

    def highscore_screen(self, name, score):
        self.canvas.destroy()
        self.canvas = Canvas(self.game_controller.window, height = 150, width = 520)
        self.canvas.pack()

        pickle_in = open('Ghost Game.hs', 'rb')
        self.player_list = pickle.load(pickle_in)

        self.player_list.append((name, score))
        self.player_list = sorted(self.player_list, key = lambda player: player[1], reverse = True)
        if len(self.player_list) > 5:
            del self.player_list[-1]
        pickle_out = open('Ghost Game.hs', 'wb')
        pickle.dump(self.player_list, pickle_out)
        pickle_out.close()
        player_num = 0
        for player in self.player_list:
            player_num += 1
            Label(self.canvas, text = player[0]).place(x = 210, y = 20 * player_num - 10)
            Label(self.canvas, text = str(player[1])).place(x = 285, y = 20 * player_num - 10)
        Button(self.canvas, text = 'to main menu', command = self.to_main_menu).place(x = 125, y = 100)
        Button(self.canvas, text = 'retry', command = self.retry).place(x = 300, y = 100)

    def get_name(self, score):
        self.name = self.entry.get()
        if self.name == '':
            label = Label(self.canvas, text = 'Hey, you HAVE to enter a name.')
            label.place(x = 180, y = 130)
            label.after(3000, label.destroy)
        else:
            self.highscore_screen(self.name, score)
        
    def game_over_screen(self, score):
        self.canvas = Canvas(self.game_controller.window, height = 500, width = 500,)
        self.canvas.pack()
        Label(self.canvas, text = 'Game over!').place(x = 225, y = 1)
        if score == 1:
            Label(self.canvas, text = 'You scored ' + str(score) + ' point.').place(x = 200, y = 20)
        else:
            Label(self.canvas, text = 'You scored ' + str(score) + ' points.').place(x = 200, y = 20)
        Label(self.canvas, text = 'Please enter your name here.').place(x = 170, y = 50)
        self.entry = Entry(self.canvas)
        self.entry.place(x = 175, y = 70)
        to_get_name = lambda player_score = score: self.get_name(player_score)
        Button(self.canvas, text = 'done', command = to_get_name).place(x = 235, y = 100)
               
class GameController:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('520x150')
        self.window.title('Ghost Game')
        self.main_menu = MainMenu(self)
        self.game = Game(self)
        self.game_over = Game_Over(self)

    def run(self):
        self.main_menu.show()

    def game_mode(self, game_mode):
        self.game.set_game_mode(game_mode)
        self.game.play()

    def player_score(self, score):
        self.game_over.game_over_screen(score)
    
    def retry(self):
        self.game.reset_score()

game = GameController()
game.run()

