//
// Copyright 2011 David Wyde and Chris Hart.
//

/** A module to enable communication between a notebook frontend,
 *  CouchDB, and a Python HTTP server.
 */
var COUCH = (function() {
    // Private variables
    var worksheet_name,
        database,
        endpoint = 'http://localhost:8282',
        db_name = 'external';
    
    // Private functions
        
    /** Initialize data structures based on the current URL. */
    $(function() {
        var location = window.location;
        var path = location.pathname.split('/');
        worksheet_name = path.pop();
        database = $.couch.db(db_name);
    });
    
    function save_with_writers(doc, success) {
        $.ajax({
            url: '/_session',
            dataType: 'json',
            success: function(response) {
                database.saveDoc(
                    $.extend({writers: [response.userCtx.name]}, doc), {
                        success: (success || null),
                    }
                );
            },
        });
    }
    
    /** Save an ordered list of this notebook's cells. */
    function save_worksheet() {
        var cells = $('#worksheet')
                    .children('.cell')
                    .map(function() {
                        return this.id;
                    }).get();
        
        
            database.openDoc(worksheet_name,
            {
                
                success: function(doc) {
                    doc.cells = cells;
                    database.saveDoc(doc);
                },
                dataType: 'json',
                error: function(status, req, e) {
                    
                    save_with_writers({
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
                    success: function(msg) {
                        //
                    }
                });
            },
            error: function(status, req, error){},
            complete: function(xhr, status) {},
        });
    }
    function output_to_json(cell_id, output) {
        if (typeof output == 'object') {
            var caller = document.createElement("script");
            caller.setAttribute('type', 'text/javascript');
            caller.innerHTML = 'var output = document.getElementById("' +
                    cell_id + '").getElementsByClassName("output") \
                    [0]; var data = ' + JSON.stringify(output) +
                    '; indent(data, output);';
            document.getElementById(cell_id).getElementsByClassName('output')[0].appendChild(caller);
        } 
        else {
            $('#' + cell_id).children('.output').text(output);
        }
    }
    // Public interface
    return {
        add_cell: function() {
            var user = save_with_writers(
                {
                    type: 'cell',
                    input: '',
                    output: '',
                }, 
                function(doc) {
                    var cell_text = new_cell(doc.id, '', '');
                    var cell = $(cell_text);
                    cell.children('.output').resizable({alsoResize: cell});
                    $('#worksheet').append(cell);
                    save_worksheet();
                }
            );
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
        compute_request: function(cell_id, input, type) {
            $('#' + cell_id).removeClass(function() {
                return 'text python ruby';
            }).addClass(type);
            
            if (type == 'text') {
                output_to_json(cell_id, '');
                save_cell(cell_id, input, {content: ''});
            }
            else {
                $.ajax({
                    url: endpoint,
                    data: {
                        content: input,
                        worksheet_id: worksheet_name,
                        language: type
                    },
                    success: function(msg){
                        output_to_json(cell_id, msg.content);
                        $('#' + cell_id).resizable({alsoResize: $('#' + 
                                cell_id).children('.output')});
                        save_cell(cell_id, input, msg);
                    },
                    global: false,
                    type: 'POST',
                    dataType: 'json',
                });
            }
        },
        output_to_json: output_to_json,
    }
}());


/** Main JQuery code */
$(document).ready(function(){
    /** Handler for submission of an input form. */
    $('.cell form').live('submit', function(){
        // Prevent the actual submission of this form.
        return false;
    });
    
    $('.cell form button').live('click', function(){
        var id = $(this).parents('div.cell').attr('id');
        var input = $(this).siblings('.input').val();
        var type = $(this).attr('class');
        COUCH.compute_request(id, input, type);
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
  
  /** Submit a cell's input when "enter" is pressed inside the textarea. */
  $('.input').live('keypress', function(event) {
      if (event.which == '13') {
          event.preventDefault();
          var cell = $(this).parents('div.cell');
          var id = cell.attr('id');
          var input = $(this).val();
          var type = cell.attr('class');
          COUCH.compute_request(id, input, type);
      }
  });
  
  /** Make output iframes resizable, using JQuery UI. */
  $('div.output').each(function(){
      var cell = $(this).parent();
      var content = $(this).text();
      try {
          content = JSON.parse(content);
      } 
      catch (error) {} 
      finally {
          COUCH.output_to_json(cell.attr('id'), content);
      }
      cell.resizable({alsoResize: $(this)});
  });
});
