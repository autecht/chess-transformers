import os

def flip_fen(fen):
    if fen == '':
        return fen
        
    parts = fen.split()

    # flip turn
    if parts[1] == 'w':
        parts[1] = 'b'
    else:
        parts[1] = 'w'

    board = '/'.join(parts[0].split('/')[::-1])

    swapped_board = []
    for char in board:
        if char.isupper():  # White piece → Black piece
            swapped_board.append(char.lower())
        elif char.islower():  # Black piece → White piece
            swapped_board.append(char.upper())
        else:
            swapped_board.append(char)
    flipped_board = ''.join(swapped_board)
    
    flipped_parts = [flipped_board, parts[1], parts[2], parts[3], parts[4], parts[5]]
    
    return ' '.join(flipped_parts)

def flip_moves(move):
    if len(move) == 4:  # Normal algebraic move
        flipped_move = (
            move[0] + str(9 - int(move[1])) +
            move[2] + str(9 - int(move[3]))
        )
    elif len(move) == 5:
        flipped_move = (
            move[0] + str(9 - int(move[1])) +
            move[2] + str(9 - int(move[3])) +
            move[4]
        )
    elif move == '1-0':
        flipped_move = '0-1'
    elif move == '0-1':
        flipped_move = '1-0'
    else:
        flipped_move = move
    return flipped_move

def process_files(fen_file, moves_file, output_fen_file, output_moves_file):
    with open(fen_file, 'r') as f_fen, open(moves_file, 'r') as f_moves:
        fens = f_fen.readlines()
        moves = f_moves.readlines()

    with open(output_fen_file, 'w') as out_fen, open(output_moves_file, 'w') as out_moves:
        for fen in fens:
            fen = fen.strip()
            flipped_fen = flip_fen(fen)
            out_fen.write(flipped_fen + '\n')
            
        for move in moves:
            move = move.strip()
            flipped_moves = flip_moves(move)
            out_moves.write(flipped_moves + '\n')

    
input_fen = '1.fens'
input_moves = '1.moves'
output_fen = 'flipped_colors.fens'
output_moves = 'flipped_colors.moves'

process_files(input_fen, input_moves, output_fen, output_moves)
print(f"Flipped data written to {output_fen} and {output_moves}")