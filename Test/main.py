from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.font_definitions import fonts
from kivymd.icon_definitions import md_icons
from kivy.metrics import dp
from DBconnection import *
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from Word import *

Window.maximize()

def calc(s,a):
    if a == 0:
        return 0
    else:
        return ((a/s) * 100)

class Tab(MDFloatLayout, MDTabsBase):
    pass

class ItemTable(BoxLayout):
    id = StringProperty()
    inicials = StringProperty()
    status = StringProperty()
    service = StringProperty()
    adress = StringProperty()
    color = ListProperty()

class MainScreen(Screen,BoxLayout,GridLayout):

    def draw_ellipse(self, wid):
        data = DBconn().SelectFromClients()
        lastdata = []
        dontKnow = 0
        measurement = 0
        conclusion_contract = 0
        upfront_payment = 0
        full_payment = 0

        for i in data:
            lastdata.append(i)

        for i in range(len(lastdata)):
            if lastdata[i][2] == 'Неопределился':
                dontKnow += 1;
            elif lastdata[i][2] == 'Замер':
                measurement += 1
            elif lastdata[i][2] == 'Заключение договора':
                conclusion_contract += 1
            elif lastdata[i][2] == 'Внёс предоплату':
                upfront_payment += 1
            elif lastdata[i][2] == 'Полностью заплатил':
                full_payment += 1

        all_count = dontKnow + measurement + conclusion_contract + upfront_payment + full_payment
        dontKnow_chart = calc(all_count, dontKnow)
        measurement_chart = calc(all_count, measurement)
        conclusion_contract_chart = calc(all_count, conclusion_contract)
        upfront_payment_chart = calc(all_count, upfront_payment)
        full_payment_chart = calc(all_count, full_payment)

        labels = 'Неопределился', 'Замер', 'Заключение Договора', 'Предоплата', 'Полностью оплатил'
        sizes = [int(dontKnow_chart), int(measurement_chart), int(conclusion_contract_chart), int(upfront_payment_chart), int(full_payment_chart)]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')

        wid.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def update_ellipse(self,wid):
        wid.clear_widgets()
        self.draw_ellipse(wid)

    def Create_Word(self, id, name, path):

        data = DBconn().SelectFromClients()
        lastdata = []
        item = None

        for i in data:
            lastdata.append(i)

        for i in lastdata:
            if str(i[0]) == id:
                item = i

        text = f'{item[1]} купил у нас  +  в количестве 100 на сумму 100000'

        CreateWordDocument(text,path,name)




class BigTableScreen(Screen):
    pass




