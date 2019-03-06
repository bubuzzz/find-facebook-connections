from algorithms import bfs, Tree
from config import target


if __name__ == '__main__':
    tree = Tree()
    tree.set_goals(target)
    results = bfs(tree)

    print '------------------------------------------'
    print "RESULT PATHS: %s\n" % '\n'.join(results)
    print '------------------------------------------'
