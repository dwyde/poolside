function(head, req) {
    start({
        'headers': {
            'Content-Type': 'text/html'
        }
    });
    
    var row;
    while (row = getRow()) {
        id = row.key;
        send(
            '<a href="nb/' + id + '">' + id + '</a> <br />\n'
        );
    }
}
