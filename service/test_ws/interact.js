function output(text) {
  //$("#result").append("<p>" + text + "</p>");
//  var cell = new_cell(text, '', text);
  $('#worksheet').append(text);
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

  var obj = JSON.parse(msg);
  switch (obj.msg_type) {
    /* IPython ZMQ messages */
    case 'pyin':
      output(obj.content.code); break;
    case 'stream':
      output(obj.content.data); break;
    case 'pyout':
      output(obj.content.data); break;
    case 'pyerr':
      output(obj.content.ename + '<br />' + obj.content.evalue); break;
    case 'complete_reply':
      output(obj.content.matches); break;
    case 'object_info_reply':
      output(msg); break;
    /* CouchDB results */
    case 'worksheet_saved':
      output(msg); break;
    case 'cell_saved':
      //output(msg); 
      var id = msg.cell_id;
      var cell = new_cell(id, '', '');
      $('#worksheet').append(cell);
      break;
    case 'cell_deleted':
      output(msg); break;
    default:
      break;
  };
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

Requester.prototype.submit = function(request_type, input) {
  /* Fill in request-specific data. */
  this[request_type](input);
  
  /* Set data that's the same for every request. */
  this.data.msg_type = request_type;
  this.data.header = {'msg_id': null};
  
  /* Send data through the web socket. */
  var data = JSON.stringify(this.data);
  this.web_socket.send(data);
};

$(document).ready(function(){
  var req;
  var web_socket = new WebSocket("ws://localhost:9996/test");
  web_socket.onopen = function() {
  };
  web_socket.onmessage = function(event) {
    var data = event.data;
    ws_receive(data);
  };
  web_socket.onclose = function() {
    alert("socket closed");
  };
  
  /* Handler for submission of the input form. */
  $('form.cell').live('submit', function(){
    var choice = 'execute_request';
    var input = $(this).children('.input').val();
    req = new Requester(web_socket);
    req.submit(choice, input);

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
});

