function(doc, req) {
    // !code _attachments/mustache.js
    // !json templates.display.iframe_cell
    // !json templates.display.output_plain
    
    var output = doc.output || '';
    //var output = toJSON(raw_output);
    
    
    // JSON object => HTML visualization
    // not sure why "instanceof" doesn't seem to work
    if ((typeof output) == 'object') { 
        var data = {
            'output': toJSON(output).replace(/\\/g, '\\\\').replace(/'/, "\\'")
                                    //.replace(/</, '&gt;'),
        };
        
        return {
            "headers" : {"Content-Type" : "text/html"},
            "body" : Mustache.to_html(templates.display.iframe_cell, data),
        }
    }
    // Plain JSON
    else {
        var data = {
            'output': output,
        };
        
        return {
            "headers" : {"Content-Type" : "text/html"},
            "body" : Mustache.to_html(templates.display.output_plain, data),
        }
    }
}
