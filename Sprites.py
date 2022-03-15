
from abc import ABC, abstractmethod

def get_real_valid_moves(pieces, color, valid_moves):
    """Elimina de la lista dada todas aquellas casillas en las que hay
        una pieza del mismo color que la pieza que llama a este método."""

    valid_moves_copy = valid_moves.copy()
    for pt in valid_moves:
        if is_same_color(pieces, color, pt[0], pt[1]):
            valid_moves_copy.remove(pt)

    return valid_moves_copy

def is_same_color(pieces, color, x, y):
    """Comprueba si la pieza en la posición dada es del mismo color
        que la pieza que llama a este método."""

    for piece in pieces:
        if piece.x == x and piece.y == y:
            if piece.color == color:
                return True
    return False

class Piece(ABC):
    def __init__(self, game, color, image, value, x, y):
        self.game = game
        self.color = color
        self.image = image
        self.value = value
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
    def __init__(self, game, color, image, value, x, y):
        super().__init__(game, color, image, value, x, y)
        self.name = "P"
        self.promoted = [False, None, None]

    def is_comible(self, sprite):
        tablero = self.game.chess_position_dict[self.game.turn - 1][0]

        if tablero[1][int(sprite.x)] == "p" and int(sprite.y) == 3 and tablero[3][int(sprite.x)] != "p":
            return True
        if tablero[6][int(sprite.x)] == "P" and int(sprite.y) == 4 and tablero[4][int(sprite.x)] != "P":
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
        if self.color == "WHITE":
            if y - 1 >= 0 and self.game.tablero[x][y - 1] == "":
                if y - 1 >= 0:
                    self.valid_moves.append((x, y - 1))
                if y == 6 and self.game.tablero[x][y - 2] == "":
                    self.valid_moves.append((x, y - 2))
            if y - 1 >= 0 and x - 1 >= 0 and not self.game.tablero[x - 1][y - 1] == "":
                self.valid_moves.append((x - 1, y - 1))
            if y - 1 >= 0 and x + 1 < 8 and not self.game.tablero[x + 1][y - 1] == "":
                self.valid_moves.append((x + 1, y - 1))
            # Al paso
            if self.y == 3:
                for sprite in self.game.pieces:
                    if sprite.name != "P" or sprite.color == self.color:
                        continue
                    elif self.x > 0 and sprite.x == x - 1 and sprite.y == y:
                        if self.is_comible(sprite):
                            self.valid_moves.append((x - 1, y - 1))

                    elif self.x < 7 and sprite.x == x + 1 and sprite.y == y:
                        if self.is_comible(sprite):
                            self.valid_moves.append((x + 1, y - 1))
        else:
            if y + 1 < 8 and self.game.tablero[x][y + 1] == "":
                if y + 1 < 8:
                    self.valid_moves.append((x, y + 1))
                if y == 1 and self.game.tablero[x][y + 2] == "":
                    self.valid_moves.append((x, y + 2))
            if y + 1 < 8 and x - 1 >= 0 and not self.game.tablero[x - 1][y + 1] == "":
                self.valid_moves.append((x - 1, y + 1))
            if y + 1 < 8 and x + 1 < 8 and not self.game.tablero[x + 1][y + 1] == "":
                self.valid_moves.append((x + 1, y + 1))
            # Al paso
            if self.y == 4:
                for sprite in self.game.pieces:
                    if sprite.name != "P" or sprite.color == self.color:
                        continue
                    elif self.x > 0 and sprite.x == x - 1 and sprite.y == y:
                        if self.is_comible(sprite):
                            self.valid_moves.append((x - 1, y + 1))

                    elif self. x < 7 and sprite.x == x + 1 and sprite.y == y:
                        if self.is_comible(sprite):
                            self.valid_moves.append((x + 1, y + 1))
                                
        return get_real_valid_moves(self.game.pieces, self.color, self.valid_moves)

class Bishop(Piece):
    def __init__(self, game, color, image, value, x, y):
        super().__init__(game, color, image, value, x, y)
        self.name = "B"

    def get_valid_moves(self, x, y):
        self.valid_moves = list()
        #Abajo derecha
        i = x + 1
        j = y + 1
        while i < 8 and j < 8 and self.game.tablero[i][j] == "":
            self.valid_moves.append((i, j))
            i += 1
            j +=1
        if i < 8 and j < 8:
            self.valid_moves.append((i, j))
        #Abajo izquierda
        i = x - 1
        j = y + 1;
        while i > 0 and j < 8 and self.game.tablero[i][j] == "":
            self.valid_moves.append((i, j))
            i -= 1
            j += 1
        if i >= 0 and j < 8:
            self.valid_moves.append((i, j))
        #Arriba derecha
        i = x + 1
        j = y - 1
        while i < 8 and j > 0 and self.game.tablero[i][j] == "":
            self.valid_moves.append((i, j))
            i += 1
            j -= 1
        if i < 8 and j >= 0:
            self.valid_moves.append((i, j))
        #Arriba izquierda
        i = x - 1 
        j = y - 1
        while i > 0 and j > 0 and self.game.tablero[i][j] == "":
            self.valid_moves.append((i, j))
            i -= 1 
            j -= 1
        if i >= 0 and j >= 0:
            self.valid_moves.append((i, j))

        return get_real_valid_moves(self.game.pieces, self.color, self.valid_moves)

