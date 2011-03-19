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
  var db_name = path[3];
  this.worksheet_name = path.pop();
  this.database = $.couch.db(db_name);
}

/**
 * Adds a new cell to this notebook. 
 */
Notebook.prototype.add_cell = function(){
  // Call external new_cell() function.
  var cell = new_cell('', '', '');
  $('#worksheet').append(cell);
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
