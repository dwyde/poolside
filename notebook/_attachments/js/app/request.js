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
  Request.prototype.endpoint = '/_eval';
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
  var self = this;
  $.ajax({
    url: self.endpoint,
    data: {
        worksheet: self.worksheet,
        content: input,
        language: self.type
    },
    success: function(msg){
        var output = msg.content;
        if (msg.type == 'error') {
          set_status(output);
        }
        else {
          var result = (typeof output == 'object') ? 
                        JSON.stringify(output) : output;
          $('#' + self.cell_id).children('.output').text(result);
          var msg = (msg.type == 'restarted') ? 'Kernel restarted.' : 
                  'Code evaluated.';
          set_status(msg);
          callback(output);
        }
    },
    error: function(req, status, error) {
        set_status(error);
    },
    dataType: 'json',
    type: 'POST',
  });
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
