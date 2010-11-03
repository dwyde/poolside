import matplotlib
matplotlib.use('Agg')
import StringIO

from decorate import allows, ALL

def image_data(self, obj):
    imgdata = StringIO.StringIO()
    obj.savefig(imgdata, format='png')
    data = imgdata.getvalue()
    imgdata.close()
    return data

#matplotlib.pyplot.plot(range(10))
#print dir(matplotlib.pyplot)

class Visualize:
    @allows(basestring)
    def html_table(self, lst):
        html = ['<td>%s</td>' % (item,) for item in lst]
        return '<table>\n%s\n</table>' % ('\n'.join(html))
            
VIZ = Visualize()
lst = [5, 'hello', 3.3, [1, 2, 3, 4]]
print VIZ.html_table(lst)