class LoginScreen(Screen):
    dialog = None

    def show_access_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text='Доступ запрещён',
                buttons=[MDFlatButton(text='Закрыть', on_release=self.close_dialog)]
            )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):

    connector = DBconn()

    data1 = connector.SelectFromServices()
    _data = connector.SelectFromUsers()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file("style.kv")
        menu_items = [
            {
                'icon': 'format-list-checkbox',
                'text': f"{i}",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.set_serv(x),
            } for i in self.data1
        ]

        data = self.connector.SelectFromStatus()
        dataStatus = []

        for i in data:
            dataStatus.append(i[1])

        menu_items_status=[
            {
                'icon': 'adjust',
                'text': f"{i}",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.set_stat(x),
            } for i in dataStatus
        ]

        self.menu_status = MDDropdownMenu(
            caller = self.screen.main.ids.status,
            items = menu_items_status,
            position="auto",
            width_mult=6
        )

        self.menu_service = MDDropdownMenu(
            caller=self.screen.main.ids.services,
            items=menu_items,
            position="auto",
            width_mult=6
        )
        self.menu_service.bind(on_release=self.set_serv)
        self.menu_status.bind(on_release=self.set_stat)


    def set_serv(self, menu ,menu_item):
        def set_item(interval):
            self.screen.main.ids.services.text = menu_item.text
            menu.dismiss()

        Clock.schedule_once(set_item, 0.5)


    def set_stat(self, menu ,menu_item):
        def set_item(interval):
            self.screen.main.ids.status.text = menu_item.text
            menu.dismiss()

        Clock.schedule_once(set_item, 0.5)

    def on_start(self):
        item_tabs = {
            'Добавление Клиента': 'account-multiple-plus',
            'Таблица Клиентов': 'table-account',
            'Статистика': 'google-analytics',
            'Настройки': 'cog'
        }

        data = self.connector.SelectFromClients()

        self.screen.main.ids.table_list.add_widget(
            ItemTable(
                color=(0.2,0.2,0.2,0.2),
                id=str('ID'),
                inicials=str('Инициалы'),
                status=str('Статус'),
                service=str('Услуга'),
                adress=str('Адресс')
            )
        )

        for i in range(len(data)):
            row_color = (0.2,0.2,0.2,0.2)

            self.screen.main.ids.table_list.add_widget(
                ItemTable(
                    color = row_color,
                    id = str(data[i][0]),
                    inicials = str(data[i][1]),
                    status = str(data[i][2]),
                    service = str(data[i][3]),
                    adress = str(data[i][4])
                )
            )




    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        pass

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return self.screen

    def ResetTable(self):
        self.screen.main.ids.table_list.clear_widgets()
        self.screen.main.ids.table_list.add_widget(
            ItemTable(
                color=(0.2, 0.2, 0.2, 0.2),
                id=str('ID'),
                inicials=str('Инициалы'),
                status=str('Статус'),
                service=str('Услуга'),
                adress=str('Адресс')
            )
        )

        data = self.connector.SelectFromClients()

        for i in range(len(data)):
            row_color = (0.2,0.2,0.2,0.2)

            self.screen.main.ids.table_list.add_widget(
                ItemTable(
                    color = row_color,
                    id = str(data[i][0]),
                    inicials = str(data[i][1]),
                    status = str(data[i][2]),
                    service = str(data[i][3]),
                    adress = str(data[i][4])
                )
            )

    searchingItems = []

    def checkbox_click(self, instance, value, topping):
        if value == True:
            self.searchingItems.append(topping)
        else:
            self.searchingItems.remove(topping)

    def search(self, data, inicialls, status, service, adress):

        startTableClients = self.connector.SelectFromClients()
        lastTableClients = []
        searchingItems = []

        for i in startTableClients:
            lastTableClients.append(i)

        if 'Инициалы' in data:
            if 'Статус' in data:
                if 'Услуга' in data:
                    if 'Адрес' in data:

                        for i in lastTableClients:
                            if inicialls == i[1] and status == i[2] and service == i[3] and adress == i[4]:
                                searchingItems.append(i)

                    else:

                        for i in lastTableClients:
                            if inicialls == i[1] and status == i[2] and service == i[3]:
                                searchingItems.append(i)

                elif 'Адрес' in data:

                    for i in lastTableClients:
                        if inicialls == i[1] and status == i[2] and adress == i[4]:
                            searchingItems.append(i)

                else:

                    for i in lastTableClients:
                        if inicialls == i[1] and status == i[2]:
                            searchingItems.append(i)

            elif 'Услуга' in data:
                if 'Адрес' in data:

                    for i in lastTableClients:
                        if inicialls == i[1] and service == i[3] and adress == i[4]:
                            searchingItems.append(i)

                else:

                    for i in lastTableClients:
                        if inicialls == i[1] and service == i[3]:
                            searchingItems.append(i)

            elif 'Адрес' in data:

                for i in lastTableClients:
                    if inicialls == i[1] and adress == i[4]:
                        searchingItems.append(i)

            else:

                for i in lastTableClients:
                    if inicialls == i[1]:
                        searchingItems.append(i)

        elif 'Статус' in data:
            if 'Услуга' in data:
                if 'Адрес' in data:

                    for i in lastTableClients:
                        if status == i[2] and service == i[3] and adress == i[4]:
                            searchingItems.append(i)

                else:

                    for i in lastTableClients:
                        if status == i[2] and service == i[3]:
                            searchingItems.append(i)

            elif 'Адрес' in data:

                for i in lastTableClients:
                    if status == i[2] and adress == i[4]:
                        searchingItems.append(i)

            else:

                for i in lastTableClients:
                    if status == i[2]:
                        searchingItems.append(i)

        elif 'Услуга' in data:
            if 'Адрес' in data:

                for i in lastTableClients:
                    if service == i[3] and adress == i[4]:
                        searchingItems.append(i)

            else:

                for i in lastTableClients:
                    if service == i[3]:
                        searchingItems.append(i)

        elif 'Адрес' in data:

            for i in lastTableClients:
                if adress == i[4]:
                    searchingItems.append(i)

        else:

            for i in lastTableClients:
                if inicialls == i[1]:
                    searchingItems.append(i)

        self.screen.main.ids.table_list.clear_widgets()
        self.screen.main.ids.table_list.add_widget(
            ItemTable(
                color=(0.2, 0.2, 0.2, 0.2),
                id=str('ID'),
                inicials=str('Инициалы'),
                status=str('Статус'),
                service=str('Услуга'),
                adress=str('Адресс')
            )
        )

        for i in range(len(searchingItems)):
            row_color = (0.2, 0.2, 0.2, 0.2)

            self.screen.main.ids.table_list.add_widget(
                ItemTable(
                    color=row_color,
                    id=str(searchingItems[i][0]),
                    inicials=str(searchingItems[i][1]),
                    status=str(searchingItems[i][2]),
                    service=str(searchingItems[i][3]),
                    adress=str(searchingItems[i][4])
                )
            )





if __name__ == "__main__":
    MainApp().run()
