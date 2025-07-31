from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
try:
    import RPi.GPIO as GPIO
except ImportError:
    class MockGPIO:
        BCM = OUT = HIGH = LOW = None
        def setmode(self, *_): pass
        def setup(self, *_): pass
        def output(self, *_): pass
        def cleanup(self): pass
    GPIO = MockGPIO()
from kivy.core.window import Window
Window.clearcolor = (0.95, 0.88, 0.7, 1)
from kivy.app import App
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton, MDRaisedButton, MDFlatButton, MDFillRoundFlatButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivymd.uix.snackbar import Snackbar
import time as t
import serial
from time import time
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.screenmanager import FadeTransition
import threading

LabelBase.register(name="Spartan-Black", fn_regular="fonts/LeagueSpartan-Black.ttf")
LabelBase.register(name="Spartan-Bold", fn_regular="fonts/LeagueSpartan-Bold.ttf")
LabelBase.register(name="Spartan-ExtraBold", fn_regular="fonts/LeagueSpartan-ExtraBold.ttf")
LabelBase.register(name="Spartan-ExtraLight", fn_regular="fonts/LeagueSpartan-ExtraLight.ttf")
LabelBase.register(name="Spartan-Light", fn_regular="fonts/LeagueSpartan-Light.ttf")
LabelBase.register(name="Spartan-Medium", fn_regular="fonts/LeagueSpartan-Medium.ttf")
LabelBase.register(name="Spartan-Regular", fn_regular="fonts/LeagueSpartan-Regular.ttf")
LabelBase.register(name="Spartan-SemiBold", fn_regular="fonts/LeagueSpartan-SemiBold.ttf")
LabelBase.register(name="Spartan-Thin", fn_regular="fonts/LeagueSpartan-Thin.ttf")


COLORS = {
    "dark_red": get_color_from_hex("#7c0a0a"),
    "red": get_color_from_hex("#bf3131"),
    "gray_orange": get_color_from_hex("#ead196"),
    "light_gray": get_color_from_hex("#eeeeee"),
}
number = "09760691268"
location = "Studio"
RELAY_PINS = {
        "Sprains and Strains": 24,
        "Nosebleeds": 25,
        "Laceration (Cut)": 18,
        "Insect Bites or Minor Allergic Reactions": 23,
        "Bruise / Contusion": 12,
        "Fainting": 16,
        "Burns (1st or 2nd)": 20,
        "Choking (Partial)": 21,
    }

