var URL_ENDPOINT = 'http://localhost:5984/notebook/_service';

function Request() {
};

Request.prototype.execute_request = function(code_str) {
  this.data = {
    json: {
        'method': 'eval_python',
        'params': {'input': code_str, 'notebook': 'david'},
        'version': '1.1',
    },
    url: URL_ENDPOINT,
  };
};

Request.prototype.complete_request = function() {
  this.data = {
    json: {
        'method': 'eval_python',
        'params': {'input': code_str},
        'version': '1.1',
    },
    url: URL_ENDPOINT,
  };
};

Request.prototype.object_info_request = function() {};

Request.prototype.submit = function() {
//  var msg = JSON.stringify(this.data);
  this.ws.send('hello');
};

$(document).ready(function(){
  var ws = new WebSocket("ws://localhost:9996/test");      
  ws.onopen = function() {
    this.send("hello from the browser");
    this.send("more from browser");
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
//    var req = new Request();
//    req.ws.send('nope');
//    req.execute_request(input);
//    req.complete_request(input);
//    req.submit();
    ws.send(input);
    // Prevent actual submission of the form.
    return false;
  });
});

