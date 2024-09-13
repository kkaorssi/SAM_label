from PyQt5.QtWidgets import *

class input_name(QDialog):
    def __init__(self, parent=None, title=str):
        super().__init__(parent)
        self.setWindowTitle(title)
        
        # Create a QLineEdit widget for input
        self.input_edit = QLineEdit(self)
        
        # Create a button to submit input
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.accept)
        
        # Add the widgets to a layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.input_edit)
        layout.addWidget(self.submit_button)
        
    def get_input_value(self):
        # Return the text entered in the QLineEdit widget
        return self.input_edit.text()
    
def choose_mode(parent):
    items = ('Manual', 'Auto')
    item, ok = QInputDialog.getItem(parent, 'Choose predictor mode',
                                    'Options: ', items, 0, False)

    return item, ok

def getTextInputDialog(parent):
    text, okPressed = QInputDialog.getText(parent, "Enter object name", 
                                           "New object name:", QLineEdit.Normal, "")   
    if okPressed and text != '':
        print(text)
        return text
        
    else:
        return None