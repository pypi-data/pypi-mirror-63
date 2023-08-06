import os
import sys
import termios
import tty


def ask(text):
    sys.stdout.write(text)
    sys.stdout.flush()
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    sys.stdout.write(os.linesep)
    return ch
