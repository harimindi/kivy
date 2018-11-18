import kivy
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from KivyCalendar import DatePicker
from kivy.uix.popup import Popup
#MyLayout
class MyWidget(Widget):
    #from kivy.properties import ObjectProperty
    #theTxt = ObjectProperty(None)
    def build(self):
        kivy = Builder.loadfile('Form1.kv')
        return kivy
    
    def show_calendar(self):
        datePicker = CustomDatePicker()
        datePicker.show_popup(1, .3)

class CustomDatePicker(DatePicker):

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = "%s.%s.%s" % tuple(self.cal.active_date)
        self.focus = False
        App.get_running_app().root.ids.txt_DOB.text = self.text

 
class Form1(App):
    def build(self):
        #self.root = Builder.loadfile('C:/Hari Docs/Kivy/programs/Form1.kv')
        #return self.root
        return MyWidget()
if __name__=='__main__':
    
    Form1().run()
