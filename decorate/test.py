import matplotlib
matplotlib.use('Agg')
import pylab
import StringIO

lookup = {}

class default:
    def __init__(self, *args):
        self.types = args
    
    def __call__(self, func):
        def modified(obj):
            for obj_type in self.types:
                lookup[obj_type] = func
            print lookup
            func(obj)
        return modified

class Visualize:
    def __call__(self, obj, **kwargs):
        mode = kwargs.get('mode', '')
        try:
            func = getattr(self, mode)
        except AttributeError:
            func = repr
        return func(obj)
    
    def image_data(self, image):
        imgdata = StringIO.StringIO()
        image.savefig(imgdata, format='png')
        data = imgdata.getvalue()
        imgdata.close()
        return data
    
    def html_table(self, lst):
        html = ['<td>%s</td>' % (item,) for item in lst]
        return '<table>\n%s\n</table>' % ('\n'.join(html))

def main():
    VIZ = Visualize()
    lst = [5, 'hello', 3.3, [1, 2, 3, 4]]

    def plot_test():
        t = pylab.arange(0.0, 2.0, 0.01)
        s = pylab.sin(2*pylab.pi*t)
        fig = pylab.figure()
        ax = fig.add_subplot(111)
        p = ax.plot(t, s, linewidth=1.0)
        pylab.grid(True)
        #pylab.show()
        return fig

    fig = plot_test()
    data = VIZ(fig, mode='image_data')
    f = open('ex.png', 'wb')
    f.write(data)
    f.close()


if __name__ == '__main__':
    main()
