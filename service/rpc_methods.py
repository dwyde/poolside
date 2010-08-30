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
        doc = {'_id': cell_id, 'input': params['input'],
                'output': params['output'], 'type': 'cell'}
        return self.db.save(doc)

    def save_worksheet(self, params):
        worksheet_id = params['worksheet_id']
        doc = {'_id': worksheet_id, 'cells': params['cell_list'],
                'type': 'worksheet'}
        return self.db.save(doc)
