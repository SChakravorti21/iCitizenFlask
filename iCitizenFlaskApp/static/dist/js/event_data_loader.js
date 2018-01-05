var eventInterval;
var count = 1;

function fetchevents() {
    $.ajax({
        url: "/get-user-events-db/",
        type: "post",
        dataType: "json",
        success: function(response){
            if(response != null){
                events = response;

                for (event of events) {
                  if(count > 10)
                    break;

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
                          <label class="custom-checkbox label_event">
                              <input type="checkbox" name = "box" style="transform: scale(1.5); margin-right: 0.5em;"/>
                              <font size="+0">Add to Saved Events</font>
                              <br>
                          </label>
                        </div>
                      </div> `

                      // html = `<div>test</div>`

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
    eventInterval = setTimeout(fetchevents, 1000);
})
