import kivy
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.core.window import Window
#Window.size = (400,130)
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

#MyLayout
class MyWidget(Widget):
    #from kivy.properties import ObjectProperty
    #theTxt = ObjectProperty(None)
    def build(self):
        kivy = Builder.loadfile('C:\Hari Docs\Kivy\programs\Form1.kv')
        return kivy
 #   pass   
class Form1(App):
    def build(self):
        #self.root = Builder.loadfile('C:/Hari Docs/Kivy/programs/Form1.kv')
        #return self.root
        return MyWidget()
if __name__=='__main__':
    Form1().run()
