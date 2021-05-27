"""

    File name: userInput
    Author: Ömer Ünal
    Date created: 27/05/2021
    Python Version: 3.9

"""

import tkinter as tk


class UserInput(tk.Entry):
    def __init__(self, label, is_work, placeholder="PLACEHOLDER", color='white'):
        super().__init__()

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.bind('<Return>', self.get_text)
        self.time = 0
        self.label = label
        self.is_work = is_work

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

    def get_text(self, *args):
        try:
            self.time = int(self.get())
            self.disable()
            if self.is_work:
                self.label.config(text=f"Work:{self.time}m")
            else:
                self.label.config(text=f"  Break:{self.time}m")
        except ValueError:
            pass

    def get_time(self):
        return self.time

    def disable(self):
        self.config(state='disabled')

    def enable(self):
        self.config(state='normal')
