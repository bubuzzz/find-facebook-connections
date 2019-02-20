from collections import deque


def bfs(tree):
    # a FIFO to store current nodes
    processing_nodes = deque()

    visited_nodes = dict()

    parent_map = dict()

    result_set = list()

    root = tree.get_root()
    processing_nodes.append(root)

    while processing_nodes:
        current_node = processing_nodes.popleft()
        if visited_nodes.get(current_node.get('username')):
            continue

        print('processing: ', current_node.get('username'))    

        if tree.is_goal(current_node.get('username')):
            found_path = construct_path(current_node.get('username'), parent_map)
            result_set.append(found_path)
            if len(result_set) == tree.solution_required:
                return result_set

        for child in tree.get_children(current_node.get('username')):
            # print('--child: ', child)
            if visited_nodes.get(child.get('username')):
                continue
            else:
                parent_map[child.get('username')] = current_node.get('username')
                processing_nodes.append(child)

        visited_nodes[current_node.get('username')] = True


def construct_path(node_id, parent_map):
    path = list()
    path.append(node_id)
    while parent_map.get(node_id):
        node_id = parent_map[node_id]
        path.append(node_id)
    path.reverse()
    print('found path: ', path)
    return path