guide_data = {
    "Sprains and Strains": {
        "images": [f"images/sprain{str(i).zfill(2)}.jpg" for i in range(1, 7)],
        "screen": "sprain_guide",
        "key": "Sprains and Strains",
        "question_bg": "images/sprainQuestions.jpg",
        "questions": [
            "Did you hear a “pop” or feel a snap when the injury happened?",
            "Is the area swollen, bruised, or painful to move?",
            "Is the person unable to move the area at all?"
        ],
        "severe_bg": "images/sprainSevere.jpg"
    },
    "Laceration (Cut)": {
        "images": [f"images/laceration{str(i).zfill(2)}.jpg" for i in range(1, 10)],
        "screen": "laceration_guide",
        "key": "Laceration (Cut)",
        "question_bg": "images/lacerationQuestions.jpg",
        "questions": [
            "Is the wound bleeding heavily and not stopping?",
            "Is something stuck in the wound (glass, metal)?",
            "Is the cut deep or very large?"
        ],
        "severe_bg": "images/lacerationSevere.jpg"
    },
    "Bruise / Contusion": {
        "images": [f"images/bruise{str(i).zfill(2)}.jpg" for i in range(1, 7)],
        "screen": "bruise_guide",
        "key": "Bruise / Contusion",
        "question_bg": "images/bruiseQuestions.jpg",
        "questions": [
            "Is there severe pain or swelling in the injured area?",
            "Was the bruise caused by a strong impact to the head, chest, or back?",
            "Does the skin look very dark, purple, or oddly shaped?"
        ],
        "severe_bg": "images/bruiseSevere.jpg"
    },
    "Nosebleeds": {
        "images": [f"images/nosebleed{str(i).zfill(2)}.jpg" for i in range(1, 8)],
        "screen": "nosebleed_guide",
        "key": "Nosebleeds",
        "question_bg": "images/nosebleedQuestions.jpg",
        "questions": [
            "Has the nosebleed lasted more than 20 minutes?",
            "Was the nosebleed caused by a head injury or trauma?",
            "Is the person feeling faint, dizzy, or very weak?"
        ],
        "severe_bg": "images/nosebleedSevere.jpg"
    },
    "Insect Bites": {
        "images": [f"images/insectbite{str(i).zfill(2)}.jpg" for i in range(1, 8)],
        "screen": "insect_bite_guide",
        "key": "Insect Bites or Minor Allergic Reactions",
        "question_bg": "images/insectbiteQuestions.jpg",
        "questions": [
            "Is the person having trouble breathing or swallowing?",
            "Is there swelling on the face, lips, or throat?",
            "Is the person dizzy, confused, or showing signs of fainting?"
        ],
        "severe_bg": "images/insectbiteSevere.jpg"
    },
    "Burns (1st or 2nd)": {
        "images": [f"images/burns{str(i).zfill(2)}.jpg" for i in range(1, 8)],
        "screen": "burns_guide",
        "key": "Burns (1st or 2nd)",
        "question_bg": "images/burnsQuestions.jpg",
        "questions": [
            "Is the burn larger than the size of the person's hand?",
            "Are there open blisters or raw, peeling skin?",
            "Was the burn caused by chemicals or electricity?"
        ],
        "severe_bg": "images/burnsSevere.jpg"
    },
}
def show_pin_popup(self, *args):
    popup = ModalView(size_hint=(0.6, 0.65), auto_dismiss=True)

    layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

    pin_input = TextInput(
        hint_text="Enter PIN",
        password=True,
        multiline=False,
        halign="center",
        font_size="40sp",
        size_hint_y=None,
        height=dp(80)
    )

    keypad = GridLayout(cols=3, spacing=dp(10), size_hint_y=None)
    keypad.bind(minimum_height=keypad.setter("height"))

    def add_btn(text, action=None):
        return MDFillRoundFlatButton(
            text=text,
            font_size="30sp",
            size_hint=(0.3, None),
            height=dp(80),
            on_release=action or (lambda x: pin_input.insert_text(text)),
        )

    for num in range(1, 10):
        keypad.add_widget(add_btn(str(num)))
    keypad.add_widget(Widget())  # Empty spot
    keypad.add_widget(add_btn("0"))
    keypad.add_widget(add_btn("<", lambda x: pin_input.do_backspace()))

    layout.add_widget(pin_input)
    layout.add_widget(keypad)

    popup.add_widget(layout)
    popup.open()
    
def show_settings_popup():
    global number, location

    settings_popup = ModalView(size_hint=(0.3, 0.2), auto_dismiss=True)
    layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

    input_box_style = {
        "size_hint_y": None,
        "height": dp(48),
        "font_size": "18sp",
        "halign": "left"
    }

    number_input = TextInput(
        text=number,
        hint_text="Phone Number",
        input_filter="int",
        input_type='number',
        multiline=False,
        **input_box_style
    )

    location_input = TextInput(
        text=location,
        hint_text="Location",
        input_type='text',
        multiline=False,
        **input_box_style
    )

    def save_settings(instance):
        global number, location
        number = number_input.text.strip()
        location = location_input.text.strip()
        settings_popup.dismiss()
    def focus_number_input(dt):
        number_input.focus = True
    btn_layout = BoxLayout(
        size_hint_y=None,
        height=dp(40),
        spacing=dp(10),
        padding=(0, dp(10)),
        size_hint=(.3, None),
        
        pos_hint={'center_x': 0.5}
    )
    btn_layout.add_widget(MDRaisedButton(text="Cancel",md_bg_color=get_color_from_hex("#4CAF50"), on_release=lambda x: settings_popup.dismiss()))
    btn_layout.add_widget(MDRaisedButton(text="Save",md_bg_color=get_color_from_hex("#F44336"), on_release=save_settings))

    layout.add_widget(number_input)
    layout.add_widget(location_input)
    layout.add_widget(btn_layout)

    settings_popup.add_widget(layout)
    settings_popup.open()   
    Clock.schedule_once(focus_number_input, 0.3)
    
    

