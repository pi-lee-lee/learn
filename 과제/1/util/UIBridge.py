from PyQt5 import QtWidgets

oldwidget = {}


def changeView(widget, ui, delete = True, alone = False):

    if delete : 
        for i  in widget.findChildren(QtWidgets.QFrame):
            i.setParent(None)
       
    child = QtWidgets.QFrame(widget)

    child.setGeometry(widget.geometry())

    ui.setupUi(child)

    if alone : 
        child.setParent(None)
    
    child.show()

def appendView(parent, ui, delete=True):
    child = QtWidgets.QFrame(parent)
    child.setGeometry(parent.geometry())
    ui.setupUi(child)
    child.show()
        
    


