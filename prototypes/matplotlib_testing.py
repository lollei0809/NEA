from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
import tkinter_page as tk
from tkinter_page import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = {'padx': 10, 'pady': 10}
        self.title("app")
        self.menu_frame = Menu(self)
        self.graph_frame = Graph(self)

        self.pack_frames()

    def pack_frames(self):
        self.menu_frame.pack()

    def show(self):
        self.menu_frame.pack_forget()
        self.graph_frame.pack()
    def back_to_menu(self):
        self.graph_frame.pack_forget()
        self.menu_frame.pack()

class Menu(tk.Frame):

    def __init__(self,app):
        super().__init__()
        self.settings = {'padx': 10, 'pady': 10}
        self.app=app

        self.show_btn = tk.Button(self,
                                     text="show",
                                     command=self.show_clicked)
        self.show_btn.config(bg="red")


        self.password = tk.StringVar()
        self.password_entry = tk.Entry(width=25, textvariable=self.password)

        self.username_dropdown = ttk.Combobox(values=["albert", "jenny", "lilly", "lolly", "kiran"], )
        self.username_dropdown["state"] = "readonly"

        self.username_text = tk.Label(self, text="username")

        self.password_text =tk.Label(self, text="password")


        self.place_widgets()

    def place_widgets(self):
        global settings
        self.username_dropdown.pack(side="right")
        self.username_text.pack(side="left")
        self.password_text.pack(side="left")
        self.password_entry.pack(side="right")
        self.show_btn.pack(side="bottom")


    def show_clicked(self):
        #validate password from database then
        self.app.graph_frame.show_bar()


class Graph(tk.Frame):
    def __init__(self, app):
        super().__init__()
        self.settings = {'padx': 10, 'pady': 10}
        self.app = app
    def show_bar(self):
        fig = Figure(figsize=(5, 5),
                     dpi=100)
        y = [i ** 2 for i in range(101)]
        plot1 = fig.add_subplot(111)
        plot1.plot(y)
        canvas = FigureCanvasTkAgg(fig,
                                   master=app1)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,
                                       app1)
        toolbar.update()
        canvas.get_tk_widget().pack()
        """
        x = np.arange(5)#[0,1,2,3,4]
        y1 = [34, 56, 12, 73, 67]
        y2 = [12, 64, 78, 45, 50]
        y3 = [74, 23, 45, 25, 89]
        width = 0.2

        plt.bar(x - 0.2, y1, width, color='blue')#x-0.2=[- position of bars on x axis
        plt.bar(x, y2, width, color='red')
        plt.bar(x + 0.2, y3, width, color='yellow')
        plt.xticks(x, ['albert', 'jenny', 'lilly', 'lolly', 'kiran'])
        plt.ylabel("Scores")
        plt.legend(["logical shifts", "normalisation", "two's compliment"])
    """
if __name__ == '__main__':
    app1 = App()
    app1.mainloop()



