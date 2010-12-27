var WS_ADDRESS = 'localhost:9996/notebook';
var path = window.location.pathname.split('/');
var WORKSHEET_NAME = path.pop();
var DATABASE = path[1];
var TMP_ID = '_tmp';

function output_cell(response) {
  var cell_id = response.target;
  var text = response.content;
  if (cell_id) {
    cell = $('#' + cell_id);
    cell.children('.output').html(text);
  }
  else {
    $('#worksheet').append(text);
  }
}

function assign_id(response, ws_client) {
  cell = $('#' + TMP_ID);
  cell.attr('id', response['id']);
  ws_client.save_worksheet();
}

function WebSocketClient(address) { 
  var client = this;
  this.connection = new WebSocket('ws://' + address);
  this.connection.onopen = function() {};
  this.connection.onmessage = function(event) {
    var result = JSON.parse(event.data);
    if (result && result.type == 'output') {
      output_cell(result);
    } else if (result && result.type == 'new_id') { /** MAKE A DICTIONARY **/
      assign_id(result, client);
    }
  };
  this.connection.onclose = function() {
      output_cell({target: '__messages', content: 'WebSocket closed'});
  };
  this.connection.onerror = function(event) {
      output_cell(event);
  };
}

WebSocketClient.prototype.python_request = function(input, cell_id) {
  var data = {
    type: 'python',
    input: input,
    caller: cell_id,
  };
  this.connection.send(JSON.stringify(data));
};

WebSocketClient.prototype.save_worksheet = function() {
  var cells = $('#worksheet')
              .children('.cell')
              .map(function() {
                  return this.id;
              }).get();
  var data = {
    type: 'save_worksheet',
    id: WORKSHEET_NAME,
    cells: cells,
  };
  this.connection.send(JSON.stringify(data));
};

WebSocketClient.prototype.new_id = function() {
  this.connection.send(JSON.stringify({type: 'new_id'}));
};

WebSocketClient.prototype.delete_cell = function(id) {
  var data = {
    type: 'delete_cell',
    id: id,
  }
  this.connection.send(JSON.stringify(data));
}

/* Main JQuery code */
$(document).ready(function(){
  var ws_client = new WebSocketClient(WS_ADDRESS);
  
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
    var cell = new_cell(TMP_ID, '', '');
    ws_client.new_id();
    $('#worksheet').append(cell);
    //ws_client.save_cell(
  });
  
  $('button.delete').live('click', function(){
    var ans = confirm('Do you really want to delete this cell?');
    if (ans) {
      cell_id = $(this).parent().attr('id');
      ws_client.delete_cell(cell_id);
      $('#worksheet #' + cell_id).remove();
      ws_client.save_worksheet();
    }
    return false;
  });
});

