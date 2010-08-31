function new_cell(input, output) {
   var cell = '<form class="cell" method="POST"> \
   <input type="textarea" class="input" value="' + input + '" /> \
   <button type="submit">Evaluate</button> \
   <p class="output">' + output + '</p> \
   </form>';
   
   return cell;
}
