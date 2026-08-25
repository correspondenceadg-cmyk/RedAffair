cat > game_browser.py << 'EOF'
# Section: Imports
import sys
import random
import os

sys.path.insert(0, 'src/redaffair')
import game

# Section: SFX Bridge
def web_play_sfx(name):
    import _pyodide
    _pyodide.output(f"[SFX] {name}\n")

game.sfx_queue = None

# Section: Game Loop
def start():
    game.clear_screen = lambda: sys.stdout.write("\n\n--- SCREEN CLEARED ---\n\n")
    game.play_game()

if __name__ == "__main__":
    start()
EOF