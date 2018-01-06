var nationalInterval, stateInterval;
var count = 1;

var state, national;
var image_class = (window.location.pathname === '/dashboard/') ? 'col-sm-5' : 'col-sm-3';

var regularStar = "<i style='color: tomato;' class='fa-2x far fa-star' data-fa-transform='shrink-7'></i>";
var solidStar = "<i style='color: tomato;' class='fa-2x fas fa-star' data-fa-transform='shrink-7'></i>";

function fetchnationallegs() {
    $.ajax({
        url: "/get-national-legislators-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                national = response['national_legislators'];
                var saved_legislators = response['saved_legislators']
                count = 1;

                for (legislator of national) {
                    if(count > 10)
                        break;

                    var party = legislator['party'];
                    if(party === 'D') {
                        party = 'Democrat';
                    } else if (party === 'R') {
                        party = 'Republican';
                    } else {
                        party = 'Independent';
                    }

                    var info = '';
                    if( legislator['district'] ){
                        info += 'District: ' + legislator['district'] + '<br><br>';
                    }
                    var level = legislator['level'];
                    info += 'Level: ' + level.charAt(0).toUpperCase() + level.substring(1, level.length).toLowerCase() + '<br><br>';
                    info += 'Party: ' + party + '<br><br>';
                    info += 'State: ' + legislator['state'];

                    console.log(legislator['id']);
                    var saved = "saved=" + ( (legislator['id'] in saved_legislators) ? "'true'" : "'false'");
                    console.log(saved);
                    var star = (saved === "saved='true'") ? solidStar : regularStar;

                    $('#legislator_national_'+count).html(`
                        <div class="card mb-4" style='height: 25rem; box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                            <div class='card-header clearfix d-inline-flex'>
                                <h4 class='mr-auto'>` + legislator['last_name'] + ', ' + legislator['first_name'] + `</h4>
                                <!-- data-count is used for saving and retrieving polls -->
                                <div class='star-holder' level='national' data-count='`+ count +`' ` + saved + `>
                                    ` + star + `
                                </div>
                            </div>
                            <div class="card-block">
                                <div class="row ml-3" style='height: 16rem;'>
                                    <div class=` + image_class + ` 
                                        style='
                                            background-image: url(` + legislator['photo_url'] + `);
                                            background-repeat: no-repeat;
                                            background-position: center;
                                            background-size: cover;
                                            border: 0.25em solid #59698d;
                                            border-radius: 1em;'>
                                    </div>
                                    <div class='col-sm-6 pull-left'>
                                        <h6 class='card-title' style='color: cornflowerblue;'>Chamber: ` + legislator['chamber'] + `</h6><br>
                                        <p class='card-text' style='color: coral;'>` + info + `</p>
                                    </div>
                                </div>
                                
                            </div>
                            <div class="card-footer text-muted">Legislator ID: ` + legislator['id'] + `</div>
                            </div>
                        </div>
                        `)
                    count++;
                }

                console.log("National legislator interval has been cleared");
                clearTimeout(nationalInterval);
            } else {
                console.log("Still polling");
                setTimeout(fetchnationallegs, 1000);
            }
        },
        complete: function(response) {
            if(response === null)
                setTimeout(fetchnationallegs, 1000);
        }
    })
}

function fetchstatelegs() {
    $.ajax({
        url: "/get-state-legislators-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                state = response['state_legislators'];
                var saved_legislators = response['saved_legislators'];

                count = 1;
                for (legislator of state) {
                    if(count > 10)
                        break;

                    var party = legislator['party'];
                    var info = '';
                    if( legislator['district'] ){
                        info += 'District: ' + legislator['district'] + '<br><br>';
                    }
                    var level = legislator['level'];
                    info += 'Level: ' + level.charAt(0).toUpperCase() + level.substring(1, level.length) + '<br><br>';
                    info += 'Party: ' + party + '<br><br>';
                    info += 'State: ' + legislator['state'].toUpperCase();

                    var chamber = legislator['chamber'];
                    chamber = chamber.charAt(0).toUpperCase() + chamber.substring(1, level.length);

                    console.log(legislator['id']);
                    var saved = "saved=" + ( (legislator['id'] in saved_legislators) ? "'true'" : "'false'");
                    console.log(saved);
                    var star = (saved === "saved='true'") ? solidStar : regularStar;

                    $('#legislator_state_'+count).html(`
                        <div class="card mb-4" style='height: 25rem; box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                            <div class='card-header clearfix d-inline-flex'>
                                <h4 class='mr-auto'>` + legislator['last_name'] + ', ' + legislator['first_name'] + `</h4>
                                <!-- data-count is used for saving and retrieving polls -->
                                <div class='star-holder' level='state' data-count='`+ count +`' ` + saved + `>
                                    ` + star + `
                                </div>
                            </div>
                            <div class="card-block">
                                <div class="row ml-3" style='height: 16rem;'>
                                    <div class=` + image_class + `
                                        style='
                                            background-image: url(` + legislator['photo_url'] + `);
                                            background-repeat: no-repeat;
                                            background-position: center;
                                            background-size: cover;
                                            border: 0.25em solid #59698d;
                                            border-radius: 1em;'>
                                    </div>
                                    <div class='col-sm-6 pull-left'>
                                        <h6 class='card-title' style='color: cornflowerblue;'>Chamber: ` + chamber + `</h6><br>
                                        <p class='card-text' style='color: coral;'>` + info + `</p>
                                    </div>
                                </div>
                                
                            </div>
                            <div class="card-footer text-muted">Legislator ID: ` + legislator['id'] + `</div>
                            </div>
                        </div>
                        `
                    );
                    $('#loader').html("");
                    $('#loader').attr('style', '')
                    count++;
                }

                console.log("State legislator interval has been cleared")
                clearTimeout(stateInterval)
            } else {
                console.log("Still polling")
                setTimeout(fetchstatelegs, 1000);
            }
        },
        complete: function(response) {
            if(response === null)
                setTimeout(fetchstatelegs, 1000);
        }
    });
}

$(document).ready(function(){
    nationalInterval = setTimeout(fetchnationallegs, 1000);

    // Only load state legislators if we are not on the dashboard
    if( image_class === 'col-sm-3')
        stateInterval = setTimeout(fetchstatelegs, 1000);

    $('body').on('click', 'div.star-holder', function() {
        var div = $(this);
        var index = $(this).attr('data-count');
        console.log(state);
        var legislator = (div.attr('level') === 'national') ? national[index - 1] : state[index - 1];

        if(div.attr('saved') === 'false') {
            console.log('was not saved');

            $.ajax({
                url: '/save-legislator/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(legislator),
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
            console.log('index: ' + (index - 1));

            $.ajax({
                url: '/delete-saved-legislator/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({'id': legislator['id']}),
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
    })
})