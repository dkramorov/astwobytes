
(function($){
	timerid=false;
	$.fn.liMenuVert = function(params){
		var p = {
			delayShow:300,		//Задержка перед появлением выпадающего меню (ms)
			delayHide:300	    //Задержка перед исчезанием выпадающего меню (ms)
		};
		if (params) {
			$.extend(p, params); 
		}
		return this.each(function(){
			var 
			menuWrap = $(this),
			menuWrapWidth = menuWrap.outerWidth(),
			menuWrapLeft = menuWrap.offset().left,
			menuSubSub = $('ul',menuWrap)
			menuSubSub.each(function(){
				var 
				mArrowRight = $('<div>').addClass('arrow-right'),
				mSubSub = $(this),
				mSubList = mSubSub.closest('li'),
				mSubLink = mSubList.children('a').append(mArrowRight),
				mSubArrow = $('<div>').addClass('arrow-left').prependTo(mSubSub),
				mSubArrow2 = $('<div>').addClass('arrow-left2').prependTo(mSubSub),
				mFuncId = function(){},
				mFuncIdOut = function(){};
				
				mSubList.on('mouseenter',function(){
					clearTimeout(mFuncIdOut);
					mHoverLink = $(this).children('a');
					mFuncId = setTimeout(function(){
						mHoverLink.next('ul').children('li').width(mHoverLink.next('ul').width());	//correct width in ie7			
						mSubArrow.css({top:mSubLink.outerHeight()/2 - 5});
						mSubArrow2.css({top:mSubLink.outerHeight()/2 - 5});
						var 
						mSubSubLeft = mSubLink.position().left + mSubLink.outerWidth(),
						p1 = (mSubLink.closest('ul').outerWidth()-mSubLink.closest('ul').width())/2;
						mSubSub.css({top:(mSubLink.position().top - p1)});	
						mSubSub.css({left:mSubSubLeft});
						mSubSub.show();
						var w3 = $(window).width();
						var w6 = (mSubSub.offset().left + mSubSub.outerWidth());
						if(w6 >= w3){
							mSubSub.closest('ul').addClass('toLeft');
							mSubSubLeft = -mSubSub.outerWidth();
						}
						if(mSubSub.parents('ul').hasClass('toLeft')){
							mSubSubLeft = -mSubSub.outerWidth();
						}
						mSubSub.css({left:mSubSubLeft});				
						mSubLink.addClass('active');
					},p.delayShow)
				})
				mSubList.on('mouseleave',function(){
					clearTimeout(mFuncId);
					mFuncIdOut = setTimeout(function(){
						
						mSubSub.hide();
						mSubLink.removeClass('active')
					},p.delayHide)
				});
			});
			menuWrapWidth = menuWrap.outerWidth();
			menuWrapLeft = menuWrap.offset().left;
			$(window).resize(function(){
				menuWrapWidth = menuWrap.outerWidth();
				menuWrapLeft = menuWrap.offset().left;	
			});
		});
	};
})(jQuery);

$(function(){


$(".outer").hover(
		function(){if(timerid) clearInterval(timerid); $("#"+$(this).attr("rel")).show(); }, //clearTimeout();
		function(){ 
		var obj=$("#"+$(this).attr("rel"));
		timerid=setInterval( function (){
		obj.fadeOut();
		} ,1000)
		}
);




	$(document).mouseup(function (e){ 
		var div = $(".lev00");
		if (!div.is(e.target) 
		    && div.has(e.target).length === 0) { 
			clearsubmenu();
		}
	});




function clearsubmenu()
{
//if ($(".level0").is(":hover")) return false;
$(".level0").delay(300).hide(); $(".arsm").delay(300).hide(); $(".lev00").delay(300).removeClass("mvhover");
}


$("#catalogmenupc .lev00").live("hover, click", function(){
	if ($(this)){
	var wself=$(this);
	var winscroll=Math.round($(window).scrollTop()-150), 
	menuitem=$(this),
	id=menuitem.attr("rel"), 
	submenu=$("#subc"+id), 
	topitem=menuitem.offset().top , 
	submenuH=submenu.height(), newtop=10; 

	if(submenuH > 600) submenu.addClass("column3"); else if (submenuH > 300) submenu.addClass("column2");
	if ((topitem+menuitem.height()-150 )> submenu.height()) { newtop=Math.round(topitem-200-submenu.height()/2); };
	if ( newtop < winscroll ) newtop = winscroll;

	clearsubmenu ();
	if (submenuH) 
	{
	submenu.css("top", newtop+"px").delay(300).show();
	menuitem.delay(300).addClass("mvhover");
	}
	//if (wself)setInterval (function(){timeclear(wself);}, 3000);
	}
})


});


