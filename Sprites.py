
from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, game, color, x, y):
        self.game = game
        self.color = color
        self.x = x
        self.y = y
        self.alive = True

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def get_valid_moves(self):
        pass

class Pawn(Piece):
    def __init__(self, game, color, x, y):
        super().__init__(game, color, x, y)
        self.name = "P"
        self.promoted = [False, None, None]

        if (color == "WHITE"):
            self.image = game.img_pawn_w
            self.value = 10
        if (color == "BLACK"):
            self.image = game.img_pawn_b
            self.value = -10

    def is_comible(self, sprite):
        tablero = self.game.chess_position_dict[self.game.turn - 1][0]

        if tablero[1][int(sprite.x)] == "Pb" and int(sprite.y) == 3 and tablero[3][int(sprite.x)] != "Pb":
            return True
        if tablero[6][int(sprite.x)] == "Pw" and int(sprite.y) == 4 and tablero[4][int(sprite.x)] != "Pw":
            return True
        
        return False

    def get_valid_moves(self, x, y):
        if self.promoted[0]:
            if self.promoted[1] == 0:
                return Queen.get_valid_moves(self, x, y)
            elif self.promoted[1] == 1:
                return Rook.get_valid_moves(self, x, y)
            elif self.promoted[1] == 2:
                return Knight.get_valid_moves(self, x, y)
            elif self.promoted[1] == 3:
                return Bishop.get_valid_moves(self, x, y)

        self.valid_moves = list()
        if (self.color == "WHITE"):
            if (y - 1 >= 0 and self.game.tablero[x][y - 1] == ""):
                if (y - 1 >= 0):
                    self.valid_moves.append((x, y - 1))
                if (y == 6 and self.game.tablero[x][y - 2] == ""):
                    self.valid_moves.append((x, y - 2))
            if (y - 1 >= 0 and x - 1 >= 0 and not self.game.tablero[x - 1][y - 1] == ""):
                self.valid_moves.append((x - 1, y - 1))
            if (y - 1 >= 0 and x + 1 < 8 and not self.game.tablero[x + 1][y - 1] == ""):
                self.valid_moves.append((x + 1, y - 1))
            # Al paso
            if self.y == 3:
                for sprite in self.game.pieces:
                    if sprite.name != "P":
                        continue
                    elif self.x > 0 and sprite.x == x - 1 and sprite.y == y:
                        if self.is_comible(sprite):
                            self.valid_moves.append((x - 1, y - 1))

                    elif self.x < 7 and sprite.x == x + 1 and sprite.y == y:
                        if self.is_comible(sprite):
                            self.valid_moves.append((x + 1, y - 1))
        else:
            if (y + 1 < 8 and self.game.tablero[x][y + 1] == ""):
                if (y + 1 < 8):
                    self.valid_moves.append((x, y + 1))
                if (y == 1 and self.game.tablero[x][y + 2] == ""):
                    self.valid_moves.append((x, y + 2))
            if (y + 1 < 8 and x - 1 >= 0 and not self.game.tablero[x - 1][y + 1] == ""):
                self.valid_moves.append((x - 1, y + 1))
            if (y + 1 < 8 and x + 1 < 8 and not self.game.tablero[x + 1][y + 1] == ""):
                self.valid_moves.append((x + 1, y + 1))
            # Al paso
            if self.y == 4:
                for sprite in self.game.pieces:
                    if sprite.name != "P":
                        continue
                    elif self.x > 0 and sprite.x == x - 1 and sprite.y == y:
                        if self.is_comible(sprite):
                            self.valid_moves.append((x - 1, y + 1))

                    elif self. x < 7 and sprite.x == x + 1 and sprite.y == y:
                        if self.is_comible(sprite):
                            self.valid_moves.append((x + 1, y + 1))
                                
        return self.game.get_real_valid_moves(self.color, self.valid_moves)

