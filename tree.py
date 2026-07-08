from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QColor, QPainter, QPen
import sys
from collections import deque

class TernaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.middle = None
        self.right = None
        self.x = 0
        self.y = 0

class TernaryTree:
    def __init__(self):
        self.root = None

    def build_tree(self, values):
        if not values:
            return None

        values = values.split(',')
        if not values or values[0] == '0':
            return None

        self.root = TernaryTreeNode(values[0])
        queue = deque([self.root])
        index = 1

        while queue and index < len(values):
            current = queue.popleft()

            # Add left child
            if index < len(values) and values[index] != '0':
                current.left = TernaryTreeNode(values[index])
                queue.append(current.left)
            index += 1

            # Add middle child
            if index < len(values) and values[index] != '0':
                current.middle = TernaryTreeNode(values[index])
                queue.append(current.middle)
            index += 1

            # Add right child
            if index < len(values) and values[index] != '0':
                current.right = TernaryTreeNode(values[index])
                queue.append(current.right)
            index += 1

    def pre_order(self):
        result = []
        self._pre_order(self.root, result)
        return result

    def _pre_order(self, node, result):
        if node:
            result.append(node.value)
            self._pre_order(node.left, result)
            self._pre_order(node.middle, result)
            self._pre_order(node.right, result)

    def post_order(self):
        result = []
        self._post_order(self.root, result)
        return result

    def _post_order(self, node, result):
        if node:
            self._post_order(node.left, result)
            self._post_order(node.middle, result)
            self._post_order(node.right, result)
            result.append(node.value)

    def in_order(self):
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        if node:
            self._in_order(node.left, result)
            result.append(node.value)
            self._in_order(node.middle, result)
            self._in_order(node.right, result)

class TernaryTreeVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tree = TernaryTree()
        self.nodes = []
        self.connections = []

    def initUI(self):
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("Ternary Tree Visualizer")
        self.setStyleSheet("background-color: #1e1e1e;")

        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(20, 20, 400, 40)
        self.input_field.setPlaceholderText("Enter level-order comma-separated nodes")
        self.input_field.setStyleSheet("background-color: #333; color: #fff; border-radius: 10px; padding: 5px;")

        self.build_button = self.create_button("Build Tree", 440, 20, self.build_tree)
        self.preorder_button = self.create_button("Pre-Order", 580, 20, self.print_preorder)
        self.postorder_button = self.create_button("Post-Order", 720, 20, self.print_postorder)
        self.inorder_button = self.create_button("In-Order", 860, 20, self.print_inorder)

    def create_button(self, text, x, y, func):
        button = QPushButton(text, self)
        button.setGeometry(x, y, 120, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
        """)
        button.clicked.connect(func)
        return button

    def build_tree(self):
        values = self.input_field.text()
        self.tree.build_tree(values)
        self.update_tree()

    def print_preorder(self):
        traversal = self.tree.pre_order()
        self.show_message("Pre-Order Traversal", traversal)

    def print_postorder(self):
        traversal = self.tree.post_order()
        self.show_message("Post-Order Traversal", traversal)

    def print_inorder(self):
        traversal = self.tree.in_order()
        self.show_message("In-Order Traversal", traversal)

    def show_message(self, title, traversal):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setStyleSheet("QLabel { color: white; }")
        msg.setText(str(traversal))
        msg.exec_()

    def update_tree(self):
        self.nodes.clear()
        self.connections.clear()
        self.draw_tree(self.tree.root, 600, 100, 200)
        self.update()

    def draw_tree(self, node, x, y, spacing):
        if node:
            node.x = x
            node.y = y
            self.nodes.append(node)

            if node.left:
                self.connections.append((x, y, x - spacing, y + 100))
                self.draw_tree(node.left, x - spacing, y + 100, spacing // 2)

            if node.middle:
                self.connections.append((x, y, x, y + 100))
                self.draw_tree(node.middle, x, y + 100, spacing // 2)

            if node.right:
                self.connections.append((x, y, x + spacing, y + 100))
                self.draw_tree(node.right, x + spacing, y + 100, spacing // 2)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor("#FFFFFF"), 2)
        painter.setPen(pen)
        for (x1, y1, x2, y2) in self.connections:
            painter.drawLine(x1, y1, x2, y2)

        for node in self.nodes:
            self.draw_node(painter, node)

    def draw_node(self, painter, node):
        painter.setBrush(QColor("#4682B4"))
        radius = 30
        painter.drawEllipse(node.x - radius, node.y - radius, 2 * radius, 2 * radius)
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Arial", 14))
        text_rect = QRect(node.x - radius, node.y - radius, 2 * radius, 2 * radius)
        painter.drawText(text_rect, Qt.AlignCenter, node.value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TernaryTreeVisualizer()
    window.show()
    sys.exit(app.exec_())
