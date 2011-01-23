function(doc, req) {
    // !json templates.display.iframe_cell
    
    
    
    send(templates.display.iframe_cell);
    
    var output = doc.output || '';
    
    send(output + '</body></html>');
}