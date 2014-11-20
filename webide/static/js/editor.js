//this code was partially borrowed from online: http://stackoverflow.com/questions/946534/insert-text-into-textarea-with-jquery/946556#946556
//we didnt invent this insertion function
$.fn.extend({
	insertTab: function(text) {
	    var sel, range, html;
	    if (window.getSelection) {
		sel = window.getSelection();
		if(sel.getRangeAt && sel.rangeCount) {
		    //don't do anything until we figure out how to insert a tab at the caret
		    //range = sel.getRangeAt(0);
		    //range.deleteContents();
		    //var indent = document.createElement("p");
		    //indent.style.textIndent = "4em";
		    //range.surroundContents(indent);
		}
	    } else if (document.selection && document.selection.createRange) {
		document.selection.createRange().text = text;
	    }
	}
    })

//This is our code
$(document).ready(function() {
	//set key listener
	$(".filecontentsview").keydown(function(e) {
		//override 'tab' key for indenting source code
		if(e.keyCode==9) {
		    e.preventDefault();
		    //indent the line by 4 spaces
		    $(".filecontentsview").insertTab("");
		}
	    });
	$(".filecontentsview").keyup(function(e) {
		if(e.keyCode==9) {
		    $(".filecontentsview").focus();
		}
	    });
});