function(head, req) {
    // !json templates.display.nb_start
    // !json templates.display.nb_end
    // !code _attachments/new_cell.js
    
    start({
        'headers': {
            'Content-Type': 'text/html'
        }
    });
    
    send(templates.display.nb_start);
    
    var row,
<<<<<<< HEAD
        doc;
    while (row = getRow()) {
        doc = row.doc;
        if (doc) {
            send(
                new_cell(row.value._id, doc['input'], doc['output'])
=======
        output;
    while (row = getRow()) {
        if (row.doc) {
            output = row.doc['output'];
            send(
                new_cell(
                    row.value._id,
                    row.doc['input'],
                    (typeof output == 'object') ? toJSON(output) : output
                )
>>>>>>> standalone
            );
        }
    }
    
    send(templates.display.nb_end);
}
