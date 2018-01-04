var nationalInterval, stateInterval;

function fetchnationalbills() {
    $.ajax({
        url: "/get-national-bills-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                var count = 1;
                national = response;
                for (bill of national) {
                    html = `
                        <div class="row">
                            <div class="col">
                                <div class="card mb-4" style='height: 25rem; box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                                    <div class="card-header">Bill ID: ` + bill['level'].toUpperCase() + `: ` + bill['bill_id'] + `</div>
                                    <div class="card-block">
                                        <h4 class="card-title">Author: ` + bill['author'] + `</h5>
                                        <h5 class="card-subtitle mb-2 text-muted>Bill Title: ` + bill['title'] + `</h6>
                                        <p class="card-text">Bill Description: ` + bill['description'] + `</p>
                                        <a href=`+ bill['govtrack_link'] + `" class="btn btn-primary>Bill Link</a>
                                        <a href="#" class="btn btn-success pull-right">More Info</a>
                                    </div>
                            </div>
                        </div>
                    `
                    $('#bill_'+count).html(html);
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
                var count = 11;
                state = response;
                for (bill of state) {
                    html = `
                        <div class="row">
                            <div class="col">
                                <div class="card mb-4" style='height: 25rem; box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                                    <div class="card-header">Bill ID: ` + bill['level'].toUpperCase() + `: ` + bill['bill_id'] + `</div>
                                    <div class="card-block">
                                        <h5 class="card-title">Author: ` + bill['author'] + `</h5>
                                        <p class="card-text">Bill Description: ` + bill['title'] + `</p>
                                        <a href="`+ bill['url'] + `" class="btn btn-primary>Bill Link</a>
                                        <a href="#" class="btn btn-secondary pull-right">More Info</a>
                                    </div>
                            </div>
                        </div>
                    `

                    $('#bill_'+count).html(html);
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
    nationalInterval = setInterval(fetchnationalbills, 2000);
    stateInterval = setInterval(fetchstatebills, 2000);
})