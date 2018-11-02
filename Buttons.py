# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 13:47:09 2018

@author: hxm90
"""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
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
    canvas.before:
        Color:
            rgba:0.161, 0.561, 0.761,1
        Rectangle:
            pos: self.pos
            size: self.size
    Button:
        text: "START"
        pos_hint: {'x':.1, 'y':.1}
    Button:
        text: "STOP"
        pos_hint: {'x':.6, 'y':.1}
''')

class Layout(FloatLayout):
    pass

class myKivy(App):
    def build(self):
        
        return Layout()

if __name__=='__main__':
    myKivy().run()
