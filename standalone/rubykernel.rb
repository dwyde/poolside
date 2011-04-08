#!/usr/bin/env ruby -wKU
# 
# Simple Ruby REPL
# Copyright 2011 David Wyde and Christ Hart
#

require 'stringio'

_DUMMY_CHAR = "\uffff"
_namespace = binding()
while true do
    # Read input
    _input = gets
    _input.gsub(_DUMMY_CHAR, "\n")
    
    # Trap output
    _stdout = StringIO.new
    $stdout = _stdout
    
    # Evaluate input
    begin
        print _namespace.eval(_input)
    rescue Exception => _myError
        print _myError
    end
    
    # Actually output the result
    STDOUT.puts _stdout.string.gsub("\n", _DUMMY_CHAR)
    STDOUT.flush
end
