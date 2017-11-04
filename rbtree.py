import collections


class Node:
    """A node of a Red-black Tree"""
    def __init__(self, key):
        self.left = None
        self.right = None
        self.parent = None
        self.key = key
        self.color = 'r'


class RBTree:
    def __init__(self, *args):

        self.Root = None

        if len(args) == 1:
            if isinstance(args[0], collections.Iterable):
                for x in args[0]:
                    self.insert(x)
            else:
                raise TypeError(str(args[0]) + " is not iterable")

    def get_node(self, key, *args):
        if len(args) == 0:
            start = self.Root
        else:
            start = args[0]

        if not start:
            return None
        if key == start.key:
            return start
        elif key > start.key:
            return self.get_node(key, start.right)
        else:
            return self.get_node(key, start.left)

    def insert(self, key,  *args):
        if not isinstance(key, int):
            raise TypeError(str(key) + " is not an int")
        else:
            if not self.Root:
                self.Root = Node(key)
                self.Root.color = 'k'
            elif len(args) == 0:
                if not self.get_node(key, self.Root):
                    self.insert(key, self.Root)
            else:
                child = Node(key)
                parent = args[0]
                if child.key > parent.key:
                    if not parent.right:
                        parent.right = child
                        child.parent = parent
                        if parent.color == 'r':
                            self._insert_case_one(child)
                    else:
                        self.insert(key, parent.right)
                else:
                    if not parent.left:
                        parent.left = child
                        child.parent = parent
                        if parent.color == 'r':
                            self._insert_case_one(child)
                    else:
                        self.insert(key, parent.left)

    def _insert_case_one(self, child):
        """
        T._insert_case_one(child). Considers the case in which
        child is at the root of the tree. Recolors black if so,
        otherwise moves on to case two.
        """
        if not child.parent:
            self.Root.color = 'k'
        else:
            self._insert_case_two(child)


    def _insert_case_two(self, child):
        """
        T._insert_case_two(child). Considers the case in which
        child's parent is black. If so, we are done. If not, moves
        to case three.
        """
        if child.parent.color == 'r':
            self._insert_case_three(child)

    def _insert_case_three(self, child):
        """
        T._insert_case_three(child). Considers the case in which
        child's parent and uncle are red. If so, recolors
        the parent and uncle black, and child's grandparent red.
        Note child's grandparent now may have a red parent, which
        makes T invalid. So now we start over from case one at
        the grandparent.
        """

        parent = child.parent
        grand_node = parent.parent

        if grand_node.left == parent:
            uncle = grand_node.right
        else:
            uncle = grand_node.left

        if uncle and uncle.color == 'r':
            grand_node.color = 'r'
            parent.color = 'k'
            uncle.color = 'k'
            self._insert_case_one(grand_node)
        else:
            self._insert_case_four(child)

    def _insert_case_four(self, child):
        """
        T._insert_case_four(child). Considers the case in which
        child's parent is red, child's uncle is black, and
        the parent is the left child of the grandparent while
        the child is the right child of the parent, or vice versa.
        If so, performs an appropriate tree rotation around
        child's parent and moves on to case five.
        """
        parent = child.parent
        grand_node = parent.parent
        if grand_node.left == parent:
            uncle = grand_node.right
        else:
            uncle = grand_node.left

        if grand_node.left == parent and parent.right == child:
            self._rotate_left(parent)
            child = child.left
        elif grand_node.right == parent and parent.left == child:
            self._rotate_right(parent)
            child = child.right

        self._insert_case_five(child)

    def _insert_case_five(self, child):
        """
        T._insert_case_five(child). Considers the case in which
        child's parent is red, child's uncle is black, and the
        parent is the left child of the grandparent while the child
        is the left child of the parent, or vice versa. If so,
        performs an appropriate tree rotation around the grandparent.
        """
        parent = child.parent
        grand_node = parent.parent
        if grand_node.left == parent:
            uncle = grand_node.right
        else:
            uncle = grand_node.left

        if parent.left == child:
            grand_node.color = 'r'
            parent.color = 'k'
            self._rotate_right(grand_node)
        elif parent.right == child:
            grand_node.color = 'r'
            parent.color = 'k'
            self._rotate_left(grand_node)

    def _rotate_left(self, pivot):
        """
        T.__rotate_left(pivot). Performs a left tree rotation in T
        around the Node pivot.
        """
        old_root = pivot
        parent = old_root.parent

        new_root = old_root.right
        temp = new_root.right
        old_root.right = new_root.left

        if (old_root.right):
            old_root.right.parent = old_root
        new_root.left = old_root
        old_root.parent = new_root

        if parent is None:
            self.Root = new_root
            self.Root.parent = None
        else:
            if parent.right and parent.right.key == old_root.key:
                parent.right = new_root
                new_root.parent = parent
            elif parent.left and parent.left.key == old_root.key:
                parent.left = new_root
                new_root.parent = parent

    def _rotate_right(self, pivot):
        """
        T.__rotate_right(pivot). Performs a right tree rotation in T
        around the Node pivot.
        """
        if not pivot.left:
            pass
        else:
            old_root = pivot
            parent = old_root.parent

            new_root = old_root.left
            temp = new_root.left
            old_root.left = new_root.right

            if (old_root.left):
                old_root.left.parent = old_root

            new_root.right = old_root
            old_root.parent = new_root

            if parent is None:
                self.Root = new_root
                self.Root.parent = None
            else:
                if parent.right and parent.right.key == old_root.key:
                    parent.right = new_root
                    new_root.parent = parent
                elif parent.left and parent.left.key == old_root.key:
                    parent.left = new_root
                    new_root.parent = parent

    def get_element_count(self, *args):
        """
        Counts the number of elements in a tree
        """
        if len(args) == 0:
            node = self.Root
        else:
            node = args[0]

        left = 0
        right = 0

        if node:
            if node.left:
                left = self.get_element_count(node.left)
            if node.right:
                right = self.get_element_count(node.right)

            return 1 + left + right
        else:
            return 0
