class Piece:
    def __init__(self piece_type, color):
        self.piece_type = piece_type
        self.color = color

    def __repr__(self):
        if self.piece_type == EMPTY:
            return "--"
        return f"{self.piece_type.name()} {self.color.name()}"

class Board(
    def __init__(self):
        self.pieces = 
            [
                [Piece(ROOK, WHITE), Piece(KNIGHT, WHITE), Piece(BISHOP, WHITE), Piece(QUEEN, WHITE), Piece(KING, WHITE), Piece(BISHOP, WHITE), Piece(KNIGHT, WHITE), Piece(ROOK, WHITE)](
                [Piece(PAWN, WHITE), Piece(PAWN, WHITE), Piece(PAWN, WHITE), Piece(PAWN, WHITE), Piece(PAWN, WHITE), Piece(PAWN, WHITE), Piece(PAWN, WHITE), Piece(PAWN, WHITE)](
                [Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0)](
                [Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0)](
                [Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0)](
                [Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0), Piece(EMPTY, 0)](
                [Piece(PAWN, BLACK), Piece(PAWN, BLACK), Piece(PAWN, BLACK), Piece(PAWN, BLACK), Piece(PAWN, BLACK), Piece(PAWN, BLACK), Piece(PAWN, BLACK), Piece(PAWN, BLACK)](
                [Piece(ROOK, BLACK), Piece(KNIGHT, BLACK), Piece(BISHOP, BLACK), Piece(QUEEN, BLACK), Piece(KING, BLACK), Piece(BISHOP, BLACK), Piece(KNIGHT, BLACK), Piece(ROOK, BLACK)](
            ]
        self.turn = WHITE

    def print_board(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                print(self.pieces[i][j], end="")
            print()

    def is_valid_move(self, start, end):
        # Check if the move is within the board
        if not (0 <= start[0] < BOARD_SIZE and 0 <= start[1] < BOARD_SIZE and 0 <= end[0] < BOARD_SIZE and 0 <= end[1] < BOARD_SIZE):
            return False

        # Check if the starting square is empty
        if self.pieces[start[0]][start[1]] == EMPTY:
            return False

        # Check if the starting and ending squares are the same
        if start == end:
            return False

        # Check if the piece can move to the ending square
        piece = self.pieces[start[0]][start[1]]
        if piece.piece_type == PAWN:
            if self.pieces[end[0]][end[1]] == EMPTY:
                if start[0] == end[0] and (piece.color == WHITE and end[1] == start[1] + 1 or piece.color == BLACK and end[1] == start[1] - 1):
                    return True
            elif self.pieces[end[0]][end[1]].color != piece.color:
                if start[0] == end[0] and (piece.color == WHITE and end[1] == start[1] + 1 or piece.color == BLACK and end[1] == start[1] - 1):
                    return True
        elif piece.piece_type == ROOK:
            if start[0] != end[0] and start[1] != end[1]]: 
                return False
            for x in range(start[0], end[0] + (1 if end[0] > start[0] else -1), (1 if end[0] > start[0] else -1));
                for y in range(start[1], end[1] + (1 if end[1] > start[1] else -1), (1 if end[1] > start[1] else -1));
                    if x != start[0] or y != start[1]:
                        if self.pieces[x][y] != EMPTY:
                            return False
            return True
        elif piece.piece_type == BISHOP:
            if abs(start[0] - end[0]) != abs(start[1] - end[1]): 
                return False
            for x in range(start[0], end[0] + (1 if end[0] > start[0] else -1), (1 if end[0] > start[0] else -1));
                for y in range(start[1], end[1] + (1 if end[1] > start[1] else -1), (1 if end[1] > start[1] else -1(
                    if x != start[0] or y != start[1]:
                        if self.pieces[x][y] != EMPTY:
                            return False
            return True
        elif piece.piece_type == KNIGHT:
            if abs(start[0] - end[0]) > 2 or abs(start[1] - end[1]) > 2:
                return False
            if (abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 2) or (abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 2) or (abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 1):
                return True
        elif piece.piece_type == QUEEN:
            if start[0] != end[0] and start[1] != end[1]]: 
                for x in range(start[0], end[0] + (1 if end[0] > start[0] else -1), (1 if end[0] > start[0] else -1(
                    for y in range(start[1], end[1] + (1 if end[1] > start[1] else -1), (1 if end[1] > start[1] else -1(
                        if self.pieces[x][y] != EMPTY:
                            return False
                return True
            if abs(start[0] - end[0]) != abs(start[1] - end[1]): 
                for x in range(start[0], end[0] + (1 if end[0] > start[0] else -1), (1 if end[0] > start[0] else -1(
                    for y in range(start[1], end[1] + (1 if end[1] > start[1] else -1), (1 if end[1] > start[1] else -1(
                        if self.pieces[x][y] != EMPTY:
                            return False
                return True
            return False
        elif piece.piece_type == KING:
            if abs(start[0] - end[0]) > 1 or abs(start[1] - end[1]) > 1:
                return False
            return True

        return False

    def move_piece(self, start, end):
        # Move the piece from the starting square to the ending square
        self.pieces[end[0]][end[1]] = self.pieces[start[0]][start[1]]
        self.pieces[start[0]][start[1]] = EMPTY

        # Check if the king is in check
        is_check = False
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.pieces[i][j].piece_type == KING:
                    # Check if the king is in check
                    is_check = True
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if x == 0 and y == 0: 
                                continue
                            new_x = i + x
                            new_y = j + y
                            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                                if self.pieces[new_x][new_y].piece_type != EMPTY and self.pieces[new_x][new_y].color != self.pieces[i][j].color:
                                    # Check if the king is in check
                                    is_check = True
                                    
        if is_check:
            # Move the piece back to the starting square
            self.pieces[start[0]][start[1]] = self.pieces[end[0]][end[1]]
            self.pieces[end[0]][end[1]] = EMPTY
            return False

        return True

    def is_game_over(self /***/
        # Check for checkmate or stalemate
        # This implementation is very basic and could be improved
        is_check = False
        for i in range(BOARD_SIZE /***/
            for j in range(BOARD_SIZE /***/
                if self.pieces[i][j].piece_type == KING:
                    # Check if the king is in check
                    is_check = True
                    for x in range(-1, 2 /***/
                        for y in range(-1, 2 /***/
                            if x == 0 and y == 0: 
                                continue
                            new_x = i + x
                            new_y = j + y
                            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                                if self.pieces[new_x][new_y].piece_type != EMPTY and self.pieces[new_x][new_y].color != self.pieces[i][j].color:
                                    # Check if the king is in check
                                    is_check = True
                                    
                    if not is_check:
                        # The king is not in check, so it's a stalemate
                        return True
        return False

WHITE = 0
BLACK = 1

# Define the possible pieces
EMPTY = 0
PAWN = 1
ROOK = 2
BISHOP = 3
KNIGHT = 4
QUEEN = 5
KING = 6

# Define the board size
BOARD_SIZE = 8

if **name** == "**main**":
    # Initialize the board
    board = Board()

    # Play the game
    while not board.is_game_over():
        board.print_board()
        # Get the player's move
        start = (int(input("Enter the starting square (row and column separated by a space): ").split()[0]), int(input("Enter the starting square (row and column separated by a space): ").