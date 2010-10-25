$(document).ready(function(){
    var PATH_SEP = '/';
    var SERVER_ROOT = '';
    var DB_NAME = [SERVER_ROOT, 'notebook'].join(PATH_SEP);
    var EVAL_SERVER = [DB_NAME, '_service'].join(PATH_SEP);

    var WORKSHEET_NAME = window.location.pathname.split('/').pop();
    var JSON_VERSION = '1.1';
    
    $.ajaxSetup({
        'global': false,
        'contentType': 'application/json',
        'type': 'POST',
        'processData': false,
        'dataType': 'json',
    });
    
    /*
     * Worksheet
     */
    function Worksheet() {
        this.cells = new Array();
    }
    
    Worksheet.prototype.append = function() {
        var cell = new Cell();
        cell.save();
        this.cells.push(cell);
        this.save();
    };
    
    Worksheet.prototype.save = function() {
        worksheet = this;
        $.ajax({
            url: EVAL_SERVER, 
            data: JSON.stringify({
                'method': 'save_worksheet',
                'params': {
                    'cell_list': $.map(worksheet.cells, function() {
                        return this.id;
                    }),
                    'worksheet_id': WORKSHEET_NAME,
                },
                'version': JSON_VERSION, 
            }), 
            //success: function(msg){
            //},
        });
    };
    
    /*
     * Cell
     */
    function Cell(id, input, output) {
        this.id = id || '';
        this.input = input || '';
        this.output = output || '';
    }
    
    Cell.prototype.save = function() {
        cell = this;
        $.ajax({
            'url': EVAL_SERVER,
            'data': JSON.stringify({
                'method': 'save_cell', 
                'params': {
                    'cell_id': cell.id,
                    'input': cell.input,
                    'output': cell.output
                },
                'version': JSON_VERSION, 
            }),
            success: function(msg){ // UNNEEDED
                if ($('#' + id).length == 0) {
                    alert('No cell with id ' + id);
                }
            },
        });
    }
    
    $('button#add_cell').click(function(){
	// In an external file, to be shared with a list function.
        var cell = new_cell('', '', '');
        $('#worksheet').append(cell);
    });

    $('.cell .delete').live('click', function(){
        var cell = $(this).parent();
        var json_data = {
            'version': '1.1',
            'method': 'delete_cell',
            'params': {'cell_id': cell.attr('id')},
        }
        
        ajax_json({
            'url': EVAL_SERVER,
            'data': JSON.stringify(json_data),
            'success': function(msg){
                cell.remove();
                save_worksheet();
            },
        });
        return false;
    });
 
    $('form.cell').live('submit', function(){
        var form = $(this);
        var input = form.children('.input').val();
        
        var json_data = {
            'version': '1.1', 
            'method': 'eval_python', 
            'params': {'cell_id': form.attr('id'), 'input': input},
        };
        
        ajax_json({
            'url': EVAL_SERVER, 
            'data': JSON.stringify(json_data), 
            'success': function(msg){
                var cell_id = msg.result.cell_id;
                form.attr('id', cell_id);
                var output = (msg.result.output || '');
                form.children('.output').html(output);
                save_cell(cell_id, input, output);
                save_worksheet();
            },
        });
        
        return false;
    });
});
