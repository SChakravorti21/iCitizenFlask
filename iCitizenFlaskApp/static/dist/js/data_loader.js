var result1;
var result2;

$.ajax({
    url: "/update_bills/",
    type: "post",
    success: function(response){
    result1 = response
    $('#bill_test').html(result1)
    }
});

$.ajax({
    url: "/update_events/",
    type: "post",
    success: function(response) {
    result2 = response
    $('#event_test').html(result2)
    }
});