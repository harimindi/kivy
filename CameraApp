# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 12:28:06 2018

@author: hxm90
"""

from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    
    Camera:
        id: camera
        resolution: (300, 300)
        play: True
        
    Button:
        text: "Click"
        size_hint: (.5, .2)
        pos_hint: {'x':.25, 'y':.75}
        on_press: root.onCameraClick()
''')

class CameraClick(BoxLayout):
    def onCameraClick(self, *args):
        camera = self.ids['camera']
        #camera.play = True
        camera.export_to_png("C:/Hari Docs/Kivy/pic.png")
        print("Captured")
        
class CameraApp(App):

    def build(self):
        return CameraClick()
    
CameraApp().run()
    
'''        layout = BoxLayout(orientation='vertical')
              
        #create camera object
        self.cameraObject = Camera(play=False)
        self.cameraObject.play = True
        self.cameraObject.resolution = (300,300)
      
        
        #create a button for taking photograph
        self.cameraClick = Button(text = "Click")
        self.cameraClick.size_hint = (.5, .2)
        self.cameraClick.pos_hint = {'x':.25, 'y':.75}
        
        #bind the buttons onPress to onClick
        
        self.cameraClick.bind(on_press=self.onCameraClick)
        
        #add camera and button to the layout
        f_layout.add_widget(self.cameraObject)
        f_layout.add_widget(self.cameraClick)
        
        return layout
    
    #Take the current frame of the video as the photograph
    def onCameraClick(self, *args):
        self.cameraObject.export_to_png("C:/Hari Docs/Kivy/pic.png")
        
#Start the camera app
if __name__=='__main__':
    CameraApp().run()'''
    
