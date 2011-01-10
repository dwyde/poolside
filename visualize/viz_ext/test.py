import os
import sys

from dec import VizDecor

TABLE_CELL = '  <td>%s</td>\n'

@VizDecor({list: lambda x:True})
def table(obj):
    s = '<table>\n'
    for row in obj:
        s += ' <tr>\n'
        if isinstance(row, list):
            for col in row:
                s += TABLE_CELL % (col,)
        else:
            s += TABLE_CELL % (row,)
        s += ' </tr>\n'
    s += '</table>'
    return s

if __name__ == '__main__':
    a = range(5)
    b = ['a', [1, 2], 'b']
    print table(a), '\n'
    print table(b)
