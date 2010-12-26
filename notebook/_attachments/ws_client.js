var WS_CLIENT = (function () { 
    var my = {}, 
        connection;
    
    my.connect = function(address, out_callback) {
        connection = new WebSocket('ws://' + address);
        connection.onopen = function() {};
        connection.onmessage = function(event) {
            //alert(event.data);
            var result = my.ipython.receive(JSON.parse(event.data));
            if (result) {
                out_callback(result);
            }
        };
        connection.onclose = function() {
            out_callback({target: '__messages', output: 'WebSocket closed'});
        };
        /*connection.onerror = function(event) {
            alert(event);
        };*/
    };

    my.send = function(msg) {
        connection.send(msg);
    };
     
    return my; 
}());

WS_CLIENT.ipython = (function () {
    var my = {};
    
    my.receive = function(msg) {
        return msg;
    };
    
    my.send = function(request_type, input, cell_id) {
          var data = {
            lang: 'python',
            code: input,
            caller: cell_id,
          };
          WS_CLIENT.send(JSON.stringify(data));
    };
    
    return my;
}());
