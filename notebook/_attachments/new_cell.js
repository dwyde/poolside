    function new_cell(id, input, output) {
         var cell = '<form class="cell" id="' + id + '" method="POST"> \
         <input type="textarea" class="input" value="' + 
         input.replace(/"/g, '&quot;') + '" /> \
         <button type="submit">Evaluate</button> \
         <button class="delete">Delete</button> \
         <div class="output">' + output + '</div> \
         </form>';
       
       return cell;
    }

/** */
function div_to_iframe() {
    content = '<p>' + this.innerHTML + '</p>';
    iframe = $('<iframe seamless sandbox="allow-same-origin allow-scripts"></iframe>').load(function(){
        $(this).contents().find('body').append(content);
    });
    $(this).wrapInner(iframe);
}