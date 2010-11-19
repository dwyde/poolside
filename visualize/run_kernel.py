'''
Start an IPython ZMQ kernel, customized with an additional magic function.
Derived from IPython.zmq.ipkernel.main()
'''

from IPython.zmq.ipkernel import Kernel
from IPython.zmq.entry_point import make_argument_parser, make_kernel, start_kernel
from IPython.zmq.iostream import OutStream

from viz_extension import load_ipython_extension

def main():
    # Parse command line arguments to check for user-specified ports.
    parser = make_argument_parser()
    namespace = parser.parse_args()
    
    # Create a kernel, and add a magic "Viz" visualization function to it.
    kernel = make_kernel(namespace, Kernel, OutStream)
    load_ipython_extension(kernel.shell)
    
    start_kernel(namespace, kernel)

if __name__ == '__main__':
    main()
