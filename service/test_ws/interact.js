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

  var obj = JSON.parse(msg);
  switch (obj.msg_type) {
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
    default:
      break;
  };
}

function Requester(web_socket) {
  this.web_socket = web_socket;
  this.data = {};
}

Requester.prototype.execute_request = function(code_str) {
  this.data.content = {code: code_str, silent : false};
};

Requester.prototype.complete_request = function(text) {
  this.data.content = {text: text, line: text, cursor_post: text.length - 1};
};

Requester.prototype.object_info_request = function(text) {
  this.data.content = {oname: text};
};

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
    //var choice = $("#requests").val();
    var choice = 'execute_request';
    var input = $(this).children('.input').val();
    req = new Requester(web_socket);
    req.submit(choice, input);

    /* Prevent actual submission of the form. */
    return false;
  });
});

