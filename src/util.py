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

# from asciitree import LeftAligned
# from collections import OrderedDict as OD

# tree = {
#     'asciitree':{
#         'sometimes': {
#             'you': {},
#             'just': {}
#         },
#         'want': { },
#         'a': {
#             'tree': {
#                 'in': {
#                     'your': {
#                     }
#                 },
#                 'terminal': { }
#             }
#         }
#     }
# }

# tr = LeftAligned()
# print(tr(tree))

