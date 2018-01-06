var nationalInterval, stateInterval;
var nationalBills, stateBills;

var regularStar = "<i style='color: tomato;' class='fa-2x far fa-star' data-fa-transform='shrink-7'></i>";
var solidStar = "<i style='color: tomato;' class='fa-2x fas fa-star' data-fa-transform='shrink-7'></i>";

function fetchnationalbills() {
    $.ajax({
        url: "/get-saved-national-bills/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                var count = 1;
                nationalBills = response;
                for (var key in nationalBills) {
                    bill = nationalBills[key];
                    if(count > 10)
                        break;

                    var saved = "saved='true'"
                    var star = solidStar;
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
                            <div class="card-header clearfix d-inline-flex">` + 
                                `<h4 class='mr-auto'>` + bill['level'].toUpperCase() + `</h4>
                                <div class='star-holder' bill_id="`+ bill['bill_id'] + `" level="`+ bill['level'] + `" data-count='`+ count +`' ` + saved + `>` + star + `</div>
                            </div>
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
                    count++;
                }

                $('#loader').html("");
                $('#loader').attr('style', '')
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
        url: "/get-saved-state-bills/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                var count = 11;
                stateBills = response;
                for (var key in stateBills) {
                    bill = stateBills[key];
                    if(count >= 20)
                        break;
                    
                    var saved = "saved='true'"
                    var star = solidStar;

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
                            <div class="card-header clearfix d-inline-flex">` + 
                                `<h4 class='mr-auto'>` + bill['level'].toUpperCase() + `</h4>
                                <div class='star-holder' bill_id="`+ bill['bill_id'] + `" level="`+ bill['level'] + `" data-count='`+ count +`' ` + saved + `>` + star + `</div>
                            </div>
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
                clearInterval(stateInterval)
            } else {
                console.log("Still polling")
            }
        }
    });
}
$(document).ready(function(){
    nationalInterval = setInterval(fetchnationalbills, 1000);
    stateInterval = setInterval(fetchstatebills, 1000);

    $('body').on('click', 'div.star-holder', function() {
        var div = $(this);
        var level = $(this).attr('level');
        var id = $(this).attr('bill_id');
        console.log('Sending: ');
        if(level === 'national') {
            if(div.attr('saved') === 'false') {
                console.log('was not saved');
                $.ajax({
                    url: '/save-national-bill/',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(nationalBills[id]['bill_id']),
                    success: function(data) {
                        if(data) {
                            console.log('Post successful. Result: ');
                            console.log(data);
    
                            div.html(solidStar);
                            div.attr('saved', 'true');
                        }
                    }
                });
            } else {
                console.log('was saved');
                $.ajax({
                    url: '/delete-saved-national-bill/',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({'bill_id': nationalBills[id]['bill_id']}),
                    success: function(data) {
                        if(data) {
                            console.log('Post successful. Result: ');
                            console.log(data);
    
                            div.html(regularStar);
                            div.attr('saved', 'false');
                        }
                    }
                });
            }
        } else {
            if(div.attr('saved') === 'false') {
                console.log('was not saved');
                $.ajax({
                    url: '/save-state-bill/',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(stateBills[id]['bill_id']),
                    success: function(data) {
                        if(data) {
                            console.log('Post successful. Result: ');
                            console.log(data);
    
                            div.html(solidStar);
                            div.attr('saved', 'true');
                        }
                    }
                });
            } else {
                console.log('was saved');
                $.ajax({
                    url: '/delete-saved-state-bill/',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({'bill_id': stateBills[id]['bill_id']}),
                    success: function(data) {
                        if(data) {
                            console.log('Post successful. Result: ');
                            console.log(data);
    
                            div.html(regularStar);
                            div.attr('saved', 'false');
                        }
                    }
                });
            }
        }
    })
})