/**
 * WS_CLIENT is a module for communicating with a Tornado WebSocket server
 * via a JSON-based API.
 */
var WS_CLIENT = (function() {
    /** A WebSocket connection object */
    var connection;
    
    /** 
     * Update the content of a notebook cell.
     * @param response A JSON object containing a cell ID and text content.
     */
    function output_cell(response) {
        var cell_id = response.target;
        var text = response.content;
        if (cell_id) {
            cell = $('#' + cell_id);
            cell.children('.output').html(text);
        }
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
    
    /** 
     * Upon receiving a UUID, add a new cell to this notebook. 
     * This function is called in response to a WebSocket message.
     */
    function assign_id(response) {
        var cell = new_cell(response.id, '', '');
        $('#worksheet').append(cell);
        save_worksheet();
    }
    
    return {
        /** Initialize a WebSocket connection. */
        connect: function(address) {
            connection = new WebSocket('ws://' + address);
            connection.onmessage = function(event) {
                var result = JSON.parse(event.data) || {};
                /** MAKE THIS INTO A DICTIONARY **/
                if (result.type == 'output') {
                    output_cell(result);
                } else if (result.type == 'new_id') {
                    assign_id(result);
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