#Screens
class StartScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout with dark red background
        self.md_bg_color = get_color_from_hex("#7c0a0a")

        layout = MDBoxLayout(orientation='vertical', padding=dp(38), spacing=dp(20))

        card = MDCard(
            orientation='vertical',
            size_hint=(1, 1),
            padding=dp(40),
            md_bg_color=get_color_from_hex("#ead196"),
            radius=[30],
        )

        card.add_widget(Label(
            text="FIRST AID",
            font_name="Spartan-Black",
            font_size="300sp",
            halign="center",
            color=get_color_from_hex("#7c0a0a")
        ))

        card.add_widget(Label(
            text="TAP ANYWHERE TO START",
            font_name="Spartan-Medium",
            font_size="36sp",
            halign="center",
            color=get_color_from_hex("#7c0a0a")
        ))

        layout.add_widget(card)
        self.add_widget(layout)
        self.bind(on_touch_down=self.go_to_main)

    def go_to_main(self, *args):
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = 'menu'

# Main Menu Screen
class TappableLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tap_count = 0
        self.last_tap_time = 0
        self.tap_delay = 0.3  # seconds
        self.bind(on_touch_up=self.detect_secret_tap)

    def detect_secret_tap(self, instance, touch):
        if not self.collide_point(*touch.pos):
            return False
        now = time()
        if now - self.last_tap_time < self.tap_delay:
            return False  # Ignore rapid double taps
        self.last_tap_time = now

        self.tap_count += 1
        if self.tap_count >= 5:
            self.tap_count = 0
            Clock.schedule_once(lambda dt: self.show_pin_popup())
        return True

    def show_pin_popup(self, *args):
        popup = ModalView(size_hint=(0.3, 0.4), auto_dismiss=True)

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        pin_input = TextInput(
            hint_text="Enter PIN",
            password=True,
            multiline=False,
            halign="center",
            font_size="40sp",
            size_hint_y=None,
            height=dp(80)
        )

        keypad = GridLayout(cols=3, spacing=dp(10), size_hint_y=None, size_hint=(1, None))
        keypad.bind(minimum_height=keypad.setter("height"))
        def check_pin(pin):
            if pin == "2222":
                App.get_running_app().stop()
            elif pin == "1111":
                popup.dismiss()
                Clock.schedule_once(lambda dt: show_settings_popup())
        def add_btn(text, action=None):
            debounce_flag = {"ready": True}

            def on_release(instance):
                if debounce_flag["ready"]:
                    debounce_flag["ready"] = False
                    Clock.schedule_once(lambda dt: debounce_flag.update({"ready": True}), 0.3)
                    if action:
                        action(instance)
                    else:
                        pin_input.insert_text(text)
                        if len(pin_input.text + text) == 4:
                            Clock.schedule_once(lambda dt: check_pin(pin_input.text + text), 0.1)

            return MDFillRoundFlatButton(
                text=text,
                font_size="30sp",
                size_hint=(1, None),
                height=dp(80),
                on_release=on_release,
            )

        for num in range(1, 10):
            keypad.add_widget(add_btn(str(num)))
        keypad.add_widget(Widget())
        keypad.add_widget(add_btn("0"))
        keypad.add_widget(add_btn("<", lambda x: pin_input.do_backspace()))

        layout.add_widget(pin_input)
        layout.add_widget(keypad)
        popup.add_widget(layout)
        popup.open()
        
class MainMenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#7c0a0a")
        layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(38),
            spacing=dp(30),
        )
        
        card = MDCard(
            orientation='vertical',
            size_hint=(1, 1),
            padding=dp(40),
            spacing=dp(50),
            md_bg_color=get_color_from_hex("#ead196"),
            radius=[30],
        )

        card.add_widget(Widget(size_hint_y=None, height=dp(40)))
        card.add_widget(TappableLabel(
            text="FIRST AID",
            font_name="Spartan-Black",
            font_size="150",
            halign="center",
            color=get_color_from_hex("#7c0a0a"),
        ))
        card.add_widget(Widget(size_hint_y=None, height=dp(60)))
        
        emergency_btn = MDFillRoundFlatButton(
            text="EMERGENCY",
            font_name="Spartan-Medium",
            font_size="80sp",
            size_hint=(0.4, None),
            height=dp(100),
            md_bg_color=get_color_from_hex("#7c0a0a"),
            text_color=get_color_from_hex("#ead196"),
            pos_hint={"center_x": 0.5},
            padding=(0, dp(50)),
        )
        
        emergency_btn.bind(on_release=self.goto_emergency)

        learn_btn = MDFillRoundFlatButton(
            text="LEARNING MODE",
            font_name="Spartan-Medium",
            font_size="40sp",
            size_hint=(0.3, None),
            height=dp(60),
            md_bg_color=get_color_from_hex("#7c0a0a"),
            text_color=get_color_from_hex("#ead196"),
            pos_hint={"center_x": 0.5},
            padding=(0, dp(50)),
        )
        learn_btn.set_radius()
    
        card.add_widget(emergency_btn)
        card.add_widget(learn_btn)
        card.add_widget(Widget(size_hint_y=None, height=dp(40)))
        layout.add_widget(card)
        self.add_widget(layout)
        
    def goto_emergency(self, *args):
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = 'emergency'    



