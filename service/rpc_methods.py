import couchdb
from uuid import uuid4

from config import COUCH_SERVER, DATABASE


def new_id():
    return uuid4().hex

class Methods:
    def __init__(self):
        couch = couchdb.Server(COUCH_SERVER)
        self.db = couch[DATABASE]

    def save_cell(self, cell_id, fields):
        if not isinstance(cell_id, basestring) or cell_id == '':
            cell_id = new_id()
            print cell_id
        try:
            doc = self.db[cell_id]
            for field, data in fields.iteritems():
                doc[field] = data
            if hasattr(doc, '_rev'):
                doc.update({'_rev': doc.rev})
        except couchdb.client.ResourceNotFound:
            doc = {'input': fields.get('input', ''), 'output': '',
                   'type': 'cell'}
        
        self.db[cell_id] = doc

    def save_worksheet(self, worksheet_id, cell_list):
        doc = {'cells': cell_list, 'type': 'worksheet'}
        try:
            existing = self.db[worksheet_id]
            doc['_rev'] = existing.rev
        except couchdb.client.PreconditionFailed:
            pass
        except couchdb.client.ResourceNotFound:
            pass
            
        self.db[worksheet_id] = doc
   
    def delete_cell(self, params):
        cell_id = params['cell_id']
        cell = self.db[cell_id]
        deleted = self.db.delete(cell)
        return deleted
