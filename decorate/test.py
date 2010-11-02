import matplotlib
matplotlib.use('Agg')
import StringIO

def image_data(self, obj):
    imgdata = StringIO.StringIO()
    obj.savefig(imgdata, format='png')
    data = imgdata.getvalue()
    imgdata.close()
    return data

#matplotlib.pyplot.plot(range(10))
#print dir(matplotlib.pyplot)

class Visualize:
    def __call__(self, obj):
        obj_type = obj.__class__.__name__
        func = getattr(self, obj_type)
        return func(obj)
        
    def list(self, lst):
        html = ['<td>%s</td>' % (item,) for item in lst]
        return '<table>\n%s\n</table>' % ('\n'.join(html))
            
VIZ = Visualize()
lst = [5, 'hello', 3.3, [1, 2, 3, 4]]
print VIZ(lst)
