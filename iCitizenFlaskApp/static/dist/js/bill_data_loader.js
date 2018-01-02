var nationalInterval, stateInterval;
var count = 1;

function fetchnationalbills() {
    $.ajax({
        url: "/get-national-bills-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                national = response;
                for (bill of national) {
                    $('#bill_'+count).html(bill['title']);
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

function fetchstatebills() {
    $.ajax({
        url: "/get-state-bills-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                state = response;
                for (bill of state) {
                    $('#bill_'+count).html(bill['title']);
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
    nationalInterval = setInterval(fetchnationalbills, 5000);
    stateInterval = setInterval(fetchstatebills, 5000);
})