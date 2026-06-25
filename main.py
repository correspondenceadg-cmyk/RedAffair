import sys
import threading
import queue
import re
import traceback
import os
import webbrowser
import random as py_random
from io import StringIO

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.animation import Animation

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

DARK_THEME = {
    'fg': (1, 0, 0, 1),
    'bg': (0, 0, 0, 1),
    'input_bg': (0, 0, 0, 1),
    'cursor': (1, 0, 0, 1)
}

LIGHT_THEME = {
    'fg': (0, 0, 0, 1),
    'bg': (1, 1, 1, 1),
    'input_bg': (0.95, 0.95, 0.95, 1),
    'cursor': (0, 0, 1, 1)
}


# ---------- Simple CRT Overlay (no shader) ----------
class CRTOverlay(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)

        # Create a scanline texture (2px height stripe pattern)
        scan_tex = Texture.create(size=(4, 4))
        scan_buf = bytes([
            0, 0, 0, 40,  0, 0, 0, 40,  0, 0, 0, 40,  0, 0, 0, 40,    # row 0: dark with alpha
            0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,     # row 1: transparent
            0, 0, 0, 40,  0, 0, 0, 40,  0, 0, 0, 40,  0, 0, 0, 40,    # row 2: dark
            0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0      # row 3: transparent
        ])
        scan_tex.blit_buffer(scan_buf, colorfmt='rgba', bufferfmt='ubyte')
        scan_tex.wrap = 'repeat'

        with self.canvas:
            self.scan_rect = Rectangle(texture=scan_tex, size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Glitch timer
        self.glitch_event = None

    def _update_rect(self, instance, value):
        self.scan_rect.size = instance.size
        self.scan_rect.pos = instance.pos

    def on_show(self):
        self.glitch_event = Clock.schedule_interval(self._random_glitch, 0.2)

    def on_hide(self):
        if self.glitch_event:
            self.glitch_event.cancel()

    def _random_glitch(self, dt):
        # Randomly shift the overlay a few pixels horizontally
        if py_random.random() < 0.15:
            offset = (py_random.randint(-5, 5), py_random.randint(-2, 2))
            self.scan_rect.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        else:
            self.scan_rect.pos = self.pos


# ---------- Splash Screen ----------
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        with self.layout.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.layout.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        self.bg_image = Image(source='assets/splash_bg.png',
                              allow_stretch=True, keep_ratio=False,
                              size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.layout.add_widget(self.bg_image)

        self.title_box = RelativeLayout(size_hint=(None, None),
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5})
        title_text = 'THE RED AFFAIR'
        title_font_size = '36sp'
        self.title_labels = []
        offsets = [(-2,0), (2,0), (0,-2), (0,2), (-1,-1), (1,1)]
        for dx, dy in offsets:
            lbl = Label(text=title_text,
                        font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
                        font_size=title_font_size,
                        color=(1, 1, 1, 1),
                        halign='center', valign='middle',
                        size_hint=(None, None),
                        pos=(dx, dy))
            lbl.bind(texture_size=lambda instance, size: setattr(instance, 'size', size))
            self.title_box.add_widget(lbl)
            self.title_labels.append(lbl)
        self.red_title = Label(text=title_text,
                               font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
                               font_size=title_font_size,
                               color=(1, 0, 0, 1),
                               halign='center', valign='middle',
                               size_hint=(None, None),
                               pos=(0, 0))
        self.red_title.bind(texture_size=lambda instance, size: setattr(instance, 'size', size))
        self.title_box.add_widget(self.red_title)
        self.title_labels.append(self.red_title)
        self.red_title.bind(texture_size=self._adjust_title_box_size)
        self.title_box.bind(size=self._keep_title_centered)
        self.layout.add_widget(self.title_box)

        self.spinner_scatter = Scatter(do_rotation=False, do_scale=False, do_translation=False,
                                       size_hint=(None, None), size=(64, 64),
                                       pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.spinner_image = Image(source='assets/spinner.png',
                                   size=(64, 64), size_hint=(None, None))
        self.spinner_scatter.add_widget(self.spinner_image)
        self.layout.add_widget(self.spinner_scatter)

        self.copyright_label = Label(text='TranSchizo Studios © 2026',
                                     font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
                                     font_size='11sp', color=(1, 0, 0, 1),
                                     size_hint=(None, None),
                                     pos_hint={'center_x': 0.5, 'y': 0.04})
        self.copyright_label.bind(texture_size=lambda instance, size: setattr(instance, 'size', size))
        self.layout.add_widget(self.copyright_label)

        self.add_widget(self.layout)
        self.spin_event = None
        self.fade_out_event = None

    def _update_bg_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def _adjust_title_box_size(self, *args):
        max_w, max_h = 0, 0
        for lbl in self.title_labels:
            w = lbl.width + abs(lbl.pos[0])
            h = lbl.height + abs(lbl.pos[1])
            if w > max_w: max_w = w
            if h > max_h: max_h = h
        self.title_box.size = (max_w + 4, max_h + 4)

    def _keep_title_centered(self, instance, size):
        pass

    def on_enter(self):
        self.spin_event = Clock.schedule_interval(self._rotate_spinner, 1/60.0)
        self.fade_out_event = Clock.schedule_once(self.start_fade_out, 10)

    def _rotate_spinner(self, dt):
        self.spinner_scatter.rotation += 3

    def start_fade_out(self, dt):
        fade_out = Animation(opacity=0, duration=2)
        fade_out.bind(on_complete=self._go_menu)
        fade_out.start(self.layout)

    def _go_menu(self, *args):
        if self.spin_event:
            self.spin_event.cancel()
        self.manager.current = 'menu'

    def on_leave(self):
        if self.spin_event:
            self.spin_event.cancel()
        if self.fade_out_event:
            self.fade_out_event.cancel()


# ---------- Game I/O ----------
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


# ---------- Game UI ----------
class GameUI(BoxLayout):
    def __init__(self, theme, back_callback, **kwargs):
        super().__init__(**kwargs, orientation='vertical')
        self.theme = theme
        self.back_callback = back_callback
        with self.canvas.before:
            Color(*theme['bg'])
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
        theme = self.theme

        self.output_label = Label(
            text='',
            font_name=font_to_use,
            font_size='15sp',
            color=theme['fg'],
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

        self.scroll = ScrollView(size_hint=(1, 0.80), do_scroll_x=False)
        self.scroll.add_widget(self.output_label)
        self.add_widget(self.scroll)

        self.input_box = TextInput(
            hint_text='Type command…',
            font_name=font_to_use,
            font_size='18sp',
            foreground_color=theme['fg'],
            background_color=theme['input_bg'],
            cursor_color=theme['cursor'],
            size_hint=(1, 0.1),
            multiline=False,
            padding=[10, 15, 10, 10]
        )
        self.input_box.bind(on_text_validate=self.send_input)
        self.add_widget(self.input_box)

        self.back_button = Button(
            text='Back to Menu',
            size_hint=(1, 0.05),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            opacity=0,
            disabled=True
        )
        self.back_button.bind(on_press=self._go_back)
        self.add_widget(self.back_button)

        self.input_queue = queue.Queue()
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        self.game_thread = None

        Window.bind(on_resize=self._on_window_resize)

    def _on_window_resize(self, instance, width, height):
        self.output_label.text_size = (width, None)
        self.output_label.width = width
        self.scroll.scroll_x = 0

    def _on_texture_size(self, instance, size):
        instance.height = size[1]
        instance.width = Window.width
        self.scroll.scroll_x = 0

    def start_game(self):
        self.output_label.text = ''
        self.input_box.text = ''
        self.input_box.disabled = False
        self.back_button.opacity = 0
        self.back_button.disabled = True
        if self.game_thread and self.game_thread.is_alive():
            return
        self.game_thread = threading.Thread(target=self._run_game, daemon=True)
        self.game_thread.start()

    def _run_game(self):
        old_stdout = sys.stdout
        old_stdin = sys.stdin
        sys.stdout = GameStdout(self)
        sys.stdin = GameStdin(self.input_queue)
        try:
            game.play_game()
        except SystemExit:
            pass
        except Exception:
            error_msg = traceback.format_exc()
            log_crash(error_msg)
            Clock.schedule_once(lambda dt: self.show_error(error_msg), 0)
        finally:
            sys.stdout = old_stdout
            sys.stdin = old_stdin
            Clock.schedule_once(lambda dt: self.disable_input(), 0)

    def show_error(self, error_msg):
        self.output_label.text += f"\n[ERROR]\n{error_msg}"
        self.scroll.scroll_y = 0

    def add_output(self, text):
        clean = self.ansi_escape.sub('', text)
        if '##CLEARSCREEN##' in clean:
            self.output_label.text = ''
            clean = clean.replace('##CLEARSCREEN##', '')
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
        self.back_button.opacity = 1
        self.back_button.disabled = False

    def _go_back(self, instance):
        self.back_callback()


# ---------- Menu Screen ----------
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        title = Label(
            text='THE RED AFFAIR',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='30sp',
            color=(1, 0, 0, 1),
            size_hint=(1, 0.3)
        )
        layout.add_widget(title)

        start_btn = Button(
            text='Start Game',
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2)
        )
        start_btn.bind(on_press=self.start_game)
        layout.add_widget(start_btn)

        settings_btn = Button(
            text='Settings',
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2)
        )
        settings_btn.bind(on_press=self.open_settings)
        layout.add_widget(settings_btn)

        donate_btn = Button(
            text='Donate',
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2)
        )
        donate_btn.bind(on_press=self.do_donate)
        layout.add_widget(donate_btn)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def start_game(self, instance):
        self.manager.current = 'game'

    def open_settings(self, instance):
        self.manager.current = 'settings'

    def do_donate(self, instance):
        webbrowser.open('https://www.paypal.com/donate?hosted_button_id=EXAMPLE')


