function(head, req) {
    // !json templates.cell.display
    // !code vendor/couchapp/lib/mustache.js
    
    start({
        'headers': {
            'Content-Type': 'text/html'
        }
    });
    
    var cells = [];
    var row;
    while (row = getRow()) {
        //send([row.doc['input'], row.doc['output']] + '\n');
        cells.push({'input': row.doc['input'], 'output': row.doc['output']});
    }
    
    send(
        Mustache.to_html(templates.cell.display, {
            cells : cells,
        })
    );
}
