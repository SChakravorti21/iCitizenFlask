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

                  html = `
                    <div class="card mb-4" style='height: 25rem; box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                        <h4 class="card-header" style="background-color: #cadbf7;"> ` + event['org_title'] + `</h4>
                        <div class = "card-block">
                            <div class="row ml-3" style = "height: 16rem;">
                                <div class="col-sm-3"
                                    style="
                                    background-image: url(` + event['img_link'] + `);
                                    background-repeat: no-repeat;
                                    background-position: center;
                                    background-size: cover;
                                    border: 0.25em solid #59698d;
                                    border-radius: 1em;"/>


                               <ul class="list-group list-group-flush">
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

                        <label class="custom-checkbox label_event" style="margin: 20px 0px -10px 20px">
                            <input type="checkbox" name = "box" style="transform: scale(1.5);"/>
                            <font size="+0">Add to Saved Events</font>
                            <br>
                        </label>

                        </div>


                    </div>

                  `

                    $('#event_'+count).html(html);
                    count++;
                }
            }
            if(count >= 10) {
                console.log("Event interval has been cleared")
                clearInterval(eventInterval)
            } else {
                console.log("Still polling")
            }
        }
    })
}

$(document).ready(function(){
    eventInterval = setInterval(fetchevents, 5000);
})