class Bishop(Piece):
    def __init__(self, game, color, x, y):
        super().__init__(game, color, x, y)
        self.name = "B"
        if (color == "WHITE"):
            self.image = game.img_bishop_w
            self.value = 30
        if (color == "BLACK"):
            self.image = game.img_bishop_b
            self.value = -30

    def get_valid_moves(self, x, y):
        self.valid_moves = list()
        #Abajo derecha
        i = x + 1
        j = y + 1
        while (i < 8 and j < 8 and self.game.tablero[i][j] == ""):
            self.valid_moves.append((i, j))
            i += 1
            j +=1
        if (i < 8 and j < 8 and not self.game.is_same_color(self.color, i, j)):
            self.valid_moves.append((i, j))
        #Abajo izquierda
        i = x - 1
        j = y + 1;
        while (i > 0 and j < 8 and self.game.tablero[i][j] == ""):
            self.valid_moves.append((i, j))
            i -= 1
            j += 1
        if (i >= 0 and j < 8 and not self.game.is_same_color(self.color, i, j)):
            self.valid_moves.append((i, j))
        #Arriba derecha
        i = x + 1
        j = y - 1
        while (i < 8 and j > 0 and self.game.tablero[i][j] == ""):
            self.valid_moves.append((i, j))
            i += 1
            j -= 1
        if (i < 8 and j >= 0 and not self.game.is_same_color(self.color, i, j)):
            self.valid_moves.append((i, j))
        #Arriba izquierda
        i = x - 1 
        j = y - 1
        while (i > 0 and j > 0 and self.game.tablero[i][j] == ""):
            self.valid_moves.append((i, j))
            i -= 1 
            j -= 1
        if (i >= 0 and j >= 0 and not self.game.is_same_color(self.color, i, j)):
            self.valid_moves.append((i, j))
        return self.valid_moves

class Knight(Piece):
    def __init__(self, game, color, x, y):
        super().__init__(game, color, x, y)
        self.name = "N"
        if (color == "WHITE"):
            self.image = game.img_knight_w
            self.value = 30
        if (color == "BLACK"):
            self.image = game.img_knight_b
            self.value = -30

    def get_valid_moves(self, x, y):
        self.valid_moves = list()
        #Arriba izquierda
        if (x - 1 >= 0 and y - 2 >= 0):
            self.valid_moves.append((x - 1, y - 2))
        if (x - 2 >= 0 and y - 1 >= 0):
            self.valid_moves.append((x - 2, y - 1))
        #Arriba derecha
        if (x + 1 < 8 and y - 2 >= 0):
            self.valid_moves.append((x + 1, y - 2))
        if (x + 2 < 8 and y - 1 >= 0):
            self.valid_moves.append((x + 2, y - 1))
        #Abajo izquierda
        if (x - 1 >= 0 and y + 2 < 8):
            self.valid_moves.append((x - 1, y + 2))
        if (x - 2 >= 0 and y + 1 < 8):
            self.valid_moves.append((x - 2, y + 1))
        #Abajo derecha
        if (x + 1 < 8 and y + 2 < 8):
            self.valid_moves.append((x + 1, y + 2))
        if (x + 2 < 8 and y + 1 < 8):
            self.valid_moves.append((x + 2, y + 1))
        return self.game.get_real_valid_moves(self.color, self.valid_moves)

class Rook(Piece):
    def __init__(self, game, color, x, y):
        super().__init__(game, color, x, y)
        self.name = "R"
        self.castling = True
        if (color == "WHITE"):
            self.image = game.img_rook_w
            self.value = 50
        if (color == "BLACK"):
            self.image = game.img_rook_b
            self.value = -50

    def get_valid_moves(self, x, y):
        self.valid_moves = list()
        self.left_closer_piece = (0, y)
        self.right_closer_piece = (7, y)
        self.up_closer_piece = (x, 0)
        self.down_closer_piece = (x, 7)
        r = False; d = False
        
        for i in range(8):
            if (self.game.tablero[i][y] != ""):
                if (i < x):
                    self.left_closer_piece = (i, y)
                elif (i > x and not r):
                    self.right_closer_piece = (i, y)
                    r = True
            if (self.game.tablero[x][i] != ""):
                if (i < y):
                    self.up_closer_piece = (x, i)
                elif (i > y and not d):
                    self.down_closer_piece = (x, i)
                    d = True

        for i in range(self.left_closer_piece[0], self.right_closer_piece[0] + 1):
            if (i != x and not self.game.is_same_color(self.color, i, y)):
                self.valid_moves.append((i, y))
        for j in range(self.up_closer_piece[1], self.down_closer_piece[1] + 1):
            if (j != y and not self.game.is_same_color(self.color, x, j)):
                self.valid_moves.append((x, j))
        #self.valid_moves = self.game.getRealValidMoves(self.color, self.valid_moves)
        return self.valid_moves

