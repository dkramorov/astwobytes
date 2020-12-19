function closesearch() {
  $("#search").hide();
  $("#search").val("");
  $("#searchform").stop().animate({width:"1px" },500, function(){$("#searchform").addClass("nobg")})
  $("#searchrun").removeClass("searchrunopen");
  $("#searchrun").attr("rel",1);
  clearsearchbox();
}
function show_search_panel_pw (){
  if($("#searchrun").attr("rel")==1){
    $("#searchform").removeClass("nobg").animate({width:"300px" },500, function(){$("#search").show(); $("#searchrun").addClass("searchrunopen");});
    $("#searchrun").attr("rel",0);
  }else closesearch();
}
function leftpanelclose(){
  $("#overcover2").fadeOut();
  $("#lefmobiletpanelmenu").stop().animate({left:"-450px" },300);
  $("#lefmobiletpanel").stop().animate({left:"-450px" },500);
}
function cover (){
  $(".portf").hover(function(){
  $("#"+$(this).attr("id")+"lable").animate({top: (132 - $("#"+$(this).attr("id")+"lable").height()) + "px" },500);}, function(){$("#"+$(this).attr("id")+"lable").animate({top: "152px"},500);});
}

$(function(){
  ddsmoothmenu.init({mainmenuid: "smoothmenu1", orientation: 'h',classname: 'ddsmoothmenu', contentsource: "markup"});
  $(".pzk").live("click", function(){
    $.prettyPhoto.open($(this).attr("link"),'','<span class=news >Сотрудники интернет-магазина &laquo;МедикаМаркет&raquo; свяжутся с вами по указанным контактным данным в самое ближайшее время и проконсультируют по всем интересующим вопросам о товаре</span>');
    return false;
  })
  window.onbeforeunload = function (){$("#overload").stop().fadeIn();}

  $("#overload").fadeOut();
  $("#moderator_error").fadeIn().delay(8000).fadeOut();

  $(".closepng").click(function() {
    $("#moderator_error").stop().hide();
    $("#moderator_error2").stop().hide();
    $("#moderator_error3").stop().hide();
  });
  $(".jscrol").jScrollPane();
  $("#Usregclose").click(function(){
    $("#Usdetails").hide();
    $("#overcover").fadeOut();
    return false
  })
  $("#lefmobiletpanelcontent .lev00").live("click", function(){
    var menuitem=$(this),
        id=menuitem.attr("rel"),
        submenu=$("#subc"+id);
    $("#lefmobiletpanelcontentmenu").html("<span id=lsmback >Назад</span><h3>"+menuitem.html()+"</h3>" +submenu.html());
    $("#lefmobiletpanelmenu").stop().animate({left:"0" },500);
  })

  $("#lsmback").live("click", function(){
    $("#lefmobiletpanelmenu").stop().animate({left:"-450px" },300);
  })

  $(".menucatalog").click(function(){
    $("#overcover2").fadeIn();
    $("#lefmobiletpanelcontent").html($("#catalogmenupc").html());
    $("#lefmobiletpanel").animate({left:"0" },500);
  })

  $(".menuinfo").click(function(){
    $("#overcover2").fadeIn();
    $("#lefmobiletpanelcontent").html("<div class='news iblokl PT'><h3>Информация</h3>"+$("#supermenu").html()+"</div>");
    $("#lefmobiletpanel").animate({left:"0" },500);
  })

  $(".auserinfo").click(function(){
    $("#overcover3").fadeIn();
    $("#rightmovepanel").animate({right:"0" },500);
  })

  $("#lefmobiletpanelclose,  #rightmovepanelclose, .allpanelclose, #overcover2, #overcover, #overcover3").click(function(){
    leftpanelclose();
    $("#rightmovepanel").stop().animate({right:"-450px" },500);
    $("#overcover3").fadeOut();
  })

  $("#searchrun").click(function(){show_search_panel_pw();});

  $(".jsonly").css("visibility","visible");
  cuSel({  changedEl: ".cuSelclass",  scrollArrows: true});
$(".styleds").change(function(){$("#filtrform").submit(); })
cover ();

$("a[rel^='prettyPhoto']").prettyPhoto({theme:'light_rounded'});
$("#slogans").delay(500).fadeIn(1000);

$('#slider').nivoSlider({ animSpeed: 500, pauseTime: 20000,controlNav:true});
$("#sliderbank ul").jcarousel({auto:6,scroll:3,wrap: "last",visible:3,visible:3,size:6});
$('.basc').click(function(){  //$(this).fadeOut(100);
  addToBasket($(this).attr('id'));
  $(this).attr('src','/img/bascetfull.png');
  $(this).attr('title','Добавить количество (товар уже есть в корзине)');
  $(this).fadeIn('slow');
});

$(".notoper").click(function(){
  $('#ajaxbascet').animate({top:'-500px'}, 'slow')
  $("#ajaxclose").fadeOut();
});
$("#slidepanel span").click(function(){
  $('#slidepanel span').css('background-color','#ebebeb');
  $(this).css('background-color','#fff');
  $(".slpan").css('display','none');
  $("#_"+$(this).attr('id')).fadeIn();
  if ($(this).attr('id')=='actions') {
    $('#slider').data('nivoslider').start();
  }
});

});
$(document).ready(function(){
  $(".cuSelclass").fadeIn();
})
function openloader( mid ){
  $(".usersender").slideUp();
  $("#overcover2").show();
  $("#"+ mid).slideDown();
  $("#rightmovepanel").stop().animate({right:"0" },500);
}
function clearsearchbox(){
  $("#serachico").attr("src","/media/img/search2.gif");
  $("#ajaxsearchbox").hide();
}
function plusweb_adaptive(){
  if ($(window).width() < 1000){
    $("#mainblock").addClass('mbfull');
    $(".pcstyle").addClass('mobilestyle').removeClass('pcstyle');
    $(".pconly").hide();
    $(".mobileonly").show();
    if($("#anonsmobile").html() =="" ){
      $("#anonsmobile").html($("#anonspc").html());
      $("#anonspc").html("");
    }
  }else {
    $("#mainblock").removeClass('mbfull');
    $(".mobilestyle").addClass('pcstyle').removeClass('mobilestyle');
    $(".mobileonly").hide();
    $(".pconly").css("visibility","visible").show();
    if($("#anonspc").html() =="" ){
      $("#anonspc").html($("#anonsmobile").html());
      $("#mobile").html("");
    }
  }
  $(".mobilestyle #smoothmenu1").hide();
  $(".pcstyle #smoothmenu1 ").show();
}
$(function(){
  $(".usersend .PT").click(function(){
    $(".usersender").slideUp();
    $("#detail").slideUp();
    $(".usersend .PT").show();
    $(this).hide();
    $("#"+$(this).attr("rel")).slideDown();
  });
  $(".usersend2").click(function(){
    openloader($(this).attr("rel"));
    return false;
  });
  plusweb_adaptive();
  $(window).resize(function(){
    plusweb_adaptive();
    leftpanelclose()
  });
});