import tkinter as tk

class Tooltip(tk.Tk):
    def __init__(self, count):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=5)
        self.label.pack()
        self.remaining = 0
        self.countdown(remaining=count)


    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

if __name__ == "__main__":
    app = Tooltip()
    #app.title("wm min/max")
   # app.resizable(0,0)
    def center_window(width=500, height=200, x=0, y=0):
        app.geometry('%dx%d+%d+%d' % (width, height, x, y))

    center_window(10, 10, 20, 20)
    app.overrideredirect(True)
    app.attributes("-topmost", True)
    app.mainloop()
