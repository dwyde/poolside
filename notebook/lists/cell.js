function(head, req) {
    // !json templates.display.nb_start
    // !json templates.display.nb_end
    // !code vendor/couchapp/lib/mustache.js
    // !code vendor/couchapp/mine/new_cell.js
    
    start({
        'headers': {
            'Content-Type': 'text/html'
        }
    });
    
    send(templates.display.nb_start);
    
    var row;
    while (row = getRow()) {
        send(
            new_cell(row.value._id, row.doc['input'], row.doc['output'])
        );
    }
    
    send(templates.display.nb_end);
}
