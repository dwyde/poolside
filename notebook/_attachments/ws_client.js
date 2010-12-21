var WS_CLIENT = (function () { 
    var my = {}, 
        connection;
    
    my.connect = function(address, out_callback) {
        connection = new WebSocket('ws://' + address);
        connection.onopen = function() {};
        connection.onmessage = function(event) {
            var result = my.ipython.receive(JSON.parse(event.data));
            if (result) {
                out_callback(result);
            }
        };
        connection.onclose = function() {
            alert('socket closed');
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
        },
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
    
    my.receive = function(msg) {
        if (receivers[msg.msg_type]) {
            var result = receivers[msg.msg_type](msg);
            return {result: result, caller: msg.parent_header.msg_id};
        }
    };
    
    my.send = function(request_type, input, cell_id) {
          var data = {};
          data.content = senders[request_type](input);
          
          /* Set data that's the same for every request. */
          data.msg_type = request_type;
          data.header = {'msg_id': cell_id};
          WS_CLIENT.send(JSON.stringify(data));
    };
    
    return my;
}());
