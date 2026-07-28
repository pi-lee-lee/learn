from tkinter import * 
from tkinter.filedialog import * 

def new_file():
    text_area.delete(1.0,END)

def save_file():
    f = asksaveasfile(mode='w', defaultextension='.txt', filetypes=[('Text files','.txt')])
    text_save = str(text_area.get(1.0,END))
    if f is not None:
        f.write(text_save)
        f.close()

    

    
def maker():
    help_view = Toplevel(window)
    help_view.geometry('300x50')
    help_view.title('author')
    lb = Label(help_view, text = 'ss')
    lb.pack()



window = Tk()
window.title('s')
window.geometry('400x400')
window.resizable(False, False)

menu = Menu(window)
menu_1 = Menu(menu, tearoff=0)
menu_1.add_command(label='new', command=new_file)
menu_1.add_command(label='save', command=save_file)
menu_1.add_separator()
menu_1.add_command(label='exit', command=window.destroy)

menu.add_cascade(label='file',menu=menu_1)

menu_2 = Menu(menu, tearoff=0)
menu_2.add_command(label='author', command=maker)
menu.add_cascade(label='author', menu=menu_2)

text_area = Text(window)

window.grid_rowconfigure(0,weight=1)
window.grid_columnconfigure(0,weight=1)

text_area.grid(sticky= E+W+S+N)

window.config(menu=menu)
window.mainloop()