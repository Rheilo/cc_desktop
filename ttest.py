import tkinter as tk
class Gui(object):
    def __init__(self, counter):
        self.root = tk.Tk()
        self.counter = counter
        self.ivar = tk.IntVar()
        self.ivar.set(counter)
        self.label = tk.Label(textvariable=self.ivar, width=2, font=('ARIAL', 200, 'bold'))
        self.label.pack()
        self.count()
    def count(self, speed=1000):
        self.counter -= 1
        if self.counter >= 0:
            self.ivar.set(self.counter)
            self.root.after(speed, self.count)     
        else:
            self.root.quit()
    def run(self):
        self.root.mainloop()
Gui(12).run()