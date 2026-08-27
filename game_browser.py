import sys
import types
import random
import os
import _pyodide
from pyodide.ffi import run_sync

# Section: Manifest Game Module (Bypasses import system)
game = types.ModuleType('game')
with open('game.py', 'r') as f:
    exec(compile(f.read(), 'game.py', 'exec'), game.__dict__)
sys.modules['game'] = game

# Section: Web SFX Queue
class WebSFXQueue:
    def __init__(self):
        self.miss_counter = 0
    def put(self, event):
        if event == 'miss':
            self.miss_counter += 1
            event = 'miss' if self.miss_counter % 2 == 1 else 'miss2'
        _pyodide.output(f"__SFX__{event}")

# Section: Sync Input
def js_input():
    return run_sync(_pyodide.input())

# Section: Game Loop
def start():
    sys.stdout.write("\n\n--- ENGINE STARTED ---\n\n")
    game.clear_screen = lambda: sys.stdout.write("\n\n--- SCREEN CLEARED ---\n\n")
    game.sfx_queue = WebSFXQueue()
    sys.stdin.readline = js_input
    game.play_game()

if __name__ == "__main__":
    start()