var block_hint_template = '<div class="item-hints">';
block_hint_template += '<div class="hint" data-position="4">';
block_hint_template += '<span class="hint-radius"></span>';
block_hint_template += '<span class="hint-dot"></span>';
block_hint_template += '<div class="hint-content do--split-children">';
block_hint_template += '<p class="hint_text"></p>';
block_hint_template += '</div>';
block_hint_template += '</div>';
block_hint_template += '</div>';

function prepare_hints($, block, pk, id, i, row){
  if(block.length > 0){
    pk = 'hint_' + id + "_" + i;
    var new_hint = '<div id="' + pk + '">' + block_hint_template + '</div>';
    block.append($(new_hint));
    $("#" + pk).css({'position': 'absolute', 'left': row['xpos'] + '%', 'top': row['ypos'] + '%'});
    $("#" + pk + " .hint_text").html(row['name']);
    $("#" + pk + " .hint").attr('data-position', row['direction']);
    $("#" + pk + " .hint").click(function(e){
      if($(this).hasClass("touched")){
        $(this).removeClass("touched");
      }else{
        $(this).addClass("touched");
      }
      e.stopPropagation();
    });

    $("#" + pk + " .item-hints").mouseover(function(e){
      play_sound('sound_tink');
    });
    $("#" + pk + " .item-hints").mouseout(function(e){
      stop_sound('sound_tink');
    });

  }
}

jQuery(document).ready(function($){
  var form = $("#all_blocks");
  setTimeout(function(){
    $.ajax({
      type: form.attr('method'),
      url: form.attr('action'),
      data: form.serialize(),
    }).done(function(r) {
      var block = null;
      var block_mobile = null;
      var pk = null;
      var id = null;
      var row = null;
      console.log(r);
      for(var i=0; i<r.data.length; i++){
        row = r.data[i];
        id = row['block'];
        block = $("#block_" + id);
        block_mobile = $("#block_" + id + "_mobile");
        prepare_hints($, block, pk, id, i, row);
        prepare_hints($, block_mobile, pk, id, i, row);
      }
    });
  }, 500);
  $('form').each(function(){
    if($(this).hasClass('touched')){
      return;
    }
    $(this).addClass('touched');
    if($(this).attr('action') === '/feedback/'){
      var fb = new FeedBack($(this).attr('id'));
      $("input.phone").mask("8(999)9 999-999");
    }
  });

  $(document).click(function(e) {
    if(!$(e.target).is('.hint.touched')) {
      $(".hint.touched").removeClass('touched');
    }
  });

  $("a.hvr-sweep-to-right").mouseover(function(e){
    play_sound('sound_button');
  });
  $("a.hvr-sweep-to-right").mouseout(function(e){
    stop_sound('sound_button');
  });

  var myAudio = new Audio('/media/new/bg.ogg');
  myAudio.addEventListener('ended', function() {
    this.currentTime = 0;
    this.play();
  }, false);

  $("a.mute_bg").click(function(){
    if($(this).hasClass("muted")){
      myAudio.muted = false;
      $(this).removeClass("muted");
      $(".equalizer .playing").removeClass("hidden");
      $(".equalizer .silence").addClass("hidden");
      localStorage.setItem('mute_bg', 'no');
    }else{
      myAudio.muted = true;
      $(this).addClass("muted");
      $(".equalizer .playing").addClass("hidden");
      $(".equalizer .silence").removeClass("hidden");
      localStorage.setItem('mute_bg', 'yes');
    }
  });

  if(localStorage.getItem('mute_bg') !== 'yes'){
    $(".equalizer .playing").removeClass("hidden");
    $(".equalizer .silence").addClass("hidden");
    myAudio.play();
  }else{
    $(".equalizer .playing").addClass("hidden");
    $(".equalizer .silence").removeClass("hidden");
    myAudio.play();
    myAudio.muted = true;
  }

  $("table.slider_pagination td").click(function(){
    var anchor = $(this).attr("data-anchor");
    jump(anchor);
  });

  $('.article2').owlCarousel({
    items: 1,
    loop: true,
    center: true,
    dots: false,
    nav: true,
    margin: 10,
    autoplayHoverPause: true,
    autoplay: false,
  });
  $('.slider5').owlCarousel({
    items: 1,
    loop: false,
    center: true,
    dots: false,
    margin: 10,
    callbacks: true,
    URLhashListener: true,
    startPosition: 'URLHash',
    autoHeight:true,

    responsiveClass: true,
    singleItem: true,

    autoplay: true,
    autoplaySpeed: 5000000,
    autoplayTimeout: 5000000,
    autoplayHoverPause: true,
  });
  $('.slider5').on('translated.owl.carousel', function(e) {
    var pk = $(this).attr("id");
    var paginator = pk + "_paginator";
    var ind = parseInt(e.item.index);
    refresh_slider5(paginator, ind);
  });
  function refresh_slider5(paginator, ind){
    var item;
    $("#" + paginator + " td").removeClass("active").removeClass("current");
    $("#" + paginator + " .ind_" + ind).addClass("current");
    for(var i=0; i<=ind; i++){
      item = "#" + paginator + " .ind_" + i;
      $(item).addClass('active');
    }
  }
  $('.slider5').each(function(e){
    var pk = $(this).attr("id");
    var paginator = pk + "_paginator";
    refresh_slider5(paginator, 0);
  });
  if($(".video-bg").children().length == 0){
    $(".video-bg").remove();
  }
  $('.slider5').trigger('stop.owl.autoplay');
  $('.owl-carousel').trigger('stop.owl.autoplay');
});

function jump(h){
    var url = window.location.href.split("#")[0];
    window.location.href = "#" + h;
    history.replaceState(null,null,url);
    //$('.owl-carousel').trigger('autoplay.stop.owl');
}
function play_sound(soundobj) {
    var thissound = document.getElementById(soundobj);
    thissound.play();
}
function stop_sound(soundobj) {
    var thissound = document.getElementById(soundobj);
    thissound.pause();
    thissound.currentTime = 0;
}
