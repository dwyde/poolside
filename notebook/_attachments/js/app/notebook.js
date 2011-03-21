/** 
 * Print out messages. 
 * 
 * @param {string} msg A status message to output.
 */
function set_status(msg) {
    $('#__messages').text(msg);
}

/**
 * Output a JQuery error message.
 */
function error_msg(status, req, error) {
  set_status(error);
}

/**
 * Creates an instance of Notebook.
 * 
 * @param {string} url A URL from which to derive worksheet name and database.
 * 
 * The database name is the third element in the forward slash-split URL:
 * http://localhost:5984/db_name => ['http:', '', 'localhost:5984', 'db_name'].
 */
function Notebook(url) {
  url = url || window.location.pathname;
  var path = url.split('/');
  var db_name = path[1];
  this.worksheet_name = path.pop();
  this.database = $.couch.db(db_name);
}

/**
 * Asks CouchDB for the current user's name, then executes a callback function.
 * 
 * @param {function} callback A function execute after obtaining the username.
 */
Notebook.prototype._get_username = function(callback) {
  $.couch.session({
    success: function(response){
      var user = response.userCtx.name;
      if (user == null) { // User isn't logged in
        set_status('Please log in.');
      } else {
        callback(user);
      }
    },
  });
};

/** 
 * Save this worksheet, and its list of cells, to CouchDB.
 * 
 * @param {string} user A user to set as the "writers" array field in CouchDB.
 */
Notebook.prototype._save_worksheet = function(user) {
  var cells = $('#worksheet > .cell')
                .map(function() {
                    return this.id;
                }).get();
  
  var self = this;
  this.database.openDoc(this.worksheet_name, {
    success: function(worksheet) {
      worksheet.cells = cells;
      self.database.saveDoc(worksheet);
    },
    error: function(status, request, error) {
      self.database.saveDoc({
        _id: self.worksheet_name,
        cells: cells,
        type: 'worksheet',
        writers: [user]
      });
    }
  });
};

/**
 * Adds a new cell to this notebook. 
 */
Notebook.prototype.add_cell = function(){
  var self = this;
  this._get_username(function(user) {
    self.database.saveDoc( // Create a new cell.
      {
        type: 'cell',
        input: '',
        output: '',
        eval_type: 'text',
        writers: [user],
      }, 
      {
        success: function(cell) { // The cell was saved.
          var cell_html = new_cell(cell.id, '', '');
          $('#worksheet').append(cell_html);
          self._save_worksheet(user);
        },
        error: error_msg,
      }
    );
  });
};

/**
 * Deletes an existing cell from this notebook. 
 * 
 * @param {string} id The "id" of a cell to remove.
 */
Notebook.prototype.delete_cell = function(id) {
  var self =  this;
  this.database.openDoc(id, {
    success: function(doc) {
      self.database.removeDoc(doc, {
        success: function() {
          $('#' + doc._id).remove();
          self._save_worksheet();
        },
        error: error_msg,
      });
    }
  });  
};

/** 
 * Main JQuery code: attach functions to DOM elements as JQuery handlers.
 */
$(document).ready(function(){
  var notebook = new Notebook();
  
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
});
