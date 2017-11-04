import matplotlib.pyplot as plt
import matplotlib.widgets as wd
import matplotlib
import networkx as nx
import rbtree as rbtree


class GUI:

    def __init__(self, tree):
        self.tree = tree

    def redraw(self, plt):
        plt.clf()
        self.draw()

    def draw(self):
        def _addKeyHandler(value):
            value = int(value)
            if not isinstance(value, int):
                print('Hey, {%s} should be int' % value)
            self.tree.insert(value)
            self.redraw(plt)

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
            nx.draw_networkx_nodes(G,pos,node_size=600,node_color=colors)
            nx.draw_networkx_edges(G,pos)
            nx.draw_networkx_labels(G,pos,labels,font_color='w')
        else:
            nx.draw_networkx_nodes(G,pos,node_size=600,node_color='r')
            nx.draw_networkx_edges(G,pos)
            nx.draw_networkx_labels(G,pos,labels)

        plt.axis('off')
        axbox = plt.axes([0.12, 0.03, 0.07, 0.05])
        key_field = wd.TextBox(axbox, 'Add key: ')
        # axbox2 = plt.axes([0.2, 0.03, 0.07, 0.05])
        # add_btn = wd.Button(axbox2, 'Add')
        # add_btn.on_clicked(_addBtnHandler)
        key_field.on_submit(_addKeyHandler)
        plt.show()

    def _get_pos_list(self, tree):
        """
        _get_pos_list(tree) -> Mapping. Produces a mapping
        of nodes as keys, and their coordinates for plotting
        as values. Since pyplot or networkx don't have built in
        methods for plotting binary search trees, this somewhat
        choppy method has to be used.
        """
        return self._get_pos_list_from(tree,tree.Root,{},0,(0,0),1.0)


    def _get_pos_list_from(self, tree,node,poslst,index,coords,gap):
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
            positions[0] = (0,0)
            positions = self._get_pos_list_from(tree,tree.Root.left,positions,1,(0,0),gap)
            positions = self._get_pos_list_from(tree,tree.Root.right,positions,1+tree.get_element_count(node.left),(0,0),gap)
            return positions
        elif node:
            if node.parent.right and node.parent.right.key == node.key:
                new_coords = (coords[0]+gap,coords[1]-1)
                positions[index] = new_coords
            else:
                new_coords = (coords[0]-gap,coords[1]-1)
                positions[index] = new_coords

            positions = self._get_pos_list_from(tree,node.left,positions,index+1,new_coords,gap/2)
            positions = self._get_pos_list_from(tree,node.right,positions,1+ index + tree.get_element_count(node.left), new_coords,gap/2)
            return positions
        else:
            return positions

    def _get_edge_list(self, tree):
        """
        _get_edge_list(tree) -> Sequence. Produces a sequence
        of tuples representing edges to be drawn.
        """
        return self._get_edge_list_from(tree,tree.Root,[],0)

    def _get_edge_list_from(self, tree,node,edgelst,index):
        """
        _get_edge_list_from(tree,node,edgelst,index) -> Sequence.
        Produces a sequence of tuples representing edges to be drawn.
        As stated before, index represents the index of node in
        a list of all Nodes in tree in preorder.
        """
        edges = edgelst

        if node and node.key == tree.Root.key:
            new_index = 1 + tree.get_element_count(node.left)

            if node.left:
                edges.append((0,1))
                edges = self._get_edge_list_from(tree,node.left,edges,1)
            if node.right:
                edges.append((0,new_index))
                edges = self._get_edge_list_from(tree,node.right,edges,new_index)

            return edges

        elif node:
            new_index = 1 + index + tree.get_element_count(node.left)

            if node.left:
                edges.append((index,index+1))
            if node.right:
                edges.append((index,new_index))

            edges = self._get_edge_list_from(tree,node.left,edges,index+1)
            edges = self._get_edge_list_from(tree,node.right,edges,new_index)
            return edges

        else:
            return edges

    def _get_label_list(self, tree):
        """
        _get_pos_list(tree) -> Mapping. Produces a mapping
        of nodes as keys, and their labels for plotting
        as values.
        """
        nodelist = self._preorder(tree)
        labellist = {}
        index = 0
        for node in nodelist:
            labellist[index] = node.key
            index = index + 1

        return labellist

    def _preorder(self, tree,*args):
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
            self._preorder(node.left,elements)
        if node.right:
            self._preorder(node.right,elements)

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
