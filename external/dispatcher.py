import sys
import json

    
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
    for req in requests():
        #respond(data={"qs": req["query"]})
        respond(data={"qs": 'hello!'}, headers={'Content-Type': 'application/json'})
        
if __name__ == "__main__":
    main()