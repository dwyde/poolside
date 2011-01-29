function(doc, req) {
    // !code _attachments/mustache.js
    // !json templates.display.iframe_cell
    
    
    var output = {
        'output': doc.output.replace(/\n/g, '') || '',
    };
    
    return {
        "headers" : {"Content-Type" : "text/html"},
        "body" : Mustache.to_html(templates.display.iframe_cell, output),
    }
}
 