import time

## Values
enabled               = True

shapes_visible        = True  and enabled
fps_visible           = False and enabled
path_visible          = True  and enabled
sprite_always_visible = False and enabled
avoid_error_mercy     = True  and enabled
skip_load             = True  and enabled
freeze_load           = False and enabled

## Time logging
_timer_name  = ""
_timer_start = 0
_timer_end   = 0
_elapsed     = 0
def start_timer(name):
    global _timer_name, _timer_start, _timer_end
    _timer_name  = name
    _timer_start = time.time()
def end_timer():
    global _timer_name, _timer_start, _timer_end, _elapsed
    _timer_end  = time.time()
    _elapsed    = _timer_end-_timer_start
    print(f"{_timer_name} ended in {_elapsed} seconds")
    _timer_name = ""