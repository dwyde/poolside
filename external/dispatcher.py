import sys
import json

from manager import KernelController
    
def requests():
    # 'for line in sys.stdin' won't work here
    line = sys.stdin.readline()
    while line:
        yield json.loads(line)
        line = sys.stdin.readline()
    
def respond(data={}, code=200, headers={'Content-Type': 'application/json'}):
    sys.stdout.write("%s\n" % json.dumps({"code": code, "json": data, "headers": headers}))
    sys.stdout.flush()
            
def main():
    controller = KernelController(respond)
    for req in requests():
        #respond(data={"qs": req["query"]})
        body = json.loads(req['body'])
        #respond(data={'output': body.get('input')})
        
        ##command = body.get('command')
        command = 'print "received!"'
        if command is not None:
            #worksheet_id = body.get('worksheet_id')
            worksheet_id = 'hello'
            #kernel = controller.get_or_create(worksheet_id,
            #                    writers=body.get('writers', []))
            kernel = controller.get_or_create('hello')
            kernel.execute(command)
        
if __name__ == "__main__":
    main()