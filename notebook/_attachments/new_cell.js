    function new_cell(id, input, output) {
        var cell = '<div class="cell" id="' + id + '"><form method="POST"> \
         <button type="submit" class="evaluate">Evaluate</button> \
         <button class="delete">Delete</button> \
         <input type="textarea" class="input" value="' + 
         input.replace(/"/g, '&quot;') + '" /></form> \
         <div class="output"><iframe seamless sandbox="allow-scripts \
         allow-same-origin" src="../../_show/cell_out/' + 
         id +  '"></iframe></div></div>';
         
       
       return cell;
    }
