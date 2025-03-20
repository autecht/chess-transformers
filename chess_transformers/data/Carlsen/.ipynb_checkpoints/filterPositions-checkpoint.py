import re



def removeNums(moves):
    filtered = [move for move in moves if "." not in move]
    return filtered
def filterColors(game):
    filtered = [info for info in game if ("White " in info or "Black " in info)]
    return filtered

def filterOtherMoves(magnus_colors, fen_lines, moves_lines):
    pass


all_pgns = open("./1.pgn", "r").read()


all_pgns = all_pgns.split("\n\n")
pgn_metadata = [all_pgns[i] for i in range(0, len(all_pgns), 2)]
pgn_moves = [all_pgns[i] for i in range(1, len(all_pgns), 2)]

pgn_metadata = [m.split("\n") for m in pgn_metadata]
print(len(pgn_metadata))

pgn_colors = [filterColors(game) for game in pgn_metadata]

# for game in pgn_colors:
#     print(game)
#     if ("Carlsen, Magnus" not in game[0] and "Carlsen, Magnus" not in game[0]):
#         print(game)

pgn_colors = flat_list = [
                    x
                    for xs in pgn_colors
                    for x in xs
                ]
magnus_colors = [color for color in pgn_colors if "Carlsen, Magnus" in color]
magnus_colors = [(True if "White" in color else False) for color in magnus_colors]

fen_lines = open("./1.fens").readlines
moves_lines = open("./1.moves").readlines
fen_lines, moves_lines = filterOtherMoves(magnus_colors, fen_lines, moves_lines)




