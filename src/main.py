from algorithms import bfs, Tree
from constants import TARGET


if __name__ == '__main__':
    tree = Tree()
    tree.set_goals(TARGET)
    results = bfs(tree)

    print '------------------------------------------'
    print "RESULT PATHS: %s\n" % '\n'.join(results)
    print '------------------------------------------'
