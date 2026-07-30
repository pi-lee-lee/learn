from PyQt5 import QtWidgets

oldwidget = {}


def changeView(widget, ui, delete = True, alone = False):
    if delete : 
        for i  in widget.findChildren(QtWidgets.QFrame):
            i.setParent(None)
       
    child = QtWidgets.QFrame(widget)

    child.setGeometry(0, 0, widget.width(), widget.height())
        
    ui.setupUi(child)

    if alone : 
        child.setParent(None)

    return child
    

def appendView(parent, ui, delete=True):
    child = QtWidgets.QFrame(parent)
    child.setGeometry(0, 0, parent.width(), parent.height())
    ui.setupUi(child)
    return child
        
    


