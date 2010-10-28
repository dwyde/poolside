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
    
    function save_cell(id, input, output) {
        $.ajax({
            url: EVAL_SERVER, 
            data: JSON.stringify({
                method: 'save_cell', 
                params: {cell_id: id, input: input, output: output},
                version: JSON_VERSION, 
            }), 
            success: function(msg){
                if ($('#' + id).length == 0) {
                    alert('No cell with id ' + id);
                }
            },
        });
    }
    
    function save_worksheet() {
        cells = $('#worksheet')
            .children('.cell')
            .map(function() {
                return this.id;
            }).get();
        
        $.ajax({
            url: EVAL_SERVER, 
            data: JSON.stringify({
                'method': 'save_worksheet',
                'params': {'cell_list': cells, 'worksheet_id': WORKSHEET_NAME},
                'version': JSON_VERSION, 
            }),
        });
    }
    
    $('#add_cell').click(function(){
        $.ajax({
            url: EVAL_SERVER,
            data: JSON.stringify({
                'method': 'new_id',
                'params': {},
                'version': JSON_VERSION,
            }),
            success: function(msg){
                var id = msg.result;
                var cell = new_cell(id, '', '');
                $('#worksheet').append(cell);
                save_cell(id, '', '');
                save_worksheet();
            },
        });
    });

    $('button.delete').live('click', function(){
        var cell = $(this).parent();
        $.ajax({
            'url': EVAL_SERVER,
            'data': JSON.stringify({
                'method': 'delete_cell',
                'params': {'cell_id': cell.attr('id')},
                'version': JSON_VERSION,
            }),
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
        $.ajax({
            'url': EVAL_SERVER, 
            'data': JSON.stringify({
                'method': 'eval_python', 
                'params': {'input': input},
                'version': JSON_VERSION, 
            }),
            'success': function(msg){
                var output = (msg.result.output || '');
                form.children('.output').html(output);
                save_cell(form.attr('id'), input, output);
                save_worksheet();
            },
        });
        return false;
    });
});
