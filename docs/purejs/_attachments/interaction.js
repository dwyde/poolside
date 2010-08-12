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
    
    function ajax_request(url, data, success) {
        $.ajax({
            global: false,
            contentType: 'application/json',
            type: "POST",
            processData: false,
            dataType: "json",
            url: url,
            data: data,
            success: success,
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
        
        ajax_request("/nb/_jsonrpc", JSON.stringify(json_data), function(msg){
            form.children(".output").html(msg.result);
        });
        
        return false;
    });
    
    
    /** Start of code that is automatically executed */
    append_cell();
});
