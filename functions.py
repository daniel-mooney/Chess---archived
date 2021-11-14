import numpy as np
import movement_control as move
from colours import bcolours
import math

class Chess():
    def __init__(self):

        self.board = np.array([
            ["-", "A", "B", "C", "D", "E", "F", "G", "H"],
            ['8', 'R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
            ['7', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['6', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['5', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['4', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['3', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['2', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['1', 'r', 'n', 'b', 'k', 'q', 'b', 'n', 'r']
        ])

        self.moves = []
    
    def reset_board(self):
        self.board = np.array([
            ["-", "A", "B", "C", "D", "E", "F", "G", "H"],
            ['8', 'R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
            ['7', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['6', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['5', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['4', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['3', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['2', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['1', 'r', 'n', 'b', 'k', 'q', 'b', 'n', 'r']
        ])

        print("The board has been reset")
    
    def print_control_guide(self):
        key = 'Key: R - Rook, N - Knight, B - Bishop, K - King, Q - Queen, P - Pawn.'

        print('\nLowercase is player 1, uppercase is player 2, player 1 goes first.')
        print(key, end = '\n\n')
        print(bcolours.BOLD + bcolours.GREEN + "Control Guide" + bcolours.ENDC)
        print("-------------")
        print("Choose the piece you wish to move when prompted, make sure the case type matches your player type.")
        print("Enter the square you wish to move that piece to.", end="\n\n")
        print("Other Commands:")
        print(bcolours.BOLD + "CASTLE" + bcolours.ENDC + " - when you wish to castle your king.")
        print(bcolours.BOLD + "PRINT" + bcolours.ENDC + " - prints a list of all previous moves.")
        print(bcolours.BOLD + "GUIDE" + bcolours.ENDC + " - prints the control guide to terminal")
        print()

    def print_moves(self):
        
        if len(self.moves) > 0:
            print("Moves played:", end="\n\n")

            for i in range( math.ceil(len(self.moves) / 2)):
                if self.moves[2*i][2] != '0':
                    piece = self.moves[2*i][0]
                    move_coord = self.moves[2*i][2]

                    print(f"{i+1}. {piece} - {move_coord}", end='')

                if (2*i + 1) < len(self.moves):
                    piece = self.moves[2*i + 1][0]
                    move_coord = self.moves[2*i + 1][2]

                    print(f", {piece} - {move_coord}")
                else:
                    print()
            print()
        else:
            print("No moves played so far.", end="\n\n")

    def move_piece(self, current_cord: str, move_coord: str, player_number: int):
        
        # Error Checking
        if current_cord == "castle":
            return True

        if not move.check_valid_coords(current_cord):
            print(bcolours.FAIL + f"Error: Invalid co-ordinate input: {current_cord}" + bcolours.ENDC)
            return False

        if not move.check_valid_coords(move_coord):
            print(bcolours.FAIL + f"Error: Invalid co-ordinate input: {move_coord}" + bcolours.ENDC)
            return False

        if not move.check_valid_move(current_cord, move_coord, player_number, self.board):
            return False
        
        # Move piece
        current_cord = current_cord.upper()
        move_coord = move_coord.upper()

        current_row, current_col = grid_coord_to_index(current_cord)
        move_row, move_col = grid_coord_to_index(move_coord)

        move_info = (self.board[current_row][current_col], self.board[move_row][move_col], move_coord)
        self.moves.append(move_info)

        self.board[move_row][move_col] = self.board[current_row][current_col]
        self.board[current_row][current_col] = '0'


        return True

    def play(self):
        # Message to terminal
        self.print_control_guide()

        player_number = 1

        while True:
            print(f"\n{self.board}")

            successful_move = False
            print(f"\nPlayer {player_number}'s go.")

            while not successful_move:
                current_coord = input("Choose a piece to move: ")
                current_coord = current_coord.lower()

                if current_coord == "print":
                    self.print_moves()
                    continue

                if current_coord == "guide":
                    self.print_control_guide()
                    continue

                if current_coord == "castle":
                    move_coord = input("King(K) or Queen(Q) side: ")
                else:
                    move_coord = input("Choose a square to move to: ")

                successful_move = self.move_piece(current_coord, move_coord, player_number)

                if not successful_move:
                    print(f"\nPlayer {player_number} please try again...")
        
            player_number = 2 if player_number == 1 else 1



def grid_coord_to_num_coord(coord: str):
    """
    Converts a grid co-ordinate into a numeric co-ordinate used to control movement
    """
    coord = coord.upper()

    column = ord(coord[0]) - 64
    row = int(coord[1])

    return (row * 10) + column

def grid_coord_to_index(coord: str):
    """
    Returns a tuple `(row, column)` for a given coordinate in the board matrix
    """
    row_index = [8 ,7, 6, 5, 4, 3, 2, 1]
    coord = coord.upper()

    row = row_index[int(coord[1]) - 1]
    column = ord(coord[0]) - 64

    return (row, column)

def num_coord_to_index(num_coord: int):
    
    row_index = [8 ,7, 6, 5, 4, 3, 2, 1]

    row = row_index[(num_coord // 10) - 1]
    column = num_coord % 10

    return (row, column)