# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 14:12:13 2018

@author: hxm90
"""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from kivy.lang.builder import Builder

Builder.load_string('''
<Button>:

    #background_normal: ''
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: (0.733, 0.145, 0.145,1) if self.state=='normal' else (0,.7,.7,1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]
    #background_color: 0.733, 0.145, 0.145,1.8
    font_size: 40
    color: 1,1,1,1
    size_hint: 0.3, 0.1

<Layout>:
        
    #canvas.before:
     #   Color:
      #      rgba:0.161, 0.561, 0.761,1
       # Rectangle:
        #    pos: self.pos
         #   size: self.size
    Camera:
        id: camera
        resolution: (300, 300)
        play: True
    
    Button:
        id: blink
        text: "Blink"
        pos_hint: {'x':.1, 'y':.1}
    Button:
        id: next
        text: "Next"
        pos_hint: {'x':.6, 'y':.1}
''')

class Layout(FloatLayout):
    def onCameraClick(self, *args):
        blink = self.ids['blink']
        blink
        camera = self.ids['camera']
        camera.export_to_png("C:/Hari Docs/Kivy/pic.png")
        print('Picure Taken')

class myKivy(App):
    def build(self):
        
        return Layout()

if __name__=='__main__':
    myKivy().run()
