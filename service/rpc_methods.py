import couchdb
from uuid import uuid4
from logic import Eval
from config import COUCH_SERVER, DATABASE

class Methods:
    def __init__(self):
        self.eval = Eval()
        couch = couchdb.Server(COUCH_SERVER)
        self.db = couch[DATABASE]

#    def eval_python(self, params):
#        cell_id = (params['cell_id'] or uuid4().hex)
#        evaluated = self.eval.eval(params['input'])
#        result = evaluated.replace('\n', '<br />')
#        return {'output': result, 'cell_id': cell_id}

    def eval_python(self, params):
        import zmq

        MESSAGE = {
#        'content': {'code': "print 'hello'"},
        'content': {'code': params['input']},
        'header': {'msg_id': 123},
        'msg_type': 'execute_request',
        }

        # Defaults
        ip = '127.0.0.1'
        port_base = 5575
        connection = ('tcp://%s' % ip) + ':%i'
        req_conn = connection % port_base
        sub_conn = connection % (port_base+1)

        # Create initial sockets
        c = zmq.Context()
        request_socket = c.socket(zmq.XREQ)
        request_socket.connect(req_conn)

        sub_socket = c.socket(zmq.SUB)
        sub_socket.connect(sub_conn)
        sub_socket.setsockopt(zmq.SUBSCRIBE, '')

        request_socket.send_json(MESSAGE)
        sub_socket.recv_json() # ignore the printing of our input message
        output = sub_socket.recv_json()

        return {'output': output['content']['data'], 'cell_id': params['cell_id']}

    def save_cell(self, params):
        doc = {'input': params['input'], 'output': params['output'], 
                'type': 'cell'}
        cell_id = params['cell_id']
        rev = self.rev_or_false(cell_id)
        if rev:
            doc['_rev'] = rev
        self.db[cell_id] = doc
        
        return 'cell saved'

    def save_worksheet(self, params):
        doc = {'cells': params['cell_list'], 'type': 'worksheet'}
        worksheet_id = params['worksheet_id']
        rev = self.rev_or_false(worksheet_id)
        if rev:
            doc['_rev'] = rev
        self.db[worksheet_id] = doc
        
        return params['cell_list']
   
    def delete_cell(self, params):
        cell_id = params['cell_id']
        cell = self.db[cell_id]
        deleted = self.db.delete(cell)
        return deleted
 
    def rev_or_false(self, _id):
        try:
            return self.db[_id].rev
        except couchdb.client.ResourceNotFound:
            return False
            
