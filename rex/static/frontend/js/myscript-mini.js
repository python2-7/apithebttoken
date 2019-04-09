$(document).ready(function () {    
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
        if ($(window).scrollTop() > 0) {
            $('.page-top-header').addClass('fixed');
            $('#scroll-up').addClass('active');
        } else {
            $('.page-top-header').removeClass('fixed');
            $('#scroll-up').removeClass('active');
        }
    });
});