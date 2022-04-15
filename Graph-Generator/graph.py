"""
Application built from a  .kv file
==================================

After Kivy instantiates a subclass of App, it implicitly searches for a .kv
file. The file plots.kv is selected because the name of the subclass of App is
PlotsApp.
"""

import sys
sys.argv[1:] = []
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from sympy import *
import seaborn as sns

# Set the grid to plot
sns.set()
sns.set_style("whitegrid", {'grid.linestyle': '--'})


class MyLayout(Widget):
    """ MyLayout is the class that will show the plot after submitting with button.
        It will set legend to the plot if checkbox active."""

    def update_graph(self):
        """ Get the user input and generate plot from given formula. It accepts multiple expressions divided by ';'."""
        expression = self.function.text
        try:
            # multiple plots
            if ';' in expression:
                tmp = expression.split(';')
                p = plot(tmp[0], show=False, size=(4, 3), title=self.title.text, xlabel=self.name_x.text,
                         ylabel=self.name_y.text, xlim=self.set_xrange(), ylim=self.set_yrange(),
                         legend=self.check.active)
                for i in tmp[1:]:
                    p1 = plot(i, show=False, line_color=random.choice(['g', 'r']))
                    p.extend(p1)
                p.show()
            # single plot
            else:
                plot(expression, size=(4, 3), title=self.title.text, xlabel=self.name_x.text,
                         ylabel=self.name_y.text, xlim=self.set_xrange(), ylim=self.set_yrange(),
                         legend=self.check.active)
        except:
            # string expressions are not acceptable
            popup_same = Popup(title="Warning", pos_hint={'center_x': .75, 'center_y': .5},
                               size_hint=(.25, .2), content=Label(text="Wrong input"))
            popup_same.open()

    def set_xrange(self):
        """Change the range of x-axis to given numbers"""
        min_x = self.min_x.text
        max_x = self.max_x.text
        if min_x != "" and max_x != "":
            return int(min_x), int(max_x)
        else:
            return None

    def set_yrange(self):
        """Change the range of y-axis to given numbers"""
        min_y = self.min_x.text
        max_y = self.max_x.text
        if min_y != "" and max_y != "":
            return int(min_y), int(max_y)
        else:
            return None

    def check_legend(self, instance, value):
        """Get the status of checkbox"""
        return value

    def sub_btn(self):
        """Activate graph generation"""
        print("submit pressed")
        self.update_graph()

    def quit(self):
        """Close the app"""
        sys.exit()


class PlotsApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    PlotsApp().run()
