//
// Copyright 2011 David Wyde and Chris Hart.
//

var WS_ADDRESS = 'localhost:9996/notebook';
var path = window.location.pathname.split('/');
var WORKSHEET_NAME = path.pop();

/** Main JQuery code */
$(document).ready(function(){
    
  // Connect to the WebSocket server.
  WS_CLIENT.connect(WS_ADDRESS);
  
  /** Handler for submission of an input form. */
  $('.cell form').live('submit', function(){
    var input = $(this).children('.input').val();
    var id = $(this).parent().attr('id');
    WS_CLIENT.python_request(input, id);
    //$(this).children('.output').html('');

    // Prevent the actual submission of this form.
    return false;
  });
  
  /** Add a cell to this notebook. */
  $('#add_cell').click(function(){
    WS_CLIENT.new_id();
  });
  
  /** Delete a cell from this notebook. */
  $('button.delete').live('click', function(){
    var ans = confirm('Do you want to permanently delete this cell?');
    if (ans) {
      // Be careful if the HTML structure of cell "widgets" changes.
      var cell_id = $(this).parents('div.cell').attr('id'); /** Bad! */
      WS_CLIENT.delete_cell(cell_id);
      $('#' + cell_id).remove();
      WS_CLIENT.save_worksheet();
    }
    
    // Don't actually submit the form.
    return false;
  });
  
  
  $('div.output').each(function(){
      $(this).resizable({alsoResize: $(this).parent()});
  });
  
  /*$('#worksheet').each(function(){
    $(this).accordion({header: 'input.input'});
  });*/
});
