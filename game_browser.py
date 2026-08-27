# Section: Imports
import sys
import random
import _pyodide

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
    return bridge.input()

# Section: Game Loop
def start():
    sys.stdout.write = lambda s: bridge.output(s)
    sys.stdin.readline = js_input
    sys.stdout.write("\n\n--- ENGINE STARTED ---\n\n")
    import __main__
    play_game = __main__.play_game_func
    sfx_queue = WebSFXQueue()
    play_game()