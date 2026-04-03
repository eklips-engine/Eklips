## Errors
class SceneError(Warning):
    pass
class ScriptError(Exception):
    pass
class PlayerError(Exception):
    """Exception class for problems caused in the `MediaPlayer` Node."""
class LogError(BaseException):
    """Class for `error()`"""
class TreeError(RuntimeError):
    """Tree Error."""
class LoopError(TreeError):
    """https://c.tenor.com/hdEL0uNj1Z4AAAAC"""