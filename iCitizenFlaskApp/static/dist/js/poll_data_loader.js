function convertCamelToTitle(text) {
    var result = '';
    for(var i = 0; i < text.length; i++) {
        var char = text.charAt(i);
        // Capitalize the first letter
        if(i === 0) {
            result += char.toUpperCase();
        } 
        // If a character is a number or an uppercase letter, start a new word
        else if($.isNumeric(char) || char === char.toUpperCase()) {
            result += ' ' + char;
        } 
        // Otherwise just concat the letter
        else {
            result += char;
        }
    }
    return result;
}


var pollInterval;
var poll_count = 1;
var max_count_polls = (window.location.pathname === '/dashboard/') ? 3 : 20;
var polls = null;

var regularStar = "<i style='color: tomato;' class='fa-2x far fa-star' data-fa-transform='shrink-7'></i>";
var solidStar = "<i style='color: tomato;' class='fa-2x fas fa-star' data-fa-transform='shrink-7'></i>";

function fetchpolls() {
    $.ajax({
        url: "/get-user-polls/",
        type: "post",
        dataType: "json",
        success: function(response){
            console.log(response)
            if(response != null){
                polls = response;
                var saved_polls = response['saved_polls'];
                
                polls = polls['user_polls']['contests'];
                for (poll of polls) {
                    if(poll_count > max_count_polls)
                        break;

                    console.log('adding poll')
                    var type = poll['type'];
                    if(poll['office']) {
                        type += ', ' + poll['office'];
                    }
                    if(poll['referendumTitle']) {
                        var currentTitle = poll['referendumTitle'];
                        var fixedTitle = currentTitle.charAt(0) + 
                            currentTitle.substring(1, currentTitle.length).toLowerCase();

                        type += '<br>Referendum Title: ' + fixedTitle;
                    }

                    var district = poll['district'];
                    var title = district['name'] + ', ' + convertCamelToTitle(district['scope']);

                    var info = '';
                    if(poll['level']) {
                        info += 'Levels: ';
                        for( level of poll['level']) {
                            info += convertCamelToTitle(level) + ', ';
                        }
                        //Get rid of the trailing punctuation and add a line break
                        info = info.substring(0, info.length - 2) + '<br>'; 
                    }
                    if(poll['roles']) {
                        info += 'Roles: ';
                        for( role of poll['roles']) {
                            info += convertCamelToTitle(role) + ', ';
                        }
                        info = info.substring(0, info.length - 2) + '<br>';
                    }
                    if(poll['referendumSubtitle']) {
                        info += 'Referendum Subtitle: ' + poll['referendumSubtitle'];
                    }

                    var detailsId = 'poll_' + poll_count + '_info';
                    var details = '';
                    if(poll['candidates']) {
                        var candidates = poll['candidates'];
                        details += '<strong>Candidates: </strong><br><br>';
                        var candidateCount = 1;
                        for(candidate of candidates) {
                            details += '<em>Candidate ' + candidateCount + ':</em> <br>'
                            details += 'Candidate Name: ' + candidate['name'] + '<br>';
                            details += 'Party: ' + candidate['party'] + '<br>';
                            if(candidate['candidateUrl']) {
                                var url = candidate['candidateUrl'];
                                details += 'Additional information: <a href="' + url + '">' + url + '</a><br>';
                            }
                            if(candidate['channels']) {
                                var channels = candidate['channels'];
                                details += '<div>Contact candidate: ';
                                details += '<div class="fa-3x">'
                                for(channel of channels) {
                                    var channelType = channel['type'].toLowerCase();
                                    details += '<a class="font-awesome-link" href="' + channel['id'] + '" target="_blank"> <i class="fab fa-' + channelType + '" data-fa-transform="shrink-4" data-fa-mask="fas fa-square"></i></a> ';
                                }
                                details += '</div></div>'
                            }
                            candidateCount++;
                        }
                    }

                    if(poll['referendumUrl']) {
                        var url = poll['referendumUrl'];
                        details += 'Link: <a href="' + url + '">' + url + '</a>';
                    }

                    var saved = "saved=" + ( (poll['poll_id'] in saved_polls) ? "'true'" : "'false'");
                    var star = (saved === "saved='true'") ? solidStar : regularStar;

                    $('.poll_'+poll_count).html(`
                        <div class='card mb-4' style='box-shadow: -5px 5px rgba(120,144,156,0.3);'>
                            <div class='card-header clearfix d-inline-flex'>
                                <h4 class='mr-auto'>`+ type +`</h4>
                                <!-- data-count is used for saving and retrieving polls -->
                                <div class='star-holder-poll' data-count='`+ poll_count +`' ` + saved + `>
                                    ` + star + `
                                </div>
                            </div>
                            <div class='card-block'>
                                <h6 class='card-title' style='color: cornflowerblue;'>` + title + `</h6>
                                <p class='card-text' style='color: coral;'>` + info + `</p>
                                <button class='btn btn-info mb-2' type='button' data-toggle='collapse' 
                                    data-target='#` + detailsId + `' aria-expanded="false" aria-controls="collapseExample">
                                    More info
                                </button>
                                <div class='card-body collapse' id='` + detailsId + `'>
                                    <br>
                                    <p class='card-text'>` + details + `</p>
                                </div>
                            </div>
                        </div> `
                    );
                    $('#loader').html("");
                    $('#loader').attr('style', '');
                    poll_count++;
                }

                console.log("Poll interval has been cleared");
                clearTimeout(pollInterval);

            } else {
                console.log("Still polling")
            }
        },
        complete: function() {
            if(polls == null)
                setTimeout(fetchpolls, 1000);
        }

    })
}

$(document).ready(function(){
    pollInterval = setTimeout(fetchpolls, 1000);

    $('body').on('click', 'div.star-holder-poll', function() {
        var div = $(this);
        var index = $(this).attr('data-count');
        console.log('Sending: ');
        console.log('here index: ' + index);

        if(div.attr('saved') === 'false') {
            console.log('was not saved');
            $.ajax({
                url: '/save-poll/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(polls[index - 1]),
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
            console.log(polls);
            $.ajax({
                url: '/delete-saved-poll/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({'poll_id': polls[index - 1]['poll_id']}),
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
});