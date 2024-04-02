from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.properties import *
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.lang.builder import Builder
from kivy.utils import get_hex_from_color, get_color_from_hex
from pathlib import Path
import boardai, piecesai, ai
from move import Move
import os
import sys
import platform
import sysconfig
import csv
import time

indent = '    '
Width, Height = 800, 800
Window.size = (Width, Height)

def get_user_move(movestr):
    move_str = movestr
    move_str = move_str.replace(" ", "")
    try:
        xfrom = letter_to_xpos(move_str[0:1])
        yfrom = 8 - int(move_str[1:2])
        xto = letter_to_xpos(move_str[2:3])
        yto = 8 - int(move_str[3:4])
        return Move(xfrom, yfrom, xto, yto)
    except ValueError:
        print("Invalid format. Example: A2 A4")
        return get_user_move()
        
def letter_to_xpos(letter):
    letter = letter.upper()
    if letter == 'A':
        return 0
    if letter == 'B':
        return 1
    if letter == 'C':
        return 2
    if letter == 'D':
        return 3
    if letter == 'E':
        return 4
    if letter == 'F':
        return 5
    if letter == 'G':
        return 6
    if letter == 'H':
        return 7
    raise ValueError("Invalid letter.")
        
def xpos_to_letter(digit):
    if digit >= 0 and digit <= 7:
        str = "ABCDEFGH"
        letter = str[digit]
        return letter
    raise ValueError("Invalid digit")
     
def ypos_to_digit(digit):
    if digit >= 0 and digit <= 7:
        letter = chr(ord('0')+digit+1)
        return letter
    raise ValueError("Invalid digit")
    
def ai_to_hm_x(xpos):
    return xpos
    
def ai_to_hm_y(ypos):
    return 7 - ypos
    
class ChessPiece(ButtonBehavior, Image):

    grid_x = NumericProperty()
    grid_y = NumericProperty()
    id = StringProperty()
    First_use = BooleanProperty()
    def available_moves(self, pieces):
        pass

class Pawn(ChessPiece):

    def callback(instance, value):
        print("Value of First_use changed", value)

    def available_moves(self, pieces):
        if self.id[:5] == "White":
            available_moves = {"available_moves":(), "pieces_to_capture":[]}
            if self.First_use:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y+1), (self.grid_x, self.grid_y+2)}
            else:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y+1)}
            pclup = 0
            pcrup = 0
            for piece in pieces:
                if piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y + 1:
                    pclup = piece
                if piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y + 1:
                    pcrup = piece
            for piece in pieces:
                if piece.grid_y == self.grid_y + 1 and piece.grid_x == self.grid_x:
                    available_moves["available_moves"] = ()
                if self.First_use and piece.grid_y == self.grid_y + 2 and piece.grid_x == self.grid_x:
                    if len(available_moves) == 2:
                        available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                ### 1
                if piece.id[:9] == "BlackPawn" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y and self.grid_y == 4 and pcrup == 0:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y + 1))
                ### 2
                if piece.id[:9] == "BlackPawn" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y and self.grid_y == 4 and pclup == 0:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y + 1))
                ### 3
                if piece.id[:5] == "Black" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y + 1:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y + 1))
                ### 4
                if piece.id[:5] == "Black" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y + 1:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y + 1))
            return available_moves
        if self.id[:5] == "Black":
            available_moves = {"available_moves":(), "pieces_to_capture":[]}
            if self.First_use:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y-1), (self.grid_x, self.grid_y-2)}
            else:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y-1)}
            pclup = 0
            pcrup = 0
            for piece in pieces:
                if piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y - 1:
                    pclup = piece
                if piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y - 1:
                    pcrup = piece
            for piece in pieces:
                if piece.grid_y == self.grid_y - 1 and piece.grid_x == self.grid_x:
                    available_moves["available_moves"] = ()
                if self.First_use and piece.grid_y == self.grid_y - 2 and piece.grid_x == self.grid_x:
                    if len(available_moves) == 2:
                        available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                ### 1
                if piece.id[:9] == "WhitePawn" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y and self.grid_y == 3 and pcrup == 0:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y - 1))          
                ### 2
                if piece.id[:9] == "WhitePawn" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y and self.grid_y == 3 and pclup == 0:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y - 1))
                ### 3
                if piece.id[:5] == "White" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y - 1:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y - 1))
                ### 4
                if piece.id[:5] == "White" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y - 1:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y - 1))
            return available_moves

