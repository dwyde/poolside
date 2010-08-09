$(document).ready(function(){
    $("button#new").click(function(){
        var name = prompt("Please enter a name for the new worksheet.");
        if (name != undefined) {
            $("form#new_worksheet input#worksheet").val(name);
            $("form#new_worksheet").submit();
        }
    });
    
    $("button#delete").click(function(){
        var worksheet = $("input[@id=worksheet]:checked").val();
        if (worksheet != undefined) {
            var accepted = confirm("Are you sure you want to delete worksheet \"" + worksheet + "\"?");
            if (accepted) {
                $("form#worksheet_action input#action").val('delete');
                $("form#worksheet_action").submit();
            }
        }
    });
    
    $("button#copy").click(function(){
        var worksheet = $("input[@id=worksheet]:checked").val();
        if (worksheet != undefined) {
            var name = prompt("Please enter a name for the new worksheet.");
            if (name != undefined) {
                $("form#worksheet_action input#action").val('copy');
                $("form#worksheet_action input#new_name").val(name);
                $("form#worksheet_action").submit();
            }
        }
    });
});
