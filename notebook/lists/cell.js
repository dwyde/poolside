function(head, req) {
    // !json templates.display.nb_start
    // !json templates.display.nb_end
    // !code _attachments/mustache.js
    // !code _attachments/new_cell.js
    
    start({
        'headers': {
            'Content-Type': 'text/html'
        }
    });
    
    send(templates.display.nb_start);
    
    var row,
        doc;
    while (row = getRow()) {
        doc = row.doc;
        if (doc) {
            send(
                new_cell(row.value._id, doc['input'], doc['output'])
            );
        }
    }
    
    send(templates.display.nb_end);
}
