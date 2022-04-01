
class IA():
    def __init__(self, game, color, level=1):
        self.game = game
        self.color = color
        self.level = level
        self.p = 0

    def make_move(self, cnt):
        if cnt == 0:
            return 1

        num_positions = 0
        for sprite in self.game.pieces:
            if sprite.color == self.color and sprite.alive:
                valid_moves = self.game.get_valid_moves(sprite)
                for move in valid_moves:                    
                    if move[1] == 0 and hasattr(sprite, "promoted") and sprite.promoted[0] == False or move[1] == 7 and hasattr(sprite, "promoted") and sprite.promoted[0] == False:
                        for i in range(4):
                            self.game.make_move(sprite, move[0], move[1], i)
                            self.change_color()

                            num_positions += self.make_move(cnt - 1)

                            self.game.unmake_move()
                            self.change_color()
                    else:        
                        self.game.make_move(sprite, move[0], move[1])

                        self.change_color()

                        num_positions += self.make_move(cnt - 1)

                        self.game.unmake_move()
                        self.change_color()

        return num_positions

    def change_color(self):
        if self.color == "WHITE":
            self.color = "BLACK"
        else:
            self.color = "WHITE"

    def evaluate(self):
        evaluation = 0

        for sprite in self.game.all_sprites:
            evaluation += sprite.value

        return evaluation