function(doc) {
    if (doc.type == 'worksheet') {
        emit(doc._id, null);
    }
}
