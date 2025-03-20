import os

def flip_fen(fen):
    if fen == '':
        return fen
        
    parts = fen.split()

    board = '/'.join(parts[0].split('/')[::-1])
    
    flipped_parts = [board, parts[1], parts[2], parts[3], parts[4], parts[5]]
    
    return ' '.join(flipped_parts)

def flip_moves(move):
    if len(move) == 4:  # Normal algebraic move
        flipped_move = (
            move[0] + str(9 - int(move[1])) +
            move[2] + str(9 - int(move[3]))
        )
        flipped_moves.append(flipped_move)
    elif len(move) == 5:
        flipped_move = (
            move[0] + str(9 - int(move[1])) +
            move[2] + str(9 - int(move[3])) +
            move[4]
        )
    else:
        flipped_move = move
    return flipped_move

def process_files(fen_file, moves_file, output_fen_file, output_moves_file):
    with open(fen_file, 'r') as f_fen, open(moves_file, 'r') as f_moves:
        fens = f_fen.readlines()
        moves = f_moves.readlines()

    with open(output_fen_file, 'w') as out_fen, open(output_moves_file, 'w') as out_moves:
        for fen, move in zip(fens, moves):
            fen = fen.strip()
            move = move.strip().split()

            # Flip FEN and moves
            flipped_fen = flip_fen(fen)
            flipped_moves = flip_moves(move)

            # Write flipped data
            out_fen.write(flipped_fen + '\n')
            out_moves.write(' '.join(flipped_moves) + '\n')

    
input_fen = '1.fens'
input_moves = '1.moves'
output_fen = 'flipped_1.fens'
output_moves = 'flipped_1.moves'

process_files(input_fen, input_moves, output_fen, output_moves)
print(f"Flipped data written to {output_fen} and {output_moves}")