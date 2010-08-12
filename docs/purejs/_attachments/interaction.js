$(document).ready(function(){
    var PATH_SEP = '/'
    var DB_NAME = PATH_SEP + 'nb'
    var EVAL_SERVER = [DB_NAME, '_jsonrpc'].join(PATH_SEP)
    
    function append_cell() {
       var worksheet = $("div#worksheet");
       var cell = '<form class="cell" method="POST"> \
       <input type="textarea" class="input" /> \
       <button type="submit">Evaluate</button> \
       <p class="output"></p> \
       </form>';
       //cell_count += 1;
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
    
    /*function save_cell() {
        ajax_json({
            url: ,
            data: ,
            success: ,
        });
    }*/
    
    function save_worksheet() {
        
    }
    
    $("button#new").click(function(){
        append_cell();
    });
    
    $("form.cell").live('submit', function(){
        var form = $(this);
        var data = form.children(".input").val();
        
        var json_data = {
            'version': '1.1', 
            'method': '', 
            'params': data,
        };
        
        ajax_json({
            url: EVAL_SERVER, 
            data: JSON.stringify(json_data), 
            success: function(msg){
                form.children(".output").html(msg.result);
                save_cell();
                save_worksheet();
            },
        });
        
        return false;
    });
    
    
    /** Start of code that is automatically executed */
    append_cell();
});
