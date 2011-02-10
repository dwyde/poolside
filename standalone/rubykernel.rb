#!/usr/bin/env ruby

_b = binding()
while true do
    g = gets
    begin
        puts _b.eval(g)
    rescue Exception => myError
        puts myError
    end
    STDOUT.flush
end