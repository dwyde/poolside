$(document).ready(function(){
    $("button#new").click(function(){
        append_cell();
    });
    
    $("button#delete").click(function(){
        var worksheet = $("input[@id=worksheet]:checked").val();
        if (worksheet != undefined) {
            var accepted = confirm("Are you sure you want to delete worksheet \"" + worksheet + "\"?");
            if (accepted) {
                $("form#worksheet_action input#action").val('delete');
                $("form#worksheet_action").submit();
            }
        }
    });
    
    $("button#copy").click(function(){
        var worksheet = $("input[@id=worksheet]:checked").val();
        if (worksheet != undefined) {
            var name = prompt("Please enter a name for the new worksheet.");
            if (name != undefined) {
                $("form#worksheet_action input#action").val('copy');
                $("form#worksheet_action input#new_name").val(name);
                $("form#worksheet_action").submit();
            }
        }
    });
    
    function append_cell() {
       var worksheet = $("div#worksheet");
       var cell = '<div class="cell"> \
       <input type="textarea" /> \
       <button>Submit</button> \
       </div>';
       //cell_count += 1;
       worksheet.append(cell);
    }
    
    $("div.cell button").live('click', function(){
        var json_data = {
            'version': '1.1', 
            'method': 'save_cell', 
            'params': 'param string',
        }
        
        $.ajax({
          url: "/nb/_jsonrpc",
          global: false,
          contentType: 'application/json',
          type: "POST",
          processData: false,
          data: JSON.stringify(json_data),
          dataType: "json",
          async:false,
          success: function(msg){
             alert(msg.result);
          }
       });
    });
});
