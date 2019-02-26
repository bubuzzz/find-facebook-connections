from collections import deque
from util import draw_tree
from constants import SOLUTION_REQUIRED

def print_tree(tree):
    print 'Current tree: '
    print draw_tree(tree.get_root().generate_tree())

def bfs(tree):
    # a FIFO to store current nodes
    processing_nodes = deque()
    visited_nodes    = dict()
    parent_map       = dict()
    result_set       = list()

    root = tree.get_root()
    processing_nodes.append(root)

    while processing_nodes:
        print '-----------------------------------------'
        current_node     = processing_nodes.popleft()
        current_username = current_node.username
        print 'Processing: %s' % current_username

        if visited_nodes.get(current_username):
            print 'User %s has been visited. Moving on' % current_username
            continue

        # Expand the tree to the next level of the children list
        children = tree.get_children(current_username)

        print_tree(tree)

        for idx, child in enumerate(children):
            # if any child already in the visited nodes, remove that child
            # from the children list
            if visited_nodes.get(child.username):
                del children[idx]
            else:
                parent_map[child.username] = current_username
                processing_nodes.append(child)
                current_node.children = children

        visited_nodes[current_username] = True

        if tree.is_goal(current_username):
            found_path = construct_path(current_username, parent_map)
            result_set.append(found_path)
            if len(result_set) == SOLUTION_REQUIRED:
                print_tree(tree)
                return result_set


def construct_path(node_id, parent_map):
    path = list()
    path.append(node_id)
    while parent_map.get(node_id):
        node_id = parent_map[node_id]
        path.append(node_id)
    path.reverse()
    print 'FOUND PATH: %s' % path
    return str(path)
