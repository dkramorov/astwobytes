function set_cost_type(el){
  if(el.prop("checked")){
    var product_id = el.attr("data-product_id");
    var cost = el.attr("data-cost");
    $(".product_price_" + product_id).html(cost + " ₽");
  }
}
jQuery(document).ready(function($) {
  /* ------------- */
  /* HOVER product */
  /* ------------- */
  /*
  $(".slider-img-thumb").lightSlider({
    loop: false,
    vertical:false,
    slideMargin: 0,
    item: 1,
    controls : true, // Show next and prev buttons
    pager: true,
  });
  */
  /* --------- */
  /* GO TO TOP */
  /* --------- */
  $("#yt-totop").hide();
  $(function () {
    var wh = $(window).height();
    var whtml =  $(document).height();
    $(window).scroll(function () {
      if ($(this).scrollTop() > whtml/10) {
        $('#yt-totop').fadeIn();
      } else {
        $('#yt-totop').fadeOut();
      }
    });
    $('#yt-totop').click(function () {
      $('body,html').animate({
        scrollTop: 0
      }, 800);
      return false;
    });
  });
  /* ------------------ */
  /* REMOVE PADDING TOP */
  /* ------------------ */
  if($('.breadcrumbs').length > 0){
    $('.sidebar, .col-main').css({'padding-top':'0'});
  }
  /* ------------------- */
  /* Autocomplete search */
  /* ------------------- */
  /*
  var searchForm = new Varien.searchForm('search_mini_form', 'search', 'Search entire store here...');
  searchForm.initAutocomplete('/suggest/', 'search_autocomplete');
  */
  /* --------- */
  /* MEGA MENU */
  /* --------- */
  var menu_width = $('.sm_megamenu_wrapper_horizontal_menu .sm_megamenu_menu').width();
  $('.sm_megamenu_wrapper_horizontal_menu .sm_megamenu_menu > li').mouseover(function() {
    $(this).addClass('hover_item');
    var item_position =  $(this).position().left;
    var dropdown_item = $(this).children('div').width();
    if(dropdown_item > (menu_width - item_position)){
      var dropdown_item = $(this).children('div').css({'right':'0', 'left': 'auto'});
    }
  }).mouseout(function() {
    $('.sm_megamenu_wrapper_horizontal_menu .sm_megamenu_menu > li').removeClass('hover_item');
  });
  /* ----------- */
  /* MOBILE MENU */
  /* ----------- */
  $('.dropdown_sidebar .nav-mobile > li').has('ul').append( '<span class="touch-button"><span>open</span></span>' );
  $('.btn-sidebar').click(function(){
    $('.dropdown_sidebar').toggleClass('active');
    $(this).toggleClass('active active_btn');
    $('body').toggleClass('active_sidebar');
  });
  $('.touch-button').click(function(){
    $(this).prev().slideToggle(200);
    $(this).toggleClass('active');
    $(this).parent().toggleClass('parent-active');
  });
  /* ------------------- */
  /* LEFT CATALOGUE MENU */
  /* ------------------- */
  $(".megamenu-vertical > li:gt(7)").addClass('item-hidden');
  $( ".btn-showmore a" ).click(function() {
    $(this).toggleClass('btn-active');
    if($(this).hasClass('btn-active')){
      $(this).text("Less Categories");
    } else {
      $(this).text("More Categories");
    }
    $(".megamenu-vertical > li:gt(7)").toggleClass('active');
  });
  var menu_width = $('.sm_megamenu_wrapper_horizontal_menu').width();
  $('.sm_megamenu_wrapper_horizontal_menu .sm_megamenu_menu > li > div').each(function(){
    $this = $(this);
    var lv2w = $this.width();
    var lv2ps = $this.position();
    var lv2psl = $this.position().left;
    var sw = lv2w + lv2psl;
    if( sw > menu_width ){
      $this.css({'right': '0'});
    }
  });
  /* ------------------- */
  /* MAIN SLIDER (right) */
  /* ------------------- */
  $(".slidershow").owlCarousel({
    responsive:{
      0:{items:1},
      480:{items:1},
      768:{items:1},
      992:{items:1},
      1200:{items:1},
    },
    autoplay:true,
    loop:true,
    nav : true,
    dots: true,
    autoplaySpeed : 500,
    navSpeed : 500,
    dotsSpeed : 500,
    autoplayHoverPause: true,
    margin:0,
  });
  /* -------------------- */
  /* IMG SLIDER (clients) */
  /* -------------------- */
  $(".slider-brand").owlCarousel({
    responsive:{
      0:{items:2},
      480:{items:3},
      768:{items:5},
      992:{items:6},
      1200:{items:6}
    },
    autoplay:false,
    loop:true,
    nav : true,
    dots: false,
    autoplaySpeed : 500,
    navSpeed : 500,
    dotsSpeed : 500,
    autoplayHoverPause: true,
    margin:30,
  });
  /* ---------- */
  /* Cart click */
  /* ---------- */
  $(window).click(function() {
    $("#sm_cartpro").removeClass("cartpro-hover");
  });
  $("#sm_cartpro").click(function(e){
    e.stopPropagation();
    if($(this).hasClass("cartpro-hover")){
      $(this).removeClass("cartpro-hover");
    }else{
      $(this).addClass("cartpro-hover");
    }
  });
  /* ----------- */
  /* Cost filter */
  /* ----------- */
  if ($('.range-slider').length > 0) {
    $('.range-slider').each(function () {
      var range_slider = $(this);
      $(range_slider).ionRangeSlider({
        type: "double",
        grid: range_slider.data('grid'),
        min: range_slider.data('min'),
        max: range_slider.data('max'),
        from: range_slider.data('from'),
        to: range_slider.data('to'),
        prefix: range_slider.data('prefix')
      });
    });
  }
  $(".cost-type-radio").each(function(){
    set_cost_type($(this));
    $(this).change(function(){
      set_cost_type($(this));
    });
  });
});