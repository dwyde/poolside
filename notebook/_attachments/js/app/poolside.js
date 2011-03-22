/*
 * Main JQuery code: attach functions to DOM elements as JQuery handlers.
 */
$(document).ready(function(){
  // Create a Notebook instance.
  var notebook = new Notebook();
  
  // Initialize future Requests.
  Request._init_once(notebook.worksheet_name);
  
  /** Prevent the actual submission of cell forms. */
  $('.cell form').live('submit', function(){
      return false;
  });
  
  /** Attach a handler to the "Add cell" button. */
  $('#add_cell').click(function(){
    notebook.add_cell();
  });
  
  /** Delete a cell from this notebook. */
  $('button.delete').live('click', function(){
    var ans = confirm('Do you want to permanently delete this cell?');
    if (ans) {
      // Be careful if the HTML structure of cell "widgets" changes.
      var id = $(this).parents('div.cell').attr('id');
      notebook.delete_cell(id);
    }

    // Don't actually submit the form.
    return false;
  });
  
  /** React to one of the cell submission buttons being clicked. */
  $('.cell form button').live('click', function(){
    var cell_id = $(this).parents('div.cell').attr('id');
    var input = $(this).siblings('.input').val();
    var type = $(this).attr('class');
    var req = new Request(type, cell_id);
    
    // Execute the request, with a callback to save the cell.
    req.execute(input, function(output){
      notebook.save_cell(new Cell({
        cell_id: cell_id,
        input: input,
        output: output,
        type: type,
      }))
    });
  });
});
