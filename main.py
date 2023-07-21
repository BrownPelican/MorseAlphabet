import kivy
kivy.require('1.9.0')
import kivymd

from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.audio import SoundLoader
from kivy.utils import platform

from kivy.metrics import dp
from jnius import autoclass
#import android


import time

class MainApp(MDApp):

    alphabetToMorse ={"A": "._", "B": "_...", "C": "_._.", "D": "_..", "E": ".", "F": ".._.", "G": "__.", "H": "....",
                      "I": "..", "J": ".___", "K": "_._", "L": "._..", "M": "__", "N": "_.", "O": "___", "P": ".__.",
                      "Q": "__._", "R": "._.", "S": "...", "T": "_", "U": ".._", "V": "..._", "W": ".__ ", "X": "_.._",
                      "Y": "_.__", "Z": "__.."
    }

    morseToAlphabet = {v: k for k, v in alphabetToMorse.items()}

    dot = "."   #E
    dash = "_"  #T

    language = "./images/flag_germany.png"

    menu_text = []
    menu_text_de = ["Deutsch", "Englisch"]
    menu_text_en = ["German", "English"]
    title_text = ""
    title_text_de = "Morsen"
    title_text_en = "Morse-Alphabet"

    flat_button_text = []
    flat_button_text_de = ["Morse-Code", "Eingabe leeren"]
    flat_button_text_en = ["Morse-Code", "Clear"]

    nav_drawer_text = []
    nav_drawer_text_de = ["Home", "Einstellungen", "SOS", "Exit"]
    nav_drawer_text_en = ["Home", "Settings", "SOS", "Exit"]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = 0
        self.menu_text = self.menu_text_de
        self.title_text = self.title_text_de
        self.title = self.title_text
        self.flat_button_text = self.flat_button_text_de
        self.nav_drawer_text = self.nav_drawer_text_de

        self.theme_cls.primary_palette = "Blue"
        self.dotMP3 = SoundLoader.load('./sounds/dotmp3.mp3')
        self.dashMP3 = SoundLoader.load('./sounds/dashmp3.mp3')

        menu_items = [{"viewclass": "OneLineIconListItem",
                       "height": dp(56),
                       "text": self.menu_text[0],  # "Deutsch",
                       "on_release": lambda x="DE": self.menu_callback(x),
                       "IconLeftWidget": 'icon',
                       "icon": "./images/flag_germany.png"},
                      {"viewclass": "OneLineAvatarListItem",
                       "height": dp(56),
                       "text": self.menu_text[1],
                       "on_release": lambda x="EN": self.menu_callback(x),
                       "ImageLeftWidget": "icon",
                       "icon": "./images/flag_usa.png"
                       }
                      ]

        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

    def callback(self, button):
        print(button)
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        self.language = self.setLanguage(text_item)
        print(self.language)
        print(text_item)
        self.root.ids.button.icon = self.language
        if text_item == 'EN':
            self.root.ids.toolbar.title = self.title_text_en
            self.menu_text = self.menu_text_en
            self.flat_button_text = self.flat_button_text_en
            self.nav_drawer_text = self.nav_drawer_text_en
            self.state = 1
        else:
            self.root.ids.toolbar.title = self.title_text_de
            self.menu_text = self.menu_text_de
            self.flat_button_text = self.flat_button_text_de
            self.nav_drawer_text = self.nav_drawer_text_de
            self.state = 0

        self.root.ids.flat_button0.text = str(self.flat_button_text[0])
        self.root.ids.flat_button1.text = str(self.flat_button_text[1])
        self.root.ids.line_item0.text = self.nav_drawer_text[0]
        self.root.ids.line_item1.text = self.nav_drawer_text[1]
        self.root.ids.line_item2.text = self.nav_drawer_text[2]
        self.root.ids.line_item3.text = self.nav_drawer_text[3]

        self.menu_items = [{"viewclass": "OneLineIconListItem",
                       "height": dp(56),
                       "text": self.menu_text[0],  # "Deutsch",
                       "on_release": lambda x="DE": self.menu_callback(x),
                       "IconLeftWidget": 'icon',
                       "icon": "./images/flag_germany.png"},
                      {"viewclass": "OneLineAvatarListItem",
                       "height": dp(56),
                       "text": self.menu_text[1],
                       "on_release": lambda x="EN": self.menu_callback(x),
                       "ImageLeftWidget": "icon",
                       "icon": "./images/flag_usa.png"
                       }
                      ]

        self.menu = MDDropdownMenu(
            items=self.menu_items,
            width_mult=4,
        )

    def setLanguage(self, item):
        if item == "DE":
            self.language = "./images/flag_germany.png"
        elif item == "EN":
            self.language = "./images/flag_usa.png"
        return self.language

    def encode(self):
        output = ' '
        print(self.root.ids.text_input.text)
        for w in self.root.ids.text_input.text:
            if w == ' ':
                output = output + w
            elif w == '\n':
                continue
            else:
                output = output + self.alphabetToMorse[w.upper()]
                print(self.alphabetToMorse[w.upper()])

        self.root.ids.text_output.text = output

    def clearInput(self):
        self.root.ids.text_input.text = ''
        self.root.ids.text_output.text = ''

    def playSound(self):
        print(self.root.ids.text_output.text)
        for e in self.root.ids.text_output.text:
            if e == self.dot:
                self.dotMP3.play()
            else:
                self.dashMP3.play()
            time.sleep(0.5)

    def useFlashlight(self):
        print('Light')
        if platform == 'android' or platform == 'ios':
            from android.permissions import request_permissions, Permission
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")
                else:
                    print("Did not get all permissions")

            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.CAMERA, Permission.FLASHLIGHT], callback())

        # is flashlight available?
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        PackageManager = autoclass('android.content.pm.PackageManager')
        pm = PythonActivity.mActivity.getPackageManager()
        flash_available = pm.hasSystemFeature(PackageManager.FEATURE_CAMERA_FLASH)


        # if yes -> turn it on - if no -show unavailable message
        if flash_available:
            Camera = autoclass('android.hardware.Camera')
            CameraParameters = autoclass('android.hardware.Camera$Parameters')
            cam = Camera.open()
            for e in self.root.ids.text_output.text:

                if e == self.dot:
                    self.lightOn(cam, CameraParameters)
                    print("0.5")
                    time.sleep(0.5)
                    self.lightOff(cam)
                elif e == self.dash:
                    self.lightOn(cam)
                    print("1.0")
                    time.sleep(1.0)
                    self.lightOff(cam)
                else:
                    continue


    def lightOn(self, cam, CameraParameters):
        print("Light On")

        params = cam.getParameters()
        params.setFlashMode(CameraParameters.FLASH_MODE_TORCH)
        cam.setParameters(params)
        cam.startPreview()

    def lightOff(self, cam):
        print("Light Off")
        cam.stopPreview()
        cam.release()

    def setSOS(self):
        self.root.ids.text_input.text = "SOS"
        self.root.ids.text_output.text = "...___..."

    def quit(self):
        MainApp().stop()

if __name__ == '__main__':
    MainApp().run()
