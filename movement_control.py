from colours import bcolours
import coordinate_conversions as convert


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

def check_valid_move(current_coord: str, move_coord: str, player_number: int, board: iter):

    current_row, current_col = convert.grid_coord_to_index(current_coord)
    move_row, move_col = convert.grid_coord_to_index(move_coord)

    current_num = convert.grid_coord_to_num_coord(current_coord)
    move_num = convert.grid_coord_to_num_coord(move_coord)

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

def check_valid_movement(current_coord: str, move_coord: str, player_number: int, board: iter):
    
    current_num = convert.grid_coord_to_num_coord(current_coord)
    move_num = convert.grid_coord_to_num_coord(move_coord)
    square_difference = current_num - move_num
    start_row, start_column = convert.grid_coord_to_index(current_coord)
    piece_type = (board[start_row][start_column]).upper()

    divisors = [9, 10, 11]

    if square_difference == 0:
        return False
    
    # Iterate through direction of movement
    if square_difference > 0 and piece_type != 'N':
        lowest_divisor = min([d for d in divisors if square_difference % d == 0])
        current_num -= lowest_divisor

        while current_num > move_num:
            row, column = convert.num_coord_to_index(current_num)

            if board[row][column] != '0':
                return False
            
            current_num -= lowest_divisor
    elif piece_type != 'N':
        lowest_divisor = min([d for d in divisors if square_difference % d == 0])
        current_num += lowest_divisor

        while current_num < move_num:
            row, column = convert.num_coord_to_index(current_num)

            if board[row][column] != '0':
                return False
            
            current_num += lowest_divisor

    # Check if valid ending square
    end_row, end_column = convert.grid_coord_to_index(move_coord)
    
    if player_number == 1 and (board[end_row][end_column]).islower():
        return False
    elif player_number == 2 and (board[end_row][end_column]).isupper():
        return False

    return True

def valid_castle(side: str, player_number: int ,board: iter, moves: list):
    """
    Checks whether a castle command is valid
    """
    row, col = (8, 5) if player_number == 1 else (1, 5)

    # Check if king has been previously moved
    player_king = 'k' if player_number == 1 else 'K'

    for move in moves:
        if player_king in move:
            return False
    
    # Check if corresponding rook has been moved
    if player_number == 1:
        for move in moves:
            if side == 'Q' and 'A1' in move:
                return False
            elif side == 'K' and 'H1' in move:
                return False
    elif player_number == 2:
        for move in moves:
            if side == 'Q' and 'A8' in move:
                return False
            elif side == 'K' and 'H8' in move:
                return False
    
    # Check for blocking pieces or checks
    check_map = create_check_map(board)
    valid_sqaures = ['0', str(player_number)]

    if side.upper() == 'K':
        for i in range(1, 3):
            if check_map[row][col + i] not in valid_sqaures:
                return False
    elif side.upper() == 'Q':
        for i in range(1, 4):
            if check_map[row][col - i] not in valid_sqaures:
                return False

    return True


def create_check_map(board: iter):
    """
    Creates a check map of the entire board, used to determine whether a kind is in check, a castle command
    is valid or if the king is in mate.
    """
    # key = {1 = player one check, 2 = player two check, X = both check, 0 = no check}
    
    # Iterate through board
    for row in range(1, 9):
        for column in range(1, 9):
            if board[row][column].isalpha():
                board = set_check_lines(board, row, column)
    return board
                

def set_check_lines(board: iter, piece_row: int, piece_col: int):
    """
    Sets the checklines (line of attack) of a piece in a particular row and column of a chess board.
    """
    piece_range = {
        'k': [1, 9, 10, 11],    # King
        'q': [1, 9, 10 ,11],    # Queen
        'r': [1, 10],           # Rook
        'b': [9, 11],           # Bishop
        'n': [8, 12, 19, 21],   # Knight
        'p': [9, 11]            # Pawn
    }

    starting_num = convert.index_to_num_coord(piece_row, piece_col)
    piece = board[piece_row][piece_col]
    player_number = '1' if piece.islower() else '2'
    opposite_king = 'K' if player_number == '1' else 'k'

    # King or Knight
    if piece.lower() == 'k' or piece.lower() == 'n':
        for n in piece_range[piece.lower()]:
            # Add movement num
            if convert.valid_num_coord(starting_num + n):
                row, col = convert.num_coord_to_index(starting_num + n)
                if not board[row][col].isalpha():
                    board[row][col] = player_number if board[row][col] == '0' or board[row][col] == player_number else 'X'
                if board[row][col] == opposite_king:
                    board[row][col] = 'C'
            
            # Subtract movement num
            if convert.valid_num_coord(starting_num - n):
                row, col = convert.num_coord_to_index(starting_num - n)
                if not board[row][col].isalpha():
                    board[row][col] = player_number if board[row][col] == '0' or board[row][col] == player_number else 'X'
                if board[row][col] == opposite_king:
                    board[row][col] = 'C'
    # Pawn
    elif piece.lower() == 'p':
        sign = 1 if piece.islower() else -1

        for n in piece_range[piece.lower()]:
            # Add movement num
            n = n * sign
            if convert.valid_num_coord(starting_num + n):
                row, col = convert.num_coord_to_index(starting_num + n)
                if not board[row][col].isalpha():
                    board[row][col] = player_number if board[row][col] == '0' or board[row][col] == player_number else 'X'
                if board[row][col] == opposite_king:
                    board[row][col] = 'C'
    # All other pieces
    elif piece.lower() in piece_range.keys():
        for n in piece_range[piece.lower()]:
            # Add movement num
            current_num = starting_num + n

            while convert.valid_num_coord(current_num):
                row, col = convert.num_coord_to_index(current_num)

                if board[row][col].isalpha():
                    if board[row][col] == opposite_king:
                        board[row][col] = 'C'
                    break
                else:
                    board[row][col] = player_number if board[row][col] == '0' or board[row][col] == player_number else 'X'
                    current_num = current_num + n
            
            # Subtract movement num
            current_num = starting_num - n

            while convert.valid_num_coord(current_num):
                row, col = convert.num_coord_to_index(current_num)

                if board[row][col].isalpha():
                    if board[row][col] == opposite_king:
                        board[row][col] = 'C'
                    break
                else:
                    board[row][col] = player_number if board[row][col] == '0' or board[row][col] == player_number else 'X'
                    current_num = current_num - n
    return board