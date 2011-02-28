    function new_cell(id, input, output) {
        function html_escape(str) {
            if (typeof str == 'string') {  
                return str.replace(/&/g, '&amp;').replace(/>/g, '&gt;')
                        .replace(/</g, '&lt;').replace(/"/g, '&quot;')
                        .replace(/'/, '&#039;');
            } else {
                return str;
            }
        }
      
        return '<div class="cell" id="'+ html_escape(id) + '"> \
              <form method="POST"> \
                <button type="submit" class="text">txt</button> \
                <button type="submit" class="python">py</button> \
                <button type="submit" class="ruby">rb</button> \
                <button class="delete">X</button> \
                <textarea class="input">' + html_escape(input) + '</textarea> \
              </form> \
              <div class="output">' + html_escape(output) + '</div> \
            </div>';
    }
