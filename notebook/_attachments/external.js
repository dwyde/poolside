var COUCH = (function() {
    // Private variables
    var worksheet_name,
        endpoint,
        database;
    
    // Private functions
        
    /** Initialize data structures based on the current URL. */
    $(function() {
        var location = window.location;
        var path = location.pathname.split('/');
        var db_name = path[1];
        worksheet_name = path.pop();
        /*endpoint = [location.protocol + '/', location.host, db_name,
                    '_server'].join('/');*/
        endpoint = 'http://localhost:8080';
        database = $.couch.db(db_name);
    });
    
    /** Save an ordered list of this notebook's cells. */
    function save_worksheet() {
        var cells = $('#worksheet')
                    .children('.cell')
                    .map(function() {
                        return this.id;
                    }).get();
        
        
            database.openDoc(worksheet_name, {
            }, 
            {
                
                success: function(doc) {
                    doc.cells = cells;
                    database.saveDoc(doc);
                },
                dataType: 'json',
                error: function(status, req, e) {
                    database.saveDoc({
                        type: 'worksheet',
                        _id: worksheet_name,
                        cells: cells,
                    });
                },
                complete: function(XMLHttpRequest, textStatus) {},
            });
    }
    
    function save_cell(id, input, msg) {
        database.openDoc(id, {
            success: function(doc) {
                //alert(JSON.stringify(msg));
                doc.input = input;
                doc.output = msg.content;
                database.saveDoc(doc, {
                    success: function() {
                        iframe = $('#' + id)
                        .find('div.output iframe')
                        .each(function(){
                            this.contentWindow.location.reload(true);
                        });
                    }
                });
            },
            error: function(status, req, error){},
            complete: function(xhr, status) {},
        });
    }
    
    // Public interface
    return {
        add_cell: function() {
            database.saveDoc({
                type: 'cell',
                input: '',
                output: '',
            }, 
            {
                success: function(doc){
                    var cell_text = new_cell(doc.id, '', '');
                    var cell = $(cell_text);
                    cell.children('.output').resizable({alsoResize: cell});
                    $('#worksheet').append(cell);
                    save_worksheet();
                },
            });
        },
        delete_cell: function(id) {
            database.openDoc(id, {
                success: function(doc) {
                    database.removeDoc(doc, {
                        success: function() {
                            $('#' + doc._id).remove();
                            save_worksheet();
                        }
                    });
                }
            });
        },
        compute_request: function(cell_id, input) {
            $.ajax({
                url: endpoint,
                data: {
                    content: input,
                    worksheet_id: worksheet_name,
                },
                success: function(msg){
                    save_cell(cell_id, input, msg);
                },
                global: false,
                type: 'POST',
                dataType: 'json',
            });
        }
    }
}());


/** Main JQuery code */
$(document).ready(function(){
    /** Handler for submission of an input form. */
    $('.cell form').live('submit', function(){
        var input = $(this).children('.input').val();
        var id = $(this).parent().attr('id');
        COUCH.compute_request(id, input);

        // Prevent the actual submission of this form.
        return false;
    });
  
  /** Add a cell to this notebook. */
    $('#add_cell').click(function(){
        COUCH.add_cell();
    });
  
  /** Delete a cell from this notebook. */
  $('button.delete').live('click', function(){
    var ans = confirm('Do you want to permanently delete this cell?');
    if (ans) {
      // Be careful if the HTML structure of cell "widgets" changes.
      var id = $(this).parents('div.cell').attr('id');
      COUCH.delete_cell(id);
    }
    
    // Don't actually submit the form.
    return false;
  });
  
  /** Make output iframes resizable, using JQuery UI. */
  $('div.output').each(function(){
    $(this).resizable({alsoResize: $(this).parent()});
  });
});
