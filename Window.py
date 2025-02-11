from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
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
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from pathlib import Path
import boardai, piecesai, ai
from move import Move
import os
import sys
import io
import platform
import sysconfig
import csv
import time
import random

Width, Height = 800, 800
Window.size = (Width, Height)

def play_sound(sorf):
    if sorf:
        sound = SoundLoader.load('WAV/success.wav')
    else:
        sound = SoundLoader.load('WAV/failure.wav')
    if sound: 
        sound.play()

def get_user_move(movestr):
    try:
        xfrom = letter_to_xpos(movestr[0:1])
        yfrom = 8 - int(movestr[1:2])
        xto = letter_to_xpos(movestr[2:3])
        yto = 8 - int(movestr[3:4])
        return Move(xfrom, yfrom, xto, yto)
    except ValueError:
        print("Invalid format. Example: A2A4")
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
            available_moves = {"available_moves":[], "pieces_to_capture":[]}
            if self.First_use:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y+1), (self.grid_x, self.grid_y+2)}
            else:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y+1)}
            for piece in pieces:
                if piece.grid_y == self.grid_y + 1 and piece.grid_x == self.grid_x:
                    available_moves["available_moves"] = ()
                if self.First_use and piece.grid_y == self.grid_y + 2 and piece.grid_x == self.grid_x:
                    if len(available_moves) == 2:
                        available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                if piece.id[:9] == "BlackPawn" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y and self.grid_y == 4 and boardai.bep[round(piece.grid_x)]:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y + 1))
                if piece.id[:9] == "BlackPawn" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y and self.grid_y == 4 and boardai.bep[round(piece.grid_x)]:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y + 1))
                if piece.id[:5] == "Black" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y + 1:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y + 1))
                if piece.id[:5] == "Black" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y + 1:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y + 1))
            return available_moves
        if self.id[:5] == "Black":
            available_moves = {"available_moves":(), "pieces_to_capture":[]}
            if self.First_use:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y-1), (self.grid_x, self.grid_y-2)}
            else:
                available_moves["available_moves"] = {(self.grid_x, self.grid_y-1)}
            for piece in pieces:
                if piece.grid_y == self.grid_y - 1 and piece.grid_x == self.grid_x:
                    available_moves["available_moves"] = ()
                if self.First_use and piece.grid_y == self.grid_y - 2 and piece.grid_x == self.grid_x:
                    if len(available_moves) == 2:
                        available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
                if piece.id[:9] == "WhitePawn" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y and self.grid_y == 3 and boardai.wep[round(piece.grid_x)]:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y - 1))          
                if piece.id[:9] == "WhitePawn" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y and self.grid_y == 3 and boardai.wep[round(piece.grid_x)]:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y - 1))
                if piece.id[:5] == "White" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y - 1:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y - 1))
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
                else:
                    available_moves["available_moves"].remove((piece.grid_x, piece.grid_y))
        if self.First_use:
            available_moves["castling"] = self.castling(pieces)
        return available_moves

    def create_moves(self):
        available_moves = {"available_moves":[], "pieces_to_capture":[], "castling": []}
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
        no_attack_left = True
        no_attack_right = True
        if self.First_use:              
            if not ChessBoard.piece_pressed:
                return
            no_piece_left = True
            no_piece_right = True
            for piece in pieces:
                if piece.grid_y == self.grid_y and piece.grid_x > self.grid_x and (piece.id[5:9] != "Rook" or self.id[:5] != piece.id[:5]):
                    no_piece_right = False
                elif piece.grid_y == self.grid_y and piece.grid_x < self.grid_x and (piece.id[5:9] != "Rook" or self.id[:5] != piece.id[:5]):
                    no_piece_left = False
            if no_piece_right:
                aiposx = 7
                if self.id == "WhiteKing":
                     aiposy = 7
                     if boardai.chesspiecesai[aiposx][aiposy] == 0:
                         return []
                     if boardai.chesspiecesai[aiposx][aiposy].id[:9] != "WhiteRook":
                         return []
                     else:
                         if boardai.chesspiecesai[aiposx][aiposy].f == False:
                             return [] 
                if self.id == "BlackKing":
                     aiposy = 0
                     if boardai.chesspiecesai[aiposx][aiposy] == 0:
                         return []
                     if boardai.chesspiecesai[aiposx][aiposy].id[:9] != "BlackRook":
                         return []
                     else:
                         if boardai.chesspiecesai[aiposx][aiposy].f == False:
                             return [] 
            if no_piece_left:
                aiposx = 0
                if self.id == "WhiteKing":
                     aiposy = 7
                     if boardai.chesspiecesai[aiposx][aiposy] == 0:
                         return []
                     if boardai.chesspiecesai[aiposx][aiposy].id[:9] != "WhiteRook":
                         return []
                     else:
                         if boardai.chesspiecesai[aiposx][aiposy].f == False:
                             return [] 
                if self.id == "BlackKing":
                     aiposy = 0
                     if boardai.chesspiecesai[aiposx][aiposy] == 0:
                         return []
                     if boardai.chesspiecesai[aiposx][aiposy].id[:9] != "BlackRook":
                         return []
                     else:
                         if boardai.chesspiecesai[aiposx][aiposy].f == False:
                             return [] 
            if no_piece_left and no_piece_right and self.id == "WhiteKing":
                no_attack_left = self.safe_left(pieces)
                no_attack_right = self.safe_right(pieces)
                if no_attack_left and no_attack_right:
                    return [(self.grid_x-2, 0),(self.grid_x+2, 0)]      
                if no_attack_left:
                    return [(self.grid_x-2, 0)]
                if no_attack_right:  
                    return [(self.grid_x+2, 0)]       
            elif no_piece_left and self.id == "WhiteKing":
                no_attack_left = self.safe_left(pieces) 
                if no_attack_left:
                    return [(self.grid_x-2, 0)]                      
            elif no_piece_right and self.id == "WhiteKing":
                 no_attack_right = self.safe_right(pieces)
                 if no_attack_right:
                     return [(self.grid_x+2, 0)]               
            elif no_piece_left and no_piece_right and self.id == "BlackKing":
                 no_attack_left = self.safe_left(pieces) 
                 no_attack_right = self.safe_right(pieces) 
                 if no_attack_left and no_attack_right:
                     return [(self.grid_x-2, 7),(self.grid_x+2, 7)]     
                 if no_attack_left:
                     return [(self.grid_x-2, 7)]
                 if no_attack_right:
                     return [(self.grid_x+2, 7)]      
            elif no_piece_left and self.id == "BlackKing":
                 no_attack_left = self.safe_left(pieces)  
                 if no_attack_left:
                     return [(self.grid_x-2, 7)]               
            elif no_piece_right and self.id == "BlackKing":
                 no_attack_right = self.safe_right(pieces) 
                 if no_attack_right:
                     return [(self.grid_x+2, 7)]        
            return []
            
    def safe_left(self, pieces):
        if self.id == "WhiteKing":
            places = [[4,0],[3,0],[2,0],[1,0]]
            for plc in places:
                if not self.safe_place(plc, pieces):
                    return False
        if self.id == "BlackKing":
            places = [[4,7],[3,7],[2,7],[1,7]]
            for plc in places:
                if not self.safe_place(plc, pieces):
                    return False
        return True
        
    def safe_right(self, pieces):
        if self.id == "WhiteKing":
            places = [[4,0],[5,0],[6,0]]
            for plc in places:
                if not self.safe_place(plc, pieces):
                    return False
        if self.id == "BlackKing":
            places = [[4,7],[5,7],[6,7]]
            for plc in places:
                if not self.safe_place(plc, pieces):
                    return False
        return True
        
    def safe_place(self, plc, pieces):
        for piece in pieces:
            if (plc[1] == 0 and piece.id[:5] == "Black") or (plc[1] == 7 and piece.id[:5] == "White"):
                if self.attacked(plc, piece):
                    return False
        return True
        
    def attacked(self, plc, piece):
        piecekind = piece.id[5:9]
        if piecekind == "Knig":
            if (piece.grid_x + 2, piece.grid_y + 1) == (plc[0],plc[1]) or (piece.grid_x + 1, piece.grid_y + 2) == (plc[0],plc[1]) or (piece.grid_x - 2, piece.grid_y + 1) == (plc[0],plc[1]) or  (piece.grid_x - 1, piece.grid_y + 2) == (plc[0],plc[1]) or (piece.grid_x + 1, piece.grid_y - 2) == (plc[0],plc[1]) or (piece.grid_x + 2, piece.grid_y - 1) == (plc[0],plc[1]) or  (piece.grid_x - 2, piece.grid_y - 1) == (plc[0],plc[1]) or (piece.grid_x - 1, piece.grid_y - 2) == (plc[0],plc[1]):
               return True
        if piecekind == "Bish":
            if self.diagonal(plc, piece):
                return True
        if piecekind == "Rook":
            if self.straight(plc, piece):
                return True
        if piecekind == "Quee":
            if self.diagonal(plc, piece) or self.straight(plc, piece):
                return True
        if piecekind == "Pawn":
            if (piece.grid_x + 1, piece.grid_y + 1) == (plc[0],plc[1]) or (piece.grid_x - 1, piece.grid_y + 1) == (plc[0],plc[1]) or (piece.grid_x + 1, piece.grid_y - 1) == (plc[0],plc[1]) or (piece.grid_x - 1, piece.grid_y - 1) == (plc[0],plc[1]):
                return True
        return False
        
    def diagonal(self, plc, piece):
        deltax = abs(round(piece.grid_x) - plc[0])
        deltay = abs(round(piece.grid_y) - plc[1])
        if deltax == deltay:
            if piece.grid_x < self.grid_x:
               stepx = +1
            else:
                stepx = -1
            if piece.grid_y < self.grid_y:
                stepy = +1
            else:
                stepy = -1
            for i in range(deltax):
                aiposx = ai_to_hm_x(round(piece.grid_x) + i * stepx + stepx)
                aiposy = ai_to_hm_y(round(piece.grid_y) + i * stepy + stepy)
                if boardai.chesspiecesai[aiposx][aiposy] != 0:
                    break
            if aiposy == ai_to_hm_y(plc[1]) and (boardai.chesspiecesai[aiposx][aiposy] == 0 or boardai.chesspiecesai[aiposx][aiposy].id[5:9] == "King"):
                return True
        return False
    
    def straight(self, plc, piece):
        deltax = abs(round(piece.grid_x) - plc[0])
        deltay = abs(round(piece.grid_y) - plc[1])
        if deltax == 0 or deltay == 0:
            if deltay == 0:
                aiposy = ai_to_hm_y(plc[1])
                if piece.grid_x < self.grid_x:
                    stepx = +1
                if piece.grid_x > self.grid_x:
                    stepx = -1
                for i in range(deltax):
                    aiposx = ai_to_hm_x(round(piece.grid_x) + i * stepx + stepx)
                    if boardai.chesspiecesai[aiposx][aiposy] != 0:
                        break
                if aiposx == ai_to_hm_x(plc[0]) and (boardai.chesspiecesai[aiposx][aiposy] == 0 or boardai.chesspiecesai[aiposx][aiposy].id[5:9] == "King"):
                    return True
            if deltax == 0:
                aiposx = ai_to_hm_x(plc[0])
                if piece.grid_y < self.grid_y:
                    stepy = +1
                if piece.grid_y > self.grid_y:
                    stepy = -1
                for i in range(deltay):
                    aiposy = ai_to_hm_y(round(piece.grid_y) + i * stepy + stepy)
                    if boardai.chesspiecesai[aiposx][aiposy] != 0:
                        break
                if aiposy == ai_to_hm_y(plc[1]) and (boardai.chesspiecesai[aiposx][aiposy] == 0 or boardai.chesspiecesai[aiposx][aiposy].id[5:9] == "King"):
                    return True
        return False
       
