import sys
import threading
import queue
import re
import traceback
from io import StringIO

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

import game


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

        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.output_label = Label(
            text='Loading…\n',
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.output_label.bind(texture_size=self.output_label.setter('size'))
        self.scroll.add_widget(self.output_label)
        self.add_widget(self.scroll)

        self.input_box = TextInput(
            hint_text='Type command…',
            size_hint=(1, 0.1),
            multiline=False
        )
        self.input_box.bind(on_text_validate=self.send_input)
        self.add_widget(self.input_box)

        self.input_queue = queue.Queue()
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        self.game_thread = None

        Clock.schedule_once(self.start_game, 1)

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
                Clock.schedule_once(lambda dt: self.add_output(f"\n[ERROR]\n{error_msg}"), 0)
            finally:
                sys.stdout = old_stdout
                sys.stdin = old_stdin
                Clock.schedule_once(lambda dt: self.disable_input(), 0)

        self.game_thread = threading.Thread(target=run, daemon=True)
        self.game_thread.start()

    def add_output(self, text):
        clean = self.ansi_escape.sub('', text)
        max_lines = 500
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
    MyGameApp().run()