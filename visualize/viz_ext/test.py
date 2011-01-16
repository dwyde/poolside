import os
import sys

from dec import VizDecor

@VizDecor({list: lambda x: True})
def table(obj):
    s = '<div><table class="viz_list"><tr>'
    for item in obj:
        s += '<td>'
        if isinstance(item, list):
            # Nested lists
            s += Viz(item)
        else:
            # One-dimensional
            s += '%s' % (str(item),)
        s += '</td>'
    s += '</tr></table></div>'
    return s

if __name__ == '__main__':
    a = range(5)
    b = ['a',[1,2],'b']
    print table(a)
    print table(b)
