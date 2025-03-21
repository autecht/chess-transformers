import torch
import pathlib

from chess_transformers.train.utils import get_lr
from chess_transformers.configs.data.LE22c import *
from chess_transformers.configs.other.stockfish import *
from chess_transformers.train.datasets import ChessDatasetFT
from chess_transformers.configs.other.fairy_stockfish import *
from chess_transformers.transformers.criteria import LabelSmoothedCE
from chess_transformers.data.levels import TURN, PIECES, UCI_MOVES, BOOL
from chess_transformers.transformers.models import ChessTransformerEncoderFT


###############################
############ Name #############
###############################

NAME = "CT-EFT-85"  # name and identifier for this configuration

###############################
######### Dataloading #########
###############################

DATASET = ChessDatasetFT  # custom PyTorch dataset
BATCH_SIZE = 512  # batch size
NUM_WORKERS = 0  # number of workers to use for dataloading
PREFETCH_FACTOR = None  # number of batches to prefetch per worker
PIN_MEMORY = False  # pin to GPU memory when dataloading?

###############################
############ Model ############
###############################

VOCAB_SIZES = {
    "moves": len(UCI_MOVES),
    "turn": len(TURN),
    "white_kingside_castling_rights": len(BOOL),
    "white_queenside_castling_rights": len(BOOL),
    "black_kingside_castling_rights": len(BOOL),
    "black_queenside_castling_rights": len(BOOL),
    "board_position": len(PIECES),
}  # vocabulary sizes
D_MODEL = 768  # size of vectors throughout the transformer model
N_HEADS = 12  # number of heads in the multi-head attention
D_QUERIES = 64  # size of query vectors (and also the size of the key vectors) in the multi-head attention
D_VALUES = 64  # size of value vectors in the multi-head attention
D_INNER = 4 * D_MODEL  # an intermediate size in the position-wise FC
N_LAYERS = 12  # number of layers in the Encoder and Decoder
DROPOUT = 0.2  # dropout probability
N_MOVES = 1  # expected maximum length of move sequences in the model, <= MAX_MOVE_SEQUENCE_LENGTH
DISABLE_COMPILATION = False  # disable model compilation?
COMPILATION_MODE = "default"  # mode of model compilation (see torch.compile())
DYNAMIC_COMPILATION = True  # expect tensors with dynamic shapes?
SAMPLING_K = 1  # k in top-k sampling model predictions during play
MODEL = ChessTransformerEncoderFT  # custom PyTorch model to train

###############################
########### Training ##########
###############################

BATCHES_PER_STEP = (
    4  # perform a training step, i.e. update parameters, once every so many batches
)
PRINT_FREQUENCY = 1  # print status once every so many steps
N_STEPS = 500000  # number of training steps
WARMUP_STEPS = 8000  # number of warmup steps where learning rate is increased linearly; twice the value in the paper, as in the official transformer repo.
STEP = 1  # the step number, start from 1 to prevent math error in the 'LR' line
LR_SCHEDULE = "exp_decay"  # the learning rate schedule; see utils.py for learning rate schedule
LR_DECAY = 0.06  # the decay rate for 'exp_decay' schedule
LR = get_lr(
    step=STEP,
    d_model=D_MODEL,
    warmup_steps=WARMUP_STEPS,
    schedule=LR_SCHEDULE,
    decay=LR_DECAY,
)  # see utils.py for learning rate schedule
START_EPOCH = 0  # start at this epoch
BETAS = (0.9, 0.98)  # beta coefficients in the Adam optimizer
EPSILON = 1e-9  # epsilon term in the Adam optimizer
LABEL_SMOOTHING = 0.1  # label smoothing co-efficient in the Cross Entropy loss
BOARD_STATUS_LENGTH = 70  # total length of input sequence
USE_AMP = True  # use automatic mixed precision training?
CRITERION = LabelSmoothedCE  # training criterion (loss)
OPTIMIZER = torch.optim.Adam  # optimizer
LOGS_FOLDER = str(
    pathlib.Path(__file__).parent.parent.parent.resolve() / "train" / "logs" / NAME
)  # logs folder

###############################
######### Checkpoints #########
###############################

CHECKPOINT_FOLDER = str(
    pathlib.Path(__file__).parent.parent.parent.resolve() / "checkpoints" / NAME
)  # folder containing checkpoints
 # path to model checkpoint (NAME + ".pt") to resume training, None if none
print("Checkpoint Folder", CHECKPOINT_FOLDER)
TRAINING_CHECKPOINT = r"averaged_CT-EFT-85.pt"
AVERAGE_STEPS = {491000, 492500, 494000, 495500, 497000, 498500, 500000}
CHECKPOINT_AVG_PREFIX = (
    "step"  # prefix to add to checkpoint name when saving checkpoints for averaging
)
CHECKPOINT_AVG_SUFFIX = (
    ".pt"  # checkpoint end string to match checkpoints saved for averaging
)
FINAL_CHECKPOINT = (
    "averaged_" + NAME + ".pt"
)  # final checkpoint to be used for eval/inference
FINAL_CHECKPOINT_GDID = (
    "1OHtg336ujlOjp5Kp0KjE1fAPF74aZpZD"  # Google Drive ID for download
)


################################
########## Evaluation ##########
################################

EVAL_GAMES_FOLDER = str(
    pathlib.Path(__file__).parent.parent.parent.resolve() / "evaluate" / "games" / NAME
)  # folder where evaluation games are saved in PGN files


###############################
############ Data #############
###############################
DATASET_NAME = "Carlsen"
DATA_FOLDER = (
    os.path.join(os.environ.get("CT_DATA_FOLDER"), DATASET_NAME)
    if os.environ.get("CT_DATA_FOLDER")
    else None
)  # folder containing all data files
H5_FILE = DATASET_NAME + ".h5"  # H5 file containing data
MAX_MOVE_SEQUENCE_LENGTH = 10  # expected maximum length of move sequences
EXPECTED_ROWS = 12500000  # expected number of rows, approximately, in the data
VAL_SPLIT_FRACTION = 0.925  # marker (% into the data) where the validation split begins