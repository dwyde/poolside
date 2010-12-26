var WS_ADDRESS = 'localhost:9996/test';
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

WebSocketClient.prototype.send = function(request_type, input, cell_id) {
  var data = {
    lang: 'python',
    code: input,
    caller: cell_id,
  };
  this.connection.send(JSON.stringify(data));
};


/* Main JQuery code */
$(document).ready(function(){
  var ws_client = new WebSocketClient(WS_ADDRESS);
  //var db = $.couch.db(DATABASE);
  
  function save_worksheet() {
    var cells = $('#worksheet')
              .children('.cell')
              .map(function() {
                  return this.id;
              }).get();
    
    var data = {cells: cells, type: 'worksheet'};
    /*db.openDoc(WORKSHEET_NAME, { success: function(doc) {
      $.extend(data, {_id: doc._id, _rev: doc._rev});
      db.saveDoc(data);
    }});*/
  }
  
  /* Handler for submission of the input form. */
  $('form.cell').live('submit', function(){
    var choice = 'execute_request';
    var input = $(this).children('.input').val();
    var id = $(this).attr('id');
    ws_client.send(choice, input, id);
    $(this).children('p.output').html('');

    /* Prevent actual submission of the form. */
    return false;
  });
  
  $('#add_cell').click(function(){
    //db.saveDoc({type: 'cell', input: '', output: ''});
    var cell = new_cell('', '', '');
    $('#worksheet').append(cell);
  });
  
  $('form.cell > p').live('change', function(){ // ('.cell .output') doesn't work?
    /*var cell = $(this);
    var input = {
      id: cell.attr('id'),
      input: cell.children('.input').val(),
      output: cell.children('p').html(), //output
    };
    alert(input.output);
    req = new Requester(web_socket);
    req.submit('save_cell', input);*/
    
    var id = $(this).attr('id') || '';
    alert(id);
//    save_worksheet();
    
    
  });
});

