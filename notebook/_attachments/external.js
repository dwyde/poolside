//
// Copyright 2011 David Wyde and Chris Hart.
//
/**
 * JavaScript for Poolside's notebook user interface.
 * 
 * Some of the URL paths might not work if we ever move to CouchDB vhosts,
 * e.g., /_session and COUCH.db_name.
 * 
 */

/** Global function to print errors in a standard way. */
function output_error(status, request, error_msg) {
    $('#__messages').text(error_msg);
}

/** 
 * A module to enable communication between a notebook frontend,
 *  CouchDB, and a Python HTTP server.
 */
var COUCH = (function() {
    // Private variables
    var worksheet_name,
        database,
        endpoint;
    
    // Initialize data structures based on the current URL.
    
    // Get the eval server's address from the _design doc.
    $.getJSON(
        '../../eval_server.json',
        function(data, textStatus, jqXHR) {
            endpoint = 'http://' + data.server + ':' + data.port;
        }
    );
    
    // Parse the URL for the database name.
    $(function() {
        var location = window.location;
        var path = location.pathname.split('/');
        var db_name = path[1];
        worksheet_name = path.pop();
        database = $.couch.db(db_name);
    });
    
    // Private functions
    function save_with_writers(doc, success) {
        $.ajax({
            url: '/_session',
            dataType: 'json',
            success: function(response) {
                database.saveDoc(
                    $.extend({writers: [response.userCtx.name]}, doc), {
                        success: (success || null),
                        error: output_error,
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
                doc.input = input;
                doc.output = msg.content;
                database.saveDoc(doc, {
                    success: function(msg) {},
                    error: output_error,
                });
            },
            error: function(status, req, error) {},
            complete: function(xhr, status) {},
        });
    }
    
    /** Enable dynamic visualization of JSON data with Protovis.
     *  This has potential to be cool, but isn't particularly useful right now.
     */
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
                        },
                        error: output_error,
                    });
                }
            });
        },
        compute_request: function(cell_id, input, type) {
            $.couch.session({
                success: function(msg) {
                    name = msg.userCtx.name;
                    if (name != 'null') {
                        // Logic to handle logged-in users
                    } else {
                        output_error(null, null, 'Please log in.');
                    }
                },
                error: output_error
            });
        
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
                    error: output_error,
                    type: 'GET',
                    dataType: 'jsonp',
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