class Rook(ChessPiece):

    def available_moves(self, pieces):
        available_moves = {"available_moves":[], "pieces_to_capture":[]}
        rows = 8
        cols = 8
        for x in range(int(self.grid_x) + 1, cols):
            found = False
            for piece in pieces:
                if piece.grid_x == x and piece.grid_y == self.grid_y:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
                    break
            if found:
                break
            available_moves["available_moves"].append((x, self.grid_y))
        for y in range(int(self.grid_y) + 1, rows):
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x and piece.grid_y == y:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x, y))
        for x in range(int(self.grid_x) - 1, -1, -1):
            found = False
            for piece in pieces:
                if piece.grid_x == x and piece.grid_y == self.grid_y:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
                    break
            if found:
                break
            available_moves["available_moves"].append((x, self.grid_y))
        for y in range(int(self.grid_y) - 1, -1, -1):
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x and piece.grid_y == y:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x, y))
        return available_moves

class Knight(ChessPiece):

    def available_moves(self, pieces):
        available_moves = {"available_moves":self.create_moves(), "pieces_to_capture":[]}
        for piece in pieces:
            if self.id[:5] == "White":
                if piece.id[:5] == "White" and (piece.grid_x, piece.grid_y) in available_moves["available_moves"]:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                if piece.id[:5] == "Black" and (piece.grid_x, piece.grid_y) in available_moves["available_moves"]:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                    available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
            if self.id[:5] == "Black":
                if piece.id[:5] == "Black" and (piece.grid_x, piece.grid_y) in available_moves["available_moves"]:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                if piece.id[:5] == "White" and (piece.grid_x, piece.grid_y) in available_moves["available_moves"]:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                    available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
        return available_moves

    def create_moves(self):
        moves = [
            (self.grid_x + 2, self.grid_y + 1),
            (self.grid_x + 1, self.grid_y + 2),
            (self.grid_x - 2, self.grid_y + 1),
            (self.grid_x - 1, self.grid_y + 2),
            (self.grid_x + 1, self.grid_y - 2),
            (self.grid_x + 2, self.grid_y - 1),
            (self.grid_x - 2, self.grid_y - 1),
            (self.grid_x - 1, self.grid_y - 2),
        ]
        good_moves = []
        for move in moves:
            if move[0] <= 7 and move[1] <= 7 and move[0] >= 0 and move[1] >= 0:
                good_moves.append((move))

        return good_moves

class Bishop(ChessPiece):

    def available_moves(self, pieces):
        available_moves = {"available_moves":[], "pieces_to_capture":[]}
        rows = 8
        cols = 8
        for i in range(1, rows):
            if self.grid_x + i >= rows or self.grid_y + i >= cols:
                break
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x + i and piece.grid_y == self.grid_y + i:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((self.grid_x + i, self.grid_y + i))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x + i, self.grid_y + i))
        for i in range(1, rows):
            if self.grid_x - i < 0 or self.grid_y + i >= rows:
                break
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x - i and piece.grid_y == self.grid_y + i:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((self.grid_x - i, self.grid_y + i))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x - i, self.grid_y + i))
        for i in range(1, rows):
            if self.grid_x - i < 0 or self.grid_y - i < 0:
                break
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x - i and piece.grid_y == self.grid_y - i:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((self.grid_x - i, self.grid_y - i))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x - i, self.grid_y - i))
        for i in range(1, rows):
            if self.grid_x + i >= rows or self.grid_y - i < 0:
                break
            found = False
            for piece in pieces:
                if piece.grid_x == self.grid_x + i and piece.grid_y == self.grid_y - i:
                    found = True
                    if piece.id[:5] != self.id[:5]:
                        available_moves["pieces_to_capture"].append((self.grid_x + i, self.grid_y - i))
                    break
            if found:
                break
            available_moves["available_moves"].append((self.grid_x + i, self.grid_y - i))
        return available_moves

class Queen(Rook, Bishop):
    def available_moves(self, pieces):
        available_moves1 = Rook.available_moves(self,pieces)
        available_moves2 = Bishop.available_moves(self,pieces)
        available_moves = {key: val + available_moves2[key] for key, val in available_moves1.items()}
        return available_moves

