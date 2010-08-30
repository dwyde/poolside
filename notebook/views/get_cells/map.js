function(doc) {
    if (doc.type == 'worksheet') {
        for (var i in doc.cells) {
            emit([doc._id, i], {_id: doc.cells[i]});
        }
//        emit(doc._id, doc);
    }
}
