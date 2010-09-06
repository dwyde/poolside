$(document).ready(function(){
    var PATH_SEP = '/';
    var SERVER_ROOT = '';
    var DB_NAME = [SERVER_ROOT, 'notebook'].join(PATH_SEP);
    var EVAL_SERVER = [DB_NAME, '_service'].join(PATH_SEP);

    var HARDCODED_NAME = 'example';
    
    function ajax_json(params) {
        $.ajax({
            'url': params['url'],
            'data': params['data'],
            'success': params['success'],
            'global': false,
            'contentType': 'application/json',
            'type': 'POST',
            'processData': false,
            'dataType': 'json',
        });
    }
    
    function save_cell(id, input, output) {
        var json_data = {
            'version': '1.1', 
            'method': 'save_cell', 
            'params': {'cell_id': id, 'input': input, 'output': output},
        };

        ajax_json({
            url: EVAL_SERVER, 
            data: JSON.stringify(json_data), 
            success: function(msg){
                if ($('#' + id).length == 0) {
                    alert('No cell with id ' + id);
                }
            },
        });
    }
    
    function save_worksheet() {
        cell_list = $('div#worksheet')
            .children('.cell')
            .map(function() {
                return this.id;
            }).get();
        
        var json_data = {
            'version': '1.1', 
            'method': 'save_worksheet',
            'params': {'cell_list': cell_list, 'worksheet_id': HARDCODED_NAME},
        };
        
        ajax_json({
            url: EVAL_SERVER, 
            data: JSON.stringify(json_data), 
            success: function(msg){
            },
        });
    }
    
    $('button#add_cell').click(function(){
	// In an external file, to be shared with a list function.
        var cell = new_cell('', '', '');
        $('#worksheet').append(cell);
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
            url: EVAL_SERVER, 
            data: JSON.stringify(json_data), 
            success: function(msg){
                var cell_id = msg.result.cell_id;
                form.attr('id', cell_id);
                var output = msg.result.output;
                form.children('.output').html(output);
                save_cell(cell_id, input, output);
                save_worksheet();
            },
        });
        
        return false;
    });
    
    
    /** Start of code that is automatically executed */
//    new_cell(id, input, output);
});
