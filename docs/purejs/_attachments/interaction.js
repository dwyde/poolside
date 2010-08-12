$(document).ready(function(){
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
    
    function ajax_request(params) {
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
        
        ajax_request({
            url: "/nb/_jsonrpc", 
            data: JSON.stringify(json_data), 
            success: function(msg){
                form.children(".output").html(msg.result);
            },
        });
        
        return false;
    });
    
    
    /** Start of code that is automatically executed */
    append_cell();
});
