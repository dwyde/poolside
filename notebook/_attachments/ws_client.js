var WS_CLIENT = (function () { 
    var my = {}, 
        connection;

    function receive(msg) { 
        handler = ipy_receivers[msg.msg_type];
        return handler(msg);
    } 
     
    my.receivers = {};
    my.senders = {};
    
    my.connect = function(address) {
        connection = new WebSocket('ws://' + address);
        connection.onopen = function() {alert('open')};
        connection.onmessage = function(event) {
            alert(receive(event.data));
        };
        connection.onclose = function() {
            alert('socket closed');
        };
    };

    my.send = function(msg) {
        
    };
     
    return my; 
}());

WS_CLIENT.receivers.ipython = (function () { 
    var my = {},
        receivers = {
            stream: function(msg) {return msg.content.data;},
            pyin: function(msg) {return msg.content.code;},
            pyout: function(msg) {return msg.content.data;},
            pyerr: function(msg) {
                return msg.content.ename +  '<br />' + msg.content.evalue;
            },
            complete_reply: function(msg) {return msg.content.matches;},
            object_info_reply: function(msg) {return msg;},
        };
        
    my.handle = function(msg) {
        return receivers[msg.msg_type](msg);
    };

    return my;
}());

WS_CLIENT.senders.ipython = (function () {
    var my = {},
        senders = {
            execute_request: function(code_str) {
                return {code: code_str, silent : false};
            },
            complete_request: function(text) {
                return {text: text, line: text, cursor_post: text.length - 1};
            },
            object_info_request: function(text) {
                return {oname: text};
            }
        };
    
    my.handle = function(request_type, input, cell_id) {
          var data = {};
          data.content = senders[request_type](input);
          
          /* Set data that's the same for every request. */
          data.msg_type = request_type;
          data.header = {'msg_id': cell_id};
          
          return data;
    };
    
    return my;
}());
