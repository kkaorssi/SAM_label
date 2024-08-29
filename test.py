from PyQt5.QtWidgets import *
import sys

class input_name(QDialog):
    def __init__(self, parent=None, title=str):
        super().__init__(parent)
        self.setWindowTitle(title)
        
        # Create a QLineEdit widget for input
        self.input_edit = QLineEdit(self)

        # Sample data
        data = ["Item 1", "Item 2", "Item 3"]
        data_list = QListWidget()
        data_list.addItems(data)
        data_list.currentItemChanged.connect(self.set_text)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Add the widgets to a layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.input_edit)
        layout.addWidget(data_list)
        layout.addWidget(button_box)
        
    def get_input_value(self):
        self.show()
        # Return the text entered in the QLineEdit widget
        return self.input_edit.text()
    
    def set_text(self, current, previous):
        text = current.text()
        self.input_edit.setText(text)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWindow = QMainWindow()
    myWindow.showMaximized() 

    data = ["Item 1", "Item 2", "Item 3"]
    data_list = QListWidget()
    data_list.addItems(data)

    getT = input_name(myWindow, 'get txt')
    getT.get_input_value()

    sys.exit(app.exec_())

# from PyQt5.QtCore import Qt, QThread, pyqtSignal
# from PyQt5.QtGui import QIcon
# from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QProgressBar, QPushButton, QVBoxLayout, QProgressDialog

# import time

# class Worker(QThread):
#     progress = pyqtSignal(int)
#     finished = pyqtSignal()

#     def run(self):
#         # Simulate a long-running task
#         for i in range(100):
#             time.sleep(0.1)
#             self.progress.emit(i+1)

#         self.finished.emit()

# class MainWindow(QDialog):
#     def __init__(self):
#         super().__init__()

#         layout = QVBoxLayout()

#         self.button = QPushButton("Start")
#         self.button.clicked.connect(self.start_worker)
#         layout.addWidget(self.button)

#         self.progress_bar = QProgressBar()
#         layout.addWidget(self.progress_bar)

#         self.setLayout(layout)

#     def start_worker(self):
#         self.worker = Worker()
#         self.worker.progress.connect(self.update_progress)
#         self.worker.finished.connect(self.close_dialog)

#         self.dialog = QProgressDialog("Task in progress...", "Cancel", 0, 100)
#         self.dialog.setWindowModality(Qt.WindowModal)
#         self.dialog.show()

#         self.worker.start()

#     def update_progress(self, value):
#         self.progress_bar.setValue(value)
#         self.dialog.setValue(value)

#     def close_dialog(self):
#         self.dialog.close()

# if __name__ == "__main__":
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()