#!/usr/bin/env ruby
# 
# Simple Ruby REPL
# Copyright 2011 David Wyde and Christ Hart
#

require 'stringio'

_namespace = binding()
while true do
    # Read input
    _input = gets
    
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
    STDOUT.puts _stdout.string.gsub("\n", " ")
    STDOUT.flush
end