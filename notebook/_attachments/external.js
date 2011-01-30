/** Main JQuery code */
$(document).ready(function(){
    var location = window.location;
    var path = location.pathname.split('/');
    const WORKSHEET_NAME = path.pop();
    const DB_NAME = path[1];
    const ENDPOINT = [location.protocol + '/', location.host, DB_NAME, '_server']
            .join('/');
    //var DB = $.couch.db(DB_NAME);
            
    function compute_request(cell_id, input) {
        $.ajax({
            url: ENDPOINT,
            data: {
                input: input,
            },
            success: function(msg){
                iframe = $('#' + cell_id)
                    .find('div.output iframe')
                    .each(function(){
                        this.contentWindow.location.reload(true);
                    });
            },
            global: false,
            contentType: 'application/json',
            type: 'POST',
            processData: false,
            dataType: 'json',
        });
    }
    
    /** Save an ordered list of this notebook's cells. */
    function save_worksheet() {
        var cells = $('#worksheet')
        .children('.cell')
        .map(function() {
            return this.id;
        }).get();
        connection.send(JSON.stringify({
            type: 'save_worksheet',
            id: WORKSHEET_NAME,
            cells: cells,
        }));
    }
    
    /** Handler for submission of an input form. */
    $('.cell form').live('submit', function(){
        var input = $(this).children('.input').val();
        var id = $(this).parent().attr('id');
        compute_request(id, input);

        // Prevent the actual submission of this form.
        return false;
    });
  
  /** Add a cell to this notebook. */
    $('#add_cell').click(function(){
        $.couch.db(DB_NAME).saveDoc({}, {
            success: function(doc){
                var cell_text = new_cell(doc.id, '', '');
                var cell = $(cell_text);
                cell.children('.output').resizable({alsoResize: cell});
                $('#worksheet').append(cell);
            },
        });
    });
  
  /** Delete a cell from this notebook. */
  $('button.delete').live('click', function(){
    var ans = confirm('Do you want to permanently delete this cell?');
    if (ans) {
      // Be careful if the HTML structure of cell "widgets" changes.
      var cell_id = $(this).parents('div.cell').attr('id');
      WS_CLIENT.delete_cell(cell_id);
      $('#' + cell_id).remove();
      WS_CLIENT.save_worksheet();
    }
    
    // Don't actually submit the form.
    return false;
  });
  
  /** Make output iframes resizable, using JQuery UI. */
  $('div.output').each(function(){
    $(this).resizable({alsoResize: $(this).parent()});
  });
});