# ---------- Settings Screen ----------
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        label = Label(
            text='Settings',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='28sp',
            color=(1, 0, 0, 1),
            size_hint=(1, 0.2)
        )
        layout.add_widget(label)

        self.theme_toggle = ToggleButton(
            text='Dark Mode (Red on Black)',
            state='down',
            font_size='20sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.15)
        )
        self.theme_toggle.bind(on_press=self.toggle_theme)
        layout.add_widget(self.theme_toggle)

        self.dynamic_lighting_toggle = ToggleButton(
            text='Dynamic Lighting: OFF',
            state='normal',
            font_size='20sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.15)
        )
        self.dynamic_lighting_toggle.bind(on_press=self.toggle_dynamic_lighting)
        layout.add_widget(self.dynamic_lighting_toggle)

        back_btn = Button(
            text='Back',
            font_size='20sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.15)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def toggle_theme(self, instance):
        app = App.get_running_app()
        if instance.state == 'down':
            instance.text = 'Dark Mode (Red on Black)'
            app.current_theme = DARK_THEME
        else:
            instance.text = 'Light Mode (Black on White)'
            app.current_theme = LIGHT_THEME
        game_screen = self.manager.get_screen('game')
        game_screen.update_theme(app.current_theme)

    def toggle_dynamic_lighting(self, instance):
        app = App.get_running_app()
        if instance.state == 'down':
            instance.text = 'Dynamic Lighting: ON'
            app.enable_crt()
        else:
            instance.text = 'Dynamic Lighting: OFF'
            app.disable_crt()

    def go_back(self, instance):
        self.manager.current = 'menu'


# ---------- Game Screen ----------
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_ui = None

    def on_enter(self):
        if not self.game_ui:
            app = App.get_running_app()
            self.game_ui = GameUI(theme=app.current_theme, back_callback=self.go_menu)
            self.add_widget(self.game_ui)
        self.start_game()

    def start_game(self):
        try:
            self.game_ui.start_game()
        except Exception:
            err = traceback.format_exc()
            log_crash(err)
            self.game_ui.output_label.text = f"FATAL STARTUP ERROR\n{err}"

    def update_theme(self, theme):
        if self.game_ui:
            self.game_ui.theme = theme
            self.game_ui.output_label.color = theme['fg']
            self.game_ui.input_box.foreground_color = theme['fg']
            self.game_ui.input_box.background_color = theme['input_bg']
            self.game_ui.input_box.cursor_color = theme['cursor']
            with self.game_ui.canvas.before:
                Color(*theme['bg'])
                self.game_ui.bg_rect = Rectangle(size=self.game_ui.size, pos=self.game_ui.pos)

    def go_menu(self):
        self.manager.current = 'menu'


# ---------- Root Widget ----------
class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=FadeTransition(duration=0.5))
        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(GameScreen(name='game'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.current = 'splash'
        self.add_widget(self.sm)

        # CRT overlay always present (but hidden)
        self.crt_overlay = CRTOverlay()
        self.crt_overlay.opacity = 0.0
        self.add_widget(self.crt_overlay)


# ---------- App ----------
class RedAffairApp(App):
    current_theme = DARK_THEME
    crt_enabled = False

    def build(self):
        self.root_widget = RootWidget()
        return self.root_widget

    def enable_crt(self):
        if not self.crt_enabled:
            self.crt_enabled = True
            self.root_widget.crt_overlay.opacity = 1.0
            self.root_widget.crt_overlay.on_show()

    def disable_crt(self):
        if self.crt_enabled:
            self.crt_enabled = False
            self.root_widget.crt_overlay.opacity = 0.0
            self.root_widget.crt_overlay.on_hide()


if __name__ == '__main__':
    try:
        RedAffairApp().run()
    except Exception:
        log_crash(traceback.format_exc())
        raise