import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QTreeWidget, QTreeWidgetItem, QStackedWidget,
    QListWidget
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D


class GraphCanvas(FigureCanvas):
    def __init__(self, title, y_data, parent=None):
        fig = Figure(figsize=(5, 3), facecolor="#121212")
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        self.setup_graph(title, y_data)

    def setup_graph(self, title, y_data):
        self.ax.clear()
        self.ax.set_facecolor("#1e1e1e")
        self.ax.plot(y_data, color='cyan', linewidth=2)
        self.ax.set_title(title, color='white')
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.draw()


class GraphCanvas3D(FigureCanvas):
    def __init__(self, title, parent=None):
        fig = Figure(figsize=(5, 4), facecolor="#121212")
        self.ax = fig.add_subplot(111, projection='3d')
        super().__init__(fig)
        self.setParent(parent)
        self.setup_graph(title)

    def setup_graph(self, title):
        self.ax.clear()
        self.ax.set_facecolor("#1e1e1e")
        self.ax.set_title(title, color='white')

        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x = 10 * np.outer(np.cos(u), np.sin(v))
        y = 10 * np.outer(np.sin(u), np.sin(v))
        z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

        self.ax.plot_surface(x, y, z, cmap='cool', edgecolor='none', alpha=0.8)

        self.ax.xaxis.set_pane_color((0.12, 0.12, 0.12, 1))
        self.ax.yaxis.set_pane_color((0.12, 0.12, 0.12, 1))
        self.ax.zaxis.set_pane_color((0.12, 0.12, 0.12, 1))

        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.zaxis.label.set_color('white')
        self.ax.tick_params(colors='white')

        self.draw()


class AnimatedGraphCanvas(FigureCanvas):
    def __init__(self, title, parent=None):
        fig = Figure(figsize=(5, 3), facecolor="#121212")
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        self.x = np.linspace(0, 10, 100)
        self.phase = 0
        self.setup_graph(title)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)

    def setup_graph(self, title):
        self.ax.set_facecolor("#1e1e1e")
        self.ax.set_title(title, color='white')
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.line, = self.ax.plot(self.x, np.sin(self.x), color='lime', linewidth=2)

    def update_plot(self):
        self.phase += 0.1
        y = np.sin(self.x + self.phase)
        self.line.set_ydata(y)
        self.draw()


class DashboardBoard(QWidget):
    def __init__(self, board_name, graph_data_list=None, is_3d=False, is_animated=False, is_combo=False):
        super().__init__()

        if is_combo:
            # 수평 레이아웃: 왼쪽 리스트, 오른쪽 그래프 스택
            layout = QHBoxLayout()
            self.setLayout(layout)

            self.list_widget = QListWidget()
            self.list_widget.setFixedWidth(120)
            layout.addWidget(self.list_widget)

            self.graph_stack = QStackedWidget()
            layout.addWidget(self.graph_stack)

            for idx, data in enumerate(graph_data_list):
                canvas = GraphCanvas(f"{board_name} - 그래프 {idx + 1}", data, self)
                self.graph_stack.addWidget(canvas)
                self.list_widget.addItem(f"그래프 {idx + 1}")

            self.list_widget.currentRowChanged.connect(self.graph_stack.setCurrentIndex)
            self.list_widget.setCurrentRow(0)

        else:
            layout = QVBoxLayout()
            self.setLayout(layout)

            if is_animated:
                canvas = AnimatedGraphCanvas(board_name + " - 애니메이션 그래프", self)
                layout.addWidget(canvas)
            elif is_3d:
                canvas = GraphCanvas3D(board_name + " - 3D 그래프", self)
                layout.addWidget(canvas)
            else:
                for idx, data in enumerate(graph_data_list):
                    canvas = GraphCanvas(f"{board_name} - 그래프 {idx + 1}", data, self)
                    layout.addWidget(canvas)


class DashboardMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("폴더구조 트리 선택 대시보드 (3D + 애니메이션 + 콤보 그래프 포함)")
        self.setGeometry(100, 100, 1200, 700)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#121212"))
        self.setPalette(palette)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setFixedWidth(250)
        self.tree.setStyleSheet("""
            QTreeWidget { background-color: #1e1e1e; color: white; font-size: 14px; }
            QTreeWidget::item:selected { background-color: #333; }
        """)
        main_layout.addWidget(self.tree)
#나는 아름다운 나비
        self.board_stack = QStackedWidget()
        main_layout.addWidget(self.board_stack)

        x = np.linspace(0, 10, 100)
        board1_data = [np.sin(x), np.cos(x)]
        board2_data = [np.sin(2 * x), np.cos(2 * x)]
        board3_data = [np.sin(3 * x), np.cos(3 * x)]
        board4_data = [np.sin(4 * x), np.cos(4 * x)]

        self.boards = []
        self.item_to_index = dict()

        folder_a = QTreeWidgetItem(self.tree)
        folder_a.setText(0, "폴더 A")
        folder_a.setExpanded(True)

        # 보드 1과 2를 합쳐서 콤보 보드로 생성
        board1_2_item = QTreeWidgetItem(folder_a)
        board1_2_item.setText(0, "보드 1,2")
        self.add_board("보드 1,2", board1_data + board2_data, board1_2_item, is_combo=True)

        folder_b = QTreeWidgetItem(self.tree)
        folder_b.setText(0, "폴더 B")
        folder_b.setExpanded(True)

        board3_item = QTreeWidgetItem(folder_b)
        board3_item.setText(0, "보드 3")
        self.add_board("보드 3", board3_data, board3_item)

        board4_item = QTreeWidgetItem(folder_b)
        board4_item.setText(0, "보드 4")
        self.add_board("보드 4", board4_data, board4_item)

        folder_c = QTreeWidgetItem(self.tree)
        folder_c.setText(0, "폴더 C (3D 그래프)")
        folder_c.setExpanded(True)

        board_3d_item = QTreeWidgetItem(folder_c)
        board_3d_item.setText(0, "3D 그래프 보드")
        self.add_board("3D 그래프 보드", None, board_3d_item, is_3d=True)

        folder_d = QTreeWidgetItem(self.tree)
        folder_d.setText(0, "폴더 D (애니메이션 그래프)")
        folder_d.setExpanded(True)

        animated_board_item = QTreeWidgetItem(folder_d)
        animated_board_item.setText(0, "실시간 사인파 그래프")
        self.add_board("실시간 사인파 그래프", None, animated_board_item, is_animated=True)

        self.tree.currentItemChanged.connect(self.on_tree_item_changed)
        self.tree.setCurrentItem(board1_2_item)

    def add_board(self, board_name, graph_data_list, tree_item, is_3d=False, is_animated=False, is_combo=False):
        board = DashboardBoard(board_name, graph_data_list, is_3d, is_animated, is_combo)
        self.boards.append(board)
        idx = self.board_stack.addWidget(board)
        self.item_to_index[id(tree_item)] = idx

    def on_tree_item_changed(self, current, previous):
        if current is None:
            return
        key = id(current)
        if key in self.item_to_index:
            idx = self.item_to_index[key]
            self.board_stack.setCurrentIndex(idx)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardMainWindow()
    window.show()
    sys.exit(app.exec_())