class King(ChessPiece):

    def available_moves(self, pieces):
        available_moves = self.create_moves()
        rows, cols = 8,8
        good_available_moves = []
        for move in available_moves["available_moves"]:
            if move[0] <= cols and move[1] <= rows and move[1] >= 0 and move[0] >= 0:
                good_available_moves.append(move)
        available_moves["available_moves"] = good_available_moves
        for piece in pieces:
            if (piece.grid_x, piece.grid_y) in available_moves["available_moves"]:
                if piece.id[:5] != self.id[:5]:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                    available_moves["pieces_to_capture"].append((piece.grid_x, piece.grid_y))
        if self.First_use:
            available_moves["castling"] = self.castling(pieces)
        return available_moves

    def create_moves(self):
        available_moves = {"available_moves":[], "pieces_to_capture":[]}
        available_moves["available_moves"].append((self.grid_x, self.grid_y+1))
        available_moves["available_moves"].append((self.grid_x-1, self.grid_y+1))
        available_moves["available_moves"].append((self.grid_x+1, self.grid_y+1))
        available_moves["available_moves"].append((self.grid_x-1, self.grid_y))
        available_moves["available_moves"].append((self.grid_x-1, self.grid_y-1))
        available_moves["available_moves"].append((self.grid_x+1, self.grid_y))
        available_moves["available_moves"].append((self.grid_x+1, self.grid_y-1))
        available_moves["available_moves"].append((self.grid_x, self.grid_y-1))
        return available_moves

    def castling(self, pieces):
        if self.First_use:
            no_piece_left = True
            no_piece_right = True
            for piece in pieces:
                if piece.grid_y == self.grid_y and piece.grid_x > self.grid_x and (piece.id[5:9] != "Rook" or self.id[:5] != piece.id[:5]):
                    no_piece_right = False
                elif piece.grid_y == self.grid_y and piece.grid_x < self.grid_x and (piece.id[5:9] != "Rook" or self.id[:5] != piece.id[:5]):
                    no_piece_left = False
            if no_piece_right and no_piece_left:
                return [(self.grid_x-2, self.grid_y),(self.grid_x+2, self.grid_y)]
            if no_piece_right:
                return [(self.grid_x+2, self.grid_y)]
            if no_piece_left:
                return [(self.grid_x-2, self.grid_y)]
        return []

