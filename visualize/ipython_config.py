import sys

# IPython needs to find its extension files.
sys.path.append('magic')

# Get the config being loaded so we can set its attributes.
c = get_config()

c.Global.extensions = [
    'viz_extension'
]
