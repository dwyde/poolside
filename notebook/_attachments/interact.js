var path = window.location.pathname.split('/');
var WORKSHEET_NAME = path.pop();
var DATABASE = path[1];
var WEBSOCKET = 'localhost:9996/test';

function output_cell(text, cell_id) {
  //$("#result").append("<p>" + text + "</p>");
//  var cell = new_cell(text, '', text);
  if (cell_id) {
    cell = $("#" + cell_id);
    cell.children('.output').html(text);
  }
  else {
    $('#worksheet').append(text);
  }
}

function ws_receive(msg) {
  /* 
   * 
   * Skip 'execute_reply' messages.
   */

//////
/// Convert this to some sort of object/hash/dictionary structure
/// Also deal with cell_ids
//////
  var output, cell_id;
  var obj = JSON.parse(msg);
  switch (obj.msg_type) {
    /* IPython ZMQ messages */
    case 'pyin':
      output = obj.content.code; break;
    case 'stream':
      output = obj.content.data; break;
    case 'pyout':
      output = obj.content.data; break;
    case 'pyerr':
      output = obj.content.ename + '<br />' + obj.content.evalue; break;
    case 'complete_reply':
      output = obj.content.matches; break;
    case 'object_info_reply':
      output = msg; break;
    /* CouchDB results */
    case 'worksheet_saved':
      output = msg; break;
    case 'cell_saved':
      var cell = new_cell(obj.id, obj.input, obj.output);
      output = cell; 
      break;
    case 'cell_deleted':
      output = msg; break;
    default:
      break;
  };
  
  var header = obj.parent_header || null;
  if (header) {
    cell_id = header.msg_id;
  } else {
    cell_id = null;
  }
  
  output_cell(output, cell_id);
}

function Requester(web_socket) {
  this.web_socket = web_socket;
  this.data = {};
}

/* IPython requests */
Requester.prototype.execute_request = function(code_str) {
  this.data.content = {code: code_str, silent : false};
};

Requester.prototype.complete_request = function(text) {
  this.data.content = {text: text, line: text, cursor_post: text.length - 1};
};

Requester.prototype.object_info_request = function(text) {
  this.data.content = {oname: text};
};

/* Notebook/Database requests */
Requester.prototype.save_cell = function(data) {
  this.data.cell_id = (data.id || null);
  this.data.input = data.input;
  this.data.output = data.output;
}

Requester.prototype.submit = function(request_type, input, cell_id) {
  /* Fill in request-specific data. */
  this[request_type](input);
  
  /* Set data that's the same for every request. */
  this.data.msg_type = request_type;
  this.data.header = {'msg_id': cell_id};
  
  /* Send data through the web socket. */
  var data = JSON.stringify(this.data);
  this.web_socket.send(data);
};

$(document).ready(function(){
  var db = $.couch.db(DATABASE);
  var req;
  var web_socket = new WebSocket('ws://' + WEBSOCKET);
  web_socket.onopen = function() {
  };
  web_socket.onmessage = function(event) {
    var data = event.data;
    ws_receive(data);
  };
  web_socket.onclose = function() {
    alert("socket closed");
  };
  
  function save_worksheet() {
    var cells = $('#worksheet')
              .children('.cell')
              .map(function() {
                  return this.id;
              }).get();
    
    var data = {cells: cells, type: 'worksheet'};
    db.openDoc(WORKSHEET_NAME, { success: function(doc) {
      $.extend(data, {_id: doc._id, _rev: doc._rev});
      db.saveDoc(data);
    }});
  }
  
  /* Handler for submission of the input form. */
  $('form.cell').live('submit', function(){
    var choice = 'execute_request';
    var input = $(this).children('.input').val();
    var id = $(this).attr('id');
    req = new Requester(web_socket);
    req.submit(choice, input, id);

    /* Prevent actual submission of the form. */
    return false;
  });
  
  $('#add_cell').click(function(){
    var choice = 'save_cell';
    var input = {
      id: null,
      input: '',
      output: '',
    };
    req = new Requester(web_socket);
    req.submit(choice, input);
  });
  
  $('.cell').live('change', function(){ // ('.cell .output') doesn't work?
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
    save_worksheet();
    
    
  });
});

