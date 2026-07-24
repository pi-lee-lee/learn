from tkinter import * 
from tkinter.filedialog import * 



window = Tk()
window.title('s')
window.geometry('400x400')
window.resizable(False, False)

menu = Menu(window)
menu_1 = Menu(menu, tearoff=0)
menu_1.add_command(label='new')
menu_1.add_command(label='save')
menu_1.add_separator()
menu_1.add_command(label='exit', command=window.destroy)

menu.add_cascade(label='file',menu=menu_1)

menu_2 = Menu(menu, tearoff=0)
menu_2.add_command(label='author')
menu.add_cascade(label='author', menu=menu_2)

text_area = Text(window)

window.grid_rowconfigure(0,weight=1)
window.grid_columnconfigure(0,weight=1)

text_area.grid(sticky= E+W+S+N)

window.config(menu=menu)
window.mainloop()