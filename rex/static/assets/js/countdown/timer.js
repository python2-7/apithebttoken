$(function(){
    function timer(settings){
        var config = {
            endDate: '2017-12-31 09:00:00',
            timeZone: 'America/New_York',
            hours: $('#hours'),
            minutes: $('#minutes'),
            seconds: $('#seconds'),
            newSubMessage: ''
        };
        function prependZero(number){
            return number < 10 ? '0' + number : number;
        }
        $.extend(true, config, settings || {});
        var currentTime = moment();
        var endDate = moment.tz(config.endDate, config.timeZone);
        var diffTime = endDate.valueOf() - currentTime.valueOf();
        var duration = moment.duration(diffTime, 'milliseconds');
        var days = duration.days();
        var interval = 1000;
        var subMessage = $('.sub-message');
        var clock = $('.clock');
        if(diffTime < 0){
            endEvent(subMessage, config.newSubMessage, clock);
            return;
        }
        if(days > 0){
            $('#days').text(prependZero(days));
            $('.days').css('display', 'inline-block');
        }
        var intervalID = setInterval(function(){
            duration = moment.duration(duration - interval, 'milliseconds');
            var hours = duration.hours(),
                minutes = duration.minutes(),
                seconds = duration.seconds();
            days = duration.days();
            if(hours  <= 0 && minutes <= 0 && seconds  <= 0 && days <= 0){
                clearInterval(intervalID);
                endEvent(subMessage, config.newSubMessage, clock);
                window.location.reload();
            }
            if(days === 0){
                $('.days').hide();
            }
            $('#days').text(prependZero(days));
            config.hours.text(prependZero(hours));
            config.minutes.text(prependZero(minutes));
            config.seconds.text(prependZero(seconds));
        }, interval);
    }


    function timers(settings){
        var config = {
            endDate: '2017-12-31 09:00:00',
            timeZone: 'America/New_York',
            hours: $('#hourss'),
            minutes: $('#minutess'),
            seconds: $('#secondss'),
            newSubMessage: ''
        };
        function prependZero(number){
            return number < 10 ? '0' + number : number;
        }
        $.extend(true, config, settings || {});
        var currentTime = moment();
        var endDate = moment.tz(config.endDate, config.timeZone);
        var diffTime = endDate.valueOf() - currentTime.valueOf();
        var duration = moment.duration(diffTime, 'milliseconds');
        var days = duration.days();
        var interval = 1000;
        var subMessage = $('.sub-messages');
        var clock = $('.clocks');
        if(diffTime < 0){
            endEvent(subMessage, config.newSubMessage, clock);
            return;
        }
        if(days > 0){
            $('#dayss').text(prependZero(days));
            $('.dayss').css('display', 'inline-block');
        }
        var intervalID = setInterval(function(){
            duration = moment.duration(duration - interval, 'milliseconds');
            var hours = duration.hours(),
                minutes = duration.minutes(),
                seconds = duration.seconds();
            days = duration.days();
            if(hours  <= 0 && minutes <= 0 && seconds  <= 0 && days <= 0){
                clearInterval(intervalID);
                endEvent(subMessage, config.newSubMessage, clock);
                window.location.reload();
            }
            if(days === 0){
                $('.dayss').hide();
            }
            $('#dayss').text(prependZero(days));
            config.hours.text(prependZero(hours));
            config.minutes.text(prependZero(minutes));
            config.seconds.text(prependZero(seconds));
        }, interval);
    }

    function endEvent($el, newText, hideEl){
        $el.text(newText);
        hideEl.hide();
    }
    timer();
    timers();
});

// $(function(){
//    $("#d .number").countdown("2018/01/01 09:59:59", function(event) {
//     $(this).text(event.strftime('%D'));
//     });
//     $("#h .number").countdown("2018/01/01 09:59:59", function(event) {
//         $(this).text(event.strftime('%H'));
//     });
//     $("#m .number").countdown("2018/01/01 09:59:59", function(event) {
//         $(this).text(event.strftime('%M'));
//     });
//     $("#s .number").countdown("2018/01/01 09:59:59", function(event) {
//         $(this).text(event.strftime('%S'));
//     });
// });

/*

$(function(){
  var deadline_start = new Date(Date.parse("Sat Dec 10 2017 10:00:00") + 2 * 24 * 60 * 60 * 1000);
  initializeClock('clockdiv_ico', deadline_start);
});


function getTimeRemaining(endtime) {
  var t = Date.parse(endtime) - Date.parse(new Date());
  var seconds = Math.floor((t / 1000) % 60);
  var minutes = Math.floor((t / 1000 / 60) % 60);
  var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
  var days = Math.floor(t / (1000 * 60 * 60 * 24));
  return {
    'total': t,
    'days': days,
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}

function initializeClock(id, endtime) {
  var clock = document.getElementById(id);
  var daysSpan = clock.querySelector('.days');
  var hoursSpan = clock.querySelector('.hours');
  var minutesSpan = clock.querySelector('.minutes');
  var secondsSpan = clock.querySelector('.seconds');

  function updateClock() {
    var t = getTimeRemaining(endtime);

    daysSpan.innerHTML = t.days;
    hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
    minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
    secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

    if (t.total <= 0) {
      clearInterval(timeinterval);
    }
  }

  updateClock();
  var timeinterval = setInterval(updateClock, 1000);
}
*/