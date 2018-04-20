import numpy as np
import scipy.misc
import skimage.io
from random import randint
from math import ceil

def generate_block_list(img, block_size):
    """
    Create the range of block of block_size in an image
    """
    t = []
    for i in range(ceil(img.shape[0] / block_size)):
        for j in range(ceil(img.shape[1] / block_size)):
            x_range = (i * block_size, min(((i+1)*block_size), img.shape[0]))
            y_range = (j * block_size, min(((j+1)*block_size), img.shape[1]))
            t.append((x_range, y_range))
    return t            


class Picture:
    """
    Create a picture and it's range of block size
    """
    def __init__(self, img_path, block_size):
        img = skimage.io.imread(img_path)
        self.initial_img = img
        self.img = np.copy(img)
        self.block_list = generate_block_list(img, block_size)
        self.displayed_block = len(self.block_list) - 1
        self.color = np.array([0, 0, 0])

    """
    Change block size
    """
    def change_block_size(self, block_size):
        self.img = np.copy(self.initial_img)
        self.block_list = generate_block_list(self.img, block_size)
        self.displayed_block = len(self.block_list) - 1
    
    """
    Delete n random block of the picture
    """
    def delete_n_random_block(self, n):
        for _ in range(n):
            self.delete_random_block()
    
    """
    Delete 1 random block of the picture
    """
    def delete_random_block(self):
        if (self.displayed_block == 0):
            return
        i = randint(0, self.displayed_block)
        tmp = self.block_list[i]
        self.block_list[i] = self.block_list[self.displayed_block]
        self.block_list[self.displayed_block] = tmp
        self.displayed_block -= 1
        x_range, y_range = tmp
        for x in range(x_range[0], x_range[1]):
            for y in range(y_range[0], y_range[1]):
                self.delete_pixel(x, y)
    
    """
    Delete 1 pixel of the picture
    """
    def delete_pixel(self, x, y):
        self.img[x][y] = self.color
    
    """
    Revert the n last deleted block of the picture
    """
    def revert_n_delete(self, n):
        for _ in range(n):
            self.revert_delete()
    
    """
    Revert the last deleted block of the picture
    """
    def revert_delete(self):
        if (self.displayed_block == len(self.block_list) - 1):
            return
        self.displayed_block += 1
        x_range, y_range = self.block_list[self.displayed_block]
        for x in range(x_range[0], x_range[1]):
            for y in range(y_range[0], y_range[1]):
                self.img[x][y] = self.initial_img[x][y]
    
    """
    Save the modified picture
    """
    def save_img(self, filename):
        scipy.misc.imsave(filename, self.img)

        
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox, QFileDialog, QMenuBar, QMainWindow, qApp
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
 
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 900
        self.p = None
        self.p = Picture("./../pictures/white_background.jpg", 1)
        self.p.save_img("outfile.jpg")
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # picture
        self.label = QLabel(self)
        pixmap = QPixmap("outfile.jpg")
        self.label.setPixmap(pixmap.scaled(900, 900))
        self.label.setScaledContents(True)

        # Block Size textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 80)
        self.textbox.resize(40, 25)
        self.button1 = QPushButton('Change block size', self)
        self.button1.move(80, 80)
        self.button1.clicked.connect(self.change_block_size)

        # Add block textbox
        self.textbox_n_block = QLineEdit(self)
        self.textbox_n_block.move(20, 110)
        self.textbox_n_block.resize(40, 25)
        self.button2 = QPushButton('Add', self)
        self.button2.move(80, 110)
        self.button2.clicked.connect(self.delete_block)
        self.button3 = QPushButton('Remove', self)
        self.button3.move(150, 110)
        self.button3.clicked.connect(self.revert_block)

        # open file
        self.button4 = QPushButton('Open', self)
        self.button4.move(20, 20)
        self.button4.clicked.connect(self.open_file)

        # save file
        self.button5 = QPushButton('Save', self)
        self.button5.move(20, 50)
        self.button5.clicked.connect(self.save_file)
 
        self.show()


    def refresh(self):
        pixmap = QPixmap("outfile.jpg")
        self.label.setPixmap(pixmap.scaled(900, 900))
        self.label.setScaledContents(True)

    @pyqtSlot()
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName()
        self.p = Picture(filename, 100)
        self.p.save_img('outfile.jpg')
        self.refresh()

    @pyqtSlot()
    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName()
        if (filename):
            self.p.save_img(filename)
 
    @pyqtSlot()
    def change_block_size(self):
        textbox_value = int(self.textbox.text())
        self.p.change_block_size(textbox_value)
        self.p.save_img('outfile.jpg')
        self.refresh()

    @pyqtSlot()
    def delete_block(self):
        textbox_value = int(self.textbox_n_block.text())
        if (self.p):
            self.p.delete_n_random_block(textbox_value)
            self.p.save_img('outfile.jpg')
            self.refresh()

    @pyqtSlot()
    def revert_block(self):
        textbox_value = int(self.textbox_n_block.text())
        if (self.p):
            self.p.revert_n_delete(textbox_value)
            self.p.save_img('outfile.jpg')
            self.refresh()
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