class Knight(Piece):
    def __init__(self, game, color, image, value, x, y):
        super().__init__(game, color, image, value, x, y)
        self.name = "N"

    def get_valid_moves(self, x, y):
        self.valid_moves = list()
        #Arriba izquierda
        if x - 1 >= 0 and y - 2 >= 0:
            self.valid_moves.append((x - 1, y - 2))
        if x - 2 >= 0 and y - 1 >= 0:
            self.valid_moves.append((x - 2, y - 1))
        #Arriba derecha
        if x + 1 < 8 and y - 2 >= 0:
            self.valid_moves.append((x + 1, y - 2))
        if x + 2 < 8 and y - 1 >= 0:
            self.valid_moves.append((x + 2, y - 1))
        #Abajo izquierda
        if x - 1 >= 0 and y + 2 < 8:
            self.valid_moves.append((x - 1, y + 2))
        if x - 2 >= 0 and y + 1 < 8:
            self.valid_moves.append((x - 2, y + 1))
        #Abajo derecha
        if x + 1 < 8 and y + 2 < 8:
            self.valid_moves.append((x + 1, y + 2))
        if x + 2 < 8 and y + 1 < 8:
            self.valid_moves.append((x + 2, y + 1))

        return get_real_valid_moves(self.game.pieces, self.color, self.valid_moves)

class Rook(Piece):
    def __init__(self, game, color, image, value, x, y):
        super().__init__(game, color, image, value, x, y)
        self.name = "R"

    def get_valid_moves(self, x, y):
        self.valid_moves = list()
        self.left_closer_piece = (0, y)
        self.right_closer_piece = (7, y)
        self.up_closer_piece = (x, 0)
        self.down_closer_piece = (x, 7)
        r = False; d = False
        
        for i in range(8):
            if self.game.tablero[i][y] != "":
                if i < x:
                    self.left_closer_piece = (i, y)
                elif i > x and not r:
                    self.right_closer_piece = (i, y)
                    r = True
            if self.game.tablero[x][i] != "":
                if i < y:
                    self.up_closer_piece = (x, i)
                elif i > y and not d:
                    self.down_closer_piece = (x, i)
                    d = True

        for i in range(self.left_closer_piece[0], self.right_closer_piece[0] + 1):
            if i != x and not is_same_color(self.game.pieces, self.color, i, y):
                self.valid_moves.append((i, y))
        for j in range(self.up_closer_piece[1], self.down_closer_piece[1] + 1):
            if j != y and not is_same_color(self.game.pieces, self.color, x, j):
                self.valid_moves.append((x, j))

        return self.valid_moves

