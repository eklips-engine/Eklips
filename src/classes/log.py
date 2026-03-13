import classes.singleton as engine

class LogError(BaseException):
    """Class for `error()`"""

def info(text):
    """Log some text as info."""
    print(f"INFO: {text}")
def warn(text):
    """Log some text as a warning."""
    print(f"WARN: {text}")
def error(text):
    """Log some text as an error and display it on a dialog."""
    print(f"ERROR: {text}")
    engine.error_handler.show_error(LogError(text))