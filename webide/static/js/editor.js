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

//global variables

//the sync polling interval (in milliseconds). the shorter, the more responsive.
window['pollinginterval'] = 500

//the client shadow for differential synchronization
window['shadow'] = "{{ clishadow }}"

//the caret position for this client, which we want to preserve
window['caretpos'] = 0

//functions

//pings the server for a sync update. The server does the computations and returns a text and updated shadow
//to the client.
function pingServer() {

//we need to keep the caret position

//send POST request with ajax

$.ajax ({
url: '/sync/',
//middleware token must be sent for django to accept the connection;
//so we will also use it as a 'session id'
data: { top: $(“#fileview”).text(), clientshadow: window['shadow'], csrfmiddlewaretoken:'{{csrf_token}}'},
dataType: 'json',
type: "POST",
success: function(response) {
//update the text in box
$(“#fileview”).text(response.topDoc);
//restore the caret position
//update client shadow
window['shadow'] = response.clientshadow;
}
})

}

//sets the sync function to run at the polling interval.
//originally responded to a button, but now will be called upon page loading.
function beginSync() {
setInterval(pingServer, window['pollinginterval']);
}

//start synchronization immediately when document is ready
//$(document).ready(beginSync);

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

	//begin polling for updates
	
});