var URL_ENDPOINT = 'http://localhost:5984/notebook/_service';

function Request() {
};

Request.prototype.execute_request = function(code_str) {
  this.data = {
    content: {
        code: code_str,
        silent : false,
    },
    msg_type: 'execute_request',
  };
  return this.data;
};

Request.prototype.complete_request = function(text) {
  this.data = {
    content: {
        text: text,
        line: text,
        cursor_post: text.length - 1,
    },
    msg_type: 'complete_request',
  };
  return this.data;
};

Request.prototype.object_info_request = function(text) {
  this.data = {
    content: {
        oname: text,
        detail_level: 1,
    },
    msg_type: 'object_info_request',
  };
  return this.data;
};

Request.prototype.submit = function() {
//  var msg = JSON.stringify(this.data);
    this.data.header = {'msg_id': null};
};

$(document).ready(function(){
  var ws = new WebSocket("ws://localhost:9996/test");
  ws.onopen = function() {
    //this.send("hello from the browser");
  };
  ws.onmessage = function(event) {
//    var data = JSON.parse(event.data);
    var data = event.data;
    $("#result").append("<p>" + data + "</p>"); // \n
  };
  ws.onclose = function() {
    alert("socket closed");
  };
  
  $("#choices").submit(function(){
    var choice = $("#requests").val();
    var input = $("#in_text").val();
    var req = new Request();
    req[choice](input);
    req.submit();
    var data = JSON.stringify(req.data);
    ws.send(data);
    // Prevent actual submission of the form.
    return false;
  });
});

