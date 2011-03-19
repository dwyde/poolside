function indent(data, output) {
    var root = pv.dom(data)
    .root("data")
    .sort(function(a, b) {return pv.naturalOrder(a.nodeName, b.nodeName);});
    
    /* Recursively compute the package sizes. */
    root.visitAfter(function(n) {
        if (n.firstChild) {
            n.nodeValue = pv.sum(n.childNodes, function(n) {return n.nodeValue;});
        }
    });
    
    var vis = new pv.Panel()
    .width(260)
    .height(function() {return (root.nodes().length + 1) * 12;})
    .margin(5)
    .canvas(output); // Output target element.
    
    var layout = vis.add(pv.Layout.Indent)
    .nodes(function() {return root.nodes();})
    .depth(12)
    .breadth(12);
    
    layout.link.add(pv.Line);
    
    var node = layout.node.add(pv.Panel)
    .top(function(n) {return n.y - 6;})
    .height(12)
    .right(6)
    .strokeStyle(null)
    .events("all")
    .event("mousedown", toggle);
    
    node.anchor("left").add(pv.Dot)
    .strokeStyle("#1f77b4")
    .fillStyle(function(n) {return n.toggled ? "#1f77b4" : n.firstChild ? "#aec7e8" : "#ff7f0e";})
    .title(function t(d) {return d.parentNode ? (t(d.parentNode) + "." + d.nodeName) : d.nodeName;})
    .anchor("right").add(pv.Label)
    .text(function(n) {return n.nodeName;});
    
    node.anchor("right").add(pv.Label)
    .textStyle(function(n) {return n.firstChild || n.toggled ? "#aaa" : "#000";})
    .text(function(n) {return (n.nodeValue);});
    
    vis.render();
    
    /* Toggles the selected node, then updates the layout. */
    function toggle(n) {
        n.toggle(pv.event.altKey);
        return layout.reset().root;
    }
}