//
// Copyright 2011 David Wyde and Chris Hart.
//

/**
 * WS_CLIENT is a module for communicating with a Tornado WebSocket server
 * via a JSON-based API.
 */
var WS_CLIENT = (function() {
        /** A WebSocket connection object */
    var connection,
        /** Map a message from the server to an appropriate handler. */
        dispatch = {
            output: output_cell,
            new_id: assign_id
        };
    
    /** 
     * Update the content of a notebook cell.
     * @param response A JSON object containing a cell ID and text content.
     */
    function output_cell(response) {
        var cell_id = response.target;
        var text = response.content;
        if (cell_id) {
            var cell = $('#' + cell_id);
            cell.find('div.output iframe').contents().find('body').html(text);
        }
    }
    
    /** 
     * Upon receiving a UUID, add a new cell to this notebook. 
     * This function is called in response to a WebSocket message.
     */
    function assign_id(response) {
        var cell = $(new_cell(response.id, '', ''));
        cell.children('div.output').each(div_to_iframe);
        $('#worksheet').append(cell);
        save_worksheet();
    }
    
    /** Save an ordered list of this notebook's cells. */
    function save_worksheet() {
        var cells = $('#worksheet')
            .children('.cell')
            .map(function() {
                return this.id;
            }).get();
        connection.send(JSON.stringify({
            type: 'save_worksheet',
            id: WORKSHEET_NAME,
            cells: cells,
        }));
    }
    
    return {
        /** Initialize a WebSocket connection. */
        connect: function(address) {
            connection = new WebSocket('ws://' + address);
            connection.onmessage = function(event) {
                var result = JSON.parse(event.data);
                var type = result.type || null;
                if (type != null) {
                    dispatch[type](result);
                }
            };
            connection.onclose = function() {
                output_cell({
                    target: '__messages', 
                    content: 'WebSocket closed'
                });
            };
            connection.onerror = function(event) {
                output_cell(event);
            };
        },
        /** Request a new cell UUID from the server. */
        new_id: function() {
            connection.send(JSON.stringify({type: 'new_id'}));
        },
        save_worksheet: save_worksheet,
        /** Request deletion of a cell by the server. */
        delete_cell: function(id) {
            connection.send(JSON.stringify({
                type: 'delete_cell',
                id: id,
            }));
        },
        /** Send Python code to the server for execution. */
        python_request: function(input, cell_id) {
            connection.send(JSON.stringify({
                type: 'python',
                input: input,
                caller: cell_id,
            }));
        },
    };
}());
