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

                  <div> TEST</div>

                  `
                  // html = `
                  //
                  // <div class="col-4 col-sm-6 col-md-4 col-lg-4 col-xl-4">
                  //
                  //   <div class="card" style="width: 20rem; padding:30px;">
                  //     <img class="card-img-top" src=` + event['img_link']  + `alt="Card image cap">
                  //     <div class="card-block">
                  //       <h4 class="card-title">` + event['org_title']  + `</h4>
                  //       <p class="card-text"> ` + event['location']   +   `</p>
                  //     </div>
                  //     <ul class="list-group list-group-flush">
                  //       <li class="list-group-item">` + event['time'] + `</li>
                  //       <li class="list-group-item">`  + event['price'] + `</li>
                  //       <li class="list-group-item">Relevance Score: ` + event['pts'] + `</li>
                  //
                  //       <label class="custom-checkbox label_event" style="margin: 20px 0px -10px 20px">
                  //
                  //         <input type="checkbox" name = "box" value=` + event['title'] + ` {% if ` + event['saved'] + ` %} checked {% endif %}/>
                  //           <span>Add to Saved Events</span>
                  //       </label>
                  //
                  //
                  //     </ul>
                  //     <div class="card-block">
                  //       <a href=` + event['link']  + `target="_blank" class="card-link">More Info</a>
                  //     </div>
                  //     </div>
                  //
                  //   </div>
                  //
                  //
                  //
                  //
                  // `

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
