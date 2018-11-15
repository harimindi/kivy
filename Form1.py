import kivy
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.core.window import Window
#Window.size = (400,130)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

Builder.load_string('''
<MyWidget>:
    canvas:
        Color: 
            rgba: (.5, 0.5, 0.93, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    
    TextInput:
        size: 130, 30
        pos: 70, 30
        #text: root.help_message
        background: 1., 1., 1., 1.
        font_size: 14
        multiline: False

    Label:
        canvas.before:
            Color:
                rgba: 1,1,1,1
        size: 200, 30
        text: 'First Name'
        pos: 0, 80
        color: 1,1,1,1
        font_size: 14

''')
#MyLayout
class MyWidget(Widget):
    #from kivy.properties import ObjectProperty
    #theTxt = ObjectProperty(None)
    pass
   
class MyApp(App):
    def build(self):
        #self.root = Builder.loadfile('Simple.kv')
        #return self.root
        return MyWidget()
if __name__=='__main__':
    MyApp().run()
