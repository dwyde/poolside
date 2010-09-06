import couchdb
from uuid import uuid4
from logic import Eval
from config import COUCH_SERVER, DATABASE

class Methods:
    def __init__(self):
        self.eval = Eval()
        couch = couchdb.Server(COUCH_SERVER)
        self.db = couch[DATABASE]

    def eval_python(self, params):
        cell_id = (params['cell_id'] or uuid4().hex)
        evaluated = self.eval.eval(params['input'])
        result = evaluated.replace('\n', '<br />')
        return {'output': result, 'cell_id': cell_id}

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
            
