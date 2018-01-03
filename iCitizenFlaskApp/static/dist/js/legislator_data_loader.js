var nationalInterval, stateInterval;
var count = 1;

function fetchnationallegs() {
    $.ajax({
        url: "/get-national-legislators-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                national = response;
                for (legislator of national) {
                    $('#bill_'+count).html(legislator['title']);
                    count++;
                }
            }
            if(count >= 10) {
                console.log("National interval has been cleared")
                clearInterval(nationalInterval)
            } else {
                console.log("Still polling")
            }
        }
    })
}

function fetchstatelegs() {
    $.ajax({
        url: "/get-state-legislators-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                state = response;
                for (legislator of state) {
                    $('#bill_'+count).html(legislator['title']);
                    count++;
                }
            }
            if(count >= 20) {
                console.log("State interval has been cleared")
                clearInterval(stateInterval)
            } else {
                console.log("Still polling")
            }
        }
    });
}
$(document).ready(function(){
    nationalInterval = setInterval(fetchnationallegs, 5000);
    stateInterval = setInterval(fetchstatelegs, 5000);
})