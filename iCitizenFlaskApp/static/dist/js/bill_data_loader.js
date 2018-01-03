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
                    var startTag = "<div class=\"card\""
                    var endTag = "</div>"
                    var startCardBlock = "<div class=\"card-block\">"
                    var header = "<div class=\"card-header\">"+bill['level']+"</div>"
                    var cardTitle = "<h4 class=\"card-title\">"+bill['title']+"</h4>"
                    var text = "<p class=\"card-text\">"+bill['author']+"</p>"
                    var info = "<a class=\"btn btn-primary\">"+"More info"+"</a"
                    var fullText = startTag+header+startCardBlock+cardTitle+text+info+endTag+endTag
                    $('#bill_'+count).html(fullText);
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
                    var startTag = "<div class=\"card\""
                    var endTag = "</div>"
                    var startCardBlock = "<div class=\"card-block\">"
                    var header = "<div class=\"card-header\">"+bill['level']+"</div>"
                    var cardTitle = "<h4 class=\"card-title\">"+bill['title']+"</h4>"
                    var text = "<p class=\"card-text\">"+bill['author']+"</p>"
                    var info = "<a class=\"btn btn-primary\">"+"More info"+"</a"
                    var fullText = startTag+header+startCardBlock+cardTitle+text+info+endTag+endTag
                    $('#bill_'+count).html(fullText);
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