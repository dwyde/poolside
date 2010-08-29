from uuid import uuid4
from logic import Eval

class Methods:
    def __init__(self):
        self.eval = Eval()

    def eval_python(self, params):
        cell_id = (params['cell_id'] or uuid4().hex)
        evaluated = self.eval.eval(params['input'])
        result = evaluated.replace('\n', '<br />')
        return {'output': result, 'cell_id': cell_id}

    def save_cell(self, cell_id):
        return 'cell saved'

    def save_worksheet(self, worksheet_id):
        return 'worksheet saved'
