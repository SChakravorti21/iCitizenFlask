var result1;
var result2;

$.ajax({
    url: "/load_db/",
    type: "post",
    success: function(response){
    result1 = response
    $('#bill_test').html(result1)
    }
});