class ChessBoard(RelativeLayout):
    piece_pressed = False
    id_piece_ = None
    available_moves = {"available_moves":(), "pieces_to_capture":[]}
    piece_index = None
    check = BooleanProperty(defaultvalue=False)
    hmmove = "C2 C3"
    index = 0
    
    def __init__(self, **kwargs):
        super(ChessBoard, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down = self.make_ai_move)
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self.make_ai_move)
        self._keyboard = None
        
    def check_ai_move(self):
        print("Check ai move:", self.hmmove)
        move = get_user_move(self.hmmove)
        boardai.perform_move(move)
        anim = Animation(grid_x = move.xto, grid_y = ai_to_hm_y(move.yto), t='in_out_expo', duration=0.5)
        ChessBoard.piece_index = ChessBoard.pieceindex_at_board(self, move.xfrom, move.yfrom)
        if ChessBoard.piece_index > -1:
            child = self.children[ChessBoard.piece_index]
            anim.start(child)
            if (child.id[0:5] == boardai.human):
                ai_move = self.let_ai_move()
            print(boardai.to_string())
            
    def perform_ai_move(self, xfrom, yfrom, xto, yto):
        hmmove = ""+xpos_to_letter(xfrom)+ypos_to_digit(yfrom)+" "+xpos_to_letter(xto)+ypos_to_digit(yto)
        move = get_user_move(hmmove)
        boardai.perform_move(move)
        
    def make_ai_move(self, keyboard, keycode, text, modifiers):
        l = keycode[1]
        if l == 'm':
            self.hmmove = "     "
            self.index = 0
        elif (l >= 'a' and l <= 'h') or (l >= '1' and l <= '8'):
            if self.index < 5:
                self.hmmove = self.hmmove[: self.index] + l + self.hmmove[self.index + 1:]
                self.index += 1
            if self.index == 2:
                self.hmmove = self.hmmove[: self.index] + ' ' + self.hmmove[self.index + 1:]
                self.index = 3
        elif l == '.':
            self.check_ai_move()
            self.hmmove = "     "
            self.index = 0
        return True

    def close_application(self): 
        App.get_running_app().stop() 
        Window.close()
    
    def listpieces(self):
        for child in self.children:
            print("Human board",child.id,child.grid_x,child.grid_y,child.First_use)
            
    def let_ai_move(self):
        if self.twoplayer_turn():
            return 0
        ai_move = ai.AI.get_ai_move(boardai, [], aicolor, hmcolor, alg)
        if type(ai_move) is int:
            print("Check mate 0 returned by ai")
            time.sleep(10)
            self.close_application()
            time.sleep(60)
        boardai.perform_move(ai_move)
        propawn = self.piece_at_board(ai_move.xfrom, ai_to_hm_y(ai_move.yfrom))
        if ai_move.yfrom == 6 and ai_move.yto == 7 and ai_move.xfrom == ai_move.xto and boardai.chesspiecesai[ai_move.xto][ai_move.yto].id == "BlackQueen" and propawn.id[:9] == "BlackPawn":
            self.remove_widget(propawn)
            self.add_widget(Queen(id="BlackQueen",source="Assets/PNG/BlackQueen.png", grid_x=ai_move.xto, grid_y=0))
        elif ai_move.yfrom == 1 and ai_move.yto == 0 and ai_move.xfrom == ai_move.xto and boardai.chesspiecesai[ai_move.xto][ai_move.yto].id == "WhiteQueen" and propawn.id[:9] == "WhitePawn":
            self.remove_widget(propawn)
            self.add_widget(Queen(id="WhiteQueen",source="Assets/PNG/WhiteQueen.png", grid_x=ai_move.xto, grid_y=7))
        else:
            anim = Animation(grid_x=ai_move.xto, grid_y=ai_to_hm_y(ai_move.yto), t='in_out_expo', duration=0.5)
            ChessBoard.piece_index = ChessBoard.pieceindex_at_board(self,ai_move.xfrom,ai_move.yfrom)
            if ChessBoard.piece_index > -1:
                anim.start(self.children[ChessBoard.piece_index])
        return ai_move
            
    def findpiece(self,id):
        for child in self.children:
            if child.id == id:
                return child
                
    def WhiteCapture(self):
        capture = False
        hmsyn = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
        for child in self.children:
            hm_x_grid = round(child.grid_x)
            hm_y_grid = round(child.grid_y)
            hmsyn[hm_x_grid][hm_y_grid] += 1
            if hmsyn[hm_x_grid][hm_y_grid] > 1:
                capture = True
                break
        if capture:
            for child in self.children:
                if child.id[0:5] == "White":
                    if [round(child.grid_x),round(child.grid_y)] == [hm_x_grid,hm_y_grid]:
                        piece = self.findpiece(child.id)
                        self.remove_widget(piece)
            
    def pieceindex_at_board(self,xpos,ypos):
        ypos = ai_to_hm_y(ypos)
        index = -1
        for child in self.children:
            index += 1
            if child.grid_x == xpos and child.grid_y == ypos:
                return index
        return -1
                
    def piece_at_board(self,xpos,ypos):
        for child in self.children:
            if child.grid_x == xpos and child.grid_y == ypos:
                return child
        print("No piece_at_board Piece 0 oordinaten", xpos, ypos)
        return 0
        
    def twoplayer_turn(self):
        if alg == '-':
            if boardai.human == "White":
                boardai.human = "Black"
            else:
                boardai.human = "White"
            return True
        else:
            return False

    def on_touch_down(self, touch):
        #boardai.listpieces()
        #self.listpieces()
        self.WhiteCapture()
        rows, cols = 8,8
        grid_x = int(touch.pos[0] / self.width * rows)
        grid_y = int(touch.pos[1] / self.height * cols)
        for id, child in enumerate(self.children):
            old_x, old_y = child.grid_x, child.grid_y
            if not ChessBoard.piece_pressed:
                if grid_x == child.grid_x and grid_y == child.grid_y and child.id[:5] == boardai.human:
                    ChessBoard.piece_pressed = True
                    ChessBoard.piece_index = id
                    ChessBoard.available_moves = child.available_moves(self.children)
                    self.draw_moves()
                    ChessBoard.id_piece_ = child.id
                    break
            elif ChessBoard.piece_pressed and grid_x == child.grid_x and grid_y == child.grid_y and ChessBoard.id_piece_[:5] == child.id[:5]:
                ChessBoard.available_moves = child.available_moves(self.children)
                self.draw_moves()
                ChessBoard.id_piece_ = child.id
                ChessBoard.piece_index = id
                break
            elif ChessBoard.piece_pressed and child.id == ChessBoard.id_piece_:
                if (grid_x, grid_y) in ChessBoard.available_moves["available_moves"]:
                    print("Normal zet", self.children[id].id, old_x, old_y, grid_x, grid_y)
                    anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_quad', duration=0.5)
                    anim.start(self.children[id])
                    ChessBoard.piece_pressed = False
                    ChessBoard.available_moves = {"available_moves":(), "pieces_to_capture":[]}
                    self.perform_ai_move(round(old_x), round(old_y), grid_x, grid_y)
                    if grid_y == 7 and child.id[0:9] == "WhitePawn":
                        self.remove_widget(child)
                        self.add_widget(Queen(id="WhiteQueen",source="Assets/PNG/WhiteQueen.png", grid_x=grid_x, grid_y=grid_y))
                    if grid_y == 0 and child.id[0:9] == "BlackPawn":
                        self.remove_widget(child)
                        self.add_widget(Queen(id="BlackQueen",source="Assets/PNG/BlackQueen.png", grid_x=grid_x, grid_y=grid_y))
                    ai_move = self.let_ai_move() 
                    if (child.id[5:9] == "Pawn" or child.id[5:9] == "Rook" or child.id[5:9] == "King") and child.First_use:
                       child.First_use = False
                    self.draw_moves()
                    if self.check_check(1):
                       break
                    else:
                       print("Turn after normal move", boardai.human)
                       self.turn()
                       break        
                elif (grid_x, grid_y) in ChessBoard.available_moves["pieces_to_capture"]:
                    for enemy in self.children:
                        if enemy.grid_x == grid_x and enemy.grid_y == grid_y:
                            anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_out_expo', duration=0.5)
                            anim.start(self.children[id])
                            self.remove_widget(enemy)
                            ChessBoard.piece_pressed = False
                            ChessBoard.available_moves = {"available_moves":(), "pieces_to_capture":[]}
                            self.perform_ai_move(round(old_x), round(old_y), grid_x, grid_y)
                            ai_move = self.let_ai_move() 
                            if (child.id[5:9] == "Pawn" or child.id[5:9] == "Rook" or child.id[5:9] == "King") and child.First_use:
                                child.First_use = False
                            self.draw_moves()     
                            if self.check_check(2):
                                break
                            else:
                                print("Turn after capture", boardai.human)
                                self.turn()                    
                                break
                        elif child.id[5:9] == "Pawn" and enemy.id[5:9] == "Pawn" and (child.grid_x - 1 == enemy.grid_x or child.grid_x + 1 == enemy.grid_x):
                            anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_out_expo', duration=0.5)
                            anim.start(child)
                            if enemy.grid_x == grid_x and enemy.grid_y == grid_y - 1 and enemy.id[:5] == "Black":
                                self.remove_widget(enemy)
                            if enemy.grid_x == grid_x and enemy.grid_y == grid_y + 1 and enemy.id[:5] == "White":
                                self.remove_widget(enemy)
                            ChessBoard.piece_pressed = False
                            ChessBoard.available_moves = {"available_moves":(), "pieces_to_capture":[]}
                            self.perform_ai_move(round(old_x), round(old_y), grid_x, grid_y)
                            self.draw_moves()
                            print("Turn after en passant", boardai.human)
                            rc = self.twoplayer_turn()
            else:
                try:
                    if ChessBoard.piece_pressed and ChessBoard.id_piece_[5:] == "King" and (grid_x, grid_y) in ChessBoard.available_moves["castling"]:
                         anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_out_expo', duration=0.5)
                         anim.start(self.children[ChessBoard.piece_index])
                         if grid_x == 2 and grid_y == 0:
                             piece = self.findpiece("WhiteRook_0")
                             anim = Animation(grid_x=grid_x+1, grid_y=grid_y, t='in_out_expo', duration=0.5)
                             anim.start(piece)
                             piece.First_use = False
                             self.perform_ai_move(4, 0, 2, 0)
                         if grid_x == 6 and grid_y == 0:
                             piece = self.findpiece("WhiteRook_1")
                             anim = Animation(grid_x=grid_x-1, grid_y=grid_y, t='in_out_expo', duration=0.5)
                             anim.start(piece)
                             piece.First_use = False
                             self.perform_ai_move(4, 0, 6, 0)
                         if grid_x == 2 and grid_y == 7:
                             piece = self.findpiece("BlackRook_0")
                             anim = Animation(grid_x=grid_x+1, grid_y=grid_y, t='in_out_expo', duration=0.5)
                             anim.start(piece)
                             piece.First_use = False
                             self.perform_ai_move(4, 7, 2, 7)
                         if grid_x == 6 and grid_y == 7:
                             piece = self.findpiece("BlackRook_1")
                             anim = Animation(grid_x=grid_x-1, grid_y=grid_y, t='in_out_expo', duration=0.5)
                             anim.start(piece)
                             piece.First_use = False
                             self.perform_ai_move(4, 7, 6, 7)
                         ai_move = self.let_ai_move() 
                         ChessBoard.piece_pressed = False
                         child.First_use = False
                         self.children[ChessBoard.piece_index].First_use = False
                         ChessBoard.available_moves = {"available_moves":(), "pieces_to_capture":[]}             
                         if self.check_check(3):
                             break
                         else:
                              print("Turn3", boardai.human)
                              self.turn()
                              self.draw_moves()
                              break
                         print("Turn after castling", boardai.human)
                         rc = self.twoplayer_turn()
                         self.turn() 
                         self.draw_moves()
                except Exception as e:
                    print(repr(e))

    def turn(self):
        print(boardai.to_string())
        #boardai.listpieces()

    def check_check(self, prm):
        WHKing = None
        BHKing = None
        for piece_ in self.children:
            if piece_.id[:5] == "White" and piece_.id[5:] == "King":
                WHKing = piece_
                break
        for piece_ in self.children:
            if piece_.id[:5] == "Black" and piece_.id[5:] == "King":
                BHKing = piece_
                break
        for piece in self.children:
            mvs = []
            piece_available_moves = piece.available_moves(mvs)
            if (WHKing.grid_x, WHKing.grid_y) in piece_available_moves["available_moves"] or (WHKing.grid_x, WHKing.grid_y) in piece_available_moves["pieces_to_capture"]:
                mvs = []
                print("Checkmate white king", piece.id, "Available moves for", WHKing.id, WHKing.available_moves(mvs), piece_available_moves)
                return True
            if (BHKing.grid_x, BHKing.grid_y) in piece_available_moves["available_moves"] or (BHKing.grid_x, BHKing.grid_y) in piece_available_moves["pieces_to_capture"]:
                mvs = []
                print("Checkmate black king", piece.id, "Available moves for", BHKing.id, BHKing.available_moves(mvs), piece_available_moves)
                return True
        return False

    def draw_moves(self):
        grid_size_x = self.width / 8
        grid_size_y = self.height / 8
        Blue = (0, 0, 1)
        Green = (0, 1, 0)

        with self.canvas:
            self.canvas.remove_group("moves")
            size = (0.2*grid_size_x, 0.2*grid_size_y)

            for idx, moves in enumerate(ChessBoard.available_moves.values()):
                if idx == 0:
                    Color(rgb=Blue)
                    for move in moves:
                        Ellipse(pos=(grid_size_x * move[0]+grid_size_x/2 - size[0]/2, grid_size_y * move[1] + grid_size_y/2 - size[1]/2), size=size, group="moves")
                elif idx == 1:
                    Color(rgb=Green)
                    for move in moves:
                        Ellipse(pos=(grid_size_x * move[0]+grid_size_x/2 - size[0]/2, grid_size_y * move[1] + grid_size_y/2 - size[1]/2), size=size, group="moves")

    def on_size(self, *_):
        self.draw_board()
        self.draw_moves()

    def update(self):
        pass

    def on_pos(self, *_):
        self.draw_board()
        self.draw_moves()

    def draw_board(self):
        is_white = False
        grid_size_x = self.width / 8
        grid_size_y = self.height / 8
        with self.canvas.before:
            for y in range(8):
                for x in range(8):
                    if is_white:
                        Color(rgb=get_color_from_hex('#ECDFCB'))
                    else:
                        Color(rgb=get_color_from_hex('#A18E6E'))
                    Rectangle(pos=(grid_size_x * x, grid_size_y * y), size=(grid_size_x, grid_size_y))
                    is_white = not is_white
                is_white = not is_white

