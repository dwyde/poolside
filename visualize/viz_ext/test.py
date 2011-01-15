import os
import sys
import json

from dec import VizDecor

@VizDecor({list: lambda x:True})
def table(obj):
    s = '<div><table class="viz_list"><tr><br>'
    for item in obj:
        s += '<td>'
        if isinstance(item,list):
            # two dimensional
            s += Viz(item)
        else:
            # still one dimensional
            s += '%s'%(str(item))
        s += '</td>'
    s+='</tr></table></div></br>'
    return(s)

#@VizDecor({dict: lambda x:True})

if __name__ == '__main__':
    a = range(5)
    b = ['a',[1,2],'b']
    print table(a)
    print table(b)
