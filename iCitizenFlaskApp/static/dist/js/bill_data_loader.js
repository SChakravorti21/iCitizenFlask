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
                    if(count > 10)
                        break;

                    detailsId = 'bill_' + count + '_info';
                    var num = bill['cosponsor_num']
                    if(bill['cosponsor_num'] == null)
                        num = 0;
                    details = `
                            <strong class="card-subtitle" style="font-size:25px"><em>Author Information</em></strong>
                            <p class="card-text" style="color:magenta; font-size:20px"><u style="color:green">Author Party</u>: ` + bill['author_party'] + `<br>
                            <u style="color:green">Author State</u>: ` + bill['author_state'] + `</p>
                            <br>
                            <strong class="card-subtitle" style="font-size:25px"><em>Bill Information</em></strong><br>
                            <p class="card-text" style="color:orange; font-size:20px"><u style="color:green">Bill Created</u>: ` + bill['created_date'] + `<br>
                            <u style="color:green">Last Action</u>: ` + bill['last_action'] + `<br><u style="color:green"># of cosponsors</u>: ` + num + `</p>
                    `

                    html = `
                        <div class="card mb-4" style="box-shadow: -5px 5px rgba(120,144,156,0.3);">
                            <div class="card-header">` + bill['level'].toUpperCase() + `</div>
                            <div class="card-block">
                                <h4 class="card-title" style="height:2.5rem; color:teal">Author: ` + bill['author'] + `</h4>
                                <h5 class="card-subtitle mb-2 text-muted" style="color:green; height:2rem; display:inline">Bill Title: </h5>
                                <h5 class="card-subtitle" style="height:2rem; color:red; display:inline">` + bill['title'] + `</h5>
                                <p></p>
                                <p class=".text-info card-text" style="line-height: 2rem; font-size: 20px">Bill Description: ` + bill['description'] + `</p>
                                <a class="btn btn-info" target="_blank" href="`+ bill['govtrack_link'] + `">Bill Link</a>
                                <button class="btn btn-primary float-right" type='button' data-toggle='collapse'
                                    data-target='#` + detailsId + `' aria-expanded="false" aria-controls="collapseExample">
                                    More info
                                </button>
                                <div class='card-body collapse' id='` + detailsId + `'>
                                    <br>
                                    <p class='card-text'>` + details + `</p>
                                </div>
                            </div>
                            <div class="card-footer text-muted">BILL ID: ` + bill['bill_id'].toUpperCase() + `</div>
                        </div>

                    `
                    $('#bill_'+count).html(html);
                    $('#loader').html("");
                    $('#loader').attr('style', '')
                    count++;
                }

                console.log("National interval has been cleared")
                clearTimeout(nationalInterval)
            } else {
                console.log("Still polling")
            }
        },
        complete: function(data) {
            if(data === null)
                setTimeout(fetchnationalbills, 1000); 
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
                    if(count >= 20)
                        break;

                    detailsId = 'bill_' + count + '_info';
                    var num = bill['cosponsor_num']
                    if(bill['cosponsor_num'] == null)
                        num = 0;
                    details = `
                            <strong class="card-subtitle" style="font-size:25px"><em>Author Information</em></strong>
                            <p class="card-text" style="color:magenta; font-size:20px">
                            <u style="color:green">Author State</u>: ` + bill['author_state'].toUpperCase() + `</p>
                            <br>
                            <strong class="card-subtitle" style="font-size:25px"><em>Bill Information</em></strong><br>
                            <p class="card-text" style="color:orange; font-size:20px"><u style="color:green">Bill Created</u>: ` + bill['created_date'] + `<br>
                            <u style="color:green">Last Action</u>: ` + bill['last_action'] + `<br><u style="color:green"># of cosponsors</u>: ` + num + `</p>

                    `

                    html = `
                        <div class="card mb-4" style="box-shadow: -5px 5px rgba(120,144,156,0.3);">
                            <div class="card-header">` + bill['level'].toUpperCase() + `</div>
                            <div class="card-block">
                                <h4 class="card-title" style="height:2.5rem; color:teal">Author: ` + bill['author'] + `</h4>
                                <p></p>
                                <p class=".text-info card-text" style="line-height: 2rem; font-size: 20px">Bill Description: ` + bill['description'] + `</p>
                                <a class="btn btn-info" href="`+ bill['url'] + `">Bill Link</a>
                                <button class="btn btn-primary float-right" type='button' data-toggle='collapse'
                                    data-target='#` + detailsId + `' aria-expanded="false" aria-controls="collapseExample">
                                    More info
                                </button>
                                <div class='card-body collapse' id='` + detailsId + `'>
                                    <br>
                                    <p class='card-text'>` + details + `</p>
                                </div>
                            </div>
                            <div class="card-footer text-muted">BILL ID: ` + bill['bill_id'].toUpperCase() + `</div>
                        </div>

                    `
                    $('#bill_'+count).html(html);
                    count++;
                }

                console.log("State interval has been cleared")
                clearTimeout(stateInterval)
            } else {
                console.log("Still polling")
            }
        }, 
        complete: function(data) {
            if(data === null)
                setTimeout(fetchstatebills, 1000);
        }
    });
}
$(document).ready(function(){
    nationalInterval = setTimeout(fetchnationalbills, 1000);
    stateInterval = setTimeout(fetchstatebills, 1000);
})
