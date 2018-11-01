from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder

Builder.load_string('''
<Button>:
    canvas.before:
        Color:
            rgba:0,0,255,0.8
        Line:
            width: 6
            rectangle: self.x, self.y, self.width, self.height
        #Rectangle:
         #   pos: self.pos
          #  size: self.size
    background_normal: ''
    background_color: 0,0,255,0.8
    font_size: 40
    color: 1,1,1,1
    size_hint: 0.3, 0.1
    #border: 10,10,10,10    
<Layout>:
    Button:
        text: "FIRST"
        pos_hint: {'x':.1, 'y':.1}
    
    Button:
        text: "SECOND"
        pos_hint: {'x':.6, 'y':.1}
''')

class Layout(FloatLayout):
    pass

    
class myKivy(App):
    def build(self):
        return Layout()
    
if __name__=='__main__':
    myKivy().run()