class King(Piece):
    def __init__(self, game, color, x, y):
        super().__init__(game, color, x, y)
        self.name = "K"
        self.castling_turn = None
        if (color == "WHITE"):
            self.image = game.img_king_w
            self.value = 900
        if (color == "BLACK"):
            self.image = game.img_king_b
            self.value = -900

    def get_valid_moves(self, x, y):
        self.valid_moves = list()
        #Arribas
        if (x - 1 >= 0 and y - 1 >= 0):
            self.valid_moves.append((x - 1, y - 1))
        if (y - 1 >= 0):
            self.valid_moves.append((x, y - 1))
        if (x + 1 < 8 and y - 1 >= 0):
            self.valid_moves.append((x + 1, y - 1))
        #Abajos
        if (x - 1 >= 0 and y + 1 < 8):
            self.valid_moves.append((x - 1, y + 1))
        if (y + 1 < 8):
            self.valid_moves.append((x, y + 1))
        if (x + 1 < 8 and y + 1 < 8):
            self.valid_moves.append((x + 1, y + 1))
        #Horizontal
        if (x - 1 >= 0):
            self.valid_moves.append((x - 1, y))
        if (x + 1 < 8):
            self.valid_moves.append((x + 1, y))
        #Enroque
        if self.castling_turn is None:
            if self.color == "WHITE":
                for sprite in self.game.pieces:
                    if sprite.x == 0 and sprite.y == 7 and sprite.image == self.game.img_rook_w:
                        if self.game.tablero[1][7] == "" and self.game.tablero[2][7] == "" and self.game.tablero[3][7] == "":
                            self.valid_moves.append((2, 7))
                    if sprite.x == 7 and sprite.y == 7 and sprite.image == self.game.img_rook_w:
                        if self.game.tablero[6][7] == "" and self.game.tablero[5][7] == "":
                            self.valid_moves.append((6, 7))
            else:
                for sprite in self.game.pieces:
                    if sprite.x == 0 and sprite.y == 0 and sprite.image == self.game.img_rook_b:
                        if self.game.tablero[1][0] == "" and self.game.tablero[2][0] == "" and self.game.tablero[3][0] == "":
                            self.valid_moves.append((2, 0))
                    if sprite.x == 7 and sprite.y == 0 and sprite.image == self.game.img_rook_b:
                        if self.game.tablero[6][0] == "" and self.game.tablero[5][0] == "":
                            self.valid_moves.append((6, 0))
                            
        return self.game.get_real_valid_moves(self.color, self.valid_moves)

class Queen(Piece):
    def __init__(self, game, color, x, y):
        super().__init__(game, color, x, y)
        self.name = "Q"
        if (color == "WHITE"):
            self.image = game.img_queen_w
            self.value = 90
        if (color == "BLACK"):
            self.image = game.img_queen_b
            self.value = -90

    def get_valid_moves(self, x, y):
        self.valid_moves = list()
        self.left_closer_piece = (0, y)
        self.right_closer_piece = (7, y)
        self.up_closer_piece = (x, 0)
        self.down_closer_piece = (x, 7)
        r = False; d = False
        
        for i in range(8):
            if (self.game.tablero[i][y] != ""):
                if (i < x):
                    self.left_closer_piece = (i, y)
                elif (i > x and not r):
                    self.right_closer_piece = (i, y)
                    r = True
            if (self.game.tablero[x][i] != ""):
                if (i < y):
                    self.up_closer_piece = (x, i)
                elif (i > y and not d):
                    self.down_closer_piece = (x, i)
                    d = True

        for i in range(self.left_closer_piece[0], self.right_closer_piece[0] + 1):
            if (i != x and not self.game.is_same_color(self.color, i, y)):
                self.valid_moves.append((i, y))
        for j in range(self.up_closer_piece[1], self.down_closer_piece[1] + 1):
            if (j != y and not self.game.is_same_color(self.color, x, j)):
                self.valid_moves.append((x, j))
        #Abajo derecha
        i = x + 1
        j = y + 1
        while (i < 8 and j < 8 and self.game.tablero[i][j] == ""):
            self.valid_moves.append((i, j))
            i += 1
            j +=1
        if (i < 8 and j < 8 and not self.game.is_same_color(self.color, i, j)):
            self.valid_moves.append((i, j))
        #Abajo izquierda
        i = x - 1
        j = y + 1;
        while (i > 0 and j < 8 and self.game.tablero[i][j] == ""):
            self.valid_moves.append((i, j))
            i -= 1
            j += 1
        if (i >= 0 and j < 8 and not self.game.is_same_color(self.color, i, j)):
            self.valid_moves.append((i, j))
        #Arriba derecha
        i = x + 1
        j = y - 1
        while (i < 8 and j > 0 and self.game.tablero[i][j] == ""):
            self.valid_moves.append((i, j))
            i += 1
            j -= 1
        if (i < 8 and j >= 0 and not self.game.is_same_color(self.color, i, j)):
            self.valid_moves.append((i, j))
        #Arriba izquierda
        i = x - 1 
        j = y - 1
        while (i > 0 and j > 0 and self.game.tablero[i][j] == ""):
            self.valid_moves.append((i, j))
            i -= 1 
            j -= 1
        if (i >= 0 and j >= 0 and not self.game.is_same_color(self.color, i, j)):
            self.valid_moves.append((i, j))
        return self.valid_moves
        