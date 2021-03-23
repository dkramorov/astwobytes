'use strict';
function bootSpriteSpin(selector, options) {
  if ("IntersectionObserver" in window) {
    // Browser supports IntersectionObserver so use that to defer the boot
    let observer = new IntersectionObserver(function(entries, observer) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          observer.unobserve(entry.target);
          $(entry.target).spritespin(options);
          console.log("booted", selector, options);
        }
      });
    });
    observer.observe($(selector)[0]);
  } else {
    // Browser does not support IntersectionObserver so boot instantly
    $(selector).spritespin(options);
    console.log("booted", selector, options);
  }
}
$(document).on('ready', function () {
	// variables
	var contextWindow = $(window);
	var $root = $('html');
	var siteHeaderFooter = $('.page-footer, .page-header, .page-cover');

	// 1. Background image and colors
	// 1.1 Background Image as data attribute
	var list = $('.bg-img');
	for (var i = 0; i < list.length; i++) {
		var src = list[i].getAttribute('data-image-src');
		list[i].style.backgroundImage = "url('" + src + "')";
		list[i].style.backgroundRepeat = "no-repeat";
		list[i].style.backgroundPosition = "center";
		list[i].style.backgroundSize = "cover";
	}
	// Image block to Background image
	var listImgBlock = $('.img-block');
	for (var i = 0; i < listImgBlock.length; i++) {
		var src = listImgBlock[i].getAttribute('src');
		var divBlock = document.createElement("div");
		divBlock.setAttribute("class", "img");
		divBlock.style.backgroundImage = "url('" + src + "')";
		divBlock.style.backgroundRepeat = "no-repeat";
		divBlock.style.backgroundPosition = "center";
		divBlock.style.backgroundSize = "cover";
		$(listImgBlock[i]).after(divBlock);
		listImgBlock[i].style.display = "none";
	}
	// 1.2. Background Color as data attribut
	var listColor = $('.bg-color');
	for (var i = 0; i < listColor.length; i++) {
		var src = listColor[i].getAttribute('data-bgcolor');
		listColor[i].style.backgroundColor = src;
	}
	// 1.3 Slideshow Background
	// vegas slideshow background
	var imageList = $('.slide-show .img');
	var imageSlides = [];
	for (var i = 0; i < imageList.length; i++) {
		var src = imageList[i].getAttribute('data-src');
		imageSlides.push({ src: src });
	}
	$('.slide-show').vegas({
		delay: 5000,
		shuffle: true,
		slides: imageSlides,
		animation: ['kenburnsUp', 'kenburnsDown', 'kenburnsLeft', 'kenburnsRight']
	});

	// 3. Menu icon clicked
	var menuIcon = $('#menu-icon');
	var navfullMenu = $('#navfull-menu');
	var navbarMenu = $('#navbar-menu');
	menuIcon.on('click', function () {
		menuIcon.toggleClass('menu-visible');
		navfullMenu.toggleClass('menu-visible');
		navbarMenu.toggleClass('menu-visible');
		// reactToMenu.toggleClass('menu-visible');
		return false;
	});

	// 4. Sliders
	var swiperSliderThumbsA = new Swiper('.slider-thumbs-a.swiper-container', {
		spaceBetween: 16,
		slidesPerView: 3,
		loop: false,
		freeMode: true,
		grabCursor: true,
		watchSlidesVisibility: true,
		watchSlidesProgress: true,
		pagination: {
			el: '.swiper-container.slider-thumbs-a .thumbs-pagination',
			clickable: true,
		},
	});

	var swiperSliderA = new Swiper('.slider-a.swiper-container', {
		navigation: {
			nextEl: '.swiper-container.slider-a .slider-next',
			prevEl: '.swiper-container.slider-a .slider-prev',
		},
		pagination: {
			el: '.swiper-container.slider-a .swiper-pagination',
			clickable: true,
			type: 'fraction',
			//   dynamicBullets: true,
		},
		spaceBetween: 0,
		slidesPerView: 1,
		// loop: true, // loop to start
		// freeMode: false,
		// freeModeSticky: true,
		// freeModeMomentumVelocityRatio: 2,
		grabCursor: false,
		autoplay: 5000,
		speed: 1200,
		virtualTranslate: false,

		thumbs: {
			swiper: swiperSliderThumbsA
		}
		// init: false, // set true to call it later
	});

	var swiperSliderB = new Swiper('.slider-b.swiper-container', {
		navigation: {
			nextEl: '.swiper-container.slider-b .slider-next',
			prevEl: '.swiper-container.slider-b .slider-prev',
		},
		pagination: {
			el: '.swiper-container.slider-b .swiper-pagination',
			clickable: true,
			// type: 'fraction',
			//   dynamicBullets: true,
		},
		slidesPerView: 1,
		// loop: true, // loop to start
		effect: 'fade',
		grabCursor: true,
		autoplay: 5000,
		speed: 1200,
		virtualTranslate: false,
		// init: false, // set true to call it later
	});

  var swiperSliderC = new Swiper('.slider-c .swiper-container', {
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    pagination: {
      el: '.swiper-pagination',
    },
    slidesPerView: 1,
    grabCursor: true,
    autoplay: 5000,
    virtualTranslate: false,
  });

	// 5. Init video background
	var videoBg = $('.video-container video, .video-container object');
	// Fix video background
	// videoBg.maximage('maxcover');

	// 6. Scrolling animation
	var scrollHeight = $(document).height() - contextWindow.height();
	contextWindow.on('scroll', function () {
		var scrollpos = $(this).scrollTop();
		// if (scrollpos > 100 && scrollpos < scrollHeight - 100) {
		if (scrollpos > 100) {
			siteHeaderFooter.addClass("scrolled");
		}
		else {
			siteHeaderFooter.removeClass("scrolled");
		}
	});

	// 8. Page Loader : hide loader when all are loaded
	contextWindow.on('load', function () {
		$('#page-loader').addClass('p-hidden');
		$('.section').addClass('anim');
		$('.scrollpage-container .section-home').addClass('active');
		siteHeaderFooter.removeClass('loading-anim');
	});

	// 9. init fullpage js
	// Get sections name
	var pageSectionDivs = $('.fullpage-scroll .section');
	var pageSections = [];
	var pageCover = $('.page-cover');
	var fpNav = $('#fp-nav');
	for (var i = 0; i < pageSectionDivs.length; i++) {
		pageSections.push(pageSectionDivs[i].getAttribute('data-id'));
	}
	var scrollOverflow = true;
	var autoScrolling = true;
	var fitToSection = true;
	if ($('.normal-scroll .section').length > 1) {
		scrollOverflow = false;
		autoScrolling = false;
		fitToSection = false;
	}
	$('.fullpage-scroll').fullpage({
		menu: '#sidebar-menu',
		anchors: pageSections,
		css3: true,
		scrollOverflow: scrollOverflow,
		verticalCentered: false,
		navigation: true,
		navigationPosition: 'right',
		responsiveWidth: 768,

		autoScrolling: autoScrolling,
		fitToSection: fitToSection,
		// scrollBar: true,
		afterLoad: function (anchorLink, index) {
			// Behavior after a section is loaded
			// Page cover
			if (index > 1) {
				if (!pageCover.hasClass('scrolled')) {
					pageCover.addClass('scrolled');
				}
				if (!siteHeaderFooter.hasClass('fp-scrolled')) {
					siteHeaderFooter.addClass('fp-scrolled');
				}
			} else {
				pageCover.removeClass('scrolled');
				siteHeaderFooter.removeClass('fp-scrolled');
			}
			// section animation
			var activeSection = $('.section.active');
			// text color of section
			// force white text color
			if (activeSection.hasClass('content-white')) {
				siteHeaderFooter.addClass('content-white');
				fpNav.addClass('content-white');
			} else {
				siteHeaderFooter.removeClass('content-white');
				fpNav.removeClass('content-white');
			}
			if (!!activeSection[0].getAttribute('data-color')) {
				pageCover[0].setAttribute('data-color', activeSection[0].getAttribute('data-color'))
				// pageCover.addClass(activeSection.getAttribute('section-color'));
			} else {
				pageCover[0].setAttribute('data-color','');
			}
		}
	});

	// Scroll to fullPage.js next/previous section
	$('.scrolldown a, .scroll.down').on('click', function () {
		try {
			// fullpage scroll
			$.fn.fullpage.moveSectionDown();
		} catch (error) {
			// normal scroll
			$root.animate({
				scrollTop: window.innerHeight
			}, 400, function () {
			});
		}

	});

  /* Spinner360 */
  $('.spritespin').each(function(){

    var tag = $(this).attr('data-folder');
    if(!tag){
      return;
    }
    var selector = $(this).attr('id');

    var folder = tag.split('/')[0];
    var max_frame = tag.split('/')[1];

    bootSpriteSpin("#" + selector, {
    //$(this).spritespin({
      source: SpriteSpin.sourceArray('/media/spinner360/' + folder + '/frame_{frame}.jpg', { frame: [1,max_frame], digits: 3 }),
      width: 1300,
      height: 900,
      sense: -1,
      responsive: true,
      plugins: [
        'progress',
        '360',
        'drag',
      ],
      animate: false,
      //preloadCount: 12,
    });

    $("#" + selector).parent().find(".rotation_left").click(function(){
      $("#" + selector).spritespin({
        reverse: false,
        animate: true,
      })
    });
    $("#" + selector).parent().find(".rotation_right").click(function(){
      $("#" + selector).spritespin({
        reverse: true,
        animate: true,
      })
    });

  });

});


