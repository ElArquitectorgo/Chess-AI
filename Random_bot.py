import pygame, sys, random
from pygame.locals import *

class Random_bot():
    def __init__(self, game):
        self.game = game

    def generate_move(self):
        selected = False
        cnt = 0
        while not selected and not self.game.mate:
            sprite = pygame.sprite.Group.sprites(self.game.all_sprites)[random.randint(0, len(pygame.sprite.Group.sprites(self.game.all_sprites)) - 1)]
            if self.game.turn % 2 == 0 and sprite.color == "BLACK" or self.game.turn % 2 == 1 and sprite.color == "WHITE":
                self.game.curr_sprite = sprite
                self.game.curr_pos_x = sprite.x
                self.game.curr_pos_y = sprite.y
                valid_moves = self.game.get_valid_moves(sprite)
                if valid_moves:
                    choice = random.choice(valid_moves)
                    self.game.generate_move(choice[0], choice[1])
                    selected = True
            cnt += 1
            if cnt > 1000:
                break
        if cnt > 1000:
            print("Seguramente el rey esté ahogado")
            print(self.game.tablero)