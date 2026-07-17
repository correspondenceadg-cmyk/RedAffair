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
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

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
FONT_PATH_DYSLEXIC = 'fonts/OpenDyslexic-Regular.otf'

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

# ---------- SFX Manager ----------
class SFXManager:
    def __init__(self, app):
        self.app = app
        self.sounds = {}
        self.miss_counter = 0

        sfx_list = [
            ('accuse', 'audio/sfx/accuse.ogg'),
            ('gameover', 'audio/sfx/GameOver.ogg'),
            ('fight', 'audio/sfx/fight.ogg'),
            ('miss', 'audio/sfx/miss.ogg'),
            ('miss2', 'audio/sfx/miss2.ogg'),
            ('jaildoor', 'audio/sfx/jaildoor.ogg'),
            ('lvlup', 'audio/sfx/lvlup.ogg'),
            ('take', 'audio/sfx/take.ogg'),
            ('cuffs', 'audio/sfx/cuffs.ogg'),
            ('hit', 'audio/sfx/hit.ogg'),
        ]
        for event, filename in sfx_list:
            try:
                self.sounds[event] = SoundLoader.load(filename)
            except Exception as e:
                log_crash(f"Failed to load SFX {filename}: {traceback.format_exc()}")

        self.queue = queue.Queue()
        Clock.schedule_interval(self._process_queue, 0.05)

    def _process_queue(self, dt):
        while not self.queue.empty():
            event = self.queue.get()
            if not self.app.dynamic_sound_enabled:
                continue
            if event == 'miss':
                self.miss_counter += 1
                key = 'miss' if self.miss_counter % 2 == 1 else 'miss2'
            else:
                key = event
            sound = self.sounds.get(key)
            if sound:
                sound.play()