class TriageScreen(MDScreen):
    def on_pre_enter(self):
        self.question_index = 0
        self.data = self.manager.current_data
        self.questions = guide_data[self.data]["questions"]
        self.build_ui()
        # Set background if available
        bg_path = guide_data[self.data].get("question_bg")
        if bg_path and hasattr(self, "bg"):
            self.bg.source = bg_path

        
        self.display_question()

    def build_ui(self):
        self.clear_widgets()

        self.bg = Image(source="", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg)

        layout = BoxLayout(orientation='vertical', spacing=40, padding=60)
        layout.size_hint = (1, 1)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        layout.add_widget(Widget(size_hint_y=0.35))
        self.question_label = Label(
            text=self.questions[0],
            color=get_color_from_hex("#7c0a0a"),
            font_name="Spartan-Medium",
            font_size="50sp",
            halign="center",
            valign="middle"
        )
        self.question_label.bind(size=self.question_label.setter("text_size"))
        self.question_label.opacity = 1
        layout.add_widget(self.question_label)
        self.question_label.size_hint_y = 0.15
        btn_layout = BoxLayout(
            orientation='horizontal',
            spacing=60,
            size_hint=(.3, None),
            height=120,
            pos_hint={'center_x': 0.5}
        )
        
        yes_btn = MDRaisedButton(
            text="YES",
            font_name="Spartan-Medium",
            md_bg_color=get_color_from_hex("#4CAF50"),
            font_size="50sp",
            pos_hint={"center_x": 0.5},
            size_hint =(.8, None),
            height=dp(120),
        )
        no_btn = MDRaisedButton(
            text="NO",
            font_name="Spartan-Medium",
            md_bg_color=get_color_from_hex("#F44336"),
            font_size="50sp",
            pos_hint={"center_x": 0.5},
            
            size_hint =(.8, None),
            height=dp(120),
        )
        
        yes_btn.bind(on_release=self.on_yes)
        no_btn.bind(on_release=self.on_no)
        
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        layout.add_widget(btn_layout)
        btn_layout.size_hint_y = 0.15
        layout.add_widget(Widget(size_hint_y=0.35))
        
        self.add_widget(layout)

    def display_question(self):
        question = self.questions[self.question_index]
        anim_out = Animation(opacity=0, duration=0.2)
        anim_in = Animation(opacity=1, duration=0.2)

        def update_label(*_):
            self.question_label.text = question
            anim_in.start(self.question_label)

        anim_out.bind(on_complete=update_label)
        anim_out.start(self.question_label)

    def on_yes(self, *args):
        self.show_dialog()

    def on_no(self, *args):
        self.question_index += 1
        if self.question_index < len(self.questions):
            self.display_question()
        else:
            self.manager.current = guide_data[self.data]["screen"]

    def show_dialog(self):
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            size_hint_y=None,
            height=dp(150),
        )

        content.add_widget(Label(
            text="This may be a severe case. Do you want to call for emergency assistance?",
            color =get_color_from_hex("#7c0a0a"),
            font_name="Spartan-Medium",
            
            font_size="30sp",
            halign="center",
            valign="middle"
        ))

        button_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            padding=[dp(40), 0, dp(40), 0],
            size_hint_y=None,
            size_hint=(.3, None),
            pos_hint={'center_x': 0.85},
            height=dp(60),
        )

        button_box.add_widget(MDRaisedButton(
            text="Cancel",
            md_bg_color=get_color_from_hex("#7c0a0a"),
            font_size="16sp",
            pos_hint={"center_x": 0.5},
            size_hint =(.8, None),
            on_release=lambda x: self.dialog.dismiss()
        ))
        button_box.add_widget(MDRaisedButton(
            text="Continue",
            md_bg_color=get_color_from_hex("#7c0a0a"),
            font_size="16sp",
            pos_hint={"center_x": 0.5},
            size_hint =(.8, None),
            on_release=self.goto_severe_screen
        ))

        content.add_widget(button_box)

        self.dialog = MDDialog(
            type="custom",
            content_cls=content,
            size_hint=(0.6, None),
            height=dp(220),
            auto_dismiss=False,
        )
        self.dialog.open()

    def goto_severe_screen(self, *args):
        self.dialog.dismiss()
        screen = self.manager.get_screen("severe_screen")
        screen.set_background(guide_data[self.data]["severe_bg"])
        self.manager.current = "severe_screen"
        send_sms(self.data)

class SevereScreen(MDScreen):
    def set_background(self, image_path):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Image(
            source=image_path,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        ))
        float_layout = FloatLayout()
        float_layout.add_widget(MDFillRoundFlatButton(
            text="MAIN MENU",
            font_name="Spartan-SemiBold",
            font_size="40sp",
            md_bg_color=get_color_from_hex("#ead196"),
            text_color=get_color_from_hex("#7c0a0a"),
            size_hint=(None, None),
            size=(245, 80),
            pos_hint={"center_x": 0.5, "y": 0.05},
            on_release=self.goto_main
        ))

        self.add_widget(layout)
        self.add_widget(float_layout)

    def goto_main(self, *args):
        self.manager.current = "start"

class EmergencyScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = get_color_from_hex("#7c0a0a")

        layout = MDBoxLayout(orientation='vertical', padding=dp(38), spacing=dp(20))

        card = MDCard(
            orientation='vertical',
            size_hint=(1, 1),
            padding=[dp(200), dp(40), dp(200), dp(40)],
            md_bg_color=get_color_from_hex("#ead196"),
            radius=[30],
        )

        content = MDBoxLayout(orientation='vertical', spacing=dp(30))

        title = Label(
            text="EMERGENCY TYPE",
            font_name="Spartan-Black",
            font_size="100sp",
            halign="center",
            color=get_color_from_hex("#7c0a0a"),
            size_hint_y=None,
            height=dp(120),
        )
        grid = MDGridLayout(
            cols=2,
            spacing=dp(40),
            adaptive_height=True,
            size_hint_y=None,
        )
        grid.bind(minimum_height=grid.setter("height"))

    
                
        emergencies = [
            "Sprains and Strains", "Nosebleeds", "Laceration (Cut)",
            "Insect Bites", "Bruise / Contusion", "Fainting",
            "Burns (1st or 2nd)", "Choking (Partial)"
        ]

        for label in emergencies:
            btn = MDFillRoundFlatButton(
                text=label,
                font_name="Spartan-Medium",
                font_size="60sp",
                size_hint=(0.3, None),
                height=dp(150),
                md_bg_color=get_color_from_hex("#7c0a0a"),
                text_color=get_color_from_hex("#ead196"),
                pos_hint={"center_x": 0.5},
            )
            
            if label in guide_data:
                btn.bind(on_release=lambda x, key=label: self.set_emergency_and_go("triage", key))

            grid.add_widget(btn)

        back_btn = MDFillRoundFlatButton(
            text="<< BACK",
            font_name="Spartan-Medium",
            font_size="40sp",
            size_hint=(0.3, None),
            height=dp(80),
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.manager.transition_to('menu'),
            md_bg_color=get_color_from_hex("#555555"),
            text_color=[1, 1, 1, 1]
        )

        
        content.add_widget(title)
        content.add_widget(Widget(size_hint_y=None, height=dp(40)))  
        content.add_widget(Widget(size_hint_y=1))                     
        content.add_widget(grid)
        content.add_widget(Widget(size_hint_y=1))                     
        content.add_widget(Widget(size_hint_y=None, height=dp(20)))   
        content.add_widget(back_btn)
        content.add_widget(Widget(size_hint_y=None, height=dp(40)))   

        card.add_widget(content)
        layout.add_widget(card)
        self.add_widget(layout)
        
    def set_emergency_and_go(self, screen_name, emergency_key):
        self.manager.current_data = emergency_key
        self.manager.transition_to(screen_name)     
            


class EmergencyGuideScreen(MDScreen):

    def gpio_setup(self):
        GPIO.setmode(GPIO.BCM)
        for pin in RELAY_PINS.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)

    def activate_solenoid(self, key, duration=5):
        pin = RELAY_PINS.get(key)
        if pin is None:
            print(f"[ERROR] Unknown solenoid key: {key}")
            return

        print(f"[INFO] Activating {key} (GPIO {pin})")
        GPIO.output(pin, GPIO.LOW)
        snackbar_width = dp(800)
        snackbar_x = (Window.width - snackbar_width) / 2
        # Run Snackbar on main thread
        Clock.schedule_once(lambda dt: 
            Snackbar(
                text=f"[color=#7c0a0a]{key} Drawer Opened![/color]",
                bg_color=get_color_from_hex("#ead196"),
                font_size="30sp",
                size_hint_x=None,
                width=dp(800),  # or whatever wide value you want
                snackbar_x=snackbar_x,
                snackbar_y=f"{Window.height - dp(100)}dp",
                snackbar_animation_dir="Top",
                duration=2
            ).open(), 0)

        # Deactivate GPIO after duration
        Clock.schedule_once(lambda dt: GPIO.output(pin, GPIO.HIGH), duration)
    def on_leave(self, *args):
        GPIO.cleanup()
    def __init__(self, images,emergency_key, **kwargs):
        super().__init__(**kwargs)
        self.images = images
        self.index = 0
        self.emergency_key = emergency_key
        self.gpio_setup()    
        self.layout = FloatLayout()
        self.bg = Image(allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg)

        self.button_box = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(20),
            size_hint=(None, None),
            width=dp(3 * 120 + 2 * 40),  
            height=dp(100),
            pos_hint={"center_x": 0.5, "y": 0.05}
        )

        self.back_btn = MDFillRoundFlatButton(
            text="<< BACK",
            font_name="Spartan-Medium",
            font_size="40sp",
            width=dp(120),
            height=dp(100),
            pos_hint={"center_x": 0.5},
            on_release=self.prev_image
        )
        self.emergency_btn = MDFillRoundFlatButton(
            text="EMERGENCY",
            font_name="Spartan-Medium",
            font_size="40sp",
            width=dp(120),
            height=dp(100),
            pos_hint={"center_x": 0.5},
            md_bg_color=get_color_from_hex("#7c0a0a"),
            text_color=get_color_from_hex("#ead196"),
            on_release=self.trigger_emergency
        )
        self.next_btn = MDFillRoundFlatButton(
            text="NEXT >>",
            font_name="Spartan-Medium",
            font_size="40sp",
            width=dp(120),
            height=dp(100),
            pos_hint={"center_x": 0.5},
            on_release=self.next_image
        )

        self.layout.add_widget(self.button_box)
        self.add_widget(self.layout)

        self.update_image()
    def on_pre_enter(self):
        self.gpio_setup()
        self.index = 0
        self.update_image()
        if self.emergency_key:
            threading.Thread(target=self.activate_solenoid, args=(self.emergency_key,), daemon=True).start()
    def update_image(self):
        self.bg.source = self.images[self.index]
        self.update_buttons()
    def update_buttons(self):
        self.button_box.clear_widgets()

        if self.index == 0:
            # centered
            self.button_box.pos_hint = {"center_x": 0.5, "y": 0.05}
            self.button_box.add_widget(self.back_btn)
            self.button_box.add_widget(self.emergency_btn)
            self.button_box.add_widget(self.next_btn)
        else:
            
            self.button_box.pos_hint = {"center_x": 0.6, "y": 0.05}
            self.button_box.add_widget(self.emergency_btn)
            self.button_box.add_widget(self.back_btn)
            self.button_box.add_widget(self.next_btn)

    def next_image(self, *args):
        if self.index < len(self.images) - 1:
            self.index += 1
            self.update_image()
        
           
        else:
            
            self.manager.transition_to("menu")
            

    def prev_image(self, *args):
        if self.index > 0:
            self.index -= 1
            self.update_image()
        else:
            
            self.manager.transition_to("menu")

    def trigger_emergency(self, *args):
        print("[ALERT] Emergency triggered!")
        send_sms(self.emergency_key)

        
