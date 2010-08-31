function(head, req) {
    // !json templates.display.cell
    // !json templates.display.worksheet
    // !code vendor/couchapp/lib/mustache.js
    // !code vendor/couchapp/mine/new_cell.js
    
    start({
        'headers': {
            'Content-Type': 'text/html'
        }
    });
    
    send(
        Mustache.to_html(templates.display.worksheet)
    );
    
    var row;
    while (row = getRow()) {
        send(
            new_cell(row.doc['input'], row.doc['output'])
        );
    }
    
    send('\n</body>\n</html>');
}
