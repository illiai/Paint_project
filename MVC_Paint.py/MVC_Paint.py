from tkinter import *
from tkinter import filedialog
from PIL import ImageGrab

default_color = "black"
default_brush_size = 2

colors = ['white', 'tan1', 'lavender', 'lightcyan', 'azure', 'chartreuse2', 'greenyellow', 'lightyellow', 'navajowhite', 'bisque', 'peachpuff', 'pink',
          'gray30', 'darkorange1', 'mediumpurple', 'cyan', 'royalblue1', 'green3', 'yellowgreen', 'yellow', 'orange', 'coral', 'indianred1', 'hotpink',
          'black', 'darkorange4', 'purple', 'cyan3', 'blue2', 'darkgreen', 'olivedrab', 'gold', 'darkorange', 'red', 'indianred4', 'deeppink']


class PaintModel(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self._brush_size = IntVar()
        self._brush_size.set(5)
        self.canv = Canvas(self, bg="white")
        self.old_x: int = None
        self.old_y: int = None

    def setCursor(self, place):
        pass

    def set_color(self, new_color):
        self.color = new_color

    def set_brush_size(self):
        self.brush_size = int(self._brush_size.get())

    def draw_point(self, event):
        self.canv.create_oval(event.x - self.brush_size / 2,
                              event.y - self.brush_size / 2,
                              event.x + self.brush_size / 2,
                              event.y + self.brush_size / 2,
                              fill=self.color, outline=self.color)

    def paint(self, event):
        if self.old_x and self.old_y:
            self.canv.create_line(self.old_x, self.old_y, event.x, event.y,
                                  width=self.brush_size, fill=self.color,
                                  capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def save_image(self):
        x = self.winfo_rootx() + self.canv.winfo_x()
        y = self.winfo_rooty() + self.canv.winfo_y()
        x1 = x + self.canv.winfo_width()
        y1 = y + self.canv.winfo_height()

        try:
            self.filename = filedialog.asksaveasfilename(initialdir="/", title="Save image",
                                                     filetypes=(("PNG", "*.png"), ("all files", "*.*")))
            ImageGrab.grab().crop((x, y, x1, y1)).save(rf"{self.filename}.png")

        except: pass


class PaintViewController(PaintModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        Frame.__init__(self, parent)
        self.canv = Canvas(self, bg="white")
        self.color = default_color
        self.brush_size = default_brush_size
        self.setUI()

    colcounter = 0
    rowcounter = 0

    def create_color_btn(self, color):
        _c = 1  # column
        _r = 0  # row
        Button(self, width=2, bg=color, command=lambda: self.set_color(color)). \
            grid(column=_c + self.colcounter, row=_r + self.rowcounter)
        self.colcounter += 1
        if self.colcounter == 12:
            self.colcounter = 0
            self.rowcounter += 1

    def setUI(self):
        self.parent.title("Paint")
        self.pack(fill=BOTH, expand=1)  # Размещаем активные элементы на родительском окне

        self.columnconfigure(14, weight=1)  # возможность растягиваться
        self.rowconfigure(4, weight=1)

        # Создаем поле для рисования, устанавливаем белый фон
        self.canv.grid(row=4, column=0, columnspan=15, padx=5, pady=5, sticky=E + W + S + N)
        self.canv.bind("<Button-1>", self.draw_point)
        self.canv.bind("<B1-Motion>", self.paint)
        self.canv.bind('<ButtonRelease-1>', self.reset)

        # Color buttons
        Label(self, text="Color: ").grid(row=0, column=0, padx=6)
        for i in colors:
            self.create_color_btn(i)

        Button(self, text="Clear all", width=10, command=lambda: self.canv.delete("all")) \
            .grid(row=0, column=13, sticky=W, padx=5)

        # Brush size
        Label(self, text="Brush size: ").grid(row=3, column=0, padx=5)

        spinbox = Spinbox(self, from_=1, to=228, width=5, textvariable=self._brush_size, command=self.set_brush_size)
        spinbox.grid(row=3, column=1, columnspan=2)

        Button(self, text='Save image', width=10, command=self.save_image).grid(row=3, column=14, sticky=E)


if __name__ == '__main__':
    root = Tk()
    root.geometry("850x500+300+300")
    PaintViewController(parent=root)
    root.mainloop()
