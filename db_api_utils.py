

def is_valid(*args):
    for arg in args:
        if not arg:
            return False
    return True