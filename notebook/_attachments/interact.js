var WS_ADDRESS = 'localhost:9996/notebook';
var path = window.location.pathname.split('/');
var WORKSHEET_NAME = path.pop();
var DATABASE = path[1];

function output_cell(response) {
  var cell_id = response.target;
  var text = response.output;
  if (cell_id) {
    cell = $('#' + cell_id);
    cell.children('.output').html(text);
  }
  else {
    $('#worksheet').append(text);
  }
}

function WebSocketClient(address) { 
  this.connection = new WebSocket('ws://' + address);
  this.connection.onopen = function() {};
  this.connection.onmessage = function(event) {
      var result = JSON.parse(event.data);
      if (result) {
          output_cell(result);
      }
  };
  this.connection.onclose = function() {
      output_cell({target: '__messages', output: 'WebSocket closed'});
  };
  this.connection.onerror = function(event) {
      output_cell(event);
  };
}

WebSocketClient.prototype.python_request = function(input, cell_id) {
  var data = {
    type: 'python',
    code: input,
    caller: cell_id,
  };
  this.connection.send(JSON.stringify(data));
};


/* Main JQuery code */
$(document).ready(function(){
  var ws_client = new WebSocketClient(WS_ADDRESS);
  
  function save_worksheet() {
    var cells = $('#worksheet')
              .children('.cell')
              .map(function() {
                  return this.id;
              }).get();
  }
  
  /* Handler for submission of the input form. */
  $('form.cell').live('submit', function(){
    var input = $(this).children('.input').val();
    var id = $(this).attr('id');
    ws_client.python_request(input, id);
    $(this).children('p.output').html('');

    /* Prevent actual submission of the form. */
    return false;
  });
  
  $('#add_cell').click(function(){
    var cell = new_cell('', '', '');
    $('#worksheet').append(cell);
  });
});

