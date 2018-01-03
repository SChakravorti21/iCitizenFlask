var pollInterval;
var count = 1;

function fetchpolls() {
    $.ajax({
        url: "/get-user-polls/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                polls = response;
                for (poll of polls) {
                    $('#event_'+count).html(poll['title']);
                    count++;
                }
            }
            if(count >= 10) {
                console.log("Event interval has been cleared")
                clearInterval(pollInterval)
            } else {
                console.log("Still polling")
            }
        }
    })
}

$(document).ready(function(){
    pollInterval = setInterval(fetchpolls, 5000);
})