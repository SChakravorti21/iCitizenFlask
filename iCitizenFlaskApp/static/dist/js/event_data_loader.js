var eventInterval;
var count = 1;
var events = null;

var regularStar = "<i style='color: tomato;' class='fa-2x far fa-star' data-fa-transform='shrink-7'></i>";
var solidStar =   "<i style='color: tomato;' class='fa-2x fas fa-star' data-fa-transform='shrink-7'></i>";

function fetchevents() {
    $.ajax({
        url: "/get-user-events-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                var saved_events = response["saved_events"];
                events = response["user_events"];

                for (event of events) {



                  if(count > 15) {
                    break;
                  }

                  var saved = "saved=";
                  if(event["event_id"] in saved_events) {
                      saved += "'true'";
                  }
                  else {
                    saved += "'false'";
                  }
                  console.log(saved);

                  var star = (saved === "saved='true'") ? solidStar : regularStar;

                  html = `
                    <div class="card mb-4" style='box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                        <h4 class="card-header" style="background-color: #cadbf7;"> ` + event['org_title'] + `</h4>
                        <div class = "card-block">
                            <div class="row ml-3">
                                <div class="col-sm-3"
                                    style="
                                    background-image: url(` + event['img_link'] + `);
                                    background-repeat: no-repeat;
                                    background-position: center;
                                    background-size: cover;
                                    border: 0.25em solid #59698d;
                                    border-radius: 1em;
                                    align="middle""/>


                               <ul class="list-group list-group-flush" style="margin-left: 1em;">
                                   <li class="list-group-item">` + event['location'] + `</li>
                                   <li class="list-group-item" style="background-color: #e5e6e8;">` + event['time'] + `</li>
                                   <li class="list-group-item">` + event['price'] + `</li>
                                   <li class="list-group-item" style="background-color: #e5e6e8;">Relevance Score: ` + event['pts'] + `</li>
                                   <li class="list-group-item">
                                      <a class="btn btn-info" target="_blank" href="`+ event['link'] + `">More Info</a>

                                   </li>
                               </ul>
                            </div>
                        </div>
                        <div class="card-footer">
                            <div class='star-holder' data-count='`+ count +`' ` + saved + `>`
                                + star + `
                                <font>Save Event</font>
                        </div>
                        </div>
                      </div> `



                    $('#event_'+count).html(html);
                    $('#loader').html("");
                    $('#loader').attr('style', '')
                    count++;
                }

                console.log("Event interval has been cleared");
                clearTimeout(eventInterval);
            } else {
                console.log("Still polling");
            }
        },
        complete: function(data) {
          if(data === null)
            setTimeout(fetchevents, 1000);
        }
    })
}

$(document).ready(function(){
    eventInterval = setInterval(fetchevents, 2000);

    $('body').on('click', 'div.star-holder', function() {

        var div = $(this);
        var index = $(this).attr('data-count');
        console.log('event being saved:' + index)

        if(div.attr('saved') === 'false') {
            console.log("clicked save button");

            $.ajax({
                url: '/save-event/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(events[index - 1]),
                success: function(data) {
                  if(data) {
                        console.log('Post successful. Result: ');
                        console.log(data);

                        div.html(solidStar);
                        div.attr('saved', 'true');
                    }
                }
            });

        }

        else {
            console.log('unclicked save button');
            console.log('index = ' + (index - 1));
            console.log(events)

            $.ajax({
                url: '/delete-saved-event/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(events[index - 1]),
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

    });



})
