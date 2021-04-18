var PHIL={};
!function(e){
  "use strict";
  var i=e(window),
      t=e(document),
      o=e("body"),
      n={},
      a=e("#site-header"),
      r=e(".counter"),
      s=e(".skills-item"),
      c=e(".js-animate-icon"),
      d=e(".right-menu"),
      u=e(".primary-menu"),
      g=e("#site-footer"),
      m=e("#hellopreloader");

  PHIL.headerSpacer={
    $spacer:null,
    $header:null,
    init:function(){
      this.$header=jQuery(a),
      this.$spacer=jQuery('<div class="header--spacer"></div>').insertAfter(this.$header)
    },resize:function(){
      var e=this;
      e.$spacer&&setTimeout(function(){
        var i=e.$header.outerHeight(),
            t=e.$header.css("background-color");
        e.$spacer.css({
          height:i+"px",
          "background-color":t
        })
      }, 100)
    }
  },
  PHIL.updateResponsiveInit=function(){
    var i=null,
        t=function(){
          i=null,
          PHIL.headerSpacer.resize()
        };
    e(window).on("resize",function(){
      null===i&&(i=window.setTimeout(function(){
        t()
      },200))
    }).resize()
  },
  PHIL.preloader=function(){
    return i.scrollTop(0),setTimeout(function(){
      m.fadeOut(800)
    },800),!1
  };

  var p=jQuery(".popup-search"),
      f=jQuery(".cart-popup-wrap");
  PHIL.fixedHeader=function(){
    a.headroom({
      offset:20,
      tolerance:5,
      classes:{
        initial:"animated",
        //pinned:"swingInX",
        //unpinned:"swingOutX"
        pinned:"fadeIn",
        unpinned:"fadeOut"
      }
    })
  },
  PHIL.parallaxFooter=function(){
    g.length&&g.hasClass("js-fixed-footer")&&(g.before('<div class="block-footer-height"></div>'),
    e(".block-footer-height").matchHeight({target:g}))
  },
/* Пока убрал, нах эти счетчики и прогрессбары
  PHIL.counters=function(){
    r.length&&r.each(function(){
      jQuery(this).waypoint(function(){
        e(this.element).find("span").countTo(),
        this.destroy()
      },{offset:"95%"})
    })
  },
  PHIL.progresBars=function(){
    s.length&&s.each(function(){
      jQuery(this).waypoint(function(){
        e(this.element).find(".count-animate").countTo(),
        e(this.element).find(".skills-item-meter-active").fadeTo(300,1).addClass("skills-animate"),this.destroy()
      },{offset:"90%"})
    })
  },
*/
/* Пока нахер не нужен, файлы удалил
  PHIL.animateSvg=function(){
    c.length&&c.each(function(){
      jQuery(this).waypoint(
        function(){
          e(this.element).find("> svg").drawsvg().drawsvg("animate"),this.destroy()
        },
        {offset:"95%"}
      )
    })
  },
*/
  PHIL.customScroll=function(){
    setTimeout(function(){
      d.mCustomScrollbar({
        axis:"y",
        scrollEasing:"linear",
        scrollInertia:150
      },500)
    })
  },
  PHIL.togglePanel=function(){
    d.length&&(d.toggleClass("opened"),
    o.toggleClass("overlay-enable"))
  },
  PHIL.toggleSearch=function(){
    o.toggleClass("open"),e(".overlay_search-input").focus()
  },
/* Пока погасил, возможно, понадобится
  PHIL.mediaPopups=function(){
    e(".js-popup-iframe").magnificPopup({
      disableOn:700,
      type:"iframe",
      mainClass:"mfp-fade",
      removalDelay:160,
      preloader:!1,
      fixedContentPos:!1,
      iframe:{
        patterns:{
          youtube:{
            src:"https://www.youtube.com/embed/%id%?autoplay=1"
          },
          vimeo:{
            src:"https://player.vimeo.com/video/%id%?autoplay=1"
          }
        }
      }
    }),
    e(".js-zoom-image, .link-image").magnificPopup({
      type:"image",
      removalDelay:500,
      callbacks:{
        beforeOpen:function(){
          this.st.image.markup=this.st.image.markup.replace("mfp-figure","mfp-figure mfp-with-anim"),
          this.st.mainClass="mfp-zoom-in"
        }
      },
      closeOnContentClick:!0,
      midClick:!0
    })
  },
*/
  PHIL.equalHeight=function(){
    e(".js-equal-child").find(".theme-module").matchHeight({
      property:"min-height"
    })
  },
/* Анимация для определенных сцен
  PHIL.SubscribeScrollAnnimation=function(){
    var e=new ScrollMagic.Controller;
    new ScrollMagic.Scene({
      triggerElement:".subscribe"
    }).setVelocity(".gear",{
      opacity:1,rotateZ:"360deg"
    },1200).triggerHook("onEnter").addTo(e),
    new ScrollMagic.Scene({
      triggerElement:".subscribe"
    }).setVelocity(".mail",{
      opacity:1,
      bottom:"0"
    },600).triggerHook(.8).addTo(e),
    new ScrollMagic.Scene({
      triggerElement:".subscribe"
    }).setVelocity(".mail-2",{
      opacity:1,right:"20"
    },800).triggerHook(.9).addTo(e)
  },
  PHIL.SeoScoreScrollAnnimation=function(){
    var e=new ScrollMagic.Controller;
    new ScrollMagic.Scene({
      triggerElement:".seo-score"
    }).setVelocity(".seo-score .images img:first-of-type",{
      opacity:1,
      top:"-10"
    },400).triggerHook("onEnter").addTo(e),
    new ScrollMagic.Scene({
      triggerElement:".seo-score"
    }).setVelocity(".seo-score .images img:nth-child(2)",{
      opacity:1,
      bottom:"0"
    },800).triggerHook(.7).addTo(e),
    new ScrollMagic.Scene({
      triggerElement:".seo-score"
    }).setVelocity(".seo-score .images img:last-child",{
      opacity:1,
      bottom:"0"
    },1e3).triggerHook(.8).addTo(e)
  },
  PHIL.TestimonialScrollAnnimation=function(){
    var e=new ScrollMagic.Controller;
    new ScrollMagic.Scene({
      triggerElement:".testimonial-slider"
    }).setVelocity(".testimonial-slider .testimonial-img",{
      opacity:1,
      bottom:"-50"
    },400).triggerHook(.6).addTo(e),
    new ScrollMagic.Scene({
      triggerElement:".testimonial-slider"
    }).setVelocity(".testimonial-slider .testimonial__thumb-img",{
      opacity:1,
      top:"-100"
    },600).triggerHook(1).addTo(e)
  },
  PHIL.OurVisionScrollAnnimation=function(){
    var e=new ScrollMagic.Controller;
    new ScrollMagic.Scene({
      triggerElement:".our-vision"
    }).setVelocity(".our-vision .elements",{
      opacity:1
    },600).triggerHook(.6).addTo(e),
    new ScrollMagic.Scene({
      triggerElement:".our-vision"
    }).setVelocity(".our-vision .eye",{
      opacity:1,bottom:"-90"
    },1e3).triggerHook(1).addTo(e)
  },
  PHIL.MountainsScrollAnnimation=function(){
    var e=new ScrollMagic.Controller;
    new ScrollMagic.Scene({
      triggerElement:".background-mountains"
    }).setVelocity(".images img:first-child",{
      opacity:1,
      bottom:"0",
      paddingBottom:"10%"
    },800).triggerHook(.4).addTo(e),
    new ScrollMagic.Scene({
      triggerElement:".background-mountains"
    }).setVelocity(".images img:last-child",{
      opacity:1,
      bottom:"0"
    },800).triggerHook(.3).addTo(e)
  },
*/
/* Пока не нужен
  PHIL.IsotopeSort=function(){
    e(".sorting-container").each(function(){
      var i=e(this),
      t=i.data("layout").length?i.data("layout"):"masonry";i.isotope({
        itemSelector:".sorting-item",
        layoutMode:t,
        percentPosition:!0
      }),i.imagesLoaded().progress(function(){
        i.isotope("layout")
      }),
      i.siblings(".sorting-menu").find("li").on("click",function(){
        if(e(this).hasClass("active"))return!1;
        e(this).parent().find(".active").removeClass("active"),
        e(this).addClass("active");
        var t=e(this).data("filter");
        return void 0!==t?(i.isotope({
          filter:t
        }),!1):void 0
      })
    })
  },
*/
/* Пока не нужен
  PHIL.rangeSlider=function(){
    e(".range-slider-js").ionRangeSlider({
      type:"double",
      grid:!0,
      min:0,
      max:1e3,
      from:200,
      to:800,
      prefix:"$"
    })
  },
*/
  PHIL.initSwiper=function(){
    var i=0,
        t=!1;
    e(".swiper-container").each(function(){
      var swiper=e(this),
          swiper_id="swiper-unique-id-"+i;
      swiper.addClass("swiper-"+swiper_id+" initialized").attr("id",swiper_id),
      swiper.find(".swiper-pagination").addClass("pagination-"+swiper_id);
      swiper.parent().find(".next").addClass("next-"+swiper_id);
      swiper.parent().find(".prev").addClass("prev-"+swiper_id);
      var r=swiper.data("effect")?swiper.data("effect"):"slide",
          s=!swiper.data("crossfade")||swiper.data("crossfade"),
          l=0!=swiper.data("loop")||swiper.data("loop"),
          c=swiper.data("show-items")?swiper.data("show-items"):1,
          d=swiper.data("scroll-items")?swiper.data("scroll-items"):1,
          u=swiper.data("direction")?swiper.data("direction"):"horizontal",
          g=!!swiper.data("mouse-scroll")&&swiper.data("mouse-scroll"),
          m=swiper.data("autoplay")?parseInt(swiper.data("autoplay"),10):0,
          p=!!swiper.hasClass("auto-height"),
          f=c>1?20:0;
      n["swiper-"+swiper_id]=new Swiper(".swiper-"+swiper_id,{

        preventClicks:!0,
        preventClicksPropagation:!0,

        uniqueNavElements:t,
        nextButton: '.next-'+swiper_id,
        prevButton: '.prev-'+swiper_id,
        pagination:".pagination-"+swiper_id,
        paginationClickable:!0,
        direction:u,
        mousewheelControl:g,
        mousewheelReleaseOnEdges:g,
        slidesPerView:c,
        slidesPerGroup:d,
        spaceBetween:f,
        keyboardControl:!0,
        setWrapperSize:!0,
        preloadImages:false,
        lazyLoading: true,
        updateOnImagesReady:!0,
        autoplay:m,
        autoHeight:p,
        loop:l,
        breakpoints:t,
        effect:r,
        fade:{
          crossFade:s
        },
        parallax:!0,
        observer: true,
        observeParents: true,
        onAfterResize: function(e){
          //var table = $(swiper).find(".swiper-slide-active table");
          //table.height(table.parent().find('img').height());
        },
        onLazyImageReady: function(e){
          setTimeout(function(){
            var table = $(swiper).find(".swiper-slide-active table");
            table.height(table.parent().find('img').height());
          }, 100);
        },
        onSlideChangeEnd:function(e){
          var table = $(swiper).find(".swiper-slide-active table");
          table.height(table.parent().find('img').height());
        },
        onSlideChangeStart:function(e){
          if(swiper.find(".slider-slides").length){
            swiper.find(".slider-slides .slide-active").removeClass("slide-active");
            var i=e.slides.eq(e.activeIndex).attr("data-swiper-slide-index");
            swiper.find(".slider-slides .slides-item").eq(i).addClass("slide-active")
          }
        }
      }),
      i++
    }),
    e(".btn-prev").on("click",function(){
      n["swiper-"+e(this).parent().attr("id")].slidePrev()
    }),
    e(".btn-next").on("click",function(){
      n["swiper-"+e(this).parent().attr("id")].slideNext()
    }),
    e(".slider-slides .slides-item").on("click",function(){
      if(e(this).hasClass("slide-active"))return!1;
      var i=e(this).parent().find(".slides-item").index(this);
      return n["swiper-"+e(this).closest(".swiper-container").attr("id")].slideTo(i+1),
             e(this).parent().find(".slide-active").removeClass("slide-active"),
             e(this).addClass("slide-active"),!1
    })
  },
  PHIL.burgerAnimation=function(){
    function e(e){
      e.draw("80% - 240","80%",.3,{
        delay:.1,
        callback:function(){
          i(e)
        }
      })
    }
    function i(e){
      e.draw("100% - 545","100% - 305",.6,{
        easing:ease.ease("elastic-out",1,.3)
      })
    }
    function t(e){
      e.draw(g-60,m+60,.1,{
        callback:function(){
          o(e)
        }
      })
    }
    function o(e){
      e.draw(g+120,m-120,.3,{
        easing:ease.ease("bounce-out",1,.3)
      })
    }
    function n(e){
      e.draw("90% - 240","90%",.1,{
        easing:ease.ease("elastic-in",1,.3),callback:function(){
          a(e)
        }
      })
    }
    function a(e){
      e.draw("20% - 240","20%",.3,{
        callback:function(){
          r(e)
        }
      })
    }
    function r(e){
      e.draw(d,u,.7,{
        easing:ease.ease("elastic-out",1,.3)
      })
    }
    function s(e){
      e.draw(g,m,.7,{
        delay:.1,
        easing:ease.ease("elastic-out",2,.4)
      })
    }
    function l(e){
      e.className="menu-icon-wrapper scaled"
    }
    function c(e){
      e.className="menu-icon-wrapper"
    }
    var d=80,
        u=320,
        g=80,
        m=320,
        p=document.getElementById("pathD"),
        f=document.getElementById("pathE"),
        h=document.getElementById("pathF"),
        y=new Segment(p,d,u),
        C=new Segment(f,g,m),
        v=new Segment(h,d,u),
        w=document.getElementById("menu-icon-wrapper"),
        S=document.getElementById("menu-icon-trigger"),
        b=!0;
        w.style.visibility="visible",
        S.onclick=function(){
          l(w),
          b?(e(y),
          t(C),
          e(v)):(n(y),
          s(C),
          n(v)),
          b=!b,
          setTimeout(function(){
            c(w)
          },450)
        }
    },i.keydown(function(e){
      27==e.which&&(d.hasClass("opened")&&PHIL.togglePanel(),
      o.hasClass("open")&&PHIL.toggleSearch())
    }),
    jQuery(".js-window-popup").on("click",function(){
      return setTimeout(function(){
        e(".window-popup").addClass("open"),
        o.toggleClass("body-overflow")
      },300), !1
    }),
    jQuery(".js-popup-close").on("click",function(){
      return e(".window-popup").removeClass("open"),
      o.removeClass("body-overflow"),!1
    }),
    jQuery(".js-close-aside").on("click",function(){
      return d.hasClass("opened")&&PHIL.togglePanel(),!1
    }),
    jQuery(".js-open-aside").on("click",function(){
      return d.hasClass("opened")||PHIL.togglePanel(),!1
    }),
    jQuery(".js-open-search").on("click",function(){
      return PHIL.toggleSearch(),!1
    }),
    jQuery(".overlay_search-close").on("click",function(){
      return o.removeClass("open"),!1
    }),
    jQuery(".js-open-p-search").on("click",function(){
      p.fadeToggle()
    }),
    jQuery("#top-bar-js").on("click",function(){
      return e(".top-bar").addClass("open"),
      o.toggleClass("overlay-enable"),!1
    }),
    jQuery("#top-bar-close-js").on("click",function(){
      return e(".top-bar").removeClass("open"),
      o.removeClass("overlay-enable"),!1
    }),
    p.length&&p.find("input").focus(function(){
      p.stop().animate({
        width:p.closest(".container").width()+70
      },600)
    }).blur(function(){
      p.fadeToggle("fast",function(){
        p.css({width:""})
      })
    }),
    t.on("click",function(i){
      e(i.target).closest(f).length||f.hasClass("visible")&&(f.fadeToggle(200),f.toggleClass("visible")),
      e(i.target).closest(d).length||d.hasClass("opened")&&PHIL.togglePanel()
    }),
    jQuery(".js-cart-animate").on("click",function(e){
      e.stopPropagation(),
      f.toggleClass("visible"),
      f.fadeToggle(200)
    }),
    e(".quantity-plus").on("click",function(){
      var i=parseInt(e(this).prev("input").val());
      return e(this).prev("input").val(i+1).change(),!1
    }),
    e(".quantity-minus").on("click",function(){
      var i=parseInt(e(this).next("input").val());
      return 1!==i&&e(this).next("input").val(i-1).change(),!1
    }),
  e(".collapse").collapse(),
  jQuery(".back-to-top").on("click",function(){
    return e("html,body").animate({
      scrollTop:0
    },1200),!1
  }),
  jQuery(".input-inline").find("input").focus(function(){
    e(this).closest("form").addClass("input-drop-shadow")
  }).blur(function(){
    e(this).closest("form").removeClass("input-drop-shadow")
  }),t.ready(function(){
    e("#menu-icon-wrapper").length&&PHIL.burgerAnimation(),
    d.length&&PHIL.customScroll(),
    u.philmegamenu({
      showSpeed:0,
      hideSpeed:0,
      trigger:"hover",
      animation:"drop-up",
      indicatorFirstLevel:"&#xf0d7",
     indicatorSecondLevel:"&#xf105"
    }),
    PHIL.fixedHeader(),
    PHIL.initSwiper(),
    PHIL.equalHeight(),
    //PHIL.mediaPopups(), // Пока погасил, возможно, понадобится magnific-popup
    //PHIL.IsotopeSort(), // Пока не нужен
    PHIL.parallaxFooter(),
    //PHIL.rangeSlider(), // Пока не нужен
    PHIL.headerSpacer.init(),
    PHIL.updateResponsiveInit()
    //PHIL.animateSvg(), // Пока нахер не нужен, файлы удалил
/* Пока убрал, нах эти счетчики и прогрессбары
    PHIL.counters(),
    PHIL.progresBars(),
*/
/* Анимация для определенных сцен
    e(".subscribe").length&&PHIL.SubscribeScrollAnnimation(),
    e(".seo-score").length&&PHIL.SeoScoreScrollAnnimation(),
    e(".testimonial-slider").length&&PHIL.TestimonialScrollAnnimation(),
    e(".our-vision").length&&PHIL.OurVisionScrollAnnimation(),
    e(".background-mountains").length&&PHIL.MountainsScrollAnnimation()
*/
  });

  var anchors = Array();
  $("#primary-menu ul li a").each(function(){
    var pk = $(this).attr("href");
    if(pk.indexOf("#") == 0 && pk.length > 1){
      var container = $(pk);
      if(container.length > 0){
        anchors.push({'container': container, 'link': $(this)});
      }
    }
  });

  $(window).scroll(function(){
    for(var i=0; i<anchors.length; i++){
      var el = anchors[i]['container'];
      var top  = el.offset().top - 100;
      var bottom = top + el.height();
      var scroll = $(window).scrollTop();
      var id = el.attr('id');
      if(scroll > top && scroll < bottom){
        $("#primary-menu li.active").removeClass("active");
        anchors[i]['link'].parent().addClass("active");
      }
    }
  });

  $("#portfolio .primary-menu-menu li a").click(function(){
    $("#portfolio .primary-menu-menu li").removeClass("active");
    $(this).parent().addClass("active");
  });

  $('.fancybox').fancybox();

  /* Ибучий сайдбар для project шаблона */

  if($(".project .sidebar .primary-menu-menu").length > 0){
    var sidebar_menu_item_height = 120;
    var sidebar_menu_animating = false;
    var sticky = null;
    var sticky_container = $(".project .sidebar .vertical-menu .primary-menu-menu");
    var sticky_container_mobile = $(".project .sidebar .horizontal-menu .primary-menu-menu");
    var link_path = window.location.pathname;

    function find_active_sidebar_menu(){
      $(".project .sidebar .vertical-menu .primary-menu-menu a").each(function(){
        if($(this).attr("href") == link_path){
          sticky_container.scrollTo($(this));
        }
      });
      $(".project .sidebar .horizontal-menu .primary-menu-menu a").each(function(){
        if($(this).attr("href") == link_path){
          sticky_container_mobile.scrollTo($(this));
        }
      });
    }
    function create_sticky_portfolio_menu(){
      sticky = new Sticky('.project .w-post-category', {
        'wrap': true,
        'wrapWith': '<span class="sticky_wrapper"></span>',
        'stickyClass': 'sticked',
        'stickyContainer': '.sticky_container',
        'marginTop': 130,
      });
    }
    function check_resize_window(){
      var windowWidth = $(window).width();
      if (windowWidth > 799){
        create_sticky_portfolio_menu();
        sidebar_menu_item_height = 120;
      }else if (sticky != null){
        sticky.destroy();
        sticky = null;
        sidebar_menu_item_height = 39;
      }else{
        sidebar_menu_item_height = 39;
      }
      find_active_sidebar_menu();
    }
    $(window).resize(function(){
      if(window.resizing) clearTimeout(window.resizing);
      window.resizing = setTimeout(check_resize_window, 500);
    });
/*
    $(window).scroll(function(){
      if($("#site-header").hasClass("fadeIn")){
        $(".project .sticky_wrapper .sticked").addClass("sticked2");
      }else{
        $(".project .sticky_wrapper .sticked").removeClass("sticked2");
      }
    });
*/
    $(".project .vertical-menu .prev").click(function(){
      if (sidebar_menu_animating) {
        return;
      }
      sidebar_menu_animating = true;
      sticky_container.animate({scrollTop: (sticky_container.scrollTop() - sidebar_menu_item_height)}, 400, 'swing', function(){
        sidebar_menu_animating = false;
      });
    });
    $(".project .vertical-menu .next").click(function(){
      if (sidebar_menu_animating) {
        return;
      }
      sidebar_menu_animating = true;
      sticky_container.animate({scrollTop: (sticky_container.scrollTop() + sidebar_menu_item_height)}, 400, "swing", function(){
        sidebar_menu_animating = false;
      });
    });

    $(".project .horizontal-menu .prev").click(function(){
      if (sidebar_menu_animating) {
        return;
      }
      sidebar_menu_animating = true;
      sticky_container_mobile.animate({scrollTop: (sticky_container_mobile.scrollTop() - sidebar_menu_item_height)}, 400, 'swing', function(){
        sidebar_menu_animating = false;
      });
    });

    $(".project .horizontal-menu .next").click(function(){
      if (sidebar_menu_animating) {
        return;
      }
      sidebar_menu_animating = true;
      sticky_container_mobile.animate({scrollTop: (sticky_container_mobile.scrollTop() + sidebar_menu_item_height)}, 400, "swing", function(){
        sidebar_menu_animating = false;
      });
    });

    if (link_path.indexOf('flatcontent') > -1){
      var z = 0;
      $(".sidebar .primary-menu-menu a").each(function(){
        z += 1;
        if(z > 6){
          $(this).parent().addClass("hidden");
        }
      });
      return;
    }
    var parts = link_path.split("/");
    var part = "/" + parts[1] + "/";
    $(".project .sidebar .primary-menu-menu a").each(function(){
      if($(this).attr("href").indexOf(part) == -1){
        $(this).parent().addClass("hidden");
      }
    });
    // Только после того как спрятали,
    // делаем показ активного меню,
    // заставляем меню быть плавучим
    check_resize_window();
  }

  /* Ибучее портфолио с мультислайдером
     https://swiperjs.com/demos/
   */
  $(".dynamic_portfolio_link").click(function(){
    var container_id = $(this).attr('data-container_id');
    var block_id = $(this).attr('data-block_id');
    $("#dynamic_portfolio_" + container_id + " .dynamic_portfolio_link").removeClass("active");
    $(this).addClass("active");
    $(".portfolio_swiper").addClass("hidden");
    $("#portfolio_" + container_id + "_" + block_id).removeClass("hidden");

    var table = $("#portfolio_" + container_id + "_" + block_id + " .swiper-slide-active table");
    table.height(table.parent().find('img').height());
  });

  $(".projects .case-item__thumb").hover(function(){
      var table = $(this).find('table');
      table.height(table.parent().find('img').height());
  });

  /* Форма обратной связи */
  var feedback_form = new FeedBack("feedback_form", {
    "wait": "Ждите...",
    //"send": "Отправить",
    "success": "Профиль обновлен",
    "progress": "Пожалуйста, ждите...",
    "error": "Произошла ошибка, сообщите нам по телефону",
    "error_captcha": "Не пройдена проверка на работа",
    "callback_success": "",
    "callback_error": "",
    "dont_reset_on_submit": 1, // or 1
    //"errorClass": "invalid",
  });
  if($("#portfolio_mini_menu_container").length > 0 && portfolio_mini_menu){
    var html = "<ul class='primary-menu-menu'>";
    var class_name = "";
    var link = "";
    for(var i=0; i<portfolio_mini_menu.length; i++){
      class_name = "";
      link = portfolio_mini_menu[i]['link'];
      if(window.location.href.indexOf(link) >= 0){
        class_name = " class='active'";
      }
      html += "<li" + class_name + "><a href=" + link + ">" + portfolio_mini_menu[i]['name'] + "</a></li>"
    }
    html += "</ul>";
    $("#portfolio_mini_menu_container").html(html);
  }
}(jQuery);