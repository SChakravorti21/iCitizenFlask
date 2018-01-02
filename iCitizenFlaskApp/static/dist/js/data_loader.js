var result1;
var result2;
var result3;

$.ajax({
    url: "/update_polls/",
    type: "post",
    success: function(response) {
    result3 = response
    $('#poll_test').html(result3)
    }
});

$.ajax({
    url: "/load_db/",
    type: "post",
    success: function(response){
    result1 = response
    $('#bill_test').html(result1)
    }
});

