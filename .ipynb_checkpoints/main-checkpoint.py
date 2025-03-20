import os
from chess_transformers.configs import import_config
from chess_transformers.play.utils import write_pgns
from chess_transformers.play import load_model, warm_up, human_v_model 

# Load configuration
config_name = "CT-EFT-85"
CONFIG = import_config(config_name)

# Load assets
model = load_model(CONFIG)

# Warmup model (triggers compilation)
warm_up(
    model=model
)
from chess_transformers.play import model_v_engine
from chess_transformers.play.utils import load_engine
# Load engine
engine = load_engine(CONFIG.STOCKFISH_PATH)

# Play
LL = 4  # Try strength levels 1 to 8 (note: 7 and 8 may be slow)
model_color = "w"  # Try "w" and "b"
wins, losses, draws, pgns = model_v_engine(
    model=model,
    k=CONFIG.SAMPLING_K,
    use_amp=CONFIG.USE_AMP,
    model_color=model_color,
    engine=engine,
    time_limit=CONFIG.LICHESS_LEVELS[LL]["TIME_CONSTRAINT"],
    depth_limit=CONFIG.LICHESS_LEVELS[LL]["DEPTH"],
    uci_options={"Skill Level": LL},
    rounds=500,
    clock=None,
    white_player_name="Fairy Stockfish @ LL {}".format(LL)
    if model_color == "b"
    else config_name,
    black_player_name="Fairy Stockfish @ LL {}".format(LL)
    if model_color == "w"
    else config_name,
    event=config_name + " v. Fairy Stockfish @ LL {}".format(LL)
    if model_color == "w"
    else "Fairy Stockfish @ LL {} v. ".format(LL) + config_name,
)