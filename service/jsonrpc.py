import sys
import json
from rpc_methods import Methods

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
    rpc_methods = Methods()
    for req in requests():
        body = json.loads(req['body'])
        method = body['method']
        params = body['params']
        result = getattr(rpc_methods, method)(params)
        respond(data={'result': result}, headers={'Content-Type': 'text/json'})

if __name__ == "__main__":
    main()
