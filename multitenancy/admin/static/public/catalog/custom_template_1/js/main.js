(function ($) {
 "use strict";
	// jQuery MeanMenu
	jQuery('nav#dropdown').meanmenu();
	//menu a active jquery
	var pgurl = window.location.href.substr(window.location.href
		.lastIndexOf("/")+1);
		$("ul li a").each(function(){
		if($(this).attr("href") == pgurl || $(this).attr("href") == '' )
		$(this).addClass("active");
	$('header ul li ul li a.active').parent('li').addClass('parent-li');
	$('header ul li ul li.parent-li').parent('ul').addClass('parent-ul');
	$('header ul li ul.parent-ul').parent('li').addClass('parent-active');
	})
	//search bar exprnd
	$('.header-top-two .right button').on('click',function(){
		$('.header-top-two .right').toggleClass('widthfull');
	});
	//search bar border color
	$('.middel-top .center').on('click',function(){
		$('.middel-top .center').toggleClass('bordercolor');
	});
	//color select jquery
	$('.color-select > span').on('click',function(){
		$('.color-select > span').toggleClass('outline');
        $(this).addClass("outline").siblings().removeClass("outline");
	});
/*----------------------------
 nivoSlider active
------------------------------ */
	$('#mainSlider').nivoSlider({
		directionNav: true,
		animSpeed: 500,
		effect: 'random',
		slices: 18,
		pauseTime: 10000,
		pauseOnHover: false,
		controlNav: true,
		prevText: '<i class="mdi mdi-chevron-left"></i>',
		nextText: '<i class="mdi mdi-chevron-right"></i>'
	});
/*----------------------------
 plus-minus-button
------------------------------ */
	$(".qtybutton").on("click", function() {
		var $button = $(this);
		var oldValue = $button.parent().find("input").val();
		if ($button.text() == "+") {
			var newVal = parseFloat(oldValue) + 1;
		} else {
			// Don't allow decrementing below zero
			if (oldValue > 0) {
				var newVal = parseFloat(oldValue) - 1;
			} else {
				newVal = 0;
			}
		}
		$button.parent().find("input").val(newVal);
	});
/*----------------------------
 price-slider active
------------------------------ */  
	$( "#slider-range" ).slider({
		range: true,
		min: 40,
		max: 600,
		values: [ 150, 399 ],
		slide: function( event, ui ) {
		$( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
		}
	});
	$( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
	" - $" + $( "#slider-range" ).slider( "values", 1 ) );
/*--------------------------
 scrollUp
---------------------------- */	
	$.scrollUp({
        scrollText: '<i class="mdi mdi-chevron-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });
/*--------------------------
 // simpleLens
 ---------------------------- */
	$('.simpleLens-image').simpleLens({
		
	});
	
})(jQuery); 

(function ($) {
	$(document).ready(function() {
	$('.xzoom, .xzoom-gallery').xzoom({zoomWidth: 400, title: true, tint: '#333', Xoffset: 15});
	$('.xzoom2, .xzoom-gallery2').xzoom({position: '#xzoom2-id', tint: '#ffa200'});
	$('.xzoom3, .xzoom-gallery3').xzoom({position: 'lens', lensShape: 'circle', sourceClass: 'xzoom-hidden'});
	$('.xzoom4, .xzoom-gallery4').xzoom({tint: '#006699', Xoffset: 15});
	$('.xzoom5, .xzoom-gallery5').xzoom({tint: '#006699', Xoffset: 15});
	
	//Integration with hammer.js
	var isTouchSupported = 'ontouchstart' in window;
	
	if (isTouchSupported) {
	//If touch device
	$('.xzoom, .xzoom2, .xzoom3, .xzoom4, .xzoom5').each(function(){
	var xzoom = $(this).data('xzoom');
	xzoom.eventunbind();
	});
	
	$('.xzoom, .xzoom2, .xzoom3').each(function() {
	var xzoom = $(this).data('xzoom');
	$(this).hammer().on("tap", function(event) {
	event.pageX = event.gesture.center.pageX;
	event.pageY = event.gesture.center.pageY;
	var s = 1, ls;
	
	xzoom.eventmove = function(element) {
	element.hammer().on('drag', function(event) {
	event.pageX = event.gesture.center.pageX;
	event.pageY = event.gesture.center.pageY;
	xzoom.movezoom(event);
	event.gesture.preventDefault();
	});
	}
	
	xzoom.eventleave = function(element) {
	element.hammer().on('tap', function(event) {
	xzoom.closezoom();
	});
	}
	xzoom.openzoom(event);
	});
	});
	
	$('.xzoom4').each(function() {
	var xzoom = $(this).data('xzoom');
	$(this).hammer().on("tap", function(event) {
	event.pageX = event.gesture.center.pageX;
	event.pageY = event.gesture.center.pageY;
	var s = 1, ls;
	
	xzoom.eventmove = function(element) {
	element.hammer().on('drag', function(event) {
	event.pageX = event.gesture.center.pageX;
	event.pageY = event.gesture.center.pageY;
	xzoom.movezoom(event);
	event.gesture.preventDefault();
	});
	}
	
	var counter = 0;
	xzoom.eventclick = function(element) {
	element.hammer().on('tap', function() {
	counter++;
	if (counter == 1) setTimeout(openfancy,300);
	event.gesture.preventDefault();
	});
	}
	
	function openfancy() {
	if (counter == 2) {
	xzoom.closezoom();
	$.fancybox.open(xzoom.gallery().cgallery);
	} else {
	xzoom.closezoom();
	}
	counter = 0;
	}
	xzoom.openzoom(event);
	});
	});
	
	$('.xzoom5').each(function() {
	var xzoom = $(this).data('xzoom');
	$(this).hammer().on("tap", function(event) {
	event.pageX = event.gesture.center.pageX;
	event.pageY = event.gesture.center.pageY;
	var s = 1, ls;
	
	xzoom.eventmove = function(element) {
	element.hammer().on('drag', function(event) {
	event.pageX = event.gesture.center.pageX;
	event.pageY = event.gesture.center.pageY;
	xzoom.movezoom(event);
	event.gesture.preventDefault();
	});
	}
	
	var counter = 0;
	xzoom.eventclick = function(element) {
	element.hammer().on('tap', function() {
	counter++;
	if (counter == 1) setTimeout(openmagnific,300);
	event.gesture.preventDefault();
	});
	}
	
	function openmagnific() {
	if (counter == 2) {
	xzoom.closezoom();
	var gallery = xzoom.gallery().cgallery;
	var i, images = new Array();
	for (i in gallery) {
	images[i] = {src: gallery[i]};
	}
	$.magnificPopup.open({items: images, type:'image', gallery: {enabled: true}});
	} else {
	xzoom.closezoom();
	}
	counter = 0;
	}
	xzoom.openzoom(event);
	});
	});
	
	} else {
	//If not touch device
	
	//Integration with fancybox plugin
	$('#xzoom-fancy').bind('click', function(event) {
	var xzoom = $(this).data('xzoom');
	xzoom.closezoom();
	$.fancybox.open(xzoom.gallery().cgallery, {padding: 0, helpers: {overlay: {locked: false}}});
	event.preventDefault();
	});
	
	//Integration with magnific popup plugin
	$('#xzoom-magnific').bind('click', function(event) {
	var xzoom = $(this).data('xzoom');
	xzoom.closezoom();
	var gallery = xzoom.gallery().cgallery;
	var i, images = new Array();
	for (i in gallery) {
	images[i] = {src: gallery[i]};
	}
	$.magnificPopup.open({items: images, type:'image', gallery: {enabled: true}});
	event.preventDefault();
	});
	}
	});
	})(jQuery);