var toClearInterval = false
var interval

interval = setInterval(
    $.ajax({
        url: "/get-bills-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            var count = 1;
            national = response;
            state = response;
            for (bill of national) {
                $('#bill_'+count).html(bill['title']);
                count++;
            }
            for (bill of state) {
                $('#bill_'+count).html(bill['title']);
                count++;
            }
            if(count >= 20) {
                toClearInterval = true;
                console.log("Got here")
            }
        }
}), 5000);

if(toClearInterval) {
    console.log("Interval has been cleared")
    clearInterval(interval)
}