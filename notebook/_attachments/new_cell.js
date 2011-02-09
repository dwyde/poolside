    function new_cell(id, input, output) {
        function html_escape(str) {
            if (typeof str == 'string') {  
                return str.replace(/&/g, '&amp;').replace(/>/g, '&gt;').replace(/</g, '&lt;');
            } else {
                return str;
            }
        }
        
        function unquote(str) {
            if (typeof str == 'string') {
                return str.replace(/"/g, '&quot;').replace(/'/, '&#039;');
            } else {
                return str;
            }
        }
      
        return '<div class="cell" id="'+ unquote(id) + '"> \
              <form method="POST"> \
                <button type="submit" class="evaluate">Evaluate</button> \
                <button class="delete">Delete</button> \
                <textarea class="input">' + html_escape(input) + '</textarea> \
              </form> \
              <div class="output">' + html_escape(output) + '</div> \
            </div>';
    }
