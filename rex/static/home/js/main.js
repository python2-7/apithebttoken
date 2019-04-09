$(function ($) {
	"use strict"


	    //    preloader js start 
			setTimeout(function () {
				$('#preloader').fadeOut('slow', function () {});
		}, 600);
	

	// Nav stiky js code
	$(window).scroll(function () {
		var scroll = $(window).scrollTop();

		if (scroll >= 50) {
			$(".navbar-custom").addClass("bgcolor");
		} else {
			$(".navbar-custom").removeClass("bgcolor");
		}
	});

	//link to scroll js code
	$('.menu-nav a').on('click', function (event) {
		var $anchor = $(this);
		$('html, body').stop().animate({
			scrollTop: $($anchor.attr('href')).offset().top - 0
		}, 1500, 'easeInOutExpo');
		event.preventDefault();
	});

	// Nav Bar Js
	$(".menu-btn-open").on("click", function (e) {
		e.preventDefault();

		$(".menu-lightbox").fadeIn("normal", function () {
			$(this).addClass("active")
		});
		$(".menu-btn-close").addClass("loaded");
	});

	$(".menu-btn-close").on("click", function (e) {
		e.preventDefault();

		$(".menu-lightbox").delay(100).removeClass("active").delay(200).fadeOut("slow");
		$(".menu-btn-close").removeClass("loaded");
	});

	// nav link toggle
	$(".menu-nav li a").on("click", function (e) {
		$(".menu-btn-close").trigger("click");
	});

	//Venobox active js
	$('.venobox').venobox(); 



	// Create the carousel.
	$('.kc-wrap').KillerCarousel({
		width: 460,
		spacing3d: 60,
		spacing2d: 120,
		showReflection: true,
		infiniteLoop: true,
		autoScale:100
	});


	//Clint Review Slider

  var $phone_slider = $('.phone-slider');
				$phone_slider.owlCarousel({
								loop: true,
								autoplay: false,
								autoPlayTimeout: 1000,
								margin:30,
								dots:true,
								nav:false,
								responsive: {
										0: {
												items: 1
										},
										450: {
												items: 1
										},
										768: {
												items: 1
										},
										992: {
												items:1
										},
										993: {
												items: 1
										},
										1200: {
												items: 1
										}
								}
				});

  var $testimonials_slider = $('#owl-demo');
				$testimonials_slider.owlCarousel({
								loop: true,
								autoplay: false,
								autoPlayTimeout: 1000,
								margin:10,
								dots:true,
								nav:false,
								responsive: {
										0: {
												items: 1
										},
										450: {
												items: 1
										},
										768: {
												items: 1
										},
										992: {
												items:1
										},
										993: {
												items: 2
										},
										1200: {
												items: 1
										}
								}
				});


	
  //for scroll bottom to top js here
  if ($('#back-to-top').length) {
    var scrollTrigger = 100, // px
      backToTop = function () {
        var scrollTop = $(window).scrollTop();
        if (scrollTop > scrollTrigger) {
          $('#back-to-top').addClass('show');
        } else {
          $('#back-to-top').removeClass('show');
        }
      };
    backToTop();
    $(window).on('scroll', function () {
      backToTop();
    });
    $('#back-to-top').on('click', function (e) {
      e.preventDefault();
      $('html,body').animate({
        scrollTop: 0
      }, 700);
    });
	}



});