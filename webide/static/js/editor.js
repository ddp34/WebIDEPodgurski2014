$(document).ready(function() {
	//set listener
	$(".filecontentsview").keydown(function(e) {
		if(e.keyCode==9) {
		    e.currentTarget.insert("\t");
		    e.stop();
		}
	    });
});