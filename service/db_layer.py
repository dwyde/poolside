#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

"""Use CouchDB as a storage backend for notebooks.
"""

import couchdb
from uuid import uuid4

def new_id():
    """Get a new UUID.
    
    Call this when a notebook cell is created.
    """
    
    return uuid4().hex

class Methods:
    def __init__(self, couch_port, database):
        couch = couchdb.Server('http://localhost:%d' % (couch_port,))
        self.db = couch[database]

    def save_cell(self, cell_id, fields):
        """Store notebook cell documents in CouchDB.
        
        .. warning:: There are **NO** security measures at the moment.  
        
            If a non-empty :class:`string` or :class:`unicode` is submitted 
            as the `cell_id`, it will be  accepted as the cell's ID. 
            
            This will be fixed, but it's a problem right now.
        
        :param cell_id: A cell's UUID, for both notebook frontends and CouchDB.
        :param fields: A :class:`dict` of key-value pairs to add to this \
            CouchDB document.
        
        If an empty string is provided as the `cell_id`, a new UUID is generated
        and a new cell created in the database.
        
        Other "incorrect" inputs will cause an immeidate return.
        """
        
        if not isinstance(cell_id, basestring):
            return
        elif cell_id == '':
            cell_id = new_id()
        try:
            doc = self.db[cell_id]
            for field, data in fields.iteritems():
                doc[field] = data
            if hasattr(doc, '_rev'):
                doc.update({'_rev': doc.rev, '_id': doc.id})
        except couchdb.client.ResourceNotFound:
            doc = {'input': fields.get('input', ''), 'output': '',
                   'type': 'cell'}
        
        self.db[cell_id] = doc

    def save_worksheet(self, worksheet_id, cell_list):
        """Save a worksheet into CouchDB.
        
        .. warning:: Two open instances of the same worksheet can overwrite \
        each other.
        
            The parameter `cell_list` is generated on the client side,
            and there are currently no locks on the CouchDB documents.
        
        :param worksheet_id: A worksheet document's UUID.
        :param cell_list: A list of cell UUIDs contained by this worksheet.
        """
        
        doc = {'cells': cell_list, 'type': 'worksheet'}
        try:
            existing = self.db[worksheet_id]
            doc['_rev'] = existing.rev
        except (couchdb.client.PreconditionFailed,
                couchdb.client.ResourceNotFound):
            pass

        self.db[worksheet_id] = doc
   
    def delete_cell(self, cell_id):
        """Delete a cell from CouchDB.
        
        .. warning:: Users can delete any cell, whether or not they own it.
        """
        cell = self.db[cell_id]
        if cell.get('type') == 'cell':
            self.db.delete(cell)
