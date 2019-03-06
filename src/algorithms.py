from collections import deque
from util import draw_tree
from constants import SOLUTION_REQUIRED

class Node:
    def __init__ (self, name, children={}, parent=None):
        self.name     = name
        self._children = children
        self.parent   = parent

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

        if children:
            for child in children:
                child.parent = self

    def generate_tree(self):
        """
        Parse the nested node into dict
        """
        tree     = dict()
        current  = tree[self.name] = dict()
        friends  = current['friends'] = dict()
        children = self.children

        if children:
            for child in children:
                friends.update(child.generate_tree())
        return tree

class Algorithm:
    def __init__(self, root, goals=[], client=None):
        self.root = Node(root)
        self.goals = [Node(name) for name in goals]
        self.client = client

    def is_goal(self, node):
        """
        Check if the new user is in the goals set
        """
        return node in self.goals

    def get_children(self, node):
        children = self.client.get_friends(node.name)
        return [Node(child) for child in children]

    def bfs(self):
        # a FIFO to store current nodes
        processing_nodes = deque()
        visited_nodes    = dict()
        result_set       = list()

        root = self.root
        processing_nodes.append(root)

        while processing_nodes:
            print '-----------------------------------------'
            current_node     = processing_nodes.popleft()
            print 'Processing: %s' % current_node

            if visited_nodes.get(current_node.name):
                print 'User %s has been visited. Moving on' % current_node
                continue

            # Expand the tree to the next level of the children list
            children = self.get_children(current_node)

            print_tree(self.root)

            # pre-processing the children list. Check if duplicated then
            # deleting that node, otherwise, adding it to the tree
            for idx, child in enumerate(children):
                if visited_nodes.get(child.name):
                    del children[idx]
                else:
                    current_node.children = children
                    processing_nodes.append(child)

            visited_nodes[current_node.name] = True

            if self.is_goal(current_node):
                found_path = construct_path(current_node)
                result_set.append(found_path)
                if len(result_set) == SOLUTION_REQUIRED:
                    print_tree(tree.root)
                    return result_set


def print_tree(root):
    print 'Current tree: '
    print draw_tree(root.generate_tree())

def construct_path(node):
    path = list()
    path.append(node)
    while node.parent:
        node = node.parent
        path.append(node)
    path.reverse()
    print 'FOUND PATH: %s' % path
    return str(path)
