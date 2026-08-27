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
    # Directly call the bridge without run_sync to prevent deadlocks
    return bridge.input()

# Section: Game Loop
def start():
    try:
        sys.stdout.write("\n\n--- ENGINE STARTED ---\n\n")
        import __main__
        play_game = __main__.play_game_func
        clear_screen = lambda: sys.stdout.write("\n\n--- SCREEN CLEARED ---\n\n")
        sfx_queue = WebSFXQueue()
        sys.stdin.readline = js_input
        play_game()
    except Exception as e:
        import traceback
        sys.stdout.write(f"\n\n--- PYTHON ERROR ---\n{traceback.format_exc()}")