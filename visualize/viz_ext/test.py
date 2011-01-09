import os
import sys

from dec import VizDecor

@VizDecor({list: lambda x:True})
def table(obj):
    s = '<table><tr>\n'
    for i in obj:
        if isinstance(i, list):
            return obj
        else:
            s+=' <td>%s</td>\n'%(i)
    s+='</tr></table>'
    return(s)

if __name__ == '__main__':
    a = range(5)
    b = ['a', 'b', [5]]
    print table(a), '\n'
    print table(b)
