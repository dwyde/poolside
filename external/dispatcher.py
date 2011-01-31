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
        
        command = body.get('content')
        worksheet_id = body.get('worksheet_id')
        
        if command and worksheet_id:
            #kernel = controller.get_or_create(worksheet_id,
            #                    writers=body.get('writers', []))
            kernel = controller.get_or_create(worksheet_id)
            kernel.execute(command)
        else:
            respond({'error': 'Parameters "content" and "worksheet_id" are \
required for Python requests.'}, code=400)
        
if __name__ == "__main__":
    main()