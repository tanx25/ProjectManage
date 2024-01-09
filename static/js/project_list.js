 function Time() {
            var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'America/New_York', timeZoneName: 'short' };
            document.getElementById('CurrentTime').innerText = new Date().toLocaleTimeString('en-US', options);
        }
        setInterval(Time, 1000);





function calculateWeekDifference() {
    var timeDifference = document.getElementById('timeDifference');
    var userStartDateElement = document.getElementById('userStartDate');
    var selectedStartDate = userStartDateElement ? userStartDateElement.dataset.startDate : null;

    if (selectedStartDate) {
        var startDate = new Date(selectedStartDate);
        var now = new Date();
        var differenceInTime = now.getTime() - startDate.getTime();
        var differenceInDays = differenceInTime / (1000 * 3600 * 24);
        var differenceInWeeks = Math.ceil(differenceInDays / 7);
        if (differenceInWeeks > 10) {
            timeDifference.innerText = "Completed!";
        } else {
            timeDifference.innerText = "Week " + differenceInWeeks;
        }
    } else {
        timeDifference.innerText = "Select a Start Date";
    }
}
 function scrollWeeks(direction) {
        var container = document.querySelector('.week-scroll');
        var scrollAmount = container.offsetWidth / 3;
        if (direction === 'left') {
        container.scrollLeft -= scrollAmount;
    } else {
        container.scrollLeft += scrollAmount;
    }
}

function updateProjectStatus(projectId, newStatus) {
    fetch(`/update_project_status/${projectId}/${newStatus}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status == 'success') {
            document.querySelector(`#projectStatus${projectId}`).innerText = newStatus;
        }
    });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


var youtubePlayers = {};

function onYouTubeIframeAPIReady() {
    var youtubeIframes = document.querySelectorAll('iframe[id^="youtubePlayer"]');
    youtubeIframes.forEach(function(iframe) {
        var projectId = iframe.id.replace('youtubePlayer', '');
        youtubePlayers[projectId] = new YT.Player(iframe.id, {
            events: {
                'onStateChange': function(event) {
                    console.log("Player State Changed", event.data);
                    if (event.data == YT.PlayerState.ENDED) {
                        console.log("Video Ended for Project ID:", projectId);
                        updateProjectStatus(projectId, 'Completed');
                    }
                }
            }
        });
    });
}

calculateWeekDifference();
