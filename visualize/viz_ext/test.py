import os
import sys

from dec import VizDecor

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
