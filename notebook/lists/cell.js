function(head, req) {
    // !json templates.display.nb_start
    // !json templates.display.nb_end
    // !json templates.display.new_cell
    // !code _attachments/mustache.js
    
    start({
        'headers': {
            'Content-Type': 'text/html'
        }
    });
    
    send(templates.display.nb_start);
    
    var row;
    while (row = getRow()) {
        if (row.doc) {
            var data = {
                id: row.value._id,
                input: row.doc['input'],
                output: row.doc['output'],
            };
            send(
                Mustache.to_html(templates.display.new_cell, data)
            );
        }
    }
    
    send(templates.display.nb_end);
}
