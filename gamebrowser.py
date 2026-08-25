# Section: Imports
import sys
import random
import os
import _pyodide
from pyodide.ffi import run_sync

sys.path.insert(0, 'src/redaffair')
import game

# Section: Web SFX Queue
class WebSFXQueue:
    def __init__(self):
        self.miss_counter = 0
    def put(self, event):
        if event == 'miss':
            self.miss_counter += 1
            event = 'miss' if self.miss_counter % 2 == 1 else 'miss2'
        _pyodide.output(f"__SFX__{event}")

# Section: Synchronous Input
def js_input():
    # run_sync blocks the worker thread until the JS promise resolves
    return run_sync(_pyodide.input())

# Section: Game Loop
def start():
    game.clear_screen = lambda: sys.stdout.write("\n\n--- SCREEN CLEARED ---\n\n")
    game.sfx_queue = WebSFXQueue()
    sys.stdin.readline = js_input
    game.play_game()

if __name__ == "__main__":
    start()