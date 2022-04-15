import sys
import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup

# get the values from nbp.pl
value = requests.get("https://api.nbp.pl/api/exchangerates/tables/a/?format=json")
initial_values = value.json()[0]
y = initial_values['rates']

short_currency = [b['code'] for b in y]
rate = [c['mid'] for c in y]
dict_rates = dict(zip(short_currency, rate))


class Exchange(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Label(text="Currency Conveter", pos_hint={'center_x': .5, 'center_y': .8},
                              size_hint=(.3, .8), font_size=40))

        self.text_inp = TextInput(pos_hint={'center_x': .25, 'center_y': .5},
                                  size_hint=(.2, .1), multiline=False,
                                  hint_text="Give value to convert")
        self.add_widget(self.text_inp)

        self.submit = Button(text="Submit", pos_hint={'center_x': .5, 'center_y': .3},
                             size_hint=(.25, .1), background_color=(.3, .6, .7, 1))
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

        self.from_value = Spinner(
            text='Result',
            values=short_currency,
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': .75, 'center_y': .65})
        self.add_widget(self.from_value)

        self.to_value = Spinner(
            text='Value to convert',
            values=short_currency,
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': .25, 'center_y': .65})
        self.add_widget(self.to_value)

        self.to_quit = Button(text="Close", pos_hint={'center_x': .8, 'center_y': .15},
                              size_hint=(.25, .1), background_color=(.3, .6, .7, 1))
        self.to_quit.bind(on_press=self.quit)
        self.add_widget(self.to_quit)

    def pressed(self, ar):
        from_currency = self.from_value.text
        final_currency = self.to_value.text
        text = self.text_inp
        print(type(text))
        if from_currency == final_currency:
            popup_same = Popup(title="The converted currency will be the same",
                               pos_hint={'center_x': .75, 'center_y': .5}, size_hint=(.25, .2))
            popup_same.open()
            self.text_inp.text = ""
        else:
            try:
                print("Convert", text.text, " ", from_currency, "to", final_currency)
                pop = Popup(title="Converted value is", pos_hint={'center_x': .75, 'center_y': .5}, size_hint=(.25, .2),
                            content=Label(text=str(self.perform())))
                pop.open()
                self.text_inp.text = ""
            except ValueError:
                popup = Popup(title="Given value is not a number",
                              pos_hint={'center_x': .75, 'center_y': .5}, size_hint=(.25, .2),)
                popup.open()
                self.text_inp.text = ""
            except KeyError:
                popup_cur = Popup(title="Give the currency", pos_hint={'center_x': .75, 'center_y': .5},
                                  size_hint=(.25, .2))
                popup_cur.open()
                self.text_inp.text = ""

    def perform(self):
        amount = float(self.text_inp.text)
        from_currency = self.from_value.text
        final_currency = self.to_value.text

        to_convert_value = amount/dict_rates[from_currency]
        return round(to_convert_value * dict_rates[final_currency], 4)

    def quit(self, ar):
        print("Closed button pressed")
        sys.exit()


class CurrencyExchange(App):
    def build(self):
        return Exchange()


if __name__ == '__main__':
    CurrencyExchange().run()
