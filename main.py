import sys
import csv
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, 
                             QMessageBox, QLabel)
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the overall theme
        self.setWindowTitle("Sorting Algorithm Visualizer")
        self.setGeometry(800, 300, 800, 300)  # Increased window size
        
        # Set dark background color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)


        self.setFont(QFont("Consolas", 15))  # Increased font size

        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)  
        
        header_layout = QVBoxLayout()
        header_layout.setSpacing(0)  


        heading = QLabel("<span style='font-family: \"Segoe UI\"; font-size: 60px; font-weight: bold; color: white;'>"
                         "<span style='font-style: italic;'>Sort</span>"
                         "<span style='color: rgb(0, 174, 255);'>Lab</span></span>")
        heading.setAlignment(Qt.AlignCenter)

        subheading = QLabel("Sorting algorithms visualised!")
        subheading.setStyleSheet("font-family: 'Segoe UI'; font-size: 30px; color: white; font-weight: bold;")
        subheading.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(heading)
        header_layout.addWidget(subheading)

        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Enter comma-separated integers")
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: rgb(110, 110, 110);
                color: white;
                padding: 12px;  /* Increased padding */
                border: 2px solid transparent;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 2px solid rgb(80, 80, 80);
            }
        """)
        
    
        button_names = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"]
        grid_layout = QGridLayout()
        grid_layout.setSpacing(40)  

        for i, name in enumerate(button_names):
            button = QPushButton(name)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgb(0, 104, 205);
                    color: white;
                    font-size: 22px;
                    padding: 20px;  /* Increased padding */
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;  /* Bold font for buttons */
                }
                QPushButton:hover {
                    background-color: rgb(255, 100, 100);
                }
                QPushButton:pressed {
                    background-color: rgb(150, 150, 150);
                }
            """)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda checked, sort_type=name: self.open_sorting_window(sort_type))
            grid_layout.addWidget(button, i // 2, i % 2)  

        
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.input_box)
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def open_sorting_window(self, sort_type):
        """Store input array to CSV and open respective sorting visualizer."""
        input_text = self.input_box.text()
        if input_text.strip() == "":
            QMessageBox.warning(self, "Input Error", "Please enter a valid comma-separated list of integers.")
            return
        
       
        try:
            array = [int(num.strip()) for num in input_text.split(',')]
            
            with open("input_array.csv", "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(array)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid integers only.")
            return
        
    
        if sort_type == "Bubble Sort":
            subprocess.Popen(["python", "C:\\Users\\DELL\\Desktop\\DSA Project\\bubble.py"])  
        elif sort_type == "Selection Sort":
            subprocess.Popen(["python", "C:\\Users\\DELL\\Desktop\\DSA Project\\selection.py"])  
        elif sort_type == "Insertion Sort":
            subprocess.Popen(["python", "C:\\Users\\DELL\\Desktop\\DSA Project\\insertion.py"]) 
        elif sort_type == "Merge Sort":
            subprocess.Popen(["python", "C:\\Users\\DELL\\Desktop\\DSA Project\\merge.py"])  


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
