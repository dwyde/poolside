    function new_cell(id, input, output) {
         var cell = '<form class="cell" id="' + id + '" method="POST"> \
         <button type="submit" class="evaluate">Evaluate</button> \
         <button class="delete">Delete</button> \
         <input type="textarea" class="input" value="' + 
         input.replace(/"/g, '&quot;') + '" /> \
         <div class="output"><iframe seamless sandbox="allow-scripts \
         allow-same-origin" src="../../_show/cell_out/' + 
         id +  '"></iframe></div></form>';
         
       
       return cell;
    }
