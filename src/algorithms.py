from collections import deque
from util import draw_tree
from constants import SOLUTION_REQUIRED, DEPTH
from config import target
from collections import OrderedDict as OD

def print_tree(root):
    print 'Current tree: '
    print draw_tree(root.generate_tree())


def construct_path(node):
    path = list()
    path.append(node.name)
    while node.parent:
        node = node.parent
        path.append(node.name)
    path.reverse()
    path.append(target)
    print 'FOUND PATH: %s' % path
    return str(path)


class Node(object):
    def __init__ (self, name, children={}, parent=None):
        self.name     = name
        self.children = children
        self.parent   = parent


    def __eq__(self, other):
        return self.name == other.name


    def __str__(self):
        return "%s [parent: %s; depth: %s]" % (
                self.name,
                self.parent.name if self.parent != None else "",
                self.get_depth())


    @property
    def children(self):
        return self._children


    @children.setter
    def children(self, children):
        self._children = children

        if self._children:
            for child in self._children:
                child.parent = self


    def generate_tree(self):
        """
        Parse the nested node into dict
        """
        tree     = OD()
        current  = tree[self.name] = OD()
        children = self.children

        if self.children:
            for child in self.children:
                current.update(child.generate_tree())
        return tree

    def get_depth(self):
        depth = 0
        node = self
        while node.parent:
            depth += 1
            node = node.parent

        return depth

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
        """
        Expanding the children of the node
        """
        children = self.client.get_friends(node.name)
        return [Node(child) for child in children]


    def bfs(self):
        """
        Using Breadth first search to explore the nodes
        """
        processing_nodes = deque()
        visited_nodes    = dict()
        result_set       = list()

        processing_nodes.appendleft(self.root)
        while processing_nodes:
            print '-----------------------------------------'
            current_node = processing_nodes.pop()
            print 'Processing: %s' % current_node
            if visited_nodes.get(current_node.name):
                print 'User %s has been visited. Moving on' % current_node
                continue
            if self.is_goal(current_node):
                found_path = construct_path(current_node)
                result_set.append(found_path)
                if len(result_set) == SOLUTION_REQUIRED:
                    print_tree(self.root)
                    return result_set
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
                    processing_nodes.appendleft(child)

            visited_nodes[current_node.name] = True


    def dfs(self):
        """
        Using Depth first search to explore the nodes
        """
        processing_nodes = deque()
        visited_nodes    = dict()
        result_set       = list()

        processing_nodes.append(self.root)
        while processing_nodes:
            print '-----------------------------------------'
            current_node = processing_nodes.pop()
            # result_set[current_node.name] = True
            print 'Processing: %s' % current_node
            if visited_nodes.get(current_node.name):
                print 'User %s has been visited. Moving on' % current_node
                continue
            if self.is_goal(current_node):
                found_path = construct_path(current_node)
                result_set.append(found_path)
                if len(result_set) == SOLUTION_REQUIRED:
                    print_tree(self.root)
                    return result_set

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
            # print result_set

