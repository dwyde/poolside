    function new_cell(id, input, output) {
         var cell = '<form class="cell" id="' + id + '" method="POST"> \
         <input type="textarea" class="input" value="' + 
         input.replace(/"/g, '&quot;') + '" /> \
         <button type="submit">Evaluate</button> \
         <button class="delete">Delete</button> \
         <div class="output"><iframe sandbox="allow-scripts \
         allow-same-origin" src="../../_show/cell_out/' + 
         id +  '"></iframe></div></form>';
       
       return cell;
    }
