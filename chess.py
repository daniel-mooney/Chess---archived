import numpy as np
from colours import bcolours
import math
import movement_control as move_ctrl
import coordinate_conversions as convert

class Chess():
    def __init__(self):

        self.board = np.array([
            ["-", "A", "B", "C", "D", "E", "F", "G", "H"],
            ['8', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['7', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['6', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['5', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['4', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['3', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['2', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['1', 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ])

        self.moves = []     # (moved_piece, taken_piece, current_coord, moved_coord)
    
    def reset_board(self):
        self.board = np.array([
            ["-", "A", "B", "C", "D", "E", "F", "G", "H"],
            ['8', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['7', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['6', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['5', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['4', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['3', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['2', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['1', 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
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
        print(bcolours.BOLD + "MOVES" + bcolours.ENDC + " - prints a list of all previous moves.")
        print(bcolours.BOLD + "PRINT" + bcolours.ENDC + " - prints the current board to terminal.")
        print(bcolours.BOLD + "GUIDE" + bcolours.ENDC + " - prints the control guide to terminal.")
        print()

    def print_moves(self):
        
        if len(self.moves) > 0:
            print("Moves played:", end="\n\n")

            for i in range( math.ceil(len(self.moves) / 2) ):
                piece = self.moves[2*i][0]
                move_coord = self.moves[2*i][3]

                if self.moves[2*i][1] == '0':
                    print(f"{i+1}. {piece} - {move_coord}", end='')
                else:
                    print(f"{i+1}. {piece} - x{move_coord}", end='')


                if (2*i + 1) < len(self.moves):
                    piece = self.moves[2*i + 1][0]
                    move_coord = self.moves[2*i + 1][3]
                    
                    if self.moves[2*i + 1][1] == '0':
                        print(f", {piece} - {move_coord}")
                    else:
                        print(f", {piece} - x{move_coord}")

                else:
                    print()
            print()
        else:
            print("No moves played so far.", end="\n\n")

    def move_piece(self, current_cord: str, move_coord: str, player_number: int):
        
        if current_cord == "castle":
            # Error checking
            if move_coord.lower() != 'k' and move_coord.lower() != 'q':
                print(f"Invalid castle command: {move_coord}")
                print(move_coord)
                return False
            if not move_ctrl.valid_castle(move_coord, player_number, self.board, self.moves):
                print("Invalid Castle move.")
                return False
            # Castle
            col = 5
            rook_col = 1 if move_coord.upper() == 'Q' else 8
            king_row = 8 if player_number == 1 else 1

            # Queen side
            if move_coord.upper() == 'Q':
                self.board[king_row][col - 2] = self.board[king_row][col]   # Move King
                self.board[king_row][col] = '0'

                self.board[king_row][rook_col + 3] = self.board[king_row][rook_col]     # Move Rook
                self.board[king_row][rook_col] = '0'
            # King side
            elif move_coord.upper() == 'K':
                self.board[king_row][col + 2] = self.board[king_row][col]   # Move King
                self.board[king_row][col] = '0'

                self.board[king_row][rook_col - 2] = self.board[king_row][rook_col]     # Move Rook
                self.board[king_row][rook_col] = '0'
                
            return True
        else:
            # Error checking
            if not move_ctrl.check_valid_coords(current_cord):
                print(bcolours.FAIL + f"Error: Invalid co-ordinate input: {current_cord}" + bcolours.ENDC)
                return False
            if not move_ctrl.check_valid_coords(move_coord):
                print(bcolours.FAIL + f"Error: Invalid co-ordinate input: {move_coord}" + bcolours.ENDC)
                return False
            if not move_ctrl.check_valid_move(current_cord, move_coord, player_number, self.board):
                return False
            if not move_ctrl.check_pin(current_cord, move_coord, player_number, self.board):
                print(bcolours.FAIL + "Cannot move a pinned piece" + bcolours.ENDC)
                return False
        
        # Move piece
        current_cord = current_cord.upper()
        move_coord = move_coord.upper()

        current_row, current_col = convert.grid_coord_to_index(current_cord)
        move_row, move_col = convert.grid_coord_to_index(move_coord)

        move_info = (self.board[current_row][current_col], self.board[move_row][move_col], current_cord, move_coord)
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

                if current_coord == "moves":
                    self.print_moves()
                    continue

                if current_coord == "guide":
                    self.print_control_guide()
                    continue

                if current_coord == "print":
                    print(self.board)
                    continue

                if current_coord == "castle":
                    move_coord = input("King(K) or Queen(Q) side: ")
                else:
                    move_coord = input("Choose a square to move to: ")

                successful_move = self.move_piece(current_coord, move_coord, player_number)

                if not successful_move:
                    print(f"\nPlayer {player_number} please try again...")
        
            player_number = 2 if player_number == 1 else 1