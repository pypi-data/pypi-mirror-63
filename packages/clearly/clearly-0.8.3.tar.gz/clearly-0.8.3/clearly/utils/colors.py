import re
from functools import partial


class Colors:
    _col = lambda color, text: color + str(text) + '\033[0m'
    BLUE = partial(_col, '\033[94m')
    GREEN = partial(_col, '\033[92m')
    YELLOW = partial(_col, '\033[93m')
    RED = partial(_col, '\033[91m')
    MAGENTA = partial(_col, '\033[95m')
    CYAN = partial(_col, '\033[96m')
    ORANGE = partial(_col, '\033[38;5;208m')
    BOLD = partial(_col, '\033[1m')
    DIM = partial(_col, '\033[2m')


def strip_colors(text):
    return re.sub(r'\033\[.+?m', '', text)
