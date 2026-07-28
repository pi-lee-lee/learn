from tkinter import *
from tkinter.filedialog import *

w = Tk()
w.title('ss')
w.geometry('400x400')

ta = Text(w)
sc = Scrollbar(ta)
ta.xview_scroll(1,'units')
ta.yview_scroll(1,'units')
w.grid_rowconfigure(0,weight=1)
w.grid_columnconfigure(0, weight=1)

ta.grid(sticky=W+ N)

w.mainloop()