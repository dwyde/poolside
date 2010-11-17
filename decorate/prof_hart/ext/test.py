import sys
sys.path.append('..')
from dec import VizDecor

def __protected(obj):
    return '***'

@VizDecor({list: lambda x:True})
def table(obj):
    s = '--'
    for i in obj:
        s+=str(i)+'\n-\n'
    return(s)

@VizDecor({str: lambda x: len(x)<10,
           list: lambda x: len(x)<10 })
def test(foo):
    return foo
