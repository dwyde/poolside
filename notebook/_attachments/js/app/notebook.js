/*
 * This file is part of Poolside, a computational notebook.
 * Copyright (C) 2011 David Wyde and Chris Hart, New College of Florida
 * 
 * Poolside is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 
 * 02110-1301, USA.
 * 
 */

/** 
 * Print out messages. 
 * 
 * @param {string} msg A status message to output.
 */
function set_status(msg) {
    var pane = $('#messages');
    pane.text(msg);
    pane.show().fadeOut(3000);
}

/**
 * Output a JQuery error message.
 */
function error_msg(req, status, error) {
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