var myMapContainer = "mapContainer";

// ----------------------
// Скролл к нужной секции
// ----------------------
function scroll_to(section, offset){
  if(typeof(offset) == "undefined"){
    offset = 0;
  }
  $("html, body").animate({
    scrollTop: $(section).offset().top + offset
  }, 500);
  console.log("scrolling to " + section + " " + $(section).offset().top);
}

function search_dealers_listener(search_arr){
  var search_field = $("#search_dealer_field");
  search_field.keyup(function(){
    var queries = search_field.val().split(" ");
    var q_arr = Array();
    var q;
    var cities = Array();
    for(var i=0; i<queries.length; i++){
      q = queries[i].toLowerCase();
      q = $.trim(q);
      if(q.length > 0){
        q_arr.push(q);
      }
    }

    var item;
    var is_visible = true;
    for(var i=0; i<search_arr.length; i++){
      is_visible = true;
      item = search_arr[i];
      for(var j=0; j<q_arr.length; j++){
        if(item['terms'].indexOf(q_arr[j]) < 0){
          $("#dealer_row_" + item['id']).hide();
          is_visible = false;
          break;
        }
      }
      if(is_visible){
        if(cities.indexOf(item['city_id']) < 0){
          cities.push(item['city_id']);
        }
        $("#dealer_row_" + item['id']).show();
      }
    }
    $(".city_row").hide();
    for(var i=0; i<cities.length; i++){
      $("#city_row_" + cities[i]).show();
    }
  })
}

