 function Time() {
            var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'America/New_York', timeZoneName: 'short' };
            document.getElementById('CurrentTime').innerText = new Date().toLocaleTimeString('en-US', options);
        }
        setInterval(Time, 1000);


function StartDate() {
    selectedStartDate = document.getElementById('startDateChoose').value;
    document.getElementById('start_date').innerText = 'Start Date: ' + selectedStartDate;
    calculateWeekDifference();
}
var selectedStartDate;

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

calculateWeekDifference();
