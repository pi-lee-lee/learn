from PyQt5 import QtWidgets

def changeView(parent, ui, delete = True, alone = False):
    if delete : 
        for i  in parent.findChildren(QtWidgets.QFrame):
            i.setParent(None)
    child = QtWidgets.QFrame(parent)
    child.setGeometry(0, 0, parent.width(), parent.height())
    ui.setupUi(child)
    if alone : 
        child.setParent(None)
    return child
    
def appendView(parent, ui):
    child = QtWidgets.QFrame(parent)
    child.setGeometry(0, 0, parent.width(), parent.height())
    ui.setupUi(child)
    return child

def clearnView(parent, target = QtWidgets.QWidget):
    for i in parent.findChildren(target):
        i.setParent(None)

        
    