function create_dealers_map(){
  var kwargs = {};
  kwargs['default_town'] = "Иркутск";

  create_new_map(myMapContainer);
  wait_for_result(myMapContainer, function(){
    var myMap = get_map(myMapContainer);
    disable_map_wheel(myMapContainer);
    myMap.kwargs = kwargs;
    var point;

    var search_arr = [];

    if(typeof(mapContainer_points) != "undefined"){
      for(var i=0; i<mapContainer_points.length; i++){
        point = mapContainer_points[i];
        myMap.myPoints.push(point);

        search_arr.push({
          'id': point['id'],
          'terms': point['terms'],
          'city_id': point['city_id'],
        });

        $("#dealer_address_" + point['id']).click(function(){
          scroll_to("#dealers_title");
          var pk = $(this).attr("id").replace("dealer_address_", "");
          var placemark = find_placemark_by_id(pk, myMap);
          console.log("placemark", placemark);
          if(placemark != null){
            var props = placemark['properties'];
            var coords = placemark['geometry']['coordinates'];
            if(myMap.balloon.isOpen()){
              myMap.balloon.close();
            }
            myMap.balloon.open(coords, props['balloonContent'], {});
            myMap.setCenter(coords, 12);
          }else{
            console.log("placemark is null", pk);
          }
        });
      }
      add_points_to_map(myMapContainer, mapContainer_points);
      set_map_bounds(myMapContainer)

      search_dealers_listener(search_arr);
    }else{
      console.log("[ERROR]: mapContainer_points undefined");
    }

  }, ["map"]);
}
$(document).ready(function(){
  if($("#" + myMapContainer).length > 0){
    //create_dealers_map();
    load_yandex_maps_script(yandex_maps_api_key, create_dealers_map);
  }
  $(".nav-item").click(function(){
    if($("#product_props").length > 0){
      scroll_to("#product_props", -100);
    }
  });
});