class ChessBoard(RelativeLayout):
    piece_pressed = False
    id_piece_ = None
    available_moves = {"available_moves":[], "pieces_to_capture":[], "castling": []}
    piece_index = None
    check = BooleanProperty(defaultvalue=False)
    hmmove = "C2C3"
    index = 0
    white_chess = False
    black_chess = False
    chessmate = False
    
    def __init__(self, **kwargs):
        super(ChessBoard, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down = self.make_ai_move)
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self.make_ai_move)
        self._keyboard = None
        
    def valid_bishop(self, move):
        print("Bishop Move", move.xfrom, move.yfrom, move.xto, move.yto)
        return True  
                
    def valid_knight(self, move):
        print("Knight Move", move.xfrom, move.yfrom, move.xto, move.yto)
        return True
        
    def validation(self, move, piece_type):
        print("Move", move.xfrom, move.yfrom, move.xto, move.yto, "Type", piece_type)
        if piece_type == "Bish":
            return self.valid_bishop(move)
        if piece_type == "Knig":
            return self.valid_knight(move)
        return True
        
    def check_ai_move(self):
        move = get_user_move(self.hmmove)
        ChessBoard.piece_index = ChessBoard.pieceindex_at_board(self, move.xfrom, move.yfrom)
        if ChessBoard.piece_index > -1:
            child = self.children[ChessBoard.piece_index]
        if not self.validation(move, child.id[5:9]):
            return False
        boardai.perform_move(move)
        ChessBoard.piece_index = ChessBoard.pieceindex_at_board(self, move.xto, move.yto)
        if ChessBoard.piece_index > -1:
             self.remove_widget(self.children[ChessBoard.piece_index])
        anim = Animation(grid_x = move.xto, grid_y = ai_to_hm_y(move.yto), t='in_out_expo', duration=0.5)
        anim.start(child)
        if (child.id[0:5] == boardai.human):
            ai_move = self.let_ai_move()
        print(boardai.to_string())
        if child.id[5:9] == "Pawn" and move.yto == 0 and (move.xfrom - move.xto) == 0:
            self.remove_widget(child)
            self.add_widget(Queen(id="WhiteQueen2",source="Assets/PNG/WhiteQueen.png", grid_x = move.xto, grid_y = 7))
        if child.id[5:9] == "Pawn" and move.yto == 7 and (move.xfrom - move.xto) == 0:
            self.remove_widget(child)
            self.add_widget(Queen(id="BlackQueen2",source="Assets/PNG/BlackQueen.png", grid_x = move.xto, grid_y = 0))
        if child.id[5:9] == "Pawn" and move.yto == 0 and abs(move.xfrom - move.xto) == 1:
            self.remove_widget(child)
            self.add_widget(Queen(id="WhiteQueen2",source="Assets/PNG/WhiteQueen.png", grid_x = move.xto, grid_y = 7))
        if child.id[5:9] == "Pawn" and move.yto == 7 and abs(move.xfrom - move.xto) == 1:
            self.remove_widget(child)
            self.add_widget(Queen(id="BlackQueen2",source="Assets/PNG/BlackQueen.png", grid_x = move.xto, grid_y = 0))
        if child.id[5:9] == "Pawn" and abs(move.xfrom - move.xto) == 1 and abs(move.yfrom - move.yto) == 1 and move.yto == 2:
            anim = Animation(grid_x = move.xto, grid_y = 5, t='in_out_expo', duration=0.5)
            anim.start(child)
            ChessBoard.piece_index = ChessBoard.pieceindex_at_board(self, move.xto, 3)
            if ChessBoard.piece_index > -1:
                child = self.children[ChessBoard.piece_index]
                self.remove_widget(child)
        if child.id[5:9] == "Pawn" and abs(move.xfrom - move.xto) == 1 and abs(move.yfrom - move.yto) == 1 and move.yto == 5:
            anim = Animation(grid_x = move.xto, grid_y = 2, t='in_out_expo', duration=0.5)
            anim.start(child)
            ChessBoard.piece_index = ChessBoard.pieceindex_at_board(self, move.xto, 4)
            if ChessBoard.piece_index > -1:
                child = self.children[ChessBoard.piece_index]
                self.remove_widget(child)
        if child.id[5:9] == "King" and child.First_use:
            if move.xfrom - move.xto == 2:
                if move.yto == 7:
                    ChessBoard.piece_index = ChessBoard.pieceindex_at_board(self, 0, 7)
                    if ChessBoard.piece_index > -1:
                        rook = self.children[ChessBoard.piece_index]
                        if rook.id[5:9] == "Rook" and rook.First_use and ChessBoard.pieceindex_at_board(self, 3, 7) == -1 and ChessBoard.pieceindex_at_board(self, 2, 7) == -1 and ChessBoard.pieceindex_at_board(self, 1, 7) == -1:
                            anim = Animation(grid_x = 3, grid_y = 0, t='in_out_expo', duration=0.5)
                            anim.start(rook)
                if move.yto == 0:
                    ChessBoard.piece_index = ChessBoard.pieceindex_at_board(self, 0, 0)
                    if ChessBoard.piece_index > -1:
                        rook = self.children[ChessBoard.piece_index]
                        if rook.id[5:9] == "Rook" and rook.First_use and ChessBoard.pieceindex_at_board(self, 3, 0) == -1 and ChessBoard.pieceindex_at_board(self, 2, 0) == -1 and ChessBoard.pieceindex_at_board(self, 1, 0) == -1:
                            anim = Animation(grid_x = 3, grid_y = 7, t='in_out_expo', duration=0.5)
                            anim.start(rook)
            if move.xfrom - move.xto == -2:
                if move.yto == 7:
                    ChessBoard.piece_index = ChessBoard.pieceindex_at_board(self, 7, 7)
                    if ChessBoard.piece_index > -1:
                        rook = self.children[ChessBoard.piece_index]
                        if rook.id[5:9] == "Rook" and rook.First_use and ChessBoard.pieceindex_at_board(self, 5, 7) == -1 and ChessBoard.pieceindex_at_board(self, 6, 7) == -1:
                            anim = Animation(grid_x = 5, grid_y = 0, t='in_out_expo', duration=0.5)
                            anim.start(rook)
                if move.yto == 0:
                    ChessBoard.piece_index = ChessBoard.pieceindex_at_board(self, 7, 0)
                    if ChessBoard.piece_index > -1:
                        rook = self.children[ChessBoard.piece_index]
                        if rook.id[5:9] == "Rook" and rook.First_use and ChessBoard.pieceindex_at_board(self, 5, 0) == -1 and ChessBoard.pieceindex_at_board(self, 6, 0) == -1:
                            anim = Animation(grid_x = 5, grid_y = 7, t='in_out_expo', duration=0.5)
                            anim.start(rook)
        return True
            
    def perform_ai_move(self, xfrom, yfrom, xto, yto):
        self.hmmove = "" + xpos_to_letter(xfrom) + ypos_to_digit(yfrom) + xpos_to_letter(xto) + ypos_to_digit(yto)
        move = get_user_move(self.hmmove)
        boardai.perform_move(move)
        
    def make_ai_move(self, keyboard, keycode, text, modifiers):
        l = keycode[1]
        if l == 'q':
            self.close_application()   
        elif l == 'm':
            self.hmmove = "    "
            self.index = 0
        elif (l >= 'a' and l <= 'h') or (l >= '1' and l <= '8'):
            if self.index < 4:
                self.hmmove = self.hmmove[: self.index] + l + self.hmmove[self.index + 1:]
                self.index += 1
        elif l == '.':
            aiposx = ai_to_hm_x(letter_to_xpos(self.hmmove[0:1]))
            aiposy = ai_to_hm_y(int(self.hmmove[1:2]) - 1)
            if boardai.human == "White":
                labelcolor = [1, 1, 1, 1] 
            else:
                labelcolor = [0, 0, 0, 1] 
            if boardai.chesspiecesai[aiposx][aiposy] != 0:
                piecestr = str(boardai.chesspiecesai[aiposx][aiposy].piece_type)
                message = Label(text = "Correct? " + self.hmmove + piecestr, color = labelcolor, font_size='50sp')
            else:
                message = Label(text = "Correct? " + self.hmmove + "None", color = labelcolor, font_size='50sp')
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(message)
            button_layout = BoxLayout(size_hint_y=0.3)
            yes_button = Button(text = 'Yes')
            yes_button.bind(on_release=self.on_yes)
            button_layout.add_widget(yes_button)
            no_button = Button(text = 'No')
            no_button.bind(on_release=self.on_no)
            button_layout.add_widget(no_button)
            layout.add_widget(button_layout)
            self.pp = Popup(title = "AI", title_size = 50, content = layout, size_hint = (0.5, 0.5), background_color = [4,.4,.2, 1])
            self.pp.open()
        return True
        
    def on_yes(self, instance):
        play_sound(self.check_ai_move())
        self.hmmove = "    "
        self.index = 0
        self.pp.dismiss()
    
    def on_no(self, instance):
        play_sound(False)
        self.pp.dismiss()

    def close_application(self): 
        App.get_running_app().stop() 
        Window.close()
    
    def listpieces(self):
        for child in self.children:
            print("Human board",child.id,child.grid_x,child.grid_y,child.First_use)
            
    def let_ai_move(self):
        if alg == '-':
            if boardai.human == "White":
                boardai.human = "Black"
            else:
                boardai.human = "White"
            return 0
        ai_move = ai.AI.get_ai_move(boardai, [], aicolor, hmcolor, alg)
        if type(ai_move) is int:
            self.chessmate = True
            color = "Black"
            if aicolor == 'W':
                color = "White"
            self.animate(color)
            return 0
        boardai.perform_move(ai_move)
        if type(boardai.pos_king(hmcolor)) is int:
            self.chessmate = True
            color = "Black"
            if aicolor == 'B':
                color = "White"
            self.animate(color)
        propawn = self.piece_at_board(ai_move.xfrom, ai_to_hm_y(ai_move.yfrom))
        if ai_move.yfrom == 6 and ai_move.yto == 7 and ai_move.xfrom == ai_move.xto and boardai.chesspiecesai[ai_move.xto][ai_move.yto].id == "BlackQueen" and propawn.id[:9] == "BlackPawn":
            self.remove_widget(propawn)
            self.add_widget(Queen(id="",source="Assets/PNG/BlackQueen.png", grid_x=ai_move.xto, grid_y=0))
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
            
    def pieceindex_at_board(self, xpos, ypos):
        ypos = ai_to_hm_y(ypos)
        index = -1
        for child in self.children:
            index += 1
            if child.grid_x == xpos and child.grid_y == ypos:
                return index
        return -1
                
    def piece_at_board(self, xpos, ypos):
        for child in self.children:
            if child.grid_x == xpos and child.grid_y == ypos:
                return child
        print("No piece_at_board Piece 0 oordinaten", xpos, ypos)
        return None
                    
    def mark_en_passant(self, c, x):
        if c == "White":
            boardai.wep[x] = True
        elif c == "Black":
            boardai.bep[x] = True
  
    def clear_en_passant(self, c):
        if c == "White":
            boardai.wep = [False,False,False,False,False,False,False,False]
        elif c == "Black":
            boardai.bep = [False,False,False,False,False,False,False,False]

    def on_touch_down(self, touch):
        if self.chessmate:
            return
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
                    anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_quad', duration=0.5)
                    anim.start(self.children[id])
                    self.children[id].grid_x = grid_x
                    self.children[id].grid_y = grid_y
                    ChessBoard.piece_pressed = False
                    ChessBoard.available_moves = {"available_moves":[], "pieces_to_capture":[]}
                    self.perform_ai_move(round(old_x), round(old_y), grid_x, grid_y)
                    if grid_y == 7 and child.id[0:9] == "WhitePawn":
                        self.remove_widget(child)
                        self.add_widget(Queen(id="WhiteQueen2",source="Assets/PNG/WhiteQueen.png", grid_x=grid_x, grid_y=grid_y))
                    if grid_y == 0 and child.id[0:9] == "BlackPawn":
                        self.remove_widget(child)
                        self.add_widget(Queen(id="BlackQueen2",source="Assets/PNG/BlackQueen.png", grid_x=grid_x, grid_y=grid_y))
                    ai_move = self.let_ai_move()
                    if child.id[5:9] == "Pawn" and abs(grid_y - old_y) == 2:
                        self.mark_en_passant(child.id[:5], grid_x)
                    else:
                        self.clear_en_passant(boardai.human) 
                    if (child.id[5:9] == "Pawn" or child.id[5:9] == "Rook" or child.id[5:9] == "King") and child.First_use:
                        child.First_use = False
                    self.draw_moves()
                    print(boardai.to_string())
                    self.check_check()
                    break      
                elif (grid_x, grid_y) in ChessBoard.available_moves["pieces_to_capture"]:
                    enpassant = False
                    for enemy in self.children:
                        if enemy.grid_x == grid_x and enemy.grid_y == grid_y:
                            anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_out_expo', duration=0.5)
                            anim.start(self.children[id])
                            self.children[id].grid_x = grid_x
                            self.children[id].grid_y = grid_y
                            self.remove_widget(enemy)
                            ChessBoard.piece_pressed = False
                            ChessBoard.available_moves = {"available_moves":[], "pieces_to_capture":[]}
                            self.perform_ai_move(round(old_x), round(old_y), grid_x, grid_y)
                            if grid_y == 7 and child.id[0:9] == "WhitePawn":
                                self.remove_widget(child)
                                self.add_widget(Queen(id="WhiteQueen2",source="Assets/PNG/WhiteQueen.png", grid_x=grid_x, grid_y=grid_y))
                            if grid_y == 0 and child.id[0:9] == "BlackPawn":
                                self.remove_widget(child)
                                self.add_widget(Queen(id="BlackQueen2",source="Assets/PNG/BlackQueen.png", grid_x=grid_x, grid_y=grid_y))
                            ai_move = self.let_ai_move() 
                            if (child.id[5:9] == "Pawn" or child.id[5:9] == "Rook" or child.id[5:9] == "King") and child.First_use:
                                child.First_use = False
                            self.draw_moves() 
                            print(boardai.to_string())
                            self.check_check()                  
                            break
                        elif child.id[5:9] == "Pawn" and enemy.id[5:9] == "Pawn" and (child.grid_x - 1 == enemy.grid_x or child.grid_x + 1 == enemy.grid_x) and child.grid_y == enemy.grid_y and child.id[:5] != enemy.id[:5]:
                            anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_out_expo', duration=0.5)
                            anim.start(child)
                            if enemy.grid_x == grid_x and enemy.grid_y == grid_y - 1 and enemy.grid_y == 4 and enemy.id[:5] == "Black":
                                self.remove_widget(enemy)
                            if enemy.grid_x == grid_x and enemy.grid_y == grid_y + 1 and enemy.grid_y == 3 and enemy.id[:5] == "White":
                                self.remove_widget(enemy)
                            ChessBoard.piece_pressed = False
                            ChessBoard.available_moves = {"available_moves":[], "pieces_to_capture":[]}
                            self.perform_ai_move(round(old_x), round(old_y), grid_x, grid_y)
                            ai_move = self.let_ai_move() 
                            self.draw_moves()
                            enpassant = True
                            self.check_check()
                    self.clear_en_passant(boardai.human) 
            elif ChessBoard.piece_pressed and ChessBoard.id_piece_[5:] == "King" and (grid_x, grid_y) in ChessBoard.available_moves["castling"]:
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
                    ChessBoard.available_moves = {"available_moves":[], "pieces_to_capture":[]}
                    print(boardai.to_string())
                    self.draw_moves()
                    
    def animate(self, color):
        id = color + "King"
        piece = self.findpiece(id)
        xpos = piece.grid_x
        ypos = piece.grid_y
        self.remove_widget(piece)
        self.add_widget(King(id="DeadKing",source="Assets/PNG/" + color + "Dead.png",grid_x=xpos, grid_y=ypos,First_use=True))
        piece = self.findpiece("DeadKing")
        while True:
            xpos = random.randint(0, 7)
            ypos = random.randint(0, 7)
            if boardai.chesspiecesai[ai_to_hm_x(xpos)][ai_to_hm_y(ypos)] == 0:
                break
        anim = Animation(grid_x=xpos, grid_y=ypos, t='out_bounce', duration=5.0)
        anim += Animation(grid_x=xpos, grid_y=ypos, t='out_bounce', duration=5.0)
        anim.start(piece)

    def attack_king(self, plc, piece, col, row):
        if piece == "N":
            if (col + 2, row + 1) == (plc[0], plc[1]) or (col + 1, row + 2) == (plc[0], plc[1]) or (col - 2, row + 1) == (plc[0], plc[1]) or (col - 1, row + 2) == (plc[0], plc[1]) or (col + 1, row - 2) == (plc[0], plc[1]) or (col + 2, row - 1) == (plc[0], plc[1]) or (col - 2, row - 1) == (plc[0], plc[1]) or (col - 1, row - 2) == (plc[0], plc[1]):
                return True
        if piece == "B":
            if self.check_diagonal(plc, col, row):
                return True
        if piece == "R":
            if self.check_straight(plc, col, row):
                return True
        if piece == "Q":
            if self.check_diagonal(plc, col, row) or self.check_straight(plc, col, row):
                return True
        if piece == "P":
            if (col + 1, row + 1) == (plc[0], plc[1]) or (col - 1, row + 1) == (plc[0], plc[1]) or (col + 1, row - 1) == (plc[0], plc[1]) or (col - 1, row - 1) == (plc[0], plc[1]):
                return True
        return False
          
    def check_diagonal(self, plc, col, row):
        deltax = abs(col - plc[0])
        deltay = abs(row - plc[1])
        if deltax == deltay:
            if col < plc[0]:
               stepx = +1
            else:
                stepx = -1
            if row < plc[1]:
                stepy = +1
            else:
                stepy = -1
            for i in range(deltax):
                aiposx = ai_to_hm_x(col + i * stepx + stepx)
                aiposy = ai_to_hm_y(row + i * stepy + stepy)
                if boardai.chesspiecesai[aiposx][aiposy] != 0:
                    piecestr = str(boardai.chesspiecesai[aiposx][aiposy].piece_type)
                    if piecestr == "K":
                        return True
                    break
        return False
        
    def check_straight(self, plc, col, row):
        deltax = abs(col - plc[0])
        deltay = abs(row - plc[1])
        if deltax == 0 or deltay == 0:
            if deltax == 0:
                if row < plc[1]:
                    stepy = +1
                if row > plc[1]:
                    stepy = -1
                aiposx = ai_to_hm_x(plc[0])
                for i in range(deltay):
                    aiposy = ai_to_hm_y(row + i * stepy + stepy)
                    if boardai.chesspiecesai[aiposx][aiposy] != 0:
                        piecestr = str(boardai.chesspiecesai[aiposx][aiposy].piece_type)
                        if piecestr == "K":
                            return True
                        break
            return False
            if deltay == 0:
                if col < plc[0]:
                    stepx = +1
                if col > plc[0]:
                    stepx = -1
                aiposy = ai_to_hm_y(plc[1])              
                for i in range(deltax):
                    aiposx = ai_to_hm_x(col + i * stepx + stepx)
                    if boardai.chesspiecesai[aiposx][aiposy] != 0:
                        piecestr = str(boardai.chesspiecesai[aiposx][aiposy].piece_type)
                        if piecestr == "K":
                            return True
                        break
            return False
        return False
          
    def check_place(self, color, plc):
        for x in range(8):
            for y in range(8):
                if boardai.chesspiecesai[x][y] != 0 and str(boardai.chesspiecesai[x][y].color) != color:
                    piecestr = str(boardai.chesspiecesai[x][y].piece_type)
                    col = ai_to_hm_x(x)
                    row = ai_to_hm_y(y)
                    if self.attack_king(plc, piecestr, col, row):
                        return True
        return False

    def check_white(self):
        for j in range(8):
            for i in range(8):
                 if boardai.chesspiecesai[i][j] != 0 and str(boardai.chesspiecesai[i][j].piece_type) == "K" and str(boardai.chesspiecesai[i][j].color) == "W":
                     return self.check_place("W", [ai_to_hm_x(i), ai_to_hm_y(j)])
        return False
        
    def check_black(self):
        for j in range(8):
            for i in range(8):
                 if boardai.chesspiecesai[i][j] != 0 and str(boardai.chesspiecesai[i][j].piece_type) == "K" and str(boardai.chesspiecesai[i][j].color) == "B":
                     return self.check_place("B", [ai_to_hm_x(i), ai_to_hm_y(j)])
        return False
        
    def check_check(self):
        if boardai.human == "Black":
            if self.white_chess:
                if self.check_white():
                    self.animate("White")
                    self.chessmate = True
                    return
                else:
                    self.white_chess = False
                    return
            if self.check_black():
                self.black_chess = True
                return
            if self.check_white():
                self.animate("White")
                self.chessmate = True
                return
        if boardai.human == "White":
            if self.black_chess:
                if self.check_black():
                    self.animate("Black")
                    self.chessmate = True
                    return
                else:
                    self.black_chess = False
                    return
            if self.check_white():
                self.white_chess = True
                return
            if self.check_black():
                self.animate("Black")
                self.chessmate = True
                return

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
