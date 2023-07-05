import sys
from PyQt5.QtWidgets import QApplication
from model import Model
from view import View


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    view = View(model)
    view.show()
    sys.exit(app.exec_())