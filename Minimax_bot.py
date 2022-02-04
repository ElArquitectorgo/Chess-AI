import pygame, sys, random
from pygame.locals import *
from Tree import *
from Random_bot import *

class Minimax_bot():
    def __init__(self, game, color):
        self.game = game
        self.color = color
        self.predict = None

    def generate_move(self):
        self.evaluate_pieces()
        if self.pos == None:
            return self.game.bots()
            
        for sprite in self.game.all_sprites:
            if sprite.x == self.pos[0] and sprite.y == self.pos[1]:
                self.game.curr_sprite = sprite
        self.game.curr_pos_x = self.pos[0]
        self.game.curr_pos_y = self.pos[1]
        self.game.generate_move(self.predict[0], self.predict[1])

    def evaluate_pieces(self):
        max_val = self.game.evaluate("WHITE")
        self.pos = None
        for b_sprite in self.game.all_sprites:
            if b_sprite.color == self.color:
                tree = Tree(b_sprite)
                b_valid_moves = self.game.get_valid_moves(b_sprite)
                pos = b_sprite.x, b_sprite.y
                for move in b_valid_moves:
                    self.game.curr_sprite = b_sprite
                    self.game.curr_pos_x = b_sprite.x
                    self.game.curr_pos_y = b_sprite.y
                    self.game.generate_move(move[0], move[1])
                    #tree.insert(b_sprite, self.game.tablero)
                    evaluation = self.game.evaluate("WHITE")
                    print(evaluation, b_sprite)
                    if evaluation < max_val:
                        max_val = evaluation
                        self.pos = pos
                        self.predict = move[0], move[1]

                    self.game.set_tablero(self.game.chess_position_dict[self.game.turn - 1])
