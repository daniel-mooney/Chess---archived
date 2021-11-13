import functions as func
from colours import bcolours


def check_valid_coords(coord: str):
    coord = coord.upper()

    if len(coord) != 2:
        return False
    if not coord[0].isalpha() or not coord[1].isdigit():
        return False
    if ord(coord[0]) - 65 < 0 or ord(coord[0]) - 65 > 7:
        return False
    if int(coord[1]) < 0 or int(coord[1]) > 8:
        return False  

    return True

def check_valid_move(current_coord: str, move_coord: str, player_number: int, board):

    current_row, current_col = func.grid_coord_to_index(current_coord)
    move_row, move_col = func.grid_coord_to_index(move_coord)

    current_num = func.grid_coord_to_num_coord(current_coord)
    move_num = func.grid_coord_to_num_coord(move_coord)

    piece_bool = True if player_number == 1 else False

    # Check through error types
    if board[current_row][current_col] == '0':
        print(bcolours.FAIL + f"Error: No piece found on square {current_coord}." + bcolours.ENDC)
        return False

    if board[current_row][current_col].islower() != piece_bool:
        player1_error = "Error: Player 1 uses lowercase pieces, not uppercase."
        player2_error = "Error: Player 2 uses uppercase pieces, not lowercase."

        print(bcolours.FAIL + player1_error + bcolours.ENDC) if piece_bool else print(bcolours.FAIL + player2_error + bcolours.ENDC)
        return False
    

    piece_type = board[current_row][current_col]
    target_square = board[move_row][move_col]

    if not check_valid_square(current_num, move_num, piece_type, target_square, player_number):
        piece_type = piece_type.lower()
        piece_dic = {'k': 'king', 'q': 'queen', 'b': 'bishop', 'n': 'knight', 'r': 'rook', 'p': 'pawn'}

        piece = piece_dic[piece_type]
        piece = piece.lower() if player_number == 1 else piece.upper()

        print(bcolours.FAIL + f"Error: Cannot move {piece} ({current_coord} square) to {move_coord} square." + bcolours.ENDC)
        return False
    
    if not check_valid_movement(current_coord, move_coord, player_number, board):
        print(bcolours.FAIL + f"Error: Movement blocked from {current_coord} to {move_coord}." + bcolours.ENDC)
        return False

    return True

def check_valid_square(current_num: int, move_num: int, piece_type: str, target_square: str, player_num: int):
    
    # Possible movements
    diagonals = [9, 11]
    lateral = [1, 2, 3, 4, 5, 6, 7, 10]
    knight = [8, 12, 19, 21]
    king = [1, 9, 10, 11]

    piece_type = piece_type.lower()
    square_difference = abs(current_num - move_num)

    # Check movement
    if piece_type == 'k' and square_difference not in king:
        return False
    elif piece_type == 'q' and (square_difference not in lateral and not [1 for i in diagonals if square_difference % i == 0] and square_difference % 10 != 0):
        return False
    elif piece_type == 'r' and (square_difference not in lateral and square_difference % 10 != 0):
        return False
    elif piece_type == 'n' and not [1 for i in knight if square_difference % i == 0]:
        return False
    elif piece_type == 'b' and not [1 for i in diagonals if square_difference % i == 0]:
        return False
    elif piece_type == 'p' and not valid_pawn_move(current_num, move_num, target_square, player_num):
        return False
    
    return True

def valid_pawn_move(current_num: int, move_num: int, target_square: str, player_num: int):
    
    # Possible movements
    pawn = [10]
    pawn_start = [10, 20]
    pawn_taking = [9, 11]

    square_difference = current_num - move_num

    # Set player respective variables
    if player_num == 1:
        square_difference *= -1
        starting_position = True if (current_num > 20 and current_num < 29) else False
    elif player_num == 2:
        starting_position = True if (current_num > 70 and current_num < 79) else False

    # Check movement scenarios
    if target_square != '0' and square_difference not in pawn_taking:
        return False
    elif target_square == '0' and starting_position and square_difference not in pawn_start:
        return False
    elif target_square == '0' and not starting_position and square_difference not in pawn:
        return False
    
    return True

def check_valid_movement(current_coord: str, move_coord: str, player_number: int, board):
    
    current_num = func.grid_coord_to_num_coord(current_coord)
    move_num = func.grid_coord_to_num_coord(move_coord)
    square_difference = current_num - move_num
    start_row, start_column = func.grid_coord_to_index(current_coord)
    piece_type = (board[start_row][start_column]).upper()

    divisors = [9, 10, 11]

    if square_difference == 0:
        return False
    
    # Iterate through direction of movement
    if square_difference > 0 and piece_type != 'N':
        lowest_divisor = min([d for d in divisors if square_difference % d == 0])
        current_num -= lowest_divisor

        while current_num > move_num:
            row, column = func.num_coord_to_index(current_num)

            if board[row][column] != '0':
                return False
            
            current_num -= lowest_divisor
    elif piece_type != 'N':
        lowest_divisor = min([d for d in divisors if square_difference % d == 0])
        current_num += lowest_divisor

        while current_num < move_num:
            row, column = func.num_coord_to_index(current_num)

            if board[row][column] != '0':
                return False
            
            current_num += lowest_divisor

    # Check if valid ending square
    end_row, end_column = func.grid_coord_to_index(move_coord)
    
    if player_number == 1 and (board[end_row][end_column]).islower():
        return False
    elif player_number == 2 and (board[end_row][end_column]).isupper():
        return False

    return True

def valid_castle(king_coord: str, side: str, player_number: int ,board):
    pass