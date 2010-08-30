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
        cell_id = params['cell_id']
        doc = {'input': params['input'], 'output': params['output'], 'type': 'cell'}
        try:
            self.db[cell_id].update(doc)
        except couchdb.client.ResourceNotFound:
            self.db[cell_id] = doc
        
        return 'cell saved'

    def save_worksheet(self, params):
        worksheet_id = params['worksheet_id']
        doc = {'cells': params['cell_list'], 'type': 'worksheet'}
        try:
            self.db[worksheet_id].update(doc)
        except couchdb.client.ResourceNotFound:
            self.db[worksheet_id] = doc

        return params['cell_list']
