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
                        <div class="row" style="padding-top: 1.5rem">
                            <div class="col">
                                <div class="card mb-4" style='height: 22.5rem; box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                                    <div class="card-header">` + bill['level'].toUpperCase() + `</div>
                                    <div class="card-block">
                                        <h4 class="card-title" style="height:2.5rem; color:teal">Author: ` + bill['author'] + `</h4>
                                        <h5 class="card-subtitle mb-2 text-muted" style="color:green; height:2rem; display:inline">Bill Title: </h5>
                                        <h5 class="card-subtitle" style="height:2rem; color:red; display:inline">` + bill['title'] + `</h5>
                                        <p></p>
                                        <p class=".text-info card-text" style="line-height: 2rem; font-size: 20px">Bill Description: ` + bill['description'] + `</p>
                                        <a class="btn btn-info" href="`+ bill['govtrack_link'] + `">Bill Link</a>
                                        <a class="btn btn-primary float-right" href="#">More Info</a>
                                    </div>
                                    <div class="card-footer text-muted">BILL ID: ` + bill['bill_id'].toUpperCase() + `</div>
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
                                        <h4 class="card-title">Author: ` + bill['author'] + `</h4>
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