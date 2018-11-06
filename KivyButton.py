from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from kivy.lang.builder import Builder

Builder.load_string('''
<Button>:
    background_normal: ''
    #background_color: 1,1,1,1
    canvas.before:
        Color:
            rgba: (1,1,1,1) 
            #if self.state=='normal' else (0,.7,.7,1)
        Line:
            width: 2
            rectangle: self.x, self.y, self.width, self.height
        #RoundedRectangle:
            #pos: self.pos
            #size: self.size
            #radius: [40,]
    background_color: (0.05,0.5,0.8,1)
    font_size: 40
    color: 1,1,1,1
    size_hint: 0.3, 0.1
<Layout>:
        
    canvas.before:
        Color:
            rgba:0.05, 0.5, 0.8,1
        Rectangle:
            pos: self.pos
            size: self.size
    
    Button:
        id: blink
        text: "Blink"
        pos_hint: {'x':.1, 'y':.1}
        on_press: root.onButtonClick()
''')
class Layout(FloatLayout):
    def onButtonClick(self, *args):
        #btn = self.ids['blink']
        #btn.background_color = (1,1,1,1)
        return

class KivyButton(App):
    def build(self):
        
        return Layout()

if __name__=='__main__':
    KivyButton().run()
