test('Notebook object constructor with url', function() {
  expect(2);
  var url = 'http://localhost:5984/yes/_design/notebook/_rewrite/poolside/okay';
  var notebook = new Notebook(url);
  equals(notebook.worksheet_name, 'okay', 'Worksheet name should be "okay"');
  equals(notebook.database.name, 'yes', 'Database name should be "yes"');
});

test('Notebook object constructor without url', function() {
  expect(2);
  var notebook = new Notebook();
  ok(notebook.worksheet_name, 'Worksheet name should be found');
  ok(notebook.database, 'Database object should exist');
});