# ---------- CRT Overlay ----------
class CRTOverlay(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)

        self.scan_tex = Texture.create(size=(4, 4))
        scan_buf = bytes([
            0, 0, 0, 32,  0, 0, 0, 32,  0, 0, 0, 32,  0, 0, 0, 32,
            0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,
            0, 0, 0, 32,  0, 0, 0, 32,  0, 0, 0, 32,  0, 0, 0, 32,
            0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0
        ])
        self.scan_tex.blit_buffer(scan_buf, colorfmt='rgba', bufferfmt='ubyte')
        self.scan_tex.wrap = 'repeat'

        with self.canvas:
            Color(1, 1, 1, 1)
            self.scan_rect = Rectangle(texture=self.scan_tex, size=self.size, pos=self.pos)

            self.edge_left_color = Color(1, 0, 0, 0.03)
            self.edge_left = Rectangle(size=(3, self.height), pos=(0, 0))
            self.edge_right_color = Color(0, 0, 1, 0.03)
            self.edge_right = Rectangle(size=(3, self.height), pos=(self.width - 3, 0))
            self.edge_top_color = Color(1, 0, 0, 0.02)
            self.edge_top = Rectangle(size=(self.width, 2), pos=(0, self.height - 2))
            self.edge_bottom_color = Color(0, 0, 1, 0.02)
            self.edge_bottom = Rectangle(size=(self.width, 2), pos=(0, 0))

            self.glitch_strips = []
            for _ in range(8):
                color_line = Color(1, 1, 1, 0)
                rect_line = Rectangle(size=(self.width, 2), pos=(0, 0))
                self.glitch_strips.append({
                    'color_line': color_line,
                    'rect_line': rect_line
                })

            self.chroma_tears = []
            for _ in range(4):
                color_white = Color(1, 1, 1, 0)
                rect_white = Rectangle(size=(self.width, 40), pos=(0, 0))
                color_red_tear = Color(1, 0, 0, 0)
                rect_red_tear = Rectangle(size=(self.width, 40), pos=(0, 0))
                color_blue_tear = Color(0, 0, 1, 0)
                rect_blue_tear = Rectangle(size=(self.width, 40), pos=(0, 0))
                self.chroma_tears.append({
                    'color_white': color_white,
                    'rect_white': rect_white,
                    'color_red': color_red_tear,
                    'rect_red': rect_red_tear,
                    'color_blue': color_blue_tear,
                    'rect_blue': rect_blue_tear,
                })

        self.bind(size=self._update_rects, pos=self._update_rects)

        self.scan_offset = 0.0
        self.scroll_timer = None
        self.hard_glitch_timer = None
        self.chroma_timer = None
        self.chroma_reset_timer = None
        self.glitch_reschedule_timer = None

    def _update_rects(self, instance, value):
        self.scan_rect.size = instance.size
        self.scan_rect.pos = instance.pos
        self.edge_left.pos = (0, 0)
        self.edge_right.pos = (instance.width - self.edge_right.size[0], 0)
        self.edge_top.pos = (0, instance.height - self.edge_top.size[1])
        self.edge_bottom.pos = (0, 0)
        for strip in self.glitch_strips:
            strip['rect_line'].size = (instance.width, 2)

    def on_show(self):
        self.scroll_timer = Clock.schedule_interval(self._scroll_scanlines, 1/30.0)
        self._schedule_glitch()
        self.chroma_timer = Clock.schedule_interval(self._trigger_chroma, 3.0)

    def on_hide(self):
        if self.scroll_timer:
            self.scroll_timer.cancel()
        if self.glitch_reschedule_timer:
            self.glitch_reschedule_timer.cancel()
        if self.hard_glitch_timer:
            self.hard_glitch_timer.cancel()
        if self.chroma_timer:
            self.chroma_timer.cancel()
        if self.chroma_reset_timer:
            self.chroma_reset_timer.cancel()
        self._reset_glitch()
        self._reset_chroma()

    def _scroll_scanlines(self, dt):
        self.scan_offset += dt * 0.5
        self.scan_offset %= 1.0
        self.scan_rect.tex_coords = (
            0, self.scan_offset,
            1, self.scan_offset,
            1, self.scan_offset + 1.0,
            0, self.scan_offset + 1.0
        )

    def _schedule_glitch(self):
        delay = py_random.uniform(0.5, 5.0)
        self.glitch_reschedule_timer = Clock.schedule_once(
            lambda dt: self._trigger_tear_glitch(), delay
        )

    def _trigger_tear_glitch(self, *args):
        if self.hard_glitch_timer:
            self.hard_glitch_timer.cancel()
        strip = py_random.choice(self.glitch_strips)
        strip_height = 2
        strip_y = py_random.randint(0, max(1, int(self.height) - strip_height))
        shift = py_random.randint(10, 30) * (1 if py_random.random() < 0.5 else -1)

        strip['color_line'].rgba = (1, 1, 1, 0.3)
        strip['rect_line'].size = (self.width, strip_height)
        strip['rect_line'].pos = (self.pos[0] + shift, self.pos[1] + strip_y)

        self.hard_glitch_timer = Clock.schedule_once(self._reset_glitch, 0.07)
        self._schedule_glitch()

    def _reset_glitch(self, dt=None):
        for strip in self.glitch_strips:
            strip['color_line'].rgba = (1, 1, 1, 0)
        self.hard_glitch_timer = None

    def _trigger_chroma(self, dt):
        if self.chroma_reset_timer:
            self.chroma_reset_timer.cancel()

        tear = py_random.choice(self.chroma_tears)
        height = py_random.randint(30, 70)
        y = py_random.randint(0, max(1, int(self.height) - height))
        shift = py_random.randint(20, 45) * (1 if py_random.random() < 0.5 else -1)

        tear['color_white'].rgba = (1, 1, 1, 0.25)
        tear['rect_white'].size = (self.width, height)
        tear['rect_white'].pos = (self.pos[0] + shift, self.pos[1] + y)

        tear['color_red'].rgba = (1, 0, 0, 0.25)
        tear['rect_red'].size = (self.width, height)
        tear['rect_red'].pos = (self.pos[0] + shift - 6, self.pos[1] + y)

        tear['color_blue'].rgba = (0, 0, 1, 0.25)
        tear['rect_blue'].size = (self.width, height)
        tear['rect_blue'].pos = (self.pos[0] + shift + 6, self.pos[1] + y)

        self.scan_rect.pos = (self.pos[0] + shift // 3, self.pos[1])

        self.chroma_reset_timer = Clock.schedule_once(self._reset_chroma, 0.1)

    def _reset_chroma(self, dt=None):
        self.scan_rect.pos = self.pos
        for tear in self.chroma_tears:
            tear['color_white'].rgba = (1, 1, 1, 0)
            tear['color_red'].rgba = (1, 0, 0, 0)
            tear['color_blue'].rgba = (0, 0, 1, 0)
        self.chroma_reset_timer = None

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
        title_text = 'RED AFFAIR'
        title_font_size = '36sp'
        self.title_labels = []
        offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1)]
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

        self.copyright_label = Label(text='SiliCast Games © 2026',
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
        self.spin_event = Clock.schedule_interval(self._rotate_spinner, 1 / 60.0)
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
        app = App.get_running_app()
        font_to_use = FONT_PATH_DYSLEXIC if (app.use_dyslexic_font and os.path.exists(FONT_PATH_DYSLEXIC)) else FONT_PATH if os.path.exists(FONT_PATH) else None
        theme = self.theme
        fg_color = theme['fg']
        if app.custom_palette_enabled:
            fg_color = app.custom_fg_color

        self.output_label = Label(
            text='',
            font_name=font_to_use,
            font_size='13sp',
            color=fg_color,
            size_hint=(None, None),
            halign='left',
            valign='top',
            text_size=(Window.width - 16, None),
            width=Window.width - 16,
            height=0,
            markup=True
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
            foreground_color=fg_color,
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
            font_size='24sp',
            size_hint=(1, None),
            height=100,
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            opacity=0,
            disabled=True
        )
        self.back_button.bind(on_press=self._go_back)
        self.add_widget(self.back_button)

        self.input_queue = queue.Queue()
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        self.evidence_tag_pattern = re.compile(r'\[EVIDENCE_COLOR\](.*?)\[/EVIDENCE_COLOR\]', re.DOTALL)
        self.game_thread = None

        Window.bind(on_resize=self._on_window_resize)

    def _on_window_resize(self, instance, width, height):
        self.output_label.text_size = (width - 16, None)
        self.output_label.width = width - 16
        self.scroll.scroll_x = 0

    def _on_texture_size(self, instance, size):
        instance.height = size[1]
        instance.width = Window.width - 16
        self.scroll.scroll_x = 0

    def start_game(self):
        self.output_label.text = ''
        self.input_box.text = ''
        self.input_box.disabled = False
        self.back_button.opacity = 0
        self.back_button.disabled = True
        if self.game_thread and self.game_thread.is_alive():
            return
        app = App.get_running_app()
        game.sfx_queue = app.sfx_manager.queue
        game.cheat_unlimited_cuffs = app.cheat_unlimited_cuffs
        game.cheat_god_mode = app.cheat_god_mode
        game.cheat_infinite_countenance = app.cheat_infinite_countenance
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

    def _hex_color(self, color):
        r, g, b, a = color
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    def add_output(self, text):
        clean = self.ansi_escape.sub('', text)
        if '##CLEARSCREEN##' in clean:
            self.output_label.text = ''
            clean = clean.replace('##CLEARSCREEN##', '')
        app = App.get_running_app()
        evidence_color = app.custom_evidence_color if app.custom_palette_enabled else (
            (1, 1, 1, 1) if app.current_theme == DARK_THEME else (1, 0, 0, 1)
        )
        hex_evidence = self._hex_color(evidence_color)
        def replace_evidence_tag(match):
            return f"[color={hex_evidence}]{match.group(1)}[/color]"
        clean = self.evidence_tag_pattern.sub(replace_evidence_tag, clean)
        clean = clean.replace('[', '&bl;').replace(']', '&br;')
        max_lines = 1000
        self.output_label.text += clean
        lines = self.output_label.text.splitlines()
        if len(lines) > max_lines:
            self.output_label.text = '\n'.join(lines[-max_lines:])
        self.scroll.scroll_y = 0

    def send_input(self, instance):
        text = instance.text.strip()
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

        self.title_label = Label(
            text='RED AFFAIR',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='36sp',
            color=(1, 0, 0, 1),
            size_hint=(1, 0.35)
        )
        layout.add_widget(self.title_label)
        self.title_taps = 0

        start_btn = Button(
            text='Start Game',
            font_size='30sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 1)
        )
        start_btn.bind(on_press=self.start_game)
        layout.add_widget(start_btn)

        settings_btn = Button(
            text='Settings',
            font_size='30sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 1)
        )
        settings_btn.bind(on_press=self.open_settings)
        layout.add_widget(settings_btn)

        about_btn = Button(
            text='About',
            font_size='30sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 1)
        )
        about_btn.bind(on_press=self.open_about)
        layout.add_widget(about_btn)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def on_enter(self):
        app = App.get_running_app()
        if not app.music_started:
            app.load_music()
            app.music_started = True
        self.title_taps = 0
        self.title_label.bind(on_touch_down=self.on_title_touch)

    def on_title_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.title_taps += 1
            if self.title_taps >= 5:
                self.manager.current = 'cheats'

    def start_game(self, instance):
        self.manager.current = 'game'

    def open_settings(self, instance):
        self.manager.current = 'settings'

    def open_about(self, instance):
        self.manager.current = 'about'

# ---------- About Screen ----------
class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        btn_game = Button(text='Game Information', font_size='30sp', size_hint=(1, 1))
        btn_game.bind(on_press=self.show_game_info)
        layout.add_widget(btn_game)

        btn_dev = Button(text='Developer Information', font_size='30sp', size_hint=(1, 1))
        btn_dev.bind(on_press=self.show_dev_info)
        layout.add_widget(btn_dev)

        btn_linkedin = Button(text='LinkedIn', font_size='30sp', size_hint=(1, 1))
        btn_linkedin.bind(on_press=lambda x: webbrowser.open('https://www.linkedin.com/in/anthony-glosson-a39580414'))
        layout.add_widget(btn_linkedin)

        btn_github = Button(text='GitHub', font_size='30sp', size_hint=(1, 1))
        btn_github.bind(on_press=lambda x: webbrowser.open('https://github.com/correspondenceadg-cmyk'))
        layout.add_widget(btn_github)

        btn_donate = Button(text='Donate', font_size='30sp', size_hint=(1, 1))
        btn_donate.bind(on_press=self.open_donate)
        layout.add_widget(btn_donate)

        back_btn = Button(text='Back', font_size='30sp', size_hint=(1, 1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def show_game_info(self, instance):
        from kivy.uix.popup import Popup
        content = Label(
            text="Red Affair is a neo-noir game inspired by Zork and Disco Elysium style games. It has been a longtime dream of mine to make something exactly like this, and now that I'm fully transitioning into tech as a career, I thought it would be the best first use of my skills and abilities. This game is free to play, own, and distribute. Anyone charging money for it(not that they would, I mean, why would they?) is scamming you or lying to you in some way. If you want, you can reach out to me through any of the links provided in the donate menu or through the Linkedin or Github links embedded into the game. I will be happy to give you the game for free quickly and without resistance.\n\nThe main point of this game is to give myself a portfolio for potential employers to look at. It's something that demonstrates an understanding of python, UI design, and game design. Everything was done entirely by me or using open-source files or otherwise free-use licensed files. I wrote the lines of dialogue, code, and narration.\n\nI hope you like it.",
            font_size='18sp',
            color=(1,0,0,1),
            markup=False
        )
        popup = Popup(title='About the game', content=content, size_hint=(0.8, 0.7))
        popup.open()

    def show_dev_info(self, instance):
        from kivy.uix.popup import Popup
        content = Label(
            text="SiliCast Games is a single-member independent developer project that is seeking to reinvigorate and reintroduce classic styles of games from a bygone era. Everything used in the games is either open-source, common use, or made entirely by hand. At no point is money ever requested for the download, use, or distribution of this game, the files therein, or the identity of the studio. For questions and comments, check the github and linkedin buttons or email me at\n\ncorrespondenceadg@gmail.com",
            font_size='18sp',
            color=(1,0,0,1),
            markup=False
        )
        popup = Popup(title='About SiliCast Games', content=content, size_hint=(0.8, 0.7))
        popup.open()

    def open_donate(self, instance):
        self.manager.current = 'donate'

    def go_back(self, instance):
        self.manager.current = 'menu'

# ---------- Donate Screen ----------
class DonateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        label = Label(
            text='Support Red Affair',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='28sp',
            color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=80
        )
        layout.add_widget(label)

        paypal_btn = Button(
            text='Donate via PayPal',
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        paypal_btn.bind(on_press=self.do_paypal)
        layout.add_widget(paypal_btn)

        cashapp_btn = Button(
            text='Donate via CashApp',
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        cashapp_btn.bind(on_press=self.do_cashapp)
        layout.add_widget(cashapp_btn)

        back_btn = Button(
            text='Back',
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def do_paypal(self, instance):
        webbrowser.open('https://www.paypal.me/panytierra')

    def do_cashapp(self, instance):
        webbrowser.open('https://cash.app/$commiesimplord')

    def go_back(self, instance):
        self.manager.current = 'about'

# ---------- Settings Screen ----------
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=30, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        header = Label(
            text='SETTINGS',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='30sp',
            color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=80
        )
        self.layout.add_widget(header)

        self.theme_toggle = ToggleButton(
            text='Dark Mode (Red on Black)',
            state='down',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        self.theme_toggle.bind(on_press=self.toggle_theme)
        self.layout.add_widget(self.theme_toggle)

        self.dynamic_lighting_toggle = ToggleButton(
            text='Dynamic Lighting: ON',
            state='down',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        self.dynamic_lighting_toggle.bind(on_press=self.toggle_dynamic_lighting)
        self.layout.add_widget(self.dynamic_lighting_toggle)

        self.dynamic_sound_toggle = ToggleButton(
            text='Dynamic Sound: ON',
            state='down',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        self.dynamic_sound_toggle.bind(on_press=self.toggle_dynamic_sound)
        self.layout.add_widget(self.dynamic_sound_toggle)

        self.music_toggle = ToggleButton(
            text='Music: ON',
            state='down',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        self.music_toggle.bind(on_press=self.toggle_music)
        self.layout.add_widget(self.music_toggle)

        self.dyslexic_font_toggle = ToggleButton(
            text='Dyslexic Font: OFF',
            state='normal',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        self.dyslexic_font_toggle.bind(on_press=self.toggle_dyslexic_font)
        self.layout.add_widget(self.dyslexic_font_toggle)

        self.palette_button = Button(
            text='Configure Palette',
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        self.palette_button.bind(on_press=self.open_palette)
        self.layout.add_widget(self.palette_button)

        self.track_label = Label(
            text='Now Playing: None',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='18sp',
            color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=80,
            halign='center',
            valign='middle',
            text_size=(Window.width - 40, None)
        )
        self.layout.add_widget(self.track_label)

        vol_label = Label(
            text='Music Volume',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='18sp',
            color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=40
        )
        self.layout.add_widget(vol_label)

        self.volume_slider = Slider(
            min=0, max=1, value=0.3,
            size_hint=(1, None), height=80,
            value_track_color=(1, 0, 0, 1),
            value_track_width=6,
            background_width=3,
            cursor_image='assets/slider.png',
            cursor_size=(0, 0)
        )
        self.volume_slider.bind(value=self.on_volume_change)
        self.layout.add_widget(self.volume_slider)

        self.vol_bar_label = Label(
            text='[          ]',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='20sp',
            color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=40,
            halign='center'
        )
        self.layout.add_widget(self.vol_bar_label)

        self.next_track_btn = Button(
            text='Next Track',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        self.next_track_btn.bind(on_press=self.next_track)
        self.layout.add_widget(self.next_track_btn)

        self.sound_test_btn = Button(
            text='Sound Test',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        self.sound_test_btn.bind(on_press=self.open_sound_test)
        self.layout.add_widget(self.sound_test_btn)

        back_btn = Button(
            text='Back',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def on_enter(self):
        app = App.get_running_app()
        self.track_label.text_size = (self.width - 40, None)
        self.volume_slider.value = app.music_volume
        self._update_track_label()
        self._update_vol_bar()
        self.dyslexic_font_toggle.state = 'down' if app.use_dyslexic_font else 'normal'
        self.dyslexic_font_toggle.text = 'Dyslexic Font: ON' if app.use_dyslexic_font else 'Dyslexic Font: OFF'

    def _update_track_label(self):
        app = App.get_running_app()
        if app.music_sound and app.music_enabled:
            info = app.music_info.get(app.music_tracks[app.music_index], ('Unknown', 'Unknown'))
            self.track_label.text = f'Now Playing: {info[0]} - {info[1]}'
        else:
            self.track_label.text = 'Music Off'

    def _update_vol_bar(self, *args):
        val = self.volume_slider.value
        filled = int(val * 10)
        empty = 10 - filled
        bar = '[' + '=' * filled + ' ' * empty + ']'
        self.vol_bar_label.text = bar

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

    def toggle_dynamic_sound(self, instance):
        app = App.get_running_app()
        if instance.state == 'down':
            instance.text = 'Dynamic Sound: ON'
            app.enable_dynamic_sound()
        else:
            instance.text = 'Dynamic Sound: OFF'
            app.disable_dynamic_sound()

    def toggle_music(self, instance):
        app = App.get_running_app()
        if instance.state == 'down':
            instance.text = 'Music: ON'
            app.enable_music()
        else:
            instance.text = 'Music: OFF'
            app.disable_music()
        self._update_track_label()

    def toggle_dyslexic_font(self, instance):
        app = App.get_running_app()
        app.use_dyslexic_font = instance.state == 'down'
        instance.text = 'Dyslexic Font: ON' if app.use_dyslexic_font else 'Dyslexic Font: OFF'

    def open_palette(self, instance):
        self.manager.current = 'palette'

    def on_volume_change(self, instance, value):
        app = App.get_running_app()
        app.set_music_volume(value)
        self._update_vol_bar()

    def next_track(self, instance):
        app = App.get_running_app()
        app.next_track()
        self._update_track_label()

    def open_sound_test(self, instance):
        self.manager.current = 'soundtest'

    def go_back(self, instance):
        self.manager.current = 'menu'

# ---------- Palette Screen ----------
class PaletteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=30, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        header = Label(
            text='CUSTOM PALETTE',
            font_name=FONT_PATH if os.path.exists(FONT_PATH) else None,
            font_size='30sp',
            color=(1, 0, 0, 1),
            size_hint=(1, None),
            height=80
        )
        self.layout.add_widget(header)

        self.toggle_btn = ToggleButton(
            text='Custom Palette: OFF',
            state='normal',
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        self.toggle_btn.bind(on_press=self.toggle_palette)
        self.layout.add_widget(self.toggle_btn)

        self.fg_section = self._build_section("Base Text Color", 'fg')
        self.bg_section = self._build_section("Background Color", 'bg')
        self.ev_section = self._build_section("Evidence Name Color", 'evidence')
        self.layout.add_widget(self.fg_section)
        self.layout.add_widget(self.bg_section)
        self.layout.add_widget(self.ev_section)

        back_btn = Button(
            text='Back to Settings',
            font_size='24sp',
            background_color=(0.2, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=100
        )
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)

    def _build_section(self, title, key):
        box = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=180)
        lbl = Label(text=title, font_size='18sp', color=(1,1,1,1), size_hint_y=None, height=30)
        box.add_widget(lbl)
        r_slider = Slider(min=0, max=1, value=1, size_hint_y=None, height=40)
        g_slider = Slider(min=0, max=1, value=0, size_hint_y=None, height=40)
        b_slider = Slider(min=0, max=1, value=0, size_hint_y=None, height=40)
        r_slider.bind(value=lambda inst, val: self._on_slider(key, inst, val))
        g_slider.bind(value=lambda inst, val: self._on_slider(key, inst, val))
        b_slider.bind(value=lambda inst, val: self._on_slider(key, inst, val))
        box.add_widget(Label(text='R', font_size='14sp', color=(1,0,0,1), size_hint_y=None, height=20))
        box.add_widget(r_slider)
        box.add_widget(Label(text='G', font_size='14sp', color=(0,1,0,1), size_hint_y=None, height=20))
        box.add_widget(g_slider)
        box.add_widget(Label(text='B', font_size='14sp', color=(0,0,1,1), size_hint_y=None, height=20))
        box.add_widget(b_slider)
        preview = Label(text='Preview', size_hint_y=None, height=30, color=(1,1,1,1))
        box.add_widget(preview)
        setattr(self, f'{key}_sliders', (r_slider, g_slider, b_slider, preview))
        return box

    def _on_slider(self, key, instance, value):
        app = App.get_running_app()
        if app.custom_palette_enabled:
            r, g, b, preview = getattr(self, f'{key}_sliders')
            color = (r.value, g.value, b.value, 1)
            if key == 'fg':
                app.custom_fg_color = color
            elif key == 'bg':
                app.custom_bg_color = color
            elif key == 'evidence':
                app.custom_evidence_color = color
            preview.color = color
            game_screen = self.manager.get_screen('game')
            game_screen.update_theme(app.current_theme)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def on_enter(self):
        app = App.get_running_app()
        self.toggle_btn.state = 'down' if app.custom_palette_enabled else 'normal'
        self.toggle_btn.text = 'Custom Palette: ON' if app.custom_palette_enabled else 'Custom Palette: OFF'
        r,g,b,_ = app.custom_fg_color
        self.fg_sliders[0].value = r
        self.fg_sliders[1].value = g
        self.fg_sliders[2].value = b
        self.fg_sliders[3].color = app.custom_fg_color
        r,g,b,_ = app.custom_bg_color
        self.bg_sliders[0].value = r
        self.bg_sliders[1].value = g
        self.bg_sliders[2].value = b
        self.bg_sliders[3].color = app.custom_bg_color
        r,g,b,_ = app.custom_evidence_color
        self.evidence_sliders[0].value = r
        self.evidence_sliders[1].value = g
        self.evidence_sliders[2].value = b
        self.evidence_sliders[3].color = app.custom_evidence_color

    def toggle_palette(self, instance):
        app = App.get_running_app()
        app.custom_palette_enabled = instance.state == 'down'
        self.toggle_btn.text = 'Custom Palette: ON' if app.custom_palette_enabled else 'Custom Palette: OFF'
        game_screen = self.manager.get_screen('game')
        game_screen.update_theme(app.current_theme)

    def go_back(self, instance):
        self.manager.current = 'settings'

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
            app = App.get_running_app()
            fg_color = theme['fg']
            if app.custom_palette_enabled:
                fg_color = app.custom_fg_color
            self.game_ui.output_label.color = fg_color
            self.game_ui.input_box.foreground_color = fg_color
            self.game_ui.input_box.background_color = theme['input_bg']
            self.game_ui.input_box.cursor_color = theme['cursor']
            with self.game_ui.canvas.before:
                Color(*theme['bg'])
                self.game_ui.bg_rect = Rectangle(size=self.game_ui.size, pos=self.game_ui.pos)

    def go_menu(self):
        self.manager.current = 'menu'

# ---------- Cheats Screen ----------
class CheatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        lbl = Label(text='CHEATS', font_size='30sp', color=(1,0,0,1))
        layout.add_widget(lbl)

        self.cuffs_toggle = ToggleButton(text='Unlimited Cuffs: OFF', font_size='24sp', size_hint=(1, None), height=100)
        self.cuffs_toggle.bind(on_press=self.toggle_cuffs)
        layout.add_widget(self.cuffs_toggle)

        self.god_toggle = ToggleButton(text='God Mode: OFF', font_size='24sp', size_hint=(1, None), height=100)
        self.god_toggle.bind(on_press=self.toggle_god)
        layout.add_widget(self.god_toggle)

        self.countenance_toggle = ToggleButton(text='Infinite Countenance: OFF', font_size='24sp', size_hint=(1, None), height=100)
        self.countenance_toggle.bind(on_press=self.toggle_countenance)
        layout.add_widget(self.countenance_toggle)

        back_btn = Button(text='Back', font_size='24sp', size_hint=(1, None), height=100)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def on_enter(self):
        app = App.get_running_app()
        self.cuffs_toggle.state = 'down' if app.cheat_unlimited_cuffs else 'normal'
        self.cuffs_toggle.text = f'Unlimited Cuffs: {"ON" if app.cheat_unlimited_cuffs else "OFF"}'
        self.god_toggle.state = 'down' if app.cheat_god_mode else 'normal'
        self.god_toggle.text = f'God Mode: {"ON" if app.cheat_god_mode else "OFF"}'
        self.countenance_toggle.state = 'down' if app.cheat_infinite_countenance else 'normal'
        self.countenance_toggle.text = f'Infinite Countenance: {"ON" if app.cheat_infinite_countenance else "OFF"}'

    def toggle_cuffs(self, instance):
        app = App.get_running_app()
        app.cheat_unlimited_cuffs = instance.state == 'down'
        instance.text = f'Unlimited Cuffs: {"ON" if app.cheat_unlimited_cuffs else "OFF"}'

    def toggle_god(self, instance):
        app = App.get_running_app()
        app.cheat_god_mode = instance.state == 'down'
        instance.text = f'God Mode: {"ON" if app.cheat_god_mode else "OFF"}'

    def toggle_countenance(self, instance):
        app = App.get_running_app()
        app.cheat_infinite_countenance = instance.state == 'down'
        instance.text = f'Infinite Countenance: {"ON" if app.cheat_infinite_countenance else "OFF"}'

    def go_back(self, instance):
        self.manager.current = 'menu'

# ---------- Sound Test Screen ----------
class SoundTestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        with self.canvas.before:
            Color(0,0,0,1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.current_label = Label(text='No Sound', font_size='22sp', color=(1,0,0,1))
        self.layout.add_widget(self.current_label)

        nav = BoxLayout(size_hint=(1, None), height=60)
        prev_btn = Button(text='<', font_size='30sp')
        prev_btn.bind(on_press=self.prev_sound)
        play_btn = Button(text='Play', font_size='30sp')
        play_btn.bind(on_press=self.play_sound)
        next_btn = Button(text='>', font_size='30sp')
        next_btn.bind(on_press=self.next_sound)
        stop_btn = Button(text='Stop', font_size='30sp')
        stop_btn.bind(on_press=self.stop_sound)
        nav.add_widget(prev_btn)
        nav.add_widget(play_btn)
        nav.add_widget(stop_btn)
        nav.add_widget(next_btn)
        self.layout.add_widget(nav)

        back_btn = Button(text='Back to Settings', font_size='24sp', size_hint=(1, None), height=100)
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)
        self.sound_list = []
        self.current_index = 0
        self.active_sound = None

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def on_enter(self):
        app = App.get_running_app()
        self.sound_list = []
        for name, sound in app.sfx_manager.sounds.items():
            self.sound_list.append(('SFX', name, sound))
        for track in app.music_tracks:
            self.sound_list.append(('MUSIC', track, None))
        self.current_index = 0
        self._update_display()

    def _update_display(self):
        if self.sound_list:
            typ, name, _ = self.sound_list[self.current_index]
            self.current_label.text = f'{typ}: {name}'
        else:
            self.current_label.text = 'No sounds loaded'

    def prev_sound(self, instance):
        if self.sound_list:
            self.current_index = (self.current_index - 1) % len(self.sound_list)
            self._update_display()

    def next_sound(self, instance):
        if self.sound_list:
            self.current_index = (self.current_index + 1) % len(self.sound_list)
            self._update_display()

    def play_sound(self, instance):
        if not self.sound_list:
            return
        self.stop_sound(None)
        typ, name, sound = self.sound_list[self.current_index]
        if typ == 'SFX' and sound:
            sound.play()
            self.active_sound = sound
        elif typ == 'MUSIC':
            app = App.get_running_app()
            s = SoundLoader.load(name)
            if s:
                s.play()
                self.active_sound = s

    def stop_sound(self, instance):
        if self.active_sound:
            self.active_sound.stop()
            self.active_sound = None

    def on_leave(self):
        self.stop_sound(None)

    def go_back(self, instance):
        self.stop_sound(None)
        self.manager.current = 'settings'

# ---------- Root Widget ----------
class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=FadeTransition(duration=0.5))
        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(AboutScreen(name='about'))
        self.sm.add_widget(DonateScreen(name='donate'))
        self.sm.add_widget(GameScreen(name='game'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(PaletteScreen(name='palette'))
        self.sm.add_widget(CheatsScreen(name='cheats'))
        self.sm.add_widget(SoundTestScreen(name='soundtest'))
        self.sm.current = 'splash'
        self.add_widget(self.sm)

        self.crt_overlay = CRTOverlay()
        self.crt_overlay.opacity = 1.0
        self.add_widget(self.crt_overlay)
        self.crt_overlay.on_show()

# ---------- App ----------
class RedAffairApp(App):
    current_theme = DARK_THEME
    crt_enabled = True
    dynamic_sound_enabled = True
    music_enabled = True
    use_dyslexic_font = False
    custom_palette_enabled = False
    custom_fg_color = (1, 0, 0, 1)
    custom_bg_color = (0, 0, 0, 1)
    custom_evidence_color = (1, 1, 1, 1)
    cheat_unlimited_cuffs = False
    cheat_god_mode = False
    cheat_infinite_countenance = False

    music_tracks = [
        'audio/track1.ogg',
        'audio/track2.ogg',
        'audio/track3.ogg',
        'audio/track4.ogg'
    ]
    music_info = {
        'audio/track1.ogg': ('Blue Eyes', 'Dotdropper'),
        'audio/track2.ogg': ('What A Shame', 'Dotdropper'),
        'audio/track3.ogg': ('Track 3', 'Composer 3'),
        'audio/track4.ogg': ('Track 4', 'Composer 4'),
    }
    music_index = 0
    music_volume = 0.3
    music_sound = None
    music_started = False

    ambient_hum = None
    footstep_sound = None
    siren_sound = None
    footstep_timer = None
    siren_timer = None

    def build(self):
        self.sfx_manager = SFXManager(self)
        self.root_widget = RootWidget()
        Clock.schedule_once(lambda dt: self.start_music(), 1)
        Clock.schedule_once(lambda dt: self.start_ambient(), 2)
        return self.root_widget

    def start_music(self):
        if not self.music_started:
            self.load_music()
            self.music_started = True

    def load_music(self):
        try:
            path = self.music_tracks[self.music_index]
            log_crash(f"Loading music: {path}")
            self.music_sound = SoundLoader.load(path)
            if self.music_sound:
                self.music_sound.volume = self.music_volume
                self.music_sound.loop = True
                if self.music_enabled:
                    self.music_sound.play()
                log_crash("Music started playing")
                settings_screen = self.root_widget.sm.get_screen('settings')
                if settings_screen:
                    settings_screen._update_track_label()
            else:
                log_crash(f"Failed to load music: {path}")
                settings_screen = self.root_widget.sm.get_screen('settings')
                if settings_screen:
                    settings_screen.track_label.text = f"Error loading {path}"
        except Exception as e:
            log_crash(f"Music error: {traceback.format_exc()}")

    def set_music_volume(self, volume):
        self.music_volume = volume
        if self.music_sound:
            self.music_sound.volume = volume

    def next_track(self):
        if len(self.music_tracks) <= 1:
            return
        self.music_index = (self.music_index + 1) % len(self.music_tracks)
        if self.music_sound:
            self.music_sound.stop()
            self.music_sound.unload()
        self.load_music()

    def enable_music(self):
        self.music_enabled = True
        if self.music_sound:
            self.music_sound.play()
        settings_screen = self.root_widget.sm.get_screen('settings')
        if settings_screen:
            settings_screen.volume_slider.disabled = False
            settings_screen._update_track_label()

    def disable_music(self):
        self.music_enabled = False
        if self.music_sound:
            self.music_sound.stop()
        settings_screen = self.root_widget.sm.get_screen('settings')
        if settings_screen:
            settings_screen.volume_slider.disabled = True
            settings_screen._update_track_label()

    def start_ambient(self):
        try:
            self.ambient_hum = SoundLoader.load('audio/crthum.ogg')
            if self.ambient_hum:
                self.ambient_hum.loop = True
                self.ambient_hum.volume = 0.15
                self.ambient_hum.play()
        except Exception as e:
            log_crash(f"Hum load error: {traceback.format_exc()}")

        try:
            self.footstep_sound = SoundLoader.load('audio/footsteps.ogg')
        except Exception as e:
            log_crash(f"Footstep load error: {traceback.format_exc()}")

        try:
            self.siren_sound = SoundLoader.load('audio/siren.ogg')
        except Exception as e:
            log_crash(f"Siren load error: {traceback.format_exc()}")

        self._schedule_footsteps()
        self._schedule_siren()

    def _schedule_footsteps(self):
        if not self.dynamic_sound_enabled:
            return
        delay = py_random.uniform(7, 21)
        self.footstep_timer = Clock.schedule_once(lambda dt: self._play_footstep(), delay)

    def _play_footstep(self):
        if self.dynamic_sound_enabled and self.footstep_sound:
            self.footstep_sound.play()
        self._schedule_footsteps()

    def _schedule_siren(self):
        if not self.dynamic_sound_enabled:
            return
        delay = py_random.uniform(21, 42)
        self.siren_timer = Clock.schedule_once(lambda dt: self._play_siren(), delay)

    def _play_siren(self):
        if self.dynamic_sound_enabled and self.siren_sound:
            self.siren_sound.play()
        self._schedule_siren()

    def enable_dynamic_sound(self):
        self.dynamic_sound_enabled = True
        if self.ambient_hum:
            self.ambient_hum.play()
        self._schedule_footsteps()
        self._schedule_siren()

    def disable_dynamic_sound(self):
        self.dynamic_sound_enabled = False
        if self.ambient_hum:
            self.ambient_hum.stop()
        if self.footstep_timer:
            self.footstep_timer.cancel()
        if self.siren_timer:
            self.siren_timer.cancel()

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