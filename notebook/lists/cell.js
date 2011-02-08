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
    
    var row,
        output;
    while (row = getRow()) {
        if (row.doc) {
            output = row.doc['output'];
            var data = {
                id: row.value._id,
                input: row.doc['input'],
                output: (typeof output == 'object') ? toJSON(output) : output,
            };
            send(
                Mustache.to_html(templates.display.new_cell, data)
            );
        }
    }
    
    send(templates.display.nb_end);
}
