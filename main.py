from rbtree import RBTree
from gui import GUI

tree = RBTree()
tree.insert(1)
tree.insert(2)
tree.insert(3)
tree.insert(4)
tree.insert(5)
gui = GUI(tree)
gui.draw()
