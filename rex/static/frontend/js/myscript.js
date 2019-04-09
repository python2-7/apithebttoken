var myVar;
var resizeLoader1;
function myLoader() {
	resizeLoader1 = setTimeout(resizeLoader,10);
  myVar = setTimeout(showPage,1000);
}

function showPage() {
	document.getElementById("loader").style.display = "none";
  document.getElementById("stage").style.display = "block";
  $("#animated-loader-spin img").appendTo(".nav-logo");
}
function resizeLoader(){
	document.getElementById("animated-loader-spin").classList.add("animate-small-width");  
}

$(function() {
  var $body = $('body'),
  $header = $body.find('header'),
  $slideshow = $body.find('#slide-show'),
  $menu = $body.find('#menu')

  $('#slide-show').superslides({
    hashchange: false,
    play: 8000,
    animation: 'fade',
    pagination: false
  }); 
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
  $('.scroll-down a').click(function(e) {
    e.preventDefault();
    $('html, body').animate({ scrollTop:  $slideshow.height()}, 500, 'linear');
  });
  $('#scroll-up').click(function(){
    $('html, body').animate({ scrollTop:  0}, 600, 'linear');
  });
  $(window).bind('scroll', function () {
      if ($(window).scrollTop() > 128) {
        // if ($(window).scrollTop() > $slideshow.height()) {
          $('.page-top-header').addClass('fixed');
          $('#logo-slide img').appendTo('#ecosystem-logo');
          $('#scroll-up').addClass('active');
      } else {
          $('.page-top-header').removeClass('fixed');
          $('#ecosystem-logo img').prependTo('#logo-slide');
          $('#scroll-up').removeClass('active');
      }
  });
});