class King(Piece):
    def __init__(self, game, color, image, value, x, y):
        super().__init__(game, color, image, value, x, y)
        self.name = "K"

    def get_valid_moves(self, x, y):
        self.valid_moves = list()
        #Arribas
        if x - 1 >= 0 and y - 1 >= 0:
            self.valid_moves.append((x - 1, y - 1))
        if y - 1 >= 0:
            self.valid_moves.append((x, y - 1))
        if x + 1 < 8 and y - 1 >= 0:
            self.valid_moves.append((x + 1, y - 1))
        #Abajos
        if x - 1 >= 0 and y + 1 < 8:
            self.valid_moves.append((x - 1, y + 1))
        if y + 1 < 8:
            self.valid_moves.append((x, y + 1))
        if x + 1 < 8 and y + 1 < 8:
            self.valid_moves.append((x + 1, y + 1))
        #Horizontal
        if x - 1 >= 0:
            self.valid_moves.append((x - 1, y))
        if x + 1 < 8:
            self.valid_moves.append((x + 1, y))
        #Enroque
        if self.game.castling != "-":
            for c in self.game.castling:
                if c == "K" and self.color == "WHITE" and self.game.white_rook_ks is not None:
                    if self.game.pieces[self.game.white_rook_ks].x == 7 and self.game.pieces[self.game.white_rook_ks].y == 7:
                        if self.game.tablero[6][7] == "" and self.game.tablero[5][7] == "":
                            self.valid_moves.append((6, 7))
                elif c == "Q" and self.color == "WHITE" and self.game.white_rook_qs is not None:
                    if self.game.pieces[self.game.white_rook_qs].x == 0 and self.game.pieces[self.game.white_rook_qs].y == 7:
                        if self.game.tablero[1][7] == "" and self.game.tablero[2][7] == "" and self.game.tablero[3][7] == "":
                            self.valid_moves.append((2, 7))
                elif c == "k" and self.color == "BLACK" and self.game.black_rook_ks is not None:
                    if self.game.pieces[self.game.black_rook_ks].x == 7 and self.game.pieces[self.game.black_rook_ks].y == 0:
                        if self.game.tablero[6][0] == "" and self.game.tablero[5][0] == "":
                            self.valid_moves.append((6, 0))
                elif c == "q" and self.color == "BLACK" and self.game.black_rook_qs is not None:
                    if self.game.pieces[self.game.black_rook_qs].x == 0 and self.game.pieces[self.game.black_rook_qs].y == 0:
                        if self.game.tablero[1][0] == "" and self.game.tablero[2][0] == "" and self.game.tablero[3][0] == "":
                            self.valid_moves.append((2, 0))

            for piece in self.game.pieces:
                if not piece.alive or piece.name == "K" or piece.color == self.color:
                    continue
                
                v_moves = piece.get_valid_moves(int(piece.x), int(piece.y))
                for move in v_moves:
                    if move[0] == 2 and move[1] == 0 or move[0] == 3 and move[1] == 0:
                        if (2, 0) in self.valid_moves:
                            self.valid_moves.remove((2, 0))
                    if move[0] == 5 and move[1] == 0 or move[0] == 6 and move[1] == 0:
                        if (6, 0) in self.valid_moves:
                            self.valid_moves.remove((6, 0))
                    if move[0] == 2 and move[1] == 7 or move[0] == 3 and move[1] == 7:
                        if (2, 7) in self.valid_moves:
                            self.valid_moves.remove((2, 7))
                    if move[0] == 5 and move[1] == 7 or move[0] == 6 and move[1] == 7:
                        if (6, 7) in self.valid_moves:
                            self.valid_moves.remove((6, 7))
                            
        return get_real_valid_moves(self.game.pieces, self.color, self.valid_moves)

class Queen(Piece):
    def __init__(self, game, color, image, value, x, y):
        super().__init__(game, color, image, value, x, y)
        self.name = "Q"

    def get_valid_moves(self, x, y):
        self.valid_moves = list()
        self.left_closer_piece = (0, y)
        self.right_closer_piece = (7, y)
        self.up_closer_piece = (x, 0)
        self.down_closer_piece = (x, 7)
        r = False; d = False
        
        for i in range(8):
            if self.game.tablero[i][y] != "":
                if i < x:
                    self.left_closer_piece = (i, y)
                elif i > x and not r:
                    self.right_closer_piece = (i, y)
                    r = True
            if self.game.tablero[x][i] != "":
                if i < y:
                    self.up_closer_piece = (x, i)
                elif i > y and not d:
                    self.down_closer_piece = (x, i)
                    d = True

        for i in range(self.left_closer_piece[0], self.right_closer_piece[0] + 1):
            if i != x and not is_same_color(self.game.pieces, self.color, i, y):
                self.valid_moves.append((i, y))
        for j in range(self.up_closer_piece[1], self.down_closer_piece[1] + 1):
            if j != y and not is_same_color(self.game.pieces, self.color, x, j):
                self.valid_moves.append((x, j))
        #Abajo derecha
        i = x + 1
        j = y + 1
        while i < 8 and j < 8 and self.game.tablero[i][j] == "":
            self.valid_moves.append((i, j))
            i += 1
            j +=1
        if i < 8 and j < 8:
            self.valid_moves.append((i, j))
        #Abajo izquierda
        i = x - 1
        j = y + 1;
        while i > 0 and j < 8 and self.game.tablero[i][j] == "":
            self.valid_moves.append((i, j))
            i -= 1
            j += 1
        if i >= 0 and j < 8:
            self.valid_moves.append((i, j))
        #Arriba derecha
        i = x + 1
        j = y - 1
        while i < 8 and j > 0 and self.game.tablero[i][j] == "":
            self.valid_moves.append((i, j))
            i += 1
            j -= 1
        if i < 8 and j >= 0:
            self.valid_moves.append((i, j))
        #Arriba izquierda
        i = x - 1 
        j = y - 1
        while i > 0 and j > 0 and self.game.tablero[i][j] == "":
            self.valid_moves.append((i, j))
            i -= 1 
            j -= 1
        if i >= 0 and j >= 0:
            self.valid_moves.append((i, j))
        
        return get_real_valid_moves(self.game.pieces, self.color, self.valid_moves)
        