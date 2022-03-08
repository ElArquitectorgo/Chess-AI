import time
import pygame, sys
from game import Game
from Sprites import *
from IA import IA

WIDTH = HEIGHT = 600
TILE_SIZE = WIDTH / 8

"""
TO-DO

Arreglar las tablas

"""

class Chess(Game):
    def __init__(self):
        super().__init__(WIDTH=WIDTH, HEIGHT=HEIGHT, TITLE="Ajedrez mortal", TICK=2400)
        self.load_data()

    def load_data(self):
        """Carga las imágenes necesarias para las piezas."""

        self.img_pawn_w = pygame.image.load('images/Peonb.png').convert_alpha()
        self.img_pawn_b = pygame.image.load('images/Peonn.png').convert_alpha()
        self.img_bishop_w = pygame.image.load('images/Alfilb.png').convert_alpha()
        self.img_bishop_b = pygame.image.load('images/Alfiln.png').convert_alpha()
        self.img_knight_w = pygame.image.load('images/Caballob.png').convert_alpha()
        self.img_knight_b = pygame.image.load('images/Caballon.png').convert_alpha()
        self.img_queen_w = pygame.image.load('images/Damab.png').convert_alpha()
        self.img_queen_b = pygame.image.load('images/Daman.png').convert_alpha()
        self.img_king_w = pygame.image.load('images/Reyb.png').convert_alpha()
        self.img_king_b = pygame.image.load('images/Reyn.png').convert_alpha()
        self.img_rook_w = pygame.image.load('images/Torreb.png').convert_alpha()
        self.img_rook_b = pygame.image.load('images/Torren.png').convert_alpha()

    def new(self):
        """Crea una nueva partida."""

        self.pieces = []
        self.valid_moves = list()
        self.chess_position_dict = dict()
        self.click = False
        self.curr_sprite = None
        self.IA = IA(self, "WHITE")

        position1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        position2 = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -"
        # Para 1 ok, 2 me sale 2043 y debería ser 2039
        position3 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - -"
        # Para 1, 2 y 3 ok, 4 me sale 43 244 y debería ser 43 238
        position4 = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
        # Para 1 y 2 ok, 3 me sale 9 551 y debería ser 9 467
        position5 = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
        # Para 1 y 2 ok, 3 me sale 62 445 y debería ser 62 379
        position6 = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"
        # Para 1, 2 y 3 ok

        tablero = self.read_FEN_notation(position6)
    
        self.create_tablero(tablero)
        
        positions = []
        for p in self.pieces:
            positions.append((p.x, p.y))

        self.chess_position_dict.setdefault(self.turn, (tablero, positions, self.castling))
        self.run()

    def read_FEN_notation(self, position):
        """Crea un tablero partiendo de la notación FEN."""

        tablero = [["" for i in range(8)] for j in range(8)]
        str = (position).split("/")
        for i in range(8):
            data = str[i]
            if i == 7:
                data = str[i].split()
                if data[1] == "w":
                    self.turn = 1
                else:
                    self.turn = 2

                self.castling = data[2]
                data = data[0]

            cnt = 0
            for c in data:
                if c.isnumeric():
                    cnt += int(c) - 1

                tablero[i][cnt] = c
                cnt += 1

        return tablero

    def create_tablero(self, tablero):
        """Método auxiliar para crear tableros personalizados."""

        self.tablero = [["" for i in range(8)] for j in range(8)]

        self.black_rook_qs = None
        self.black_rook_ks = None
        self.white_rook_qs = None
        self.white_rook_ks = None

        for i in range(8):
            for j in range(8):
                if tablero[j][i] == "p":
                    self.pieces.append(Pawn(self, "BLACK", self.img_pawn_b, -10, i, j))
                    self.tablero[i][j] = "P"
                elif tablero[j][i] == "r":
                    self.pieces.append(Rook(self, "BLACK", self.img_rook_b, -50, i, j))
                    self.tablero[i][j] = "R"
                    if i == 0 and j == 0:
                        self.black_rook_qs = len(self.pieces) - 1
                    elif i == 7 and j == 0:
                        self.black_rook_ks = len(self.pieces) - 1
                elif tablero[j][i] == "n":
                    self.pieces.append(Knight(self, "BLACK", self.img_knight_b, -30, i, j))
                    self.tablero[i][j] = "N"
                elif tablero[j][i] == "b":
                    self.pieces.append(Bishop(self, "BLACK", self.img_bishop_b, -30, i, j))
                    self.tablero[i][j] = "B"
                elif tablero[j][i] == "q":
                    self.pieces.append(Queen(self, "BLACK", self.img_queen_b, -90, i, j))
                    self.tablero[i][j] = "Q"
                elif tablero[j][i] == "k":
                    self.pieces.append(King(self, "BLACK", self.img_king_b, -900, i, j))
                    self.tablero[i][j] = "K"
                    self.black_king_index = len(self.pieces) - 1

                elif tablero[j][i] == "P":
                    self.pieces.append(Pawn(self, "WHITE", self.img_pawn_w, 10, i, j))
                    self.tablero[i][j] = "P"
                elif tablero[j][i] == "R":
                    self.pieces.append(Rook(self, "WHITE", self.img_rook_w, 50, i, j))
                    self.tablero[i][j] = "R"
                    if i == 0 and j == 7:
                        self.white_rook_qs = len(self.pieces) - 1
                    elif i == 7 and j == 7:
                        self.white_rook_ks = len(self.pieces) - 1
                elif tablero[j][i] == "N":
                    self.pieces.append(Knight(self, "WHITE", self.img_knight_w, 30, i, j))
                    self.tablero[i][j] = "N"
                elif tablero[j][i] == "B":
                    self.pieces.append(Bishop(self, "WHITE", self.img_bishop_w, 30, i, j))
                    self.tablero[i][j] = "B"
                elif tablero[j][i] == "Q":
                    self.pieces.append(Queen(self, "WHITE", self.img_queen_w, 90, i, j))
                    self.tablero[i][j] = "Q"
                elif tablero[j][i] == "K":
                    self.pieces.append(King(self, "WHITE", self.img_king_w, 900, i, j))
                    self.tablero[i][j] = "K"
                    self.white_king_index = len(self.pieces) - 1

    def set_tablero(self, tablero, positions):
        """Método auxiliar para volver a un estado anterior del tablero."""

        self.tablero = [["" for i in range(8)] for j in range(8)]

        for i in range(8):
            for j in range(8):
                if tablero[j][i] == "p":
                    self.tablero[i][j] = "P"
                elif tablero[j][i] == "r":
                    self.tablero[i][j] = "R"
                elif tablero[j][i] == "n":
                    self.tablero[i][j] = "N"
                elif tablero[j][i] == "b":
                    self.tablero[i][j] = "B"
                elif tablero[j][i] == "q":
                    self.tablero[i][j] = "Q"
                elif tablero[j][i] == "k":
                    self.tablero[i][j] = "K"

                elif tablero[j][i] == "P":
                    self.tablero[i][j] = "P"
                elif tablero[j][i] == "R":
                    self.tablero[i][j] = "R"
                elif tablero[j][i] == "N":
                    self.tablero[i][j] = "N"
                elif tablero[j][i] == "B":
                    self.tablero[i][j] = "B"
                elif tablero[j][i] == "Q":
                    self.tablero[i][j] = "Q"
                elif tablero[j][i] == "K":
                    self.tablero[i][j] = "K"

        for i in range(len(self.pieces)):
            self.pieces[i].set_pos(positions[i][0], positions[i][1])
            if positions[i][0] != -10:
                self.pieces[i].alive = True

            # Retroceder el coronamiento
            if hasattr(self.pieces[i], "promoted") and self.pieces[i].promoted[0]:
                if self.turn == self.pieces[i].promoted[2]:
                    if self.pieces[i].color == "WHITE":
                        self.pieces[i].image = self.img_pawn_w
                        self.pieces[i].value = 10
                    elif self.pieces[i].color == "BLACK":
                        self.pieces[i].image = self.img_pawn_b
                        self.pieces[i].value = -10

                    self.pieces[i].promoted = [False, None, None]
                    self.pieces[i].name == "P"
                    self.tablero[int(self.pieces[i].x)][int(self.pieces[i].y)] = "P"

            # Por algún lado se me está cambiando y no sé como arreglarlo
            if hasattr(self.pieces[i], "promoted") and not self.pieces[i].promoted[0] and self.pieces[i].name != "P":
                self.pieces[i].name = "P"
                self.tablero[int(self.pieces[i].x)][int(self.pieces[i].y)] = "P"

    def events(self):
        """Define los eventos que van a ocurrir en nuestro juego."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                if self.click == True and self.curr_sprite is not None and 1 == 2:
                    pos = pygame.mouse.get_pos()
                    self.curr_sprite.set_pos((pos[0] - 65 / 2) / TILE_SIZE, (pos[1] - 65 / 2) / TILE_SIZE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.down()
                pass
            
            if event.type == pygame.MOUSEBUTTONUP:
                self.up()
                print(self.IA.generate_move(1))
                print(self.IA.generate_move(2))
                print(self.IA.generate_move(3))
                print(self.IA.generate_move(4))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.backtrack()

    def down(self):
        pos = pygame.mouse.get_pos()
        self.curr_pos_x = pos[0] // TILE_SIZE
        self.curr_pos_y = pos[1] // TILE_SIZE
        for sprite in self.pieces:
            if sprite.x == self.curr_pos_x and sprite.y == self.curr_pos_y:
                self.curr_sprite = sprite
                if sprite.color == "WHITE" and self.turn % 2 == 1 or sprite.color == "BLACK" and self.turn % 2 == 0:
                #if self.curr_sprite.color == "WHITE" and self.turn % 2 == 1:
                    self.valid_moves = self.get_valid_moves(sprite)
        self.click = True

    def up(self):
        self.click = False
        pos = pygame.mouse.get_pos()
        pos_x = pos[0] // TILE_SIZE
        pos_y = pos[1] // TILE_SIZE
        if (pos_x, pos_y) in self.valid_moves:
            self.generate_move(self.curr_sprite, pos_x, pos_y)

        elif self.curr_sprite is not None:
            self.curr_sprite.set_pos(self.curr_pos_x, self.curr_pos_y)

        self.valid_moves.clear()
        self.check_tablero()
        self.print_tablero()

    def backtrack(self):
        """Vuelve al estado anterior del tablero actual."""

        if self.turn == 1:
            return
        data = self.chess_position_dict[self.turn - 1]
        self.set_tablero(data[0], data[1])
        self.castling = data[2]
        self.chess_position_dict.popitem()
        self.turn -= 1

    def generate_move(self, curr_sprite, pos_x, pos_y, promote=0):
        """Genera el movimiento de la pieza dada como parámetro."""

        if self.tablero[int(pos_x)][int(pos_y)] == "K":
            return None

        for sprite in self.pieces:
            if sprite.x == pos_x and sprite.y == pos_y:
                sprite.set_pos(-10, -10)
                sprite.alive = False
            # Comer al paso
            elif curr_sprite.image == self.img_pawn_w and sprite.image == self.img_pawn_b and sprite.y - 1 == pos_y and sprite.x == pos_x and sprite.y == 3:
                    self.tablero[int(sprite.x)][int(sprite.y)] = ""
                    sprite.set_pos(-10, -10)
                    sprite.alive = False
            elif curr_sprite.image == self.img_pawn_b and sprite.image == self.img_pawn_w and sprite.y + 1 == pos_y and sprite.x == pos_x and sprite.y == 4:
                    self.tablero[int(sprite.x)][int(sprite.y)] = ""
                    sprite.set_pos(-10, -10)
                    sprite.alive = False
        
        self.tablero[int(curr_sprite.x)][int(curr_sprite.y)] = ""
        self.tablero[int(pos_x)][int(pos_y)] = curr_sprite.name

        # Perder enroque
        if curr_sprite.name == "K":
            if curr_sprite.color == "WHITE":
                self.castling = self.castling.replace("Q", "")
                self.castling = self.castling.replace("K", "")
            else:
                self.castling = self.castling.replace("q", "")
                self.castling = self.castling.replace("k", "")
            if self.castling == "":
                self.castling == "-"

            if curr_sprite.image == self.img_king_w:
                if curr_sprite.x == 4 and pos_x == 6:
                        self.pieces[self.white_rook_ks].set_pos(5, 7)
                        self.tablero[7][7] = ""
                        self.tablero[5][7] = "R"
                elif curr_sprite.x == 4 and pos_x == 2:
                        self.pieces[self.white_rook_qs].set_pos(3, 7)
                        self.tablero[0][7] = ""
                        self.tablero[3][7] = "R"
            elif curr_sprite.image == self.img_king_b:
                if curr_sprite.x == 4 and pos_x == 6:
                        self.pieces[self.black_rook_ks].set_pos(5, 0)
                        self.tablero[7][0] = ""
                        self.tablero[5][0] = "R"
                elif curr_sprite.x == 4 and pos_x == 2:
                        self.pieces[self.black_rook_qs].set_pos(3, 0)
                        self.tablero[0][0] = ""
                        self.tablero[3][0] = "R"

        if curr_sprite.name == "R":
            if self.castling != "-":
                if curr_sprite.x == 0 and curr_sprite.y == 0:
                    self.castling = self.castling.replace("q", "")
                elif curr_sprite.x == 7 and curr_sprite.y == 0:
                    self.castling = self.castling.replace("k", "")
                elif curr_sprite.x == 0 and curr_sprite.y == 7:
                    self.castling = self.castling.replace("Q", "")
                elif curr_sprite.x == 7 and curr_sprite.y == 7:
                    self.castling = self.castling.replace("K", "")

        curr_sprite.set_pos(pos_x, pos_y) 

        # Coronar peón
        if curr_sprite.image == self.img_pawn_w and pos_y == 0 and not curr_sprite.promoted[0] or curr_sprite.image == self.img_pawn_b and pos_y == 7 and not curr_sprite.promoted[0]:
            if promote == 0:
                curr_sprite.name = "Q"
                curr_sprite.image = self.img_queen_w if curr_sprite.color == "WHITE" else self.img_queen_b
                curr_sprite.value = 90 if curr_sprite.color == "WHITE" else -90
                self.tablero[int(pos_x)][int(pos_y)] = "Q"
            if promote == 1:
                curr_sprite.name = "R"
                curr_sprite.image = self.img_rook_w if curr_sprite.color == "WHITE" else self.img_rook_b
                curr_sprite.value = 50 if curr_sprite.color == "WHITE" else -50
                self.tablero[int(pos_x)][int(pos_y)] = "R"
            if promote == 2:
                curr_sprite.name = "N"
                curr_sprite.image = self.img_knight_w if curr_sprite.color == "WHITE" else self.img_knight_b
                curr_sprite.value = 30 if curr_sprite.color == "WHITE" else -30
                self.tablero[int(pos_x)][int(pos_y)] = "N"
            if promote == 3:
                curr_sprite.name = "B"
                curr_sprite.image = self.img_bishop_w if curr_sprite.color == "WHITE" else self.img_bishop_b
                curr_sprite.value = 30 if curr_sprite.color == "WHITE" else -30
                self.tablero[int(pos_x)][int(pos_y)] = "B"

            curr_sprite.promoted = [True, promote, self.turn + 1]
            
        self.curr_sprite = None

        # Guardar posición del tablero.
        curr_tablero = [["" for i in range(8)] for j in range(8)]
        for sprite in self.pieces:
            if not sprite.alive:
                continue
            elif sprite.color == "WHITE":
                str = sprite.name
            else:
                str = sprite.name.lower()

            curr_tablero[int(sprite.y)][int(sprite.x)] = str
        
        positions = []
        for p in self.pieces:
            positions.append((p.x, p.y))

        self.chess_position_dict.setdefault(self.turn + 1, (curr_tablero, positions, self.castling))
        self.turn += 1

    def get_valid_moves(self, sprite):
        """Devuelve una lista con todos los movimientos válidos de una pieza."""

        valid_moves = sprite.get_valid_moves(int(sprite.x), int(sprite.y))
        return self.is_clavada(sprite, valid_moves)

    def is_clavada(self, curr_sprite, valid_moves):
        """Comprueba si una pieza al moverse deja en jaque a su rey."""

        valid_moves_copy = valid_moves.copy()
        x, y = curr_sprite.x, curr_sprite.y

        for move in valid_moves:
            self.generate_move(curr_sprite, move[0], move[1])

            if self.is_check(curr_sprite) and curr_sprite.color != self.check_color:
                valid_moves_copy.remove(move)

            self.backtrack()
            curr_sprite.set_pos(x, y)

        self.curr_sprite = curr_sprite

        return valid_moves_copy

    def is_check(self, target=None):
        """Comprueba si en la situación actual hay un jaque, para ello busca si
           entre los posibles movimientos de cada pieza se encuentra la casilla
           de un rey, de ser así guarda el color de la pieza que provoca el jaque."""

        check = False
        for sprite in self.pieces:
            if sprite.alive and sprite != target:
                moves = sprite.get_valid_moves(int(sprite.x), int(sprite.y))
                if (self.pieces[self.black_king_index].x, self.pieces[self.black_king_index].y) in moves and sprite.color == "WHITE":
                    check = True
                    self.check_color = "WHITE"
                if (self.pieces[self.white_king_index].x, self.pieces[self.white_king_index].y) in moves and sprite.color == "BLACK":
                    check = True
                    self.check_color = "BLACK"

        return check

    def is_checkmate(self, color):
        """Comprueba si el jugador del color dado puede mover."""

        for sprite in self.pieces:
            if sprite.alive and sprite.color == color:
                valid_moves = self.get_valid_moves(sprite)
                if valid_moves:
                    return False
        return True

    def check_tablero(self):
        """Comprueba varios estados del tablero que por convenio son tablas.
           Comprueba si se ha producido un jaque y en caso de ser así,
           si se ha producido un jaque mate."""

        """if pieces_left == 2:
            print("Tablas")
            self.playing = False
        elif pieces_left == 3:
            c = False
            for sprite in self.pieces:
                if sprite.name == "B" or sprite.name == "N" or sprite.name == "K":
                    c = True
                else:
                    c = False
                    break
            if c:
                print("Tablas")
                self.playing = False
        elif pieces_left == 4:
            c1 = False
            c2 = False
            for sprite in self.pieces:
                if sprite.name == "B":
                    if sprite.color == "WHITE":
                        b_white = sprite
                        c1 = True
                    elif sprite.color == "BLACK":
                        b_black = sprite
                        c2 = True
                elif sprite.name == "K":
                    pass
                else:
                    break

            if c1 and c2:
                if b_white.diagonal_color == b_black.diagonal_color:
                    print("Tablas")
                    self.playing = False"""

        if self.is_check():
            print("check")
            if self.turn % 2 == 0 and self.is_checkmate("BLACK"):
                print("Jaque mate, ganan las blancas")
                self.new()
            elif self.turn % 2 == 1 and self.is_checkmate("WHITE"):
                print("Jaque mate, ganan las negras")
                self.new()

    def draw(self):
        """Dibuja en pantalla los elementos del juego."""

        self.draw_tablero()

        for sprite in self.pieces:
            if sprite != self.curr_sprite and sprite.alive:
                self.screen.blit(sprite.image, (sprite.x * TILE_SIZE + (TILE_SIZE - 65) / 2, sprite.y * TILE_SIZE + (TILE_SIZE - 65) / 2))
        for ele in self.valid_moves:
            pygame.draw.circle(self.screen, (132, 255, 96), (ele[0] * TILE_SIZE + TILE_SIZE / 2, ele[1] * TILE_SIZE + TILE_SIZE / 2), 15, 0)

        if self.curr_sprite is not None:
            self.screen.blit(self.curr_sprite.image, (self.curr_sprite.x * TILE_SIZE + (TILE_SIZE - 65) / 2, self.curr_sprite.y * TILE_SIZE + (TILE_SIZE - 65) / 2))

        #time.sleep(0.8)

        pygame.display.flip()

    def draw_tablero(self):
        """Dibuja un tablero de 8x8 donde cada casilla es de tamaño TILE_SIZE*TILE_SIZE."""

        for i in range(8):
            for j in range(8):
                if i % 2 == 0 and j % 2 != 0 or i % 2 != 0 and j % 2 == 0:
                    color = pygame.Color(255,208,130)
                    pygame.draw.rect(self.screen, color, (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE), width=0)
                else:
                    color = pygame.Color(255,255,255)
                    pygame.draw.rect(self.screen, color, (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE), width=0)

    def print_tablero(self):
        """Método auxiliar cuyo único propósito es estudiar el comportamiento del tablero."""

        tablero = [["" for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(8):
                tablero[i][j] = self.tablero[j][i]
                if tablero[i][j] == "":
                    tablero[i][j] = " "
        for i in range(8):
            print(tablero[i])
        print()

def main():
    chess = Chess()
    chess.new()

if __name__ == "__main__":
    main()