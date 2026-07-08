from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QColor, QPainter, QPen
import sys

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return TreeNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        return node

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            min_larger_node = self._min_value_node(node.right)
            node.value = min_larger_node.value
            node.right = self._delete(node.right, min_larger_node.value)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def pre_order(self):
        result = []
        self._pre_order(self.root, result)
        return result

    def _pre_order(self, node, result):
        if node:
            result.append(node.value)
            self._pre_order(node.left, result)
            self._pre_order(node.right, result)

    def in_order(self):
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        if node:
            self._in_order(node.left, result)
            result.append(node.value)
            self._in_order(node.right, result)

    def post_order(self):
        result = []
        self._post_order(self.root, result)
        return result

    def _post_order(self, node, result):
        if node:
            self._post_order(node.left, result)
            self._post_order(node.right, result)
            result.append(node.value)

class BSTVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.bst = BinarySearchTree()
        self.nodes = []
        self.connections = []

    def initUI(self):
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("Binary Search Tree Visualizer")
        self.setStyleSheet("background-color: #1e1e1e;")

        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(20, 20, 200, 40)
        self.input_field.setPlaceholderText("Enter a number")
        self.input_field.setStyleSheet("background-color: #333; color: #fff; border-radius: 10px; padding: 5px;")

        self.add_button = self.create_button("Add Node", 240, 20, self.add_node)
        self.delete_button = self.create_button("Delete Node", 380, 20, self.delete_node)
        self.preorder_button = self.create_button("Pre-Order", 520, 20, self.print_preorder)
        self.inorder_button = self.create_button("In-Order", 660, 20, self.print_inorder)
        self.postorder_button = self.create_button("Post-Order", 800, 20, self.print_postorder)

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

    def add_node(self):
        value = self.input_field.text()
        if value.isdigit():
            self.bst.insert(int(value))
            self.input_field.clear()
            self.update_tree()
        else:
            self.show_error("Please enter a valid number.")

    def delete_node(self):
        value = self.input_field.text()
        if value.isdigit():
            self.bst.delete(int(value))
            self.input_field.clear()
            self.update_tree()
        else:
            self.show_error("Please enter a valid number.")

    def print_preorder(self):
        traversal = self.bst.pre_order()
        self.show_message("Pre-Order Traversal", traversal)

    def print_inorder(self):
        traversal = self.bst.in_order()
        self.show_message("In-Order Traversal", traversal)

    def print_postorder(self):
        traversal = self.bst.post_order()
        self.show_message("Post-Order Traversal", traversal)

    def show_message(self, title, traversal):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setStyleSheet("QLabel { color: white; }")
        msg.setText(str(traversal))
        msg.exec_()

    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)

    def update_tree(self):
        self.nodes.clear()
        self.connections.clear()
        self.draw_tree(self.bst.root, 600, 100, 300)
        self.update()

    def draw_tree(self, node, x, y, spacing):
        if node:
            node.x = x
            node.y = y
            self.nodes.append(node)

            if node.left:
                child_x = x - spacing
                child_y = y + 100
                self.connections.append((x, y, child_x, child_y))
                self.draw_tree(node.left, child_x, child_y, spacing // 2)

            if node.right:
                child_x = x + spacing
                child_y = y + 100
                self.connections.append((x, y, child_x, child_y))
                self.draw_tree(node.right, child_x, child_y, spacing // 2)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor("#FFFFFF"), 2)
        painter.setPen(pen)
        for (x1, y1, x2, y2) in self.connections:
            painter.drawLine(x1, y1, x2, y2)

        # Draw nodes
        for node in self.nodes:
            self.draw_node(painter, node)

    def draw_node(self, painter, node):
        painter.setBrush(QColor("#4682B4"))
        radius = 30
        painter.drawEllipse(node.x - radius, node.y - radius, 2 * radius, 2 * radius)

        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Arial", 14))
        text_rect = QRect(node.x - radius, node.y - radius, 2 * radius, 2 * radius)
        painter.drawText(text_rect, Qt.AlignCenter, str(node.value))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BSTVisualizer()
    window.show()
    sys.exit(app.exec_())
