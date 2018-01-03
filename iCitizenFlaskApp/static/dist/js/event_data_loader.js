var eventInterval;
var count = 1;

function fetchevents() {
    $.ajax({
        url: "/get-user-events-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                events = response;
                for (bill of events) {
                    $('#event_'+count).html(event['title']);
                    count++;
                }
            }
            if(count >= 10) {
                console.log("Event interval has been cleared")
                clearInterval(eventInterval)
            } else {
                console.log("Still polling")
            }
        }
    })
}

$(document).ready(function(){
    eventInterval = setInterval(fetchnationalbills, 5000);
})