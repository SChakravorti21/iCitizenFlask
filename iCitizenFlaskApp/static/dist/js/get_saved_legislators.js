var legislatorInterval;
var count = 1;

var saved;

var regularStar = "<i style='color: tomato;' class='fa-2x far fa-star' data-fa-transform='shrink-7'></i>";
var solidStar = "<i style='color: tomato;' class='fa-2x fas fa-star' data-fa-transform='shrink-7'></i>";

function fetchlegislators() {
    $.ajax({
        url: "/fetch-saved-legislators/",
        type: "GET",
        dataType: "json",
        success: function(response){
            if(response != null){
                saved = response;
                console.log(saved)
                count = 1;

                for (var key in saved) {
                    legislator = saved[key];
                    console.log(legislator)

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
                    var star = solidStar;

                    $('#legislator_'+count).html(`
                        <div class="card mb-4" style='height: 25rem; box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                            <div class='card-header clearfix d-inline-flex'>
                                <h4 class='mr-auto'>` + legislator['last_name'] + ', ' + legislator['first_name'] + `</h4>
                                <!-- data-count is used for saving and retrieving polls -->
                                <div class='star-holder' legislator_id='` + key + `' data-count='`+ count +`' saved='true'>
                                    ` + star + `
                                </div>
                            </div>
                            <div class="card-block">
                                <div class="row ml-3" style='height: 16rem;'>
                                    <div class="col-sm-3" 
                                        style='
                                            background-image: url(` + legislator['photo_url'] + `);
                                            background-repeat: no-repeat;
                                            background-position: center;
                                            background-size: cover;
                                            border: 0.25em solid #59698d;
                                            border-radius: 1em;'>
                                    </div>
                                    <div class='col-sm-8 pull-left'>
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

                $('#loader').html("");
                $('#loader').attr('style', '');
                console.log("Legislator interval has been cleared");
                clearTimeout(legislatorInterval);
            } else {
                console.log("Still polling");
            }
        },
        complete: function(response) {
            if(response === null)
                setTimeout(fetchlegislators, 1000);
        }
    })
}

$(document).ready(function(){
    legislatorInterval = setTimeout(fetchlegislators, 10);

    $('body').on('click', 'div.star-holder', function() {
        var div = $(this);
        var index = $(this).attr('data-count');
        var legislator = saved[div.attr('legislator_id')];

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