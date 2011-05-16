#!/usr/bin/env ruby -wKU
# 
# This file is part of Poolside, a computational notebook.
# Copyright (C) 2011 David Wyde and Chris Hart, New College of Florida
#
# Poolside is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 
# 02110-1301, USA.

require 'stringio'

_DUMMY_CHAR = [0xffff].pack('U')
_namespace = binding()
while true do
    # Read input
    _input = gets
    _input.gsub!(_DUMMY_CHAR, "\n")
    
    # Trap output
    _stdout = StringIO.new
    $stdout = _stdout
    
    # Evaluate input
    begin
        _namespace.eval(_input)
    rescue Exception => _myError
        print _myError
    end
    
    # Actually output the result
    STDOUT.puts _stdout.string.gsub("\n", _DUMMY_CHAR)
    STDOUT.flush
end
