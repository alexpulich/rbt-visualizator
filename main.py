import sys
from rbtree import RBTree
from PyQt5 import QtWidgets
import networkx as nx
import pickle

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.init_ui()
        self.init_tree()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        self.setWindowTitle('Red-Black Tree | Alex Pulich, P3417')

        # pyplot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        # self.toolbar = NavigationToolbar(self.canvas, self)

        # controls
        # tree managing group
        tree_mng_groupbox = QtWidgets.QGroupBox("Tree managing")
        tree_mng_layout = QtWidgets.QHBoxLayout()

        key_label = QtWidgets.QLabel('Key:')
        self.key_input = QtWidgets.QLineEdit()
        self.add_btn = QtWidgets.QPushButton('Add')
        self.remove_btn = QtWidgets.QPushButton('Remove')
        self.search_btn = QtWidgets.QPushButton('Search')

        self.add_btn.clicked.connect(self.add_btn_handler)
        self.remove_btn.clicked.connect(self.remove_btn_handler)
        self.search_btn.clicked.connect(self.search_btn_handler)

        tree_mng_layout.addWidget(key_label)
        tree_mng_layout.addWidget(self.key_input)
        tree_mng_layout.addWidget(self.add_btn)
        tree_mng_layout.addWidget(self.remove_btn)
        tree_mng_layout.addWidget(self.search_btn)

        tree_mng_groupbox.setLayout(tree_mng_layout)

        # import/export group
        io_groupbox = QtWidgets.QGroupBox("Export/Import")
        io_layout = QtWidgets.QHBoxLayout()

        self.export_btn = QtWidgets.QPushButton('Export')
        self.import_btn = QtWidgets.QPushButton('Import')

        io_layout.addWidget(self.export_btn)
        io_layout.addWidget(self.import_btn)

        self.import_btn.clicked.connect(self.import_btn_handler)
        self.export_btn.clicked.connect(self.export_btn_handler)

        io_groupbox.setLayout(io_layout)

        # set the main layout
        layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.addWidget(tree_mng_groupbox)
        controls_layout.addWidget(io_groupbox)
        layout.addLayout(controls_layout)
        self.setLayout(layout)
        self.center()

    def init_tree(self):
        self.tree = RBTree()

    def add_btn_handler(self):
        if len(self.key_input.text()) == 0:
            return
        key = None
        try:
            key = int(self.key_input.text())
        except ValueError:
            self.show_error('Int expected', 'The key should be a number!')

        if key:
            self.tree.insert(key)
            self.plot()
            self.key_input.clear()

    def remove_btn_handler(self):
        if len(self.key_input.text()) == 0:
            return
        key = None
        try:
            key = int(self.key_input.text())
        except ValueError:
            print('Failed to convert to int')

        if key:
            self.tree.delete(key)
            self.key_input.clear()
            self.plot()

    def search_btn_handler(self):
        if len(self.key_input.text()) == 0:
            return
        # self.tree.search_node(int(self.key_input.text()), self.tree.Root, True)
        node = self.tree.get_node(int(self.key_input.text()))
        node_path = self.tree.get_path(node)

    def export_btn_handler(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Export RBTree', 'mytree.rbtree',
                                                      'Red-Black Tree files (*.rbtree)')[0]
        if fname:
            with open(fname, 'wb') as f:
                pickle.dump(self.tree, f)

    def import_btn_handler(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Import RBTree', '',
                                                      'Red-Black Tree files (*.rbtree)')[0]
        if fname:
            with open(fname, 'rb') as f:
                self.tree = pickle.load(f)
            self.plot()

    def show_error(self, title, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
        self.key_input.clear()

    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.clear()

        G = nx.Graph()

        pos = self._get_pos_list(self.tree)
        nodes = [x.key for x in self._preorder(self.tree)]
        edges = self._get_edge_list(self.tree)
        labels = {x: x for x in nodes}
        colors = []
        try:
            colors = self._get_color_list(self.tree)
        except AttributeError:
            pass

        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        if len(colors) > 0:
            nx.draw_networkx_nodes(G, pos, node_size=600, node_color=colors, ax=ax)
            nx.draw_networkx_edges(G, pos, ax=ax)
            nx.draw_networkx_labels(G, pos, labels, font_color='w', ax=ax)
        else:
            nx.draw_networkx_nodes(G, pos, node_size=600, node_color='r', ax=ax)
            nx.draw_networkx_edges(G, pos, ax=ax)
            nx.draw_networkx_labels(G, pos, labels, ax=ax)

        ax.axis('off')

        self.canvas.draw()

    def _get_pos_list(self, tree):
        """
        _get_pos_list(tree) -> Mapping. Produces a mapping
        of nodes as keys, and their coordinates for plotting
        as values. Since pyplot or networkx don't have built in
        methods for plotting binary search trees, this somewhat
        choppy method has to be used.
        """
        return self._get_pos_list_from(tree, tree.Root, {}, 0, (0, 0), 1.0)

    def _get_pos_list_from(self, tree, node, poslst, index, coords, gap):
        """
        _get_pos_list_from(tree,node,poslst,index,coords,gap) -> Mapping.
        Produces a mapping of nodes as keys, and their coordinates for
        plotting as values.

        Non-straightforward arguments:
        index: represents the index of node in
        a list of all Nodes in tree in preorder.
        coords: represents coordinates of node's parent. Used to
        determine coordinates of node for plotting.
        gap: represents horizontal distance from node and node's parent.
        To achieve plotting consistency each time we move down the tree
        we half this value.
        """
        positions = poslst

        if node and node.key == tree.Root.key:
            positions[node.key] = (0, 0)
            positions = self._get_pos_list_from(tree, tree.Root.left, positions, 1, (0, 0), gap)
            positions = self._get_pos_list_from(tree, tree.Root.right, positions, 1 + tree.get_element_count(node.left),
                                                (0, 0), gap)
            return positions
        elif node:
            if node.parent.right and node.parent.right.key == node.key:
                new_coords = (coords[0] + gap, coords[1] - 1)
                positions[node.key] = new_coords
            else:
                new_coords = (coords[0] - gap, coords[1] - 1)
                positions[node.key] = new_coords

            positions = self._get_pos_list_from(tree, node.left, positions, index + 1, new_coords, gap / 2)
            positions = self._get_pos_list_from(tree, node.right, positions,
                                                1 + index + tree.get_element_count(node.left), new_coords, gap / 2)
            return positions
        else:
            return positions

    def _get_edge_list(self, tree):
        """
        _get_edge_list(tree) -> Sequence. Produces a sequence
        of tuples representing edges to be drawn.
        """
        return self._get_edge_list_from(tree, tree.Root, [])

    def _get_edge_list_from(self, tree, node, edgelst):
        """
        _get_edge_list_from(tree,node,edgelst,index) -> Sequence.
        Produces a sequence of tuples representing edges to be drawn.
        As stated before, index represents the index of node in
        a list of all Nodes in tree in preorder.
        """
        edges = edgelst

        if node and node.key == tree.Root.key:
            if node.left:
                edges.append((node.key, node.left.key))
                edges = self._get_edge_list_from(tree, node.left, edges)
            if node.right:
                edges.append((node.key, node.right.key))
                edges = self._get_edge_list_from(tree, node.right, edges)

            return edges

        elif node:
            if node.left:
                edges.append((node.key, node.left.key))
            if node.right:
                edges.append((node.key, node.right.key))

            edges = self._get_edge_list_from(tree, node.left, edges)
            edges = self._get_edge_list_from(tree, node.right, edges)
            return edges

        else:
            return edges

    def _preorder(self, tree, *args):
        """
        _preorder(tree,...) -> Sequence. Produces a sequence of the Nodes
        in tree, obtained in preorder. Used to get information
        for plotting.
        """
        if len(args) == 0:
            elements = []
            node = tree.Root
        else:
            node = tree
            elements = args[0]

        elements.append(node)

        if node.left:
            self._preorder(node.left, elements)
        if node.right:
            self._preorder(node.right, elements)

        return elements

    def _get_color_list(self, tree):
        """
        _get_color_list(tree) -> Sequence. Produces
        a sequence of colors in tree for plotting.
        NOTE: Assumes tree is a Red Black Tree.
        This is checked first in the main function draw().
        """
        nodelist = self._preorder(tree)
        colorlist = []
        for node in nodelist:
            if node.color:
                colorlist.append(node.color)

        return colorlist


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
