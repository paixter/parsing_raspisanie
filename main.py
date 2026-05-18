from kivy.config import Config
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '300')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

import requests
import xlrd
import urllib

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

try:
    
    link = 'https://sutd.ru/upload/raspisanie/raspisanie_o_iita_1_25_26.xlsx'  #<---------
    file_name, headers = urllib.request.urlretrieve(link)
    workbook = xlrd.open_workbook(file_name)
    sheet = workbook.sheet_by_index(0)

    lessons = []
    for i in range(sheet.nrows):
        row = sheet.cell_value(i,3)
        if row == "1-МД-35":                                              #<---------
            lessons.append(sheet.row_values(i))
            if type(lessons[-1][-1]) is float:
                lessons[-1][-1] = str(int(lessons[-1][-1]))
        elif lessons != []:
            break
    
except Exception as e:
    lessons = e
    
class RaspisanieScreen(Screen):
    
    def __init__(self, **kwargs):
        super(RaspisanieScreen, self).__init__(**kwargs)

        #MainLayout
        MainLayout = FloatLayout()
        
        label = Label(text = "Расписание",
                      pos_hint = {"left": 1, "top": 1},
                      size_hint = (1, 0.07),
                      text_size = Window.size,
                      halign = 'left',
                      valign = 'middle')
        MainLayout.add_widget(label)

        button = Button(text = "...",
                        pos_hint = {"right": 1, "top": 1},
                        size_hint = (Window.height / Window.width * 0.07, 0.07),
                        on_press = self.callback)
        MainLayout.add_widget(button)

            #ScrollLayout
        ScrollLayout = BoxLayout(orientation = "vertical",
                                 spacing = Window.height * 0.05,
                                 size_hint_y = None)
        ScrollLayout.bind(minimum_height = ScrollLayout.setter('height'))

        ScrollLayout.add_widget(Widget())
        
        for i in ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота"]:
            
            day = Label(text = "--"+i+"--",
                        color = [0.5, 0.5, 0.5, 1],
                        text_size = Window.size,
                        halign = 'left',
                        valign = 'middle')
            ScrollLayout.add_widget(day)

            if lessons == []:
                    break

            while lessons[0][9] == i:
                LessonLayout = BoxLayout(orientation = "vertical",
                                         pos_hint = {"right": 1},
                                         size_hint = (0.9, None))
                LessonLayout.bind(minimum_height = LessonLayout.setter('height'))

                for j in [11, 10, 6, 5, 13, 12]:
                    lesson = Label(text = lessons[0][j],
                                   color = [0.5, 0.5, 0.5, 1],
                                   size_hint_y = None,
                                   halign = 'left',
                                   valign = 'middle')
                    lesson.bind(width = lambda s, w: s.setter('text_size')(s, (w, None)))
                    lesson.bind(texture_size = lesson.setter('size'))
                    LessonLayout.add_widget(lesson)

                ScrollLayout.add_widget(LessonLayout)
                
                lessons.pop(0)
                if lessons == []:
                    break

        ScrollLayout.add_widget(Widget())
        
            #scroll
        scroll = ScrollView(pos_hint = {"top": 0.93},
                            height = Window.height*0.93,
                            size_hint_y = None)
        
        '''
        scroll.bind(pos=self.update_rect, size = self.update_rect)
        with scroll.canvas.before:
            Color(0, 1, 0, 1)
            self.rect = Rectangle(size = scroll.size,
                                  pos = scroll.pos)
        '''

        scroll.add_widget(ScrollLayout)
        MainLayout.add_widget(scroll)
        
        self.add_widget(MainLayout)

    '''
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    '''
    
    def callback(self, instance):
        self.manager.transition.direction = 'down'
        self.manager.current = 'settings'
        
class SettingsScreen(Screen):
    
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        #MainLayout
        MainLayout = FloatLayout()
        
        label = Label(text = "Настройки",
                      pos_hint = {"left": 1, "top": 1},
                      size_hint = (1, 0.07),
                      text_size = Window.size,
                      halign = 'left',
                      valign = 'middle')
        MainLayout.add_widget(label)

        button = Button(text = "...",
                        pos_hint = {"right": 1, "top": 1},
                        size_hint = (Window.height / Window.width * 0.07, 0.07),
                        on_press = self.callback)
        MainLayout.add_widget(button)

        #SettingLayout
        SettingLayout = BoxLayout(orientation = "vertical",
                                  pos_hint = {"top": 0.93},
                                  size_hint_y = None)

        label = Label(text = "Ссылка на файл:",
                      color = (0.5, 0.5, 0.5, 1),
                      text_size = Window.size,
                      height = Window.height * 0.07,
                      size_hint = (1, None),
                      halign = 'left',
                      valign = 'middle')
        SettingLayout.add_widget(label)

        link_input = TextInput(text = "https://sutd.ru/upload/raspisanie/2pl/raspisanie_o_iita_2_25_26.xlsx",  #<---------
                               height = Window.height * 0.07,
                               pos_hint = {"top": 1},
                               size_hint_y = None,
                               multiline = False)
        SettingLayout.add_widget(link_input)

        label = Label(text = "Выбор группы:",
                      color = (0.75, 0.75, 0.75, 1),
                      text_size = Window.size,
                      height = Window.height * 0.07,
                      size_hint = (1, None),
                      halign = 'left',
                      valign = 'middle')
        SettingLayout.add_widget(label)

        MainLayout.add_widget(SettingLayout)

        self.add_widget(MainLayout)

    def callback(self, instance):
        self.manager.transition.direction = 'up'
        self.manager.current = 'raspisanie'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(RaspisanieScreen(name = 'raspisanie'))
        sm.add_widget(SettingsScreen(name = 'settings'))
        return sm

if __name__ == "__main__":
    MyApp().run()
