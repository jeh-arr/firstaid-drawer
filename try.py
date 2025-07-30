from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.card import MDCard

# Register custom font
LabelBase.register(name="Spartan-Black", fn_regular="fonts/LeagueSpartan-Black.ttf")

KV = """
BoxLayout:
    orientation: "vertical"
    padding: "24dp"

    MDCard:
        orientation: "vertical"
        size_hint: None, None
        size: "300dp", "200dp"
        pos_hint: {"center_x": 0.5}
        elevation: 8
        padding: "12dp"
        id: card_container
"""

class TestApp(MDApp):
    def build(self):
        root = Builder.load_string(KV)

        custom_label = Label(
            text="FIRST AID",
            font_name="Spartan-Black",
            font_size="40sp",
            color=(0.49, 0.04, 0.04, 1),  # hex #7c0a0a
            halign="center",
        )
        root.ids.card_container.add_widget(custom_label)
        return root

TestApp().run()