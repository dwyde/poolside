import dec
import types

@dec.VizDecor({types.ListType: lambda x:True})
def table(obj):
    s = '--'
    for i in obj:
        s+=str(i)+'\n-\n'
    return(s)


