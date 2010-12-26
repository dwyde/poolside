import couchdb
from uuid import uuid4
import zmq

from config import COUCH_SERVER, DATABASE, KERNEL_IP, KERNEL_PORT

class Methods:
    def __init__(self):
        couch = couchdb.Server(COUCH_SERVER)
        self.db = couch[DATABASE]

    def new_id(self, params):
        return uuid4().hex

    def save_cell(self, params):
        cell_id = params['cell_id']
        doc = self.doc_or_none(cell_id)
        if doc:
            doc['input'] = params['input']
            doc['output'] = params['output']
        else:
            doc = {'input': params['input'], 'output': params['output'], 
                'type': 'cell'}
        
        self.db[cell_id] = doc
        return 'cell saved'

    def save_worksheet(self, params):
        doc = {'cells': params['cell_list'], 'type': 'worksheet'}
        worksheet_id = params['worksheet_id']
        rev = self.rev_or_false(worksheet_id)
        if rev:
            doc['_rev'] = rev
        self.db[worksheet_id] = doc
   
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
 
    def doc_or_none(self, _id):
        try:
            return self.db[_id]
        except couchdb.client.ResourceNotFound:
            return None