class ChessApp(App):
    def build(self):
        board = ChessBoard()
        if sys.platform[0] == 'l':
            path = '/home/jan/git/ChessAIKivy'
        if sys.platform[0] == 'w':
            path = "C:/Users/janbo/OneDrive/Documents/GitHub/ChessAIKivy"
        try:
            os.chdir(path)
            data_folder = Path("./CSV/")
            file_to_open = data_folder / "begin.csv"
            try:
                with open(file_to_open, 'r') as file:
                    csvreader = csv.reader(file)
                    for row in csvreader:
                        sid = row[1]
                        x = ord(row[2]) - 48
                        y = ord(row[3]) - 48
                        fu = (row[4] == 'T')
                        if row[0] == 'W':
                            if sid[0] == 'P':
                                board.add_widget(Pawn(id="WhitePawn_"+sid[1],source="Assets/PNG/WhitePawn.png",grid_x=x, grid_y=y,First_use=fu))
                            if sid[0] == 'R':
                                board.add_widget(Rook(id="WhiteRook_"+sid[1],source="Assets/PNG/WhiteRook.png",grid_x=x, grid_y=y,First_use=fu))
                            if sid[0] == 'N':
                                board.add_widget(Knight(id="WhiteKnight_"+sid[1],source="Assets/PNG/WhiteKnight.png",grid_x=x, grid_y=y,First_use=fu))
                            if sid[0] == 'B':
                                board.add_widget(Bishop(id="WhiteBishop_"+sid[1],source="Assets/PNG/WhiteBishop.png",grid_x=x, grid_y=y,First_use=fu))
                            if sid[0] == 'Q':
                                board.add_widget(Queen(id="WhiteQueen",source="Assets/PNG/WhiteQueen.png",grid_x=x, grid_y=y))
                            if sid[0] == 'K':
                                board.add_widget(King(id="WhiteKing",source="Assets/PNG/WhiteKing.png",grid_x=x,grid_y=y,First_use=fu))                        
                        if row[0] == 'B':
                            if sid[0] == 'P':
                                board.add_widget(Pawn(id="BlackPawn_"+sid[1],source="Assets/PNG/BlackPawn.png",grid_x=x, grid_y=y,First_use=fu))
                            if sid[0] == 'R':
                                board.add_widget(Rook(id="BlackRook_"+sid[1],source="Assets/PNG/BlackRook.png",grid_x=x, grid_y=y,First_use=fu))
                            if sid[0] == 'N':
                                board.add_widget(Knight(id="BlackKnight_"+sid[1],source="Assets/PNG/BlackKnight.png",grid_x=x, grid_y=y,First_use=fu))
                            if sid[0] == 'B':
                                board.add_widget(Bishop(id="BlackBishop_"+sid[1],source="Assets/PNG/BlackBishop.png",grid_x=x, grid_y=y,First_use=fu))
                            if sid[0] == 'Q':
                                board.add_widget(Queen(id="BlackQueen",source="Assets/PNG/BlackQueen.png",grid_x=x,grid_y=y,First_use=fu))
                            if sid[0] == 'K':
                                board.add_widget(King(id="BlackKing",source="Assets/PNG/BlackKing.png",grid_x=x, grid_y=y,First_use=fu))
                if boardai.human == "Black":
                    ai_move = board.let_ai_move()                
                    print(boardai.to_string()) 
                return board
            except IOError: 
                print("Error: File does not appear to exist.")
            except Exception as err:
                print("Unexpected error",repr(err))
        except FileNotFoundError:
            print("Directory: {0} does not exist".format(path))
        except NotADirectoryError:
            print("{0} is not a directory".format(path))
        except PermissionError:
            print("You do not have permissions to change to {0}".format(path))
    
boardai = boardai.Boardai.new()
alg = boardai.alg
if boardai.human == "Black":
    hmcolor = piecesai.Piece.BLACK
    aicolor = piecesai.Piece.WHITE
else:
    hmcolor = piecesai.Piece.WHITE
    aicolor = piecesai.Piece.BLACK
print("Human ", boardai.human, "Alg ", boardai.alg)
print(boardai.to_string())

if __name__ == '__main__':
    ChessApp().run()
