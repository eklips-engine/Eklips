## Import libraries
import traceback as tb, os
import classes.singleton as engine
from tkinter.messagebox import *

## Functions
def get_info(error : Exception):
    return "".join(tb.format_exception(error))

def show_error(error : Exception):
    info = get_info(error)
    print(f"Crashed! See dialog for more info.")
    showerror("Eklips Engine", info)
    os.makedirs("tmp", exist_ok=True)
    with open(f"tmp/{len(os.listdir('tmp'))}.log","w") as f:
        f.write(info)

__dict__ = {"show_error": show_error, "get_info": get_info, "traceback": tb, "os": os}