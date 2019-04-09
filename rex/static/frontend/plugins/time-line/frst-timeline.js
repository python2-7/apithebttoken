! function(t) {
    "use strict";
    t(document).ready(function() {
        $(".frst-timeline-content").css("position","relative");
        var defaultAnimation=$(".frst-container").attr("data-animation-name");       
        function n(n, i) {
            n.each(function() {
                var n = t(this).data("animation") || defaultAnimation;
                t(this).find(".frst-timeline-content").addClass("is-hidden").removeClass("animated " + n), "" == t("#select-animation").val() && t(this).find(".frst-timeline-content").removeClass("is-hidden")
            })
        }

        function i(n, i) {
            n.each(function() {
                if (t("#select-animation").val()) t(this).offset().top <= t(window).scrollTop() + t(window).height() * i && t(this).find(".frst-timeline-content").hasClass("is-hidden") && t(this).find(".frst-timeline-content").removeClass("is-hidden").addClass("animated " + 'slideInRight');
                else {
                    var n = t(this).data("animation") || defaultAnimation;
                    n && t(this).offset().top <= t(window).scrollTop() + t(window).height() * i && t(this).find(".frst-timeline-content").hasClass("is-hidden") && t(this).find(".frst-timeline-content").removeClass("is-hidden").addClass("animated " + 'slideInRight')
                }
            })
        }

        function e(n, i) {
            var e = 0;
            n.each(function() {
                var n = t(this).data("animation") || "defaultAnimation";
                if (n && t(window).scrollTop() + t(window).height() * i > t(this).offset().top && t(this).find(".frst-timeline-content").hasClass("is-hidden")) {
                    var a = t(this);
                    setTimeout(function() {
                        var fix = t("#select-animation").val() || defaultAnimation ;
                        a.find(".frst-timeline-content").removeClass("is-hidden").addClass("animated " + 'slideInRight');
                    }, e)
                }
                e += 200
            })
        }
        var a = t(".frst-timeline-block"),
            s = .8;
        n(a, s), e(a, s), t(window).on("scroll", function() {
            window.requestAnimationFrame ? window.requestAnimationFrame(function() {
                i(a, s)
            }) : setTimeout(function() {
                i(a, s)
            }, 100)
        }).change()
    })
}(jQuery);
$(document).ready(function () {
    var d = new Date();
    var nowTime = Math.floor(d.getTime()/1000);
    var arrTimeLine = [1514764800,1515110400,1517443200,1519862400,1522540800,1527811200,1535760000,1543622400,1575158400];
    var arrLen = arrTimeLine.length;
    var i = 0;

    while(i<arrLen) {           
        if (nowTime > arrTimeLine[i]) {  
            i++;               
        }   else    
            {    
                if($(window).scrollTop() < $('#' + arrTimeLine[i-1]).offset().top-400 || $(window).scrollTop() > $('#' + arrTimeLine[i-1]).offset().top+600 )  {                    
                    $('html, body').animate({scrollTop: $('#' + arrTimeLine[i-1]).offset().top-64}, 8000);                        
                }  
                i = arrLen;  
            }          
    }
    var $body = $('body'),
    $header = $body.find('header'),
    $menu = $body.find('#menu')

    $('#menu-toggle-top').click(function () {
        $('ul.navbar-nav').removeClass('flex-row');
        $('.navbar-nav-fullwidth').addClass('active');
        $('#bg-close-menu').addClass('active');
    });    
    $('#bg-close-menu').click(function() {
        $('.navbar-nav-fullwidth').removeClass('active');
        $('#bg-close-menu').removeClass('active');
        $('ul.navbar-nav').addClass('flex-row');
    });
    $('#scroll-up').on('click',function(){ 
              
        $('html, body').animate({ scrollTop:  0}, 600, 'linear');
    });
    $(window).bind('scroll', function () {
        if  ($(window).scrollTop() > 0) {
            $('#scroll-up').addClass('active');
        } else {
            $('#scroll-up').removeClass('active');
        }
    });
});