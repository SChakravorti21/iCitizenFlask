var nationalInterval, stateInterval;
var count = 1;

function fetchnationallegs() {
    $.ajax({
        url: "/get-national-legislators-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                national = response;
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

                    $('#legislator_national_'+count).html(`
                        <div class="card mb-4" style='height: 25rem; box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                            <h4 class="card-header">` + legislator['last_name'] + ', ' + legislator['first_name'] + `</h4>
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

                console.log("National legislator interval has been cleared");
                clearTimeout(nationalInterval);
            } else {
                console.log("Still polling");
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
                state = response;
                count = 1;
                for (legislator of state) {
                    if(count > 10)
                        break;

                    var party = legislator['party'];
                    var info = '';
                    if( legislator['district'] ){
                        info += 'District: ' + legislator['photo_url'] + '<br><br>';
                    }
                    var level = legislator['level'];
                    info += 'Level: ' + level.charAt(0).toUpperCase() + level.substring(1, level.length) + '<br><br>';
                    info += 'Party: ' + party + '<br><br>';
                    var state = legislator['state'].toUpperCase();
                    info += 'State: ' + state.charAt(0).toUpperCase() + state.substring(1, level.length).toLowerCase();

                    var chamber = legislator['chamber'];
                    chamber = chamber.charAt(0).toUpperCase() + chamber.substring(1, level.length);
                    $('#legislator_state_'+count).html(`
                        <div class="card mb-4" style='height: 25rem; box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                            <h4 class="card-header">` + legislator['last_name'] + ', ' + legislator['first_name'] + `</h4>
                            <div class="card-block">
                                <div class="row ml-3" style='height: 16rem;'>
                                    <div class="col-sm-3" 
                                        style='
                                            background-image: url(` + legislator['district'] + `);
                                            background-repeat: no-repeat;
                                            background-position: center;
                                            background-size: cover;
                                            border: 0.25em solid #59698d;
                                            border-radius: 1em;'>
                                    </div>
                                    <div class='col-sm-8 pull-left'>
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
    stateInterval = setTimeout(fetchstatelegs, 1000);
})