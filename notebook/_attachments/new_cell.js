    function new_cell(id, input, output) {
        var cell = '<div class="cell" id="' + id + '"><form method="POST"> \
         <button type="submit" class="evaluate">Evaluate</button> \
         <button class="delete">Delete</button> \
         <input type="textarea" class="input" value="' + 
         input.replace(/"/g, '&quot;') + '" /></form> \
         <div class="output">' + output + '</div></div>';
         
       
       return cell;
    }
