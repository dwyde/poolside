/** 
 * Print out messages. 
 * 
 * @param {string} msg A status message to output.
 */
function set_status(msg) {
    $('#__messages').text(msg);
}

/**
 * Output a JQuery error message.
 */
function error_msg(status, req, error) {
  set_status(error);
}

/*
 * Cell class.
 */

/**
 * Populate a JavaScript object with a few fields specific to Poolside Cells.
 * 
 * @param {object} params A JavaScript object.
 */
function Cell(params) {
  $.extend(this, {
    _id: params.cell_id || undefined,
    type: 'cell',
    eval_type: params.type || 'text',
    input: params.input || '',
    output: params.output || '',
    writers: params.writers || [],
  });
}

/*
 * Notebook class.
 */

/**
 * Creates an instance of Notebook.
 * 
 * @param {string} url A URL from which to derive worksheet name and database.
 * 
 * The database name is the third element in the forward slash-split URL:
 * http://localhost:5984/db_name => ['http:', '', 'localhost:5984', 'db_name'].
 */
function Notebook(url) {
  url = url || window.location.pathname;
  var path = url.split('/');
  var db_name = path[1];
  this.worksheet_name = path.pop();
  this.database = $.couch.db(db_name);
}

/**
 * Asks CouchDB for the current user's name, then executes a callback function.
 * 
 * @param {function} callback A function execute after obtaining the username.
 */
Notebook.prototype._get_username = function(callback) {
  $.couch.session({
    success: function(response){
      var user = response.userCtx.name;
      if (user == null) { // User isn't logged in
        set_status('Please log in.');
      } else {
        callback(user);
      }
    },
  });
};

/** 
 * Save this worksheet, and its list of cells, to CouchDB.
 * 
 * @param {string} user A user to set as the "writers" array field in CouchDB.
 */
Notebook.prototype._save_worksheet = function(user) {
  var cells = $('#worksheet > .cell')
                .map(function() {
                    return this.id;
                }).get();
  
  var self = this;
  this.database.openDoc(this.worksheet_name, {
    success: function(worksheet) {
      worksheet.cells = cells;
      self.database.saveDoc(worksheet);
    },
    error: function(status, request, error) {
      self.database.saveDoc({
        _id: self.worksheet_name,
        cells: cells,
        type: 'worksheet',
        writers: [user]
      });
    }
  });
};

/**
 * Adds a new cell to this notebook. 
 */
Notebook.prototype.add_cell = function(){
  var self = this;
  this._get_username(function(user) {
    self.database.saveDoc( // Create a new cell.
      new Cell({
        writers: [user]
      }), 
      {
        success: function(cell) { // The cell was saved.
          var cell_html = new_cell(cell.id, '', '');
          $('#worksheet').append(cell_html);
          self._save_worksheet(user);
        },
        error: error_msg,
      }
    );
  });
};

/**
 * Deletes an existing cell from this notebook. 
 * 
 * @param {string} id The "id" of a cell to remove.
 */
Notebook.prototype.delete_cell = function(id) {
  var self =  this;
  this.database.openDoc(id, {
    success: function(doc) {
      self.database.removeDoc(doc, {
        success: function() {
          $('#' + doc._id).remove();
          self._save_worksheet();
        },
        error: error_msg,
      });
    }
  });  
};

/**
 * Save an existing cell to CouchDB.
 * 
 * @param {object} cell_obj An instance of the Cell class: a JavaScript object.
 */
Notebook.prototype.save_cell = function(cell_obj) {
  var self = this;
  this._get_username(function(user) {
    self.database.openDoc(cell_obj._id, {
      success: function(doc) {
        self.database.saveDoc(
          $.extend(doc, cell_obj, {
            writers: [user]
          }), 
          {
            success: set_status,
            error: error_msg,
          }
        );
      }
    });
  });
};

/*
 * Request class
 */

/**
 * Initialize a Request object.
 * 
 * @param {string} type The mode in which this request will be executed.
 * @param {string} cell_id A cell's ID in CouchDB.
 * @return {function} A callback function: function callback(cell_id, input). 
 */
function Request(type, cell_id) {
  this._set_eval_type(cell_id, type);
  this.cell_id = cell_id;
  if (type == 'text') {
    this.execute = this._eval_text;
  } else {
    this.execute = this._eval_code;
    this.type = type;
  }
}

/** Initialize class variables for Request:
 * 
 *   1) get eval server's address from _design doc
 *   2) store a list of evaluation request types
 *   3) save the current worksheet's name as a class variable
 * 
 * @param {string} worksheet_name The name of the current worksheet.
 */
Request._init_once = function(worksheet_name) {
  $.getJSON(
    '../../eval_server.json',
    function(data, textStatus, jqXHR) {
      Request.prototype.endpoint = 'http://' + data.server + ':' + data.port;
    }
  );
  Request.prototype.worksheet = worksheet_name;
  Request.prototype.choices = 'text python ruby';
};

/**
 * Evaluates a cell as text: there will be no output.
 * 
 * @param {string} input Text of the cell that is being evaluated.
 * @param {function} callback A function to call at the end of this function.
 */
Request.prototype._eval_text = function(input, callback) {
  $('#' + this.cell_id).children('.output').text('');
  callback('');
};

/**
 * Evaluates a cell as code: currently Python or Ruby.
 * 
 * @param {string} input Text of the cell that is being evaluated.
 * @param {function} callback A function to call at the end of this function.
 */
Request.prototype._eval_code = function(input, callback) {
  set_status('code');
};

/**
 * Sets the class of a cell, based on the button with which it was submitted.
 * 
 * @param {string} cell_id The ID of a cell that we are modifying.
 * @param {string} type The new evaluation type.
 */
Request.prototype._set_eval_type = function(cell_id, type) {
  var self = this;
  $('#' + cell_id).removeClass(function() {
    return self.choices;
  }).addClass(type);
};

/*
 * Main JQuery code: attach functions to DOM elements as JQuery handlers.
 */
$(document).ready(function(){
  // Create a Notebook instance.
  var notebook = new Notebook();
  
  // Initialize future Requests.
  Request._init_once(notebook.worksheet_name);
  
  /** Prevent the actual submission of cell forms. */
  $('.cell form').live('submit', function(){
      return false;
  });
  
  /** Attach a handler to the "Add cell" button. */
  $('#add_cell').click(function(){
    notebook.add_cell();
  });
  
  /** Delete a cell from this notebook. */
  $('button.delete').live('click', function(){
    var ans = confirm('Do you want to permanently delete this cell?');
    if (ans) {
      // Be careful if the HTML structure of cell "widgets" changes.
      var id = $(this).parents('div.cell').attr('id');
      notebook.delete_cell(id);
    }

    // Don't actually submit the form.
    return false;
  });
  
  /** React to one of the cell submission buttons being clicked. */
  $('.cell form button').live('click', function(){
    var cell_id = $(this).parents('div.cell').attr('id');
    var input = $(this).siblings('.input').val();
    var type = $(this).attr('class');
    var req = new Request(type, cell_id);
    
    // Execute the request, with a callback to save the cell.
    req.execute(input, function(output){
      notebook.save_cell(new Cell({
        cell_id: cell_id,
        input: input,
        output: output,
        type: type,
      }))
    });
  });
});
