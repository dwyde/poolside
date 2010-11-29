function Requester() {
  this.ws = new WebSocket("ws://localhost:9996/test");
  this.ws.onopen = function() {
  };
  this.ws.onmessage = function(event) {
    var data = event.data;
    $("#result").append("<p>" + data + "</p>");
  };
  this.ws.onclose = function() {
    alert("socket closed");
  };
  
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
  this.ws.send(data);
};

$(document).ready(function(){
  /* Create a Requester instance. */
  var req = new Requester();
  
  /* Handler for submission of the input form. */
  $("#choices").submit(function(){
    var choice = $("#requests").val();
    var input = $("#in_text").val();

    req.submit(choice, input);

    /* Prevent actual submission of the form. */
    return false;
  });
});

