import couchdb


couch = couchdb.Server('http://localhost:59840/')
db = couch['nb']
db.create({'_id': 'cell_a', 'type': 'cell', 'input': '"hello"', 'output': 'hello'})
db.create({'_id': 'cell_b', 'type': 'cell', 'input': '1 + 1', 'output': '2'})
db.create({'_id': 'worksheet_1', 'type': 'worksheet', 'cells': ['cell_b', 'cell_a']})
