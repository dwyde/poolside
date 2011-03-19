/**
 * Creates an instance of Notebook.
 * 
 * @param {string} url A URL from which to derive worksheet name and database.
 */
function Notebook(url) {
  url = url || window.location.pathname;
  var path = url.split('/');
  var db_name = path[3];
  this.worksheet_name = path.pop();
  this.database = $.couch.db(db_name);
}
