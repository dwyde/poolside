test('Notebook object constructor with url', function() {
  expect(1);
  var url = 'http://localhost:5984/yes/_design/notebook/_rewrite/poolside/okay';
  var notebook = new Notebook(url);
  equals(notebook.worksheet_name, 'okay', 'Worksheet name should be "okay"');
});

test('Notebook object constructor without url', function() {
  expect(2);
  var notebook = new Notebook();
  ok(notebook.worksheet_name, 'Worksheet name should be found');
  notEqual(notebook.database.name, '', 'Database name should be nonempty');
});

/**
 * 
 * Some functions are more UI-based: use Selenium?
 * 
 * Notebook::add_cell
 */
