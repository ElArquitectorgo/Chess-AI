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
        self.turn = 1
        self.click = False
        self.curr_sprite = None
        self.IA = IA(self, "WHITE")

        tablero2 = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],
                   ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],
                   ['', '', '', '', '', '', '', ''],
                   ['', '', '', '', '', '', '', ''],
                   ['', '', '', '', '', '', '', ''],
                   ['', '', '', '', '', '', '', ''],
                   ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],
                   ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]

        # 14 20 Para 1 ok, 2 me sale 2043 y debería ser 2039
        tablero = [['Rb', '', '', '', 'Kb', '', '', 'Rb'],
                   ['Pb', '', 'Pb', 'Pb', 'Qb', 'Pb', 'Bb', ''],
                   ['Bb', 'Nb', '', '', 'Pb', 'Nb', 'Pb', ''],
                   ['', '', '', 'Pw', 'Nw', '', '', ''],
                   ['', 'Pb', '', '', 'Pw', '', '', ''],
                   ['', '', 'Nw', '', '', 'Qw', '', 'Pb'],
                   ['Pw', 'Pw', 'Pw', 'Bw', 'Bw', 'Pw', 'Pw', 'Pw'],
                   ['Rw', '', '', '', 'Kw', '', '', 'Rw']]

        tablero3 = [['', '', '', '', '', '', '', ''],
                   ['', '', 'Pb', '', '', '', '', ''],
                   ['', '', '', 'Pb', '', '', '', ''],
                   ['Kw', 'Pw', '', '', '', '', '', 'Rb'],
                   ['', 'Rw', '', '', '', 'Pb', '', 'Kb'],
                   ['', '', '', '', '', '', '', ''],
                   ['', '', '', '', 'Pw', '', 'Pw', ''],
                   ['', '', '', '', '', '', '', '']]

        # Para 1 y 2 ok, 3 me sale 9 551 y debería ser 9 467
        tablero4 = [['Rb', '', '', '', 'Kb', '', '', 'Rb'],
                   ['Pw', 'Pb', 'Pb', 'Pb', '', 'Pb', 'Pb', 'Pb'],
                   ['', 'Bb', '', '', '', 'Nb', 'Bb', 'Nw'],
                   ['Nb', 'Pw', '', '', '', '', '', ''],
                   ['Bw', 'Bw', 'Pw', '', 'Pw', '', '', ''],
                   ['Qb', '', '', '', '', 'Nw', '', ''],
                   ['Pw', 'Pb', '', 'Pw', '', '', 'Pw', 'Pw'],
                   ['Rw', '', '', 'Qw', '', 'Rw', 'Kw', '']]

        # Para 1 y 2 ok, 3 me sale 62 445 y debería ser 62 379
        tablero5 = [['Rb', 'Nb', 'Bb', 'Qb', '', 'Kb', '', 'Rb'],
                   ['Pb', 'Pb', '', 'Pw', 'Bb', 'Pb', 'Pb', 'Pb'],
                   ['', '', 'Pb', '', '', '', '', ''],
                   ['', '', '', '', '', '', '', ''],
                   ['', '', 'Bw', '', '', '', '', ''],
                   ['', '', '', '', '', '', '', ''],
                   ['Pw', 'Pw', 'Pw', '', 'Nw', 'Nb', 'Pw', 'Pw'],
                   ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', '', '', 'Rw']]

        # Para 1, 2 y 3 va perfe
        tablero6 = [['Rb', '', '', '', '', 'Rb', 'Kb', ''],
                   ['', 'Pb', 'Pb', '', 'Qb', 'Pb', 'Pb', 'Pb'],
                   ['Pb', '', 'Nb', 'Pb', '', 'Nb', '', ''],
                   ['', '', 'Bb', '', 'Pb', '', 'Bw', ''],
                   ['', '', 'Bw', '', 'Pw', '', 'Bb', ''],
                   ['Pw', '', 'Nw', 'Pw', '', 'Nw', '', ''],
                   ['', 'Pw', 'Pw', '', 'Qw', 'Pw', 'Pw', 'Pw'],
                   ['Rw', '', '', '', '', 'Rw', 'Kw', '']]
    
        self.create_tablero(tablero)
        
        positions = []
        for p in self.pieces:
            positions.append((p.x, p.y))

        self.chess_position_dict.setdefault(self.turn, (tablero, positions))
        self.run()

    def create_tablero(self, tablero):
        """Método auxiliar para crear tableros personalizados."""

        self.tablero = [["" for i in range(8)] for j in range(8)]

        for i in range(8):
            for j in range(8):
                if tablero[j][i] == "Pb":
                    self.pieces.append(Pawn(self, "BLACK", self.img_pawn_b, -10, i, j))
                    self.tablero[i][j] = "P"
                elif tablero[j][i] == "Rb":
                    self.pieces.append(Rook(self, "BLACK", self.img_rook_b, -50, i, j))
                    self.tablero[i][j] = "R"
                elif tablero[j][i] == "Nb":
                    self.pieces.append(Knight(self, "BLACK", self.img_knight_b, -30, i, j))
                    self.tablero[i][j] = "N"
                elif tablero[j][i] == "Bb":
                    self.pieces.append(Bishop(self, "BLACK", self.img_bishop_b, -30, i, j))
                    self.tablero[i][j] = "B"
                elif tablero[j][i] == "Qb":
                    self.pieces.append(Queen(self, "BLACK", self.img_queen_b, -90, i, j))
                    self.tablero[i][j] = "Q"
                elif tablero[j][i] == "Kb":
                    self.pieces.append(King(self, "BLACK", self.img_king_b, -900, i, j))
                    self.tablero[i][j] = "K"

                elif tablero[j][i] == "Pw":
                    self.pieces.append(Pawn(self, "WHITE", self.img_pawn_w, 10, i, j))
                    self.tablero[i][j] = "P"
                elif tablero[j][i] == "Rw":
                    self.pieces.append(Rook(self, "WHITE", self.img_rook_w, 50, i, j))
                    self.tablero[i][j] = "R"
                elif tablero[j][i] == "Nw":
                    self.pieces.append(Knight(self, "WHITE", self.img_knight_w, 30, i, j))
                    self.tablero[i][j] = "N"
                elif tablero[j][i] == "Bw":
                    self.pieces.append(Bishop(self, "WHITE", self.img_bishop_w, 30, i, j))
                    self.tablero[i][j] = "B"
                elif tablero[j][i] == "Qw":
                    self.pieces.append(Queen(self, "WHITE", self.img_queen_w, 90, i, j))
                    self.tablero[i][j] = "Q"
                elif tablero[j][i] == "Kw":
                    self.pieces.append(King(self, "WHITE", self.img_king_w, 900, i, j))
                    self.tablero[i][j] = "K"

    def set_tablero(self, tablero, positions):
        """Método auxiliar para volver a un estado anterior del tablero."""

        self.tablero = [["" for i in range(8)] for j in range(8)]

        for i in range(8):
            for j in range(8):
                if tablero[j][i] == "Pb":
                    self.tablero[i][j] = "P"
                elif tablero[j][i] == "Rb":
                    self.tablero[i][j] = "R"
                elif tablero[j][i] == "Nb":
                    self.tablero[i][j] = "N"
                elif tablero[j][i] == "Bb":
                    self.tablero[i][j] = "B"
                elif tablero[j][i] == "Qb":
                    self.tablero[i][j] = "Q"
                elif tablero[j][i] == "Kb":
                    self.tablero[i][j] = "K"

                elif tablero[j][i] == "Pw":
                    self.tablero[i][j] = "P"
                elif tablero[j][i] == "Rw":
                    self.tablero[i][j] = "R"
                elif tablero[j][i] == "Nw":
                    self.tablero[i][j] = "N"
                elif tablero[j][i] == "Bw":
                    self.tablero[i][j] = "B"
                elif tablero[j][i] == "Qw":
                    self.tablero[i][j] = "Q"
                elif tablero[j][i] == "Kw":
                    self.tablero[i][j] = "K"

        for i in range(len(self.pieces)):
            self.pieces[i].set_pos(positions[i][0], positions[i][1])
            if positions[i][0] != -10:
                self.pieces[i].alive = True
            if i == 14 or i == 20:
                if self.pieces[i].castling_turn is not None:
                    if self.pieces[i].castling_turn + 1 == self.turn:
                        self.pieces[i].castling_turn = None

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
                #print(self.IA.generate_move(1))
                #print(self.IA.generate_move(2))
                #print(self.IA.generate_move(3))
                #print(self.IA.generate_move(4))

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
        if curr_sprite.name == "K" and curr_sprite.castling_turn is None:
            curr_sprite.castling_turn = self.turn
            if curr_sprite.image == self.img_king_w:
                if curr_sprite.x == 4 and pos_x == 6:
                    if self.pieces[-1].x == 7 and self.pieces[-1].y == 7:
                        self.pieces[-1].set_pos(5, 7)
                        self.tablero[7][7] = ""
                        self.tablero[5][7] = "R"
                elif curr_sprite.x == 4 and pos_x == 2:
                    if self.pieces[4].x == 0 and self.pieces[4].y == 7:
                        self.pieces[4].set_pos(3, 7)
                        self.tablero[0][7] = ""
                        self.tablero[3][7] = "R"
            elif curr_sprite.image == self.img_king_b:
                if curr_sprite.x == 4 and pos_x == 6:
                    if self.pieces[-4].x == 7 and self.pieces[-4].y == 0:
                        self.pieces[-4].set_pos(5, 0)
                        self.tablero[7][0] = ""
                        self.tablero[5][0] = "R"
                elif curr_sprite.x == 4 and pos_x == 2:
                    if self.pieces[0].x == 0 and self.pieces[0].y == 0:
                        self.pieces[0].set_pos(3, 0)
                        self.tablero[0][0] = ""
                        self.tablero[3][0] = "R"

        curr_sprite.set_pos(pos_x, pos_y) 

        # Coronar peón
        # Habría que actualizar el valor de la pieza e incluir las imágenes negras
        if curr_sprite.image == self.img_pawn_w and pos_y == 0 and not curr_sprite.promoted[0] or curr_sprite.image == self.img_pawn_b and pos_y == 7 and not curr_sprite.promoted[0]:
            if promote == 0:
                curr_sprite.name = "Q"
                curr_sprite.image = self.img_queen_w
                self.tablero[int(pos_x)][int(pos_y)] = "Q"
            if promote == 1:
                curr_sprite.name = "R"
                curr_sprite.image = self.img_rook_w
                self.tablero[int(pos_x)][int(pos_y)] = "R"
            if promote == 2:
                curr_sprite.name = "N"
                curr_sprite.image = self.img_knight_w
                self.tablero[int(pos_x)][int(pos_y)] = "N"
            if promote == 3:
                curr_sprite.name = "B"
                curr_sprite.image = self.img_bishop_w
                self.tablero[int(pos_x)][int(pos_y)] = "B"

            curr_sprite.promoted = [True, promote, self.turn + 1]
            
        self.curr_sprite = None

        # Guardar posición del tablero.
        curr_tablero = [["" for i in range(8)] for j in range(8)]
        for sprite in self.pieces:
            if not sprite.alive:
                continue
            elif sprite.color == "WHITE":
                str = "w"
            else:
                str = "b"

            curr_tablero[int(sprite.y)][int(sprite.x)] = sprite.name + str
        
        positions = []
        for p in self.pieces:
            positions.append((p.x, p.y))

        self.chess_position_dict.setdefault(self.turn + 1, (curr_tablero, positions))
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
                if (self.pieces[14].x, self.pieces[14].y) in moves and sprite.color == "WHITE":
                    check = True
                    self.check_color = "WHITE"
                if (self.pieces[20].x, self.pieces[20].y) in moves and sprite.color == "BLACK":
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