import sys
import json
from rpc_methods import method_dict
from logic import Eval

def requests():
    # 'for line in sys.stdin' won't work here
    line = sys.stdin.readline()
    while line:
        yield json.loads(line)
        line = sys.stdin.readline()

def respond(code=200, data={}, headers={}):
    sys.stdout.write("%s\n" % json.dumps({"code": code, "json": data, "headers": headers}))
    sys.stdout.flush()

def main():
    e = Eval()
    for req in requests():
        body = json.loads(req['body'])
        method = body['method']
        params = body['params']
        #result = method_dict[method](params)
        evaluated = e.eval(params)
        result = evaluated.replace('\n', '<br />')
        respond(data={'result': result}, headers={'Content-Type': 'text/json'})

if __name__ == "__main__":
    main()
