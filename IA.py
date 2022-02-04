
class IA():
    def __init__(self, game, color, level=1):
        self.game = game
        self.color = color
        self.level = level

    def generate_move(self, cnt):
        #self.game.print_tablero()
        #self.game.draw()
        if cnt == 0:
            return 1

        num_positions = 0
        for sprite in self.game.pieces:
            if sprite.color == self.color and sprite.alive:
                x = sprite.x
                y = sprite.y
                valid_moves = self.game.get_valid_moves(sprite)
                if valid_moves:
                    for move in valid_moves:
                        self.game.generate_move(sprite, move[0], move[1])
                        self.change_color()

                        num_positions += self.generate_move(cnt - 1)

                        self.game.backtrack()
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