def send_sms(emergency):
    global number, location
    message = f"Emergency assistance requested for {emergency} at {location}"

    
    try:
        with serial.Serial("/dev/serial0", 9600, timeout=1) as ser:
            ser.write(b'AT+CMGF=1\r')
            time.sleep(0.5)
            ser.write(f'AT+CMGS="{number}"\r'.encode())
            time.sleep(0.5)
            ser.write(f'{message}\x1A'.encode())
            time.sleep(3)
    except Exception as e:
        print("SMS sending failed:", e)

class DrawerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "700"
        
        self.theme_cls.material_style = "M3"
        
        self.theme_cls.font_styles.update({
            "Black": ["Spartan-Black", 16, False, 0.15],
            "Bold": ["Spartan-Bold", 16, False, 0.15],
            "ExtraBold": ["Spartan-ExtraBold", 16, False, 0.15],
            "ExtraLight": ["Spartan-ExtraLight", 16, False, 0.15],
            "Light": ["Spartan-Light", 16, False, 0.15],
            "Medium": ["Spartan-Medium", 16, False, 0.15],
            "Regular": ["Spartan-Regular", 16, False, 0.15],
            "SemiBold": ["Spartan-SemiBold", 16, False, 0.15],
            "Thin": ["Spartan-Thin", 16, False, 0.15],
        })
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(EmergencyScreen(name='emergency'))
        sm.add_widget(TriageScreen(name='triage'))
        sm.add_widget(SevereScreen(name='severe_screen'))
        
        for data in guide_data.values():
            sm.add_widget(EmergencyGuideScreen(images=data["images"], name=data["screen"],emergency_key=data["key"]))

        def transition_to(self, target):
            self.transition = FadeTransition(duration=0.2)
            self.current = target
        sm.transition_to = transition_to.__get__(sm)

        return sm

if __name__ == '__main__':
    DrawerApp().run()
