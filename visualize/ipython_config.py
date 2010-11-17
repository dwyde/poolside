import sys
sys.path.append('magic')

# Get the config being loaded so we can set attributes on it
c = get_config()

c.Global.extensions = [
    'viz_extension'
]
