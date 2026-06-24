import sys
import threading
import queue
import re
import traceback
import os
from io import StringIO

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

LOG_FILE = '/sdcard/redaffair_crash.log'

def log_crash(exc_text):
    try:
        with open(LOG_FILE, 'w') as f:
            f.write(exc_text)
    except:
        pass

try:
    import game
except Exception as e:
    log_crash(f"Failed to import game.py:\n{traceback.format_exc()}")
    raise

FONT_PATH = 'fonts/DepartureMono.ttf'

RED_HEX = (1, 0, 0, 1)
BLACK_HEX = (0, 0, 0, 1)


class GameStdout(StringIO):
    def __init__(self, app_ref, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ref = app_ref

    def write(self, s):
        if s:
            Clock.schedule_once(lambda dt: self.app_ref.add_output(s), 0)
        return len(s)

    def flush(self):
        pass


class GameStdin:
    def __init__(self, input_queue):
        self.input_queue = input_queue

    def readline(self):
        line = self.input_queue.get()
        return line + '\n'

    def read(self, n=0):
        return self.readline()


class GameUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, orientation='vertical')
        with self.canvas.before:
            Color(*BLACK_HEX)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        try:
            self._init_ui()
        except Exception:
            log_crash(traceback.format_exc())
            self.add_widget(Label(text=f"FATAL ERROR\n{LOG_FILE}"))

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def _init_ui(self):
        font_to_use = FONT_PATH if os.path.exists(FONT_PATH) else None

        self.output_label = Label(
            text='',
            font_name=font_to_use,
            font_size='16sp',
            color=RED_HEX,
            size_hint=(None, None),
            halign='left',
            valign='top',
            text_size=(Window.width, None),
            width=Window.width,
            height=0
        )
        self.output_label.bind(
            texture_size=self._on_texture_size
        )

        self.scroll = ScrollView(size_hint=(1, 0.85), do_scroll_x=False)
        self.scroll.add_widget(self.output_label)
        self.add_widget(self.scroll)

        self.input_box = TextInput(
            hint_text='Type command…',
            font_name=font_to_use,
            font_size='18sp',
            foreground_color=RED_HEX,
            background_color=BLACK_HEX,
            cursor_color=RED_HEX,
            size_hint=(1, 0.1),
            multiline=False,
            padding=[10, 15, 10, 10]
        )
        self.input_box.bind(on_text_validate=self.send_input)
        self.add_widget(self.input_box)

        self.input_queue = queue.Queue()
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        self.game_thread = None

        Window.bind(on_resize=self._on_window_resize)
        Clock.schedule_once(self.start_game, 1)

    def _on_window_resize(self, instance, width, height):
        self.output_label.text_size = (width, None)
        self.output_label.width = width
        self.scroll.scroll_x = 0

    def _on_texture_size(self, instance, size):
        instance.height = size[1]
        instance.width = Window.width
        self.scroll.scroll_x = 0

    def start_game(self, dt):
        old_stdout = sys.stdout
        old_stdin = sys.stdin
        sys.stdout = GameStdout(self)
        sys.stdin = GameStdin(self.input_queue)

        def run():
            try:
                game.play_game()
            except SystemExit:
                pass
            except Exception:
                error_msg = traceback.format_exc()
                log_crash(error_msg)
                Clock.schedule_once(lambda dt: self.add_output(f"\n[ERROR]\n{error_msg}"), 0)
            finally:
                sys.stdout = old_stdout
                sys.stdin = old_stdin
                Clock.schedule_once(lambda dt: self.disable_input(), 0)

        self.game_thread = threading.Thread(target=run, daemon=True)
        self.game_thread.start()

    def add_output(self, text):
        clean = self.ansi_escape.sub('', text)
        max_lines = 1000
        self.output_label.text += clean
        lines = self.output_label.text.splitlines()
        if len(lines) > max_lines:
            self.output_label.text = '\n'.join(lines[-max_lines:])
        self.scroll.scroll_y = 0

    def send_input(self, instance):
        text = instance.text.strip()
        if text:
            self.input_queue.put(text)
        instance.text = ''

    def disable_input(self):
        self.input_box.disabled = True
        self.input_box.hint_text = 'Game over'


class MyGameApp(App):
    def build(self):
        return GameUI()


if __name__ == '__main__':
    try:
        MyGameApp().run()
    except Exception:
        log_crash(traceback.format_exc())
        raise