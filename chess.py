board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

symbols = {
    "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟"
}

turn = "white"
en_passant = None

white_king_moved = False
black_king_moved = False

white_rook_left_moved = False
white_rook_right_moved = False
black_rook_left_moved = False
black_rook_right_moved = False


def show_board():
    print()
    print("    a b c d e f g h")
    print("   -----------------")

    for r in range(8):
        print(8 - r, "|", end=" ")

        for c in range(8):
            piece = board[r][c]

            if piece == " ":
                print(".", end=" ")
            else:
                print(symbols[piece], end=" ")

        print("|", 8 - r)

    print("   -----------------")
    print("    a b c d e f g h")
    print()


def position(square):
    files = "abcdefgh"

    if len(square) != 2:
        return None

    if square[0] not in files:
        return None

    if square[1] not in "12345678":
        return None

    col = files.index(square[0])
    row = 8 - int(square[1])

    return row, col


def color(piece):
    if piece == " ":
        return None

    if piece.isupper():
        return "white"

    return "black"


def opposite(side):
    if side == "white":
        return "black"

    return "white"


def inside(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def copy_board():
    return [row[:] for row in board]


def find_king(side):
    king = "K" if side == "white" else "k"

    for r in range(8):
        for c in range(8):
            if board[r][c] == king:
                return r, c

    return None


def square_attacked(r, c, by_side):
    # Pawn attacks
    if by_side == "white":
        pawn = "P"
        directions = [(1, -1), (1, 1)]
    else:
        pawn = "p"
        directions = [(-1, -1), (-1, 1)]

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        if inside(nr, nc) and board[nr][nc] == pawn:
            return True

    # Knight attacks
    knight = "N" if by_side == "white" else "n"

    knight_moves = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]

    for dr, dc in knight_moves:
        nr = r + dr
        nc = c + dc

        if inside(nr, nc) and board[nr][nc] == knight:
            return True

    # King attacks
    king = "K" if by_side == "white" else "k"

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue

            nr = r + dr
            nc = c + dc

            if inside(nr, nc) and board[nr][nc] == king:
                return True

    # Rooks and queens
    rook = "R" if by_side == "white" else "r"
    queen = "Q" if by_side == "white" else "q"

    directions = [
        (-1, 0), (1, 0),
        (0, -1), (0, 1)
    ]

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        while inside(nr, nc):
            piece = board[nr][nc]

            if piece != " ":
                if piece == rook or piece == queen:
                    return True
                break

            nr += dr
            nc += dc

    # Bishops and queens
    bishop = "B" if by_side == "white" else "b"

    directions = [
        (-1, -1), (-1, 1),
        (1, -1), (1, 1)
    ]

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        while inside(nr, nc):
            piece = board[nr][nc]

            if piece != " ":
                if piece == bishop or piece == queen:
                    return True
                break

            nr += dr
            nc += dc

    return False


def in_check(side):
    king = find_king(side)

    if king is None:
        return True

    return square_attacked(
        king[0],
        king[1],
        opposite(side)
    )


def pseudo_moves(r, c):
    piece = board[r][c]

    if piece == " ":
        return []

    side = color(piece)
    moves = []

    # Pawn
    if piece.lower() == "p":

        direction = -1 if side == "white" else 1
        start_row = 6 if side == "white" else 1

        nr = r + direction

        if inside(nr, c) and board[nr][c] == " ":
            moves.append((nr, c))

            nr2 = r + direction * 2

            if r == start_row and board[nr2][c] == " ":
                moves.append((nr2, c))

        for dc in [-1, 1]:
            nr = r + direction
            nc = c + dc

            if inside(nr, nc):
                target = board[nr][nc]

                if target != " " and color(target) != side:
                    moves.append((nr, nc))

                if en_passant == (nr, nc):
                    moves.append((nr, nc))

    # Knight
    elif piece.lower() == "n":

        knight_moves = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]

        for dr, dc in knight_moves:
            nr = r + dr
            nc = c + dc

            if inside(nr, nc):
                if board[nr][nc] == " " or color(board[nr][nc]) != side:
                    moves.append((nr, nc))

    # Bishop
    elif piece.lower() == "b":

        directions = [
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            while inside(nr, nc):

                if board[nr][nc] == " ":
                    moves.append((nr, nc))
                else:
                    if color(board[nr][nc]) != side:
                        moves.append((nr, nc))
                    break

                nr += dr
                nc += dc

    # Rook
    elif piece.lower() == "r":

        directions = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1)
        ]

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            while inside(nr, nc):

                if board[nr][nc] == " ":
                    moves.append((nr, nc))
                else:
                    if color(board[nr][nc]) != side:
                        moves.append((nr, nc))
                    break

                nr += dr
                nc += dc

    # Queen
    elif piece.lower() == "q":

        directions = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1),
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            while inside(nr, nc):

                if board[nr][nc] == " ":
                    moves.append((nr, nc))
                else:
                    if color(board[nr][nc]) != side:
                        moves.append((nr, nc))
                    break

                nr += dr
                nc += dc

    # King
    elif piece.lower() == "k":

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:

                if dr == 0 and dc == 0:
                    continue

                nr = r + dr
                nc = c + dc

                if inside(nr, nc):
                    if board[nr][nc] == " " or color(board[nr][nc]) != side:
                        moves.append((nr, nc))

    return moves


def make_move(r1, c1, r2, c2):
    global board
    global en_passant

    piece = board[r1][c1]
    target = board[r2][c2]

    # En passant capture
    if piece.lower() == "p" and en_passant == (r2, c2) and target == " ":
        if piece.isupper():
            board[r2 + 1][c2] = " "
        else:
            board[r2 - 1][c2] = " "

    board[r2][c2] = piece
    board[r1][c1] = " "

    # Promotion
    if piece == "P" and r2 == 0:
        promote("white", r2, c2)

    elif piece == "p" and r2 == 7:
        promote("black", r2, c2)

    # Set en passant square
    en_passant = None

    if piece.lower() == "p":
        if abs(r2 - r1) == 2:
            en_passant = ((r1 + r2) // 2, c1)


def promote(side, r, c):
    while True:
        choice = input(
            "Promote to Q, R, B or N: "
        ).upper()

        if choice in ["Q", "R", "B", "N"]:
            if side == "white":
                board[r][c] = choice
            else:
                board[r][c] = choice.lower()

            break

        print("Invalid promotion.")


def legal_moves(r, c):
    piece = board[r][c]

    if piece == " ":
        return []

    side = color(piece)
    moves = pseudo_moves(r, c)

    legal = []

    for r2, c2 in moves:

        old_board = copy_board()

        make_move(r, c, r2, c2)

        if not in_check(side):
            legal.append((r2, c2))

        board[:] = old_board

    return legal


def all_legal_moves(side):
    moves = []

    for r in range(8):
        for c in range(8):

            if color(board[r][c]) == side:

                for move in legal_moves(r, c):
                    moves.append(((r, c), move))

    return moves


def castle_moves(side):
    moves = []

    if side == "white":

        if not white_king_moved:

            # King side
            if not white_rook_right_moved:
                if board[7][5] == " " and board[7][6] == " ":
                    if not in_check("white"):
                        if not square_attacked(7, 5, "black"):
                            if not square_attacked(7, 6, "black"):
                                moves.append(((7, 4), (7, 6)))

            # Queen side
            if not white_rook_left_moved:
                if (
                    board[7][1] == " "
                    and board[7][2] == " "
                    and board[7][3] == " "
                ):
                    if not in_check("white"):
                        if not square_attacked(7, 3, "black"):
                            if not square_attacked(7, 2, "black"):
                                moves.append(((7, 4), (7, 2)))

    else:

        if not black_king_moved:

            # King side
            if not black_rook_right_moved:
                if board[0][5] == " " and board[0][6] == " ":
                    if not in_check("black"):
                        if not square_attacked(0, 5, "white"):
                            if not square_attacked(0, 6, "white"):
                                moves.append(((0, 4), (0, 6)))

            # Queen side
            if not black_rook_left_moved:
                if (
                    board[0][1] == " "
                    and board[0][2] == " "
                    and board[0][3] == " "
                ):
                    if not in_check("black"):
                        if not square_attacked(0, 3, "white"):
                            if not square_attacked(0, 2, "white"):
                                moves.append(((0, 4), (0, 2)))

    return moves


def do_castle(r1, c1, r2, c2):

    if c2 == 6:
        board[r2][5] = board[r2][7]
        board[r2][7] = " "

    elif c2 == 2:
        board[r2][3] = board[r2][0]
        board[r2][0] = " "

    board[r2][c2] = board[r1][c1]
    board[r1][c1] = " "


def update_castling_rights(piece, r1, c1):

    global white_king_moved
    global black_king_moved
    global white_rook_left_moved
    global white_rook_right_moved
    global black_rook_left_moved
    global black_rook_right_moved

    if piece == "K":
        white_king_moved = True

    if piece == "k":
        black_king_moved = True

    if piece == "R":
        if r1 == 7 and c1 == 0:
            white_rook_left_moved = True

        if r1 == 7 and c1 == 7:
            white_rook_right_moved = True

    if piece == "r":
        if r1 == 0 and c1 == 0:
            black_rook_left_moved = True

        if r1 == 0 and c1 == 7:
            black_rook_right_moved = True


def play():

    global turn

    while True:

        show_board()

        if in_check(turn):
            print("CHECK!")

        moves = all_legal_moves(turn)
        moves += castle_moves(turn)

        if len(moves) == 0:

            if in_check(turn):
                print("CHECKMATE!")
                print(opposite(turn).title(), "wins!")
            else:
                print("STALEMATE!")

            break

        print(turn.title(), "turn")
        print("Type 'quit' to stop.")

        start = input("Move from: ").lower()

        if start == "quit":
            print("Game ended.")
            break

        end = input("Move to: ").lower()

        p1 = position(start)
        p2 = position(end)

        if p1 is None or p2 is None:
            print("Invalid square.")
            continue

        r1, c1 = p1
        r2, c2 = p2

        if color(board[r1][c1]) != turn:
            print("That's not your piece.")
            continue

        possible = legal_moves(r1, c1)

        # Castling
        castle = False

        for a, b in castle_moves(turn):
            if a == (r1, c1) and b == (r2, c2):
                castle = True

        if (r2, c2) not in possible and not castle:
            print("Illegal move!")
            continue

        piece = board[r1][c1]

        update_castling_rights(piece, r1, c1)

        if castle:
            do_castle(r1, c1, r2, c2)

        else:
            make_move(r1, c1, r2, c2)

        turn = opposite(turn)


play()