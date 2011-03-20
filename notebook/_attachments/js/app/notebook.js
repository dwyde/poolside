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
 * Adds a new, blank cell into the DOM.
 * 
 * @param {string} id The CouchDB _id of a new cell.
 */
Notebook.prototype._blank_cell = function(id) {
  return function(doc) {
    var cell_text = new_cell(id, '', '');
    $('#worksheet').append(cell_text);
  }
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
          var id = cell.id;
          self.database.openDoc(self.worksheet_name, {
            error: function(status, req, error){ // The worksheet doesn't exist.
              self.database.saveDoc({
                _id: self.worksheet_name,
                type: 'worksheet',
                cells: [id],
                writers: [user],
              }, {
                success: self._blank_cell(id),
              });
            },
            success: function(worksheet) { // The worksheet already exists.
              worksheet.cells.push(id);
              self.database.saveDoc(worksheet, {
                success: self._blank_cell(id),
              }); 
            },
          })
        },
        error: error_msg,
      }
    );
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
});
