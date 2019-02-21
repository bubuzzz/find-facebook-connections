tree = {
    'a' : {
        'friends': {
            'b': {
                'friends': {
                }
            },
            'c': {
                'friends': {
                    'd': {'friends': {}},
                    'e': {'friends': {
                        'f': {'friends' : {}}
                    }}
                }
            }
        }
    }
}

step = "   "
def draw_tree(tree={}, s="", level=0):
    s = [
        '%s+--%s\n%s' % (step * level, k, draw_tree(tree[k]['friends'], level=level + 1))
        for k in tree.keys()
    ]
    return ''.join(s)

