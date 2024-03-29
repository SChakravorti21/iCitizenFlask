var eventInterval;
var event_count = 1;

var regularStar = "<i style='color: tomato;' class='fa-2x far fa-star' data-fa-transform='shrink-7'></i>";
var solidStar =   "<i style='color: tomato;' class='fa-2x fas fa-star' data-fa-transform='shrink-7'></i>";

/*
calls fetch_saved_events from get_saved_data.py and receives a list of all
saved event objects
this method loops through the event list and dynamically updates the html on saved_events.html
*/
function fetchevents() {
    $.ajax({
        url: "/fetch-saved-events/",
        type: "get",
        dataType: "json",
        success: function(response){
            if(response != null){
                var saved_events = response

                for (var key in saved_events) {
                  event = saved_events[key]

                  if(event_count > 15) {
                    break;
                  }

                  var saved = "saved='true'";
                  var star = solidStar;

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
                                   <li class="list-group-item" style="background-color: #e5e6e8;">Relevance Score: ` + event['pts'] + `%</li>
                                   <li class="list-group-item">
                                      <a class="btn btn-info" target="_blank" href="`+ event['link'] + `">More Info</a>

                                   </li>
                               </ul>
                            </div>
                        </div>
                        <div class="card-footer">
                            <div class='star-holder-event' event_id='` + key + `' data-count='`+ event_count +`' ` + saved + `>`
                                + star + `

                            </div>
                        </div>
                      </div> `



                    $('#event_'+event_count).html(html);
                    $('#loader').html("");
                    $('#loader').attr('style', '')
                    event_count++;
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

    $('body').on('click', 'div.star-holder-event', function() {
      /*
      if the star is clicked and it was not already saved before, then a post request is
      made to the url 'save-event' in user_functions.py. It passes the Event object
      that corresponds to the div clicked.

      If the star is clicked but was already saved, a post request is made to 'delete-saved-event'
      in user_functions.py. It gives the ID of the event that corresponds to the div clicked
      */

        var div = $(this);
        var index = $(this).attr('data-count');
        var event_id = div.attr('event_id')

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

            $.ajax({
                url: '/delete-saved-event/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({'event_id': event_id}),
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
