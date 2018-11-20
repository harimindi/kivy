import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
#from kivy.uix.label import Label
#from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from KivyCalendar import DatePicker
from kivy.uix.screenmanager import ScreenManager, Screen

class ScreenManagement(ScreenManager):
    pass

class MainScreen(Screen):
    #from kivy.properties import ObjectProperty
    #theTxt = ObjectProperty(None)
    def build(self):
        kivy = Builder.load_file('Form1.kv')
        return kivy
    
    def show_calendar(self):
        datePicker = CustomDatePicker()
        datePicker.show_popup(1, .3)
        
class IDScreen(Screen):
    pass

class CustomDatePicker(DatePicker):

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = "%s.%s.%s" % tuple(self.cal.active_date)
        self.focus = False
        App.get_running_app().root.ids.txt_DOB.text = self.text

#kivy = Builder.load_file("Form1.kv")
class Form1(App):
    def build(self):
        #self.root = Builder.loadfile('C:/Hari Docs/Kivy/programs/Form1.kv')
        #return self.root
        return MainScreen()
if __name__=='__main__':
    
    Form1().run()
