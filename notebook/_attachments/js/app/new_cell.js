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
 
    function new_cell(id, input, output, type) {
        function html_escape(str) {
            if (typeof str == 'string') {  
                return str.replace(/&/g, '&amp;').replace(/>/g, '&gt;')
                        .replace(/</g, '&lt;').replace(/"/g, '&quot;')
                        .replace(/'/, '&#039;');
            } else {
                return str;
            }
        }
      
        return '<div class="cell ' + (type || 'text') + '" id="' + 
              html_escape(id) + '"> \ <button class="visualize"></button> \
              <button class="delete">X</button> \
              <form method="POST"> \
                <button type="submit" class="text">txt</button> \
                <button type="submit" class="python">py</button> \
                <button type="submit" class="ruby">rb</button> \
                <textarea class="input">' + html_escape(input) + '</textarea> \
              </form> \
              <div class="output">' + html_escape(output) + '</div> \
            </div>';
    }
