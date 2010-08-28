from logic import Eval

class Methods:
    def __init__(self):
        self.eval = Eval()

    def eval_python(self, params):
        evaluated = self.eval.eval(params)
        return evaluated.replace('\n', '<br />')

    def save_cell(self, cell_id):
        return 'cell saved'

    def save_worksheet(self, worksheet_id):
        return 'worksheet saved'
