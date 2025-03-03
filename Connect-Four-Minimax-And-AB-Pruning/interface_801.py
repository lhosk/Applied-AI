# UNC Charlotte 
# ITCS 5153 - Applied AI - Spring 2025 
# Lab 3 
# Adversarial Search / Game Playing 
# This module implements the interface/GUI
# Student ID: 801


import os
import pygame as pg
import random


# Creating the GUI
class Interface(object):
    # Initialize GUI
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.init()
        pg.display.set_caption("Connect Four")
        self.x = 800
        self.y = 950
        self.screen = pg.display.set_mode((self.x, self.y))
        self.mode = "INITIAL"

        # Designating positions of buttons
        self.game_pos = pg.Rect(50, 300, 700, 600)
        self.new_game_pos = pg.Rect(50, 50, 175, 200)
        self.restart_pos = pg.Rect(250, 50, 150, 200)
        self.exit_pos = pg.Rect(425, 50, 125, 200)
        self.turn_pos = pg.Rect(575, 50, 175, 200)
        
        # Designating fonts, colors, sizes
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.yellow = (255, 255, 0)
        self.red = (255, 0, 0)
        self.font = pg.font.Font(None, 36)
        self.width = 10

        # Create minimax and ab_pruning buttons
        self.minimax_box = pg.Rect(50, 250, 175, 100)
        self.ab_pruning_box = pg.Rect(50, 350, 175, 100)


    # Creating Connect 4 game visuals
    def base_display(self):
        # Draw game board
        pg.draw.rect(self.screen, self.white, self.game_pos, self.width)
        for i in range(6):
            pg.draw.line(self.screen, self.white, (150+100*i, 300), (150+100*i, 900), self.width)
        for i in range(5):
            pg.draw.line(self.screen, self.white, (50, 400+100*i), (750, 400+100*i), self.width)
            
        # Draw new game, restart, and exit buttons, alongside whose turn it is
        pg.draw.rect(self.screen, self.white, self.new_game_pos, self.width)
        pg.draw.rect(self.screen, self.white, self.restart_pos, self.width)
        pg.draw.rect(self.screen, self.white, self.exit_pos, self.width)
        pg.draw.rect(self.screen, self.white, self.turn_pos, self.width)

        # Write text on buttons
        self.write_text('New Game', self.new_game_pos)
        self.write_text('Restart', self.restart_pos)
        self.write_text('Exit', self.exit_pos)


    # Draw moves onto board
    def draw_move(self, row, column, move_type):
        if move_type == 'player':
            circle_color = self.red
        else: # move_type == 'AI'
            circle_color = self.yellow
        center_circle_x = column * 100 + 100
        center_circle_y = abs(row) * 100 + 350
        pg.draw.circle(self.screen, circle_color, (center_circle_x, center_circle_y), 50, self.width)

    
    # Write text in middle of buttons
    def write_text(self, text, rect, text_color= None):
        if text_color == None:
            text_color = self.white
        surface = self.font.render(text, True, text_color)
        surf_rect = surface.get_rect(center=rect.center)
        self.screen.blit(surface, surf_rect)


    # Choose the AI when "New Game" is clicked
    def display_choice(self):
        # Making the minimax button
        pg.draw.rect(self.screen, self.black, self.minimax_box)
        pg.draw.rect(self.screen, self.white, self.minimax_box, self.width)

        # # Making the ab_pruning button
        pg.draw.rect(self.screen, self.black, self.ab_pruning_box)
        pg.draw.rect(self.screen, self.white, self.ab_pruning_box, self.width)
        self.write_text('Minimax', self.minimax_box)
        self.write_text('AB Pruning', self.ab_pruning_box)
        pg.display.update()


    # Choosing AI when respective buttons are clicked
    def choose_AI(self, area_clicked, last_ai = None):
        random_choice = False

        if self.minimax_box.collidepoint(area_clicked):
            return 'minimax', False
        elif self.ab_pruning_box.collidepoint(area_clicked):
            return 'ab_pruning', False
        else:
            ai_chosen = random.choice(['minimax', 'ab_pruning'])
            random_choice = True
            return ai_chosen, random_choice


    # Displays a message for the winner or if drawn
    def display_win(self, winner, win = False):
        popup_box = pg.Rect((self.x - 250) // 2, (self.y - 250) // 2, 250, 250)
        pg.draw.rect(self.screen, self.black, popup_box)
        pg.draw.rect(self.screen, self.white, popup_box, self.width)

        if win:
            message = (f'{winner} Wins!')
        else:
            message = 'DRAW'

        self.write_text(message, popup_box, self.white)
        pg.display.update() 


    # Draws which AI is being used
    def write_AI(self, AI, random_choice = False):
        box = pg.Rect(350, 250, 100, 50)

        if AI == 'ab_pruning':
            message = 'AI is Alpha-Beta Pruning'
        else:
            message = 'AI is MiniMax'

        if random_choice:
            message = message + ' (Chosen randomly)'
        self.write_text(message, box, self.white)

        pg.display.update()


    # Updates game state visuals
    def update_display(self, board, player_turn = None):
        self.screen.fill((0,0,255))
        self.base_display()
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] is not None:
                    player_type = board[row][col]
                    self.draw_move(row, col, player_type)
        
        if player_turn == 'player':
            turn_text = "Your turn"
            turn_color = self.red
        else:
            turn_text = "AI's Turn"
            turn_color = self.yellow
        self.write_text(turn_text, self.turn_pos, turn_color)

        if self.mode == 'RUN':
            pass
        pg.display.update()
            

    # Close game
    def close_display(self):
        pg.quit()