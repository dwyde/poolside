$(document).ready(function(){
    var PATH_SEP = '/';
    var SERVER_ROOT = '';
    var DB_NAME = [SERVER_ROOT, 'notebook'].join(PATH_SEP);
    var EVAL_SERVER = [DB_NAME, '_service'].join(PATH_SEP);
    
    function append_cell() {
       var worksheet = $("div#worksheet");
       var cell = '<form class="cell" id="" method="POST"> \
       <input type="textarea" class="input" /> \
       <button type="submit">Evaluate</button> \
       <p class="output"></p> \
       </form>';
       worksheet.append(cell);
    }
    
    function ajax_json(params) {
        $.ajax({
            url: params['url'],
            data: params['data'],
            success: params['success'],
            global: false,
            contentType: 'application/json',
            type: "POST",
            processData: false,
            dataType: "json",
        });
    }
    
    function save_cell(id, input, output) {
        
    }
    
    function save_worksheet() {
        cell_ids = $("div#worksheet")
            .children(".cell")
            .map(function() {
                return this.id;
            }).get();
        
        //alert(cell_ids);
    }
    
    $("button#new").click(function(){
        append_cell();
    });
    
    $("form.cell").live('submit', function(){
        var form = $(this);
        var input = form.children(".input").val();
        
        var json_data = {
            'version': '1.1', 
            'method': '', 
            'params': input,
        };
        
        ajax_json({
            url: EVAL_SERVER, 
            data: JSON.stringify(json_data), 
            success: function(msg){
                var output = msg.result;
                form.children(".output").html(output);
                save_cell(form.attr("id"), input, output);
                save_worksheet();
            },
        });
        
        return false;
    });
    
    
    /** Start of code that is automatically executed */
    append_cell();
});
