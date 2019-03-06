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

from asciitree import LeftAligned
from collections import OrderedDict as OD

tree = {
    'asciitree': OD([
        ('sometimes',
            {'you': {}}),
        ('just',
            {'want': OD([
                ('to', {}),
                ('draw', {}),
            ])}),
        ('trees', {}),
        ('in', {
            'your': {
                'terminal': {}
            }
        })
    ])
}

tr = LeftAligned()
print(tr(tree))



from collections import OrderedDict as OD
from copy import deepcopy

from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_DOUBLE, BOX_BLANK

tr = LeftAligned()

# a basic tree
# OrderedDict is used in some places where node order is important, otherwise
# a normal dict is used for the sake of readabilitiy
tree = {
    'asciitree': OD([
        ('sometimes',
            {'you': {}}),
        ('just',
            {'want': OD([
                ('to', {}),
                ('draw', {}),
            ])}),
        ('trees', {}),
        ('in', {
            'your': {
                'terminal': {}
            }
        })
    ])
}

print(tr(tree))

# construct a more complex tree by copying the tree and grafting it onto itself
tree2 = deepcopy(tree)
tree2['asciitree']['trees'] = deepcopy(tree2['asciitree'])
print(tr(tree2))

# use a box style
box_tr = LeftAligned(draw=BoxStyle(gfx=BOX_DOUBLE, horiz_len=1))
print(box_tr(tree))

# more airy
air_tr = LeftAligned(draw=BoxStyle(gfx=BOX_BLANK,
                                   label_space=0,
                                   label_format='[{}]',
                                   indent=0))
print(air_tr(tree))
