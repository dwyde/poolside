function(head, req) {
    // !json templates.display.cell
    // !json templates.display.worksheet
    // !code vendor/couchapp/lib/mustache.js
    
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
            Mustache.to_html(templates.display.cell, {
                'input': row.doc['input'],
                'output': row.doc['output'],
            })
        );
    }
    
    send('\n</body>\n</html>');
}
