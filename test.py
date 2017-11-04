import sys
from rbtree import RBTree
from PyQt5 import QtGui, QtWidgets
import networkx as nx

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import random

class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtWidgets.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        tree = RBTree()
        tree.insert(1)
        tree.insert(2)
        tree.insert(3)
        tree.insert(4)
        tree.insert(5)

        G = nx.Graph()

        pos = self._get_pos_list(self.tree)
        nodes = [x for x in pos.keys()]
        edges = self._get_edge_list(self.tree)
        labels = self._get_label_list(self.tree)
        colors = []
        try:
            colors = self._get_color_list(self.tree)
        except AttributeError:
            pass

        G.add_edges_from(edges)
        G.add_nodes_from(nodes)

        if len(colors) > 0:
            nx.draw_networkx_nodes(G, pos, node_size=600, node_color=colors)
            nx.draw_networkx_edges(G, pos)
            nx.draw_networkx_labels(G, pos, labels, font_color='w')
        else:
            nx.draw_networkx_nodes(G, pos, node_size=600, node_color='r')
            nx.draw_networkx_edges(G, pos)
            nx.draw_networkx_labels(G, pos, labels)


        # data = [random.random() for i in range(10)]

        # create an axis
        # ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.clear()

        # plot data
        # ax.plot(data, '*-')

        # refresh canvas
        # self.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())