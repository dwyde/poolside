function(doc, req) {
    // !code _attachments/mustache.js
    // !json templates.display.iframe_cell
    
    var cellOut = doc.output.replace(/"/g, '\\"').replace(/\n/g, '')
                .replace(/</g, '&lt;') || '';

    var output = {
        'output': cellOut,
    };
    
    return {
        "headers" : {"Content-Type" : "text/html"},
        "body" : Mustache.to_html(templates.display.iframe_cell, output),
    }
}
 