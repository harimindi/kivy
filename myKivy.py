# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 13:47:09 2018

@author: hxm90
"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

Builder.load_string('''
<myKivy>:
    FloatLayout:
        orientation: 'vertical'
    
        b1:
            text: "START"
            pos: (200, 200)
            size_hint: (.1, .1)
        
        b2:
            text: "STOP"
            pos: (200,100)
            size_hint: (.1, .1)
''')
    
class Container(FloatLayout):
    b1 = Button()
    b2 = Button()


class myKivy(App):
    def build(self):
        self.title = "Kivy App"
        return Container()

if __name__=='__main__':
    myKivy().run()
