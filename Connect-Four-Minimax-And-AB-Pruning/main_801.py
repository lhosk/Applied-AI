# UNC Charlotte 
# ITCS 5153 - Applied AI - Spring 2025 
# Lab 3 
# Adversarial Search / Game Playing 
# This module implements the main program
# Student ID: 801


import pygame as pg
from math import floor
import interface_801 as interface
import solver_801 as solver
import textlog_801 as textlog
import random


# Controls state of the game
class Control:
    # Initialize game display and state    
    def __init__(self):
        self.interface = interface.Interface()
        self.log = textlog.LogGUI()
        self.done = False
        self.Clock = pg.time.Clock()
        self.columns = 7
        self.rows = 6
        self.reset_game(random_turn=True)
        self.choosing_AI = True
        self.selected_AI = None
        self.start = True
        self.log.add_log('Game Initialized')

    # Reset the game state and set AI
    def reset_game(self, random_turn=False):
        self.board = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        if random_turn:
            self.turn = random.choice(['player', 'AI'])
            self.first_turn = self.turn
        else:
            self.turn = self.first_turn
        
        self.game_over = False
        self.game_paused = False
        self.interface.update_display(self.board, player_turn=self.turn)

    # Handles all events in game
    def event_loop(self):
        for event in pg.event.get():
            # AI Selection
            if self.choosing_AI:
                self.interface.display_choice()
                self.selected_AI, self.random_choice = self.wait_for_ai_choice()
                self.choosing_AI = False
                self.interface.update_display(self.board, player_turn=self.turn)
                self.interface.write_AI(self.selected_AI, self.random_choice)

            # Exits program
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.done = True

            # AI Plays move via solver and writes to log
            if self.turn == 'AI' and self.game_over == False:
                ai_column, minutes, seconds, nodes = solver.pick_move(self.selected_AI, self.board)
                

                msg = f'The {self.selected_AI} AI took {minutes} minutes and {seconds} seconds to search through {nodes} nodes and played in column {ai_column}.'
                self.log.add_log(msg)
                self.log.update()
                self.column_click(ai_column)
                pg.display.update()
            
            # When the left mouse button is clicked,
            elif event.type == pg.MOUSEBUTTONDOWN:  
                x, y = event.pos

                # Plays move (if possible)  
                if self.interface.game_pos.collidepoint(event.pos):
                    self.choosing_AI = False
                    self.column_click(floor((event.pos[0] - 50) / 100))

                # Exits game
                elif self.interface.exit_pos.collidepoint(event.pos):
                    self.close_game()

                # Starts a new game (same AI)
                elif self.interface.new_game_pos.collidepoint(event.pos):
                    self.reset_game(random_turn=True)
                    self.choosing_AI = True
                    self.log.add_log(f'New game with {self.selected_AI}')
                    self.log.update()
                    self.interface.display_choice()

                # Restarts the game (lets player choose AI again)
                elif self.interface.restart_pos.collidepoint(event.pos):
                    self.reset_game(random_turn=False)
                    self.log.add_log(f'Restarting game with {self.selected_AI}')
                    self.log.update()
                    self.interface.write_AI(self.selected_AI)
                    

    # Wait for the AI selection (freezes until the user clicks a valid AI choice)
    def wait_for_ai_choice(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    return self.interface.choose_AI(event.pos)  # Return AI choice


    # Check if a player has won
    def check_win(self, player):
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True

        for row in range(self.rows - 3):
            for col in range(self.columns):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        return False


    # Check if the players have drawn
    def check_draw(self):
        return all(cell is not None for cell in self.board[0])


    # Handles player & AI moves
    def column_click(self, column):
        if self.game_over:
            return
        # Go from row=5 down to row=0
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][column] is None:
                self.board[row][column] = self.turn
                self.interface.draw_move(row, column, self.turn)
                self.interface.update_display(self.board)
                self.interface.write_AI(self.selected_AI)
                pg.display.update()

                # Check for win/draw
                if self.check_win(self.turn):
                    self.game_over = True
                    self.interface.display_win(self.turn, True)
                elif self.check_draw():
                    self.game_over = True
                    self.interface.display_win(self.turn)

                else:
                    self.switch_turn()
                break
        else:
            print("Move not playable")  # No empty spots in this column



    # Switch turns between 'player' and 'AI'
    def switch_turn(self):
        self.turn = 'AI' if self.turn == 'player' else 'player'
        self.interface.update_display(self.board, player_turn=self.turn)
        self.interface.write_AI(self.selected_AI)


    # Update game loop
    def game_loop(self):
        while not self.done:
            self.event_loop()
            pg.display.update()
            self.Clock.tick(60)


    # Close game
    def close_game(self):
        pg.quit()
        exit()


# Main function
def main():
    pg.init()
    game = Control()
    game.game_loop()
    game.close_game()


if __name__ == "__main__":
    main()
