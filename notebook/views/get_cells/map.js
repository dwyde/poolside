function(doc) {
    if (doc.type == 'worksheet') {
        for (var i in doc.cells) {
            emit([doc._id, parseInt(i)], {_id: doc.cells[i]});
        }
    }
}
