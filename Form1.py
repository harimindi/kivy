import kivy
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.core.window import Window
#Window.size = (400,130)
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

Builder.load_string('''
<MyWidget>:
    #canvas:
        #Color: 
            #rgba: (.5, 0.5, 0.5, 1)
        #Rectangle:
         #   pos: self.pos
          #  size: self.size
    
    RelativeLayout:

        TextInput:
            #size: 400, 50
            pos: 400, 50
            #text: root.help_message
            background: 1., 1., 1., 1.
            font_size: 14
            multiline: False

        Label:
            background_color:
            canvas.before:
                Color:
                    rgba: 0.5,0.5,0.5,1
                Rectangle:
                    pos: self.pos
                    size: self.size
            size: 300, 50
            #size_hint: (None, None)
            #pos_hint: {'x':.4, 'y':.4}
            text: 'First Name'
            text_size: root.width, None
            pos: 30, 50
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
