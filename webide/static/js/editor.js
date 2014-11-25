//Borrowed from Stack Overflow to insert text into a position in an HTML textarea:
//http://stackoverflow.com/questions/1064089/inserting-a-text-where-cursor-is-using-javascript-jquery
function insertAtCaret(areaId, text) {
	    var txtarea = document.getElementById(areaId);
	    var scrollPos = txtarea.scrollTop;
	    var strPos = 0;
	    var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ? 
		      "ff" : (document.selection ? "ie" : false ) );
	    if (br == "ie") { 
		txtarea.focus();
		var range = document.selection.createRange();
		range.moveStart ('character', -txtarea.value.length);
		strPos = range.text.length;
	    }
	    else if (br == "ff") strPos = txtarea.selectionStart;

	    var front = (txtarea.value).substring(0,strPos);  
	    var back = (txtarea.value).substring(strPos,txtarea.value.length); 
	    txtarea.value=front+text+back;
	    strPos = strPos + text.length;
	    if (br == "ie") { 
		txtarea.focus();
		var range = document.selection.createRange();
		range.moveStart ('character', -txtarea.value.length);
		range.moveStart ('character', strPos);
		range.moveEnd ('character', 0);
		range.select();
	    }
	    else if (br == "ff") {
		txtarea.selectionStart = strPos;
		txtarea.selectionEnd = strPos;
		txtarea.focus();
	    }
	    txtarea.scrollTop = scrollPos;
}

//code to be called immediately when page is loaded
$(document).ready(function() {
	//set key listener
	$(".filecontentsview").keydown(function(e) {
		//override 'tab' key for indenting source code
		if(e.keyCode==9) {
		    e.preventDefault();
		    insertAtCaret("fileview", "\t");
		}
	    });
	$(".filecontentsview").keyup(function(e) {
		if(e.keyCode==9) {
		    $(".filecontentsview").focus();
		}
	    });
});