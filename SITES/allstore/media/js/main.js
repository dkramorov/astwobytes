"use strict";

function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

$(document).ready(function () {

    // Single Product Tabs
    $('.prod-tabs li').on('click', 'a', function () {
        if ($(this).hasClass('active') || $(this).attr('data-prodtab') == '')
            return false;
        $(this).parents('.prod-tabs').find('li a').removeClass('active');
        $(this).addClass('active');

        // mobile
        $('.prod-tab-mob[data-prodtab-num=' + $(this).data('prodtab-num') + ']').parents('.prod-tab-cont').find('.prod-tab-mob').removeClass('active');
        $('.prod-tab-mob[data-prodtab-num=' + $(this).data('prodtab-num') + ']').addClass('active');

        $($(this).attr('data-prodtab')).parents('.prod-tab-cont').find('.prod-tab').css('height', '0px');
        $($(this).attr('data-prodtab')).css('height', 'auto');
        return false;
    });

    // Single Product Tabs (mobile)
    $('.prod-tab-cont').on('click', '.prod-tab-mob', function () {
        if ($(this).hasClass('active') || $(this).attr('data-prodtab') == '')
            return false;
        $(this).parents('.prod-tab-cont').find('.prod-tab-mob').removeClass('active');
        $(this).addClass('active');

        // main
        $('.prod-tabs li a[data-prodtab-num=' + $(this).data('prodtab-num') + ']').parents('.prod-tabs').find('li a').removeClass('active');
        $('.prod-tabs li a[data-prodtab-num=' + $(this).data('prodtab-num') + ']').addClass('active');

        $($(this).attr('data-prodtab')).parents('.prod-tab-cont').find('.prod-tab').css('height', '0px');
        $($(this).attr('data-prodtab')).css('height', 'auto').hide().fadeIn();
        return false;
    });


    // Popular Products Tabs
    $('.fr-pop-tabs li').on('click', 'a', function () {
        if ($(this).hasClass('active') || $(this).attr('data-frpoptab') == '')
            return false;
        $(this).parents('.fr-pop-tabs').find('li a').removeClass('active');
        $(this).addClass('active');

        // mobile
        $('.fr-pop-tab-mob[data-frpoptab-num=' + $(this).data('frpoptab-num') + ']').parents('.fr-pop-tab-cont').find('.fr-pop-tab-mob').removeClass('active');
        $('.fr-pop-tab-mob[data-frpoptab-num=' + $(this).data('frpoptab-num') + ']').addClass('active');

        $($(this).attr('data-frpoptab')).parents('.fr-pop-tab-cont').find('.fr-pop-tab').css('height', '0px');
        $($(this).attr('data-frpoptab')).css('height', 'auto').hide().fadeIn();
        return false;
    });

    // Popular Products Tabs (mobile)
    $('.fr-pop-tab-cont').on('click', '.fr-pop-tab-mob', function () {
        if ($(this).hasClass('active') || $(this).attr('data-frpoptab') == '')
            return false;
        $(this).parents('.fr-pop-tab-cont').find('.fr-pop-tab-mob').removeClass('active');
        $(this).addClass('active');

        // main
        $('.fr-pop-tabs li a[data-frpoptab-num=' + $(this).data('frpoptab-num') + ']').parents('.fr-pop-tabs').find('li a').removeClass('active');
        $('.fr-pop-tabs li a[data-frpoptab-num=' + $(this).data('frpoptab-num') + ']').addClass('active');

        $($(this).attr('data-frpoptab')).parents('.fr-pop-tab-cont').find('.fr-pop-tab').animate({
            'height': '0px'
        }, 350);
        $($(this).attr('data-frpoptab')).animate({
            'height': $($(this).attr('data-frpoptab')).find('.flex-viewport').outerHeight()+'px'
        }, 350);

        return false;
    });

    // Accordions
    $('.accordion-tab-cont').on('click', '.accordion-tab-mob', function () {
        if ($(this).hasClass('active') || $(this).attr('data-accordion') == '')
            return false;
        $(this).parents('.accordion-tab-cont').find('.accordion-tab-mob').removeClass('active');
        $(this).addClass('active');

        $($(this).attr('data-accordion')).parents('.accordion-tab-cont').find('.accordion-tab').animate({
            'height': '0px'
        }, 350);
        $($(this).attr('data-accordion')).animate({
            'height': $($(this).attr('data-accordion')).find('.accordion-inner').outerHeight()+'px'
        }, 350);

        return false;
    });

    // "All Features" button
    $('.prod-showprops').on('click', function () {
        if ($('.prod-tabs li a.active').attr('data-prodtab') == '#prod-tab-2') {
            $('html, body').animate({scrollTop: ($('.prod-tabs-wrap').offset().top - 10)}, 700);
        } else {
            $('.prod-tabs li a').removeClass('active');
            $('#prod-props').addClass('active');
            $('.prod-tab-cont .prod-tab').css('height', '0px');
            $('#prod-tab-2').css('height', 'auto');
            $('html, body').animate({scrollTop: ($('.prod-tabs-wrap').offset().top - 10)}, 700);
        }
        return false;
    });


    // Sidebar Categories
    $('#section-sb-toggle').on('click', function () {
        $('#section-sb-list').slideToggle();
        if ($(this).hasClass('opened'))
            $(this).removeClass("opened");
        else
            $(this).addClass('opened');
        return false;
    });

    $("#section-sb-list li.has_child").on("click", ".section-sb-toggle", function () {
        $(this).parent().next("ul").slideToggle();
        if ($(this).hasClass('opened'))
            $(this).removeClass("opened");
        else
            $(this).addClass('opened');
        return false;
    });

    // Filter Toggle (mobile)
    $('#section-filter-toggle').on('click', function () {
        $(this).next('.section-filter-cont').slideToggle();
        if ($(this).hasClass('opened')) {
            $(this).removeClass("opened").find('span').text($(this).data("open"));
        }
        else {
            $(this).addClass('opened').find('span').text($(this).data("close"));
        }
        return false;
    });

    // Product Offers (select type)
    $('body').on('click', '.offer-props-select p', function () {
        if ($(this).parent().hasClass('opened'))
            $(this).parent().removeClass('opened');
        else
            $(this).parent().addClass('opened');
        return false;
    });
    $('body').on('click', '.offer-props-select li', function () {
        if ($(this).parent().parent().hasClass('opened'))
            $(this).parent().parent().removeClass('opened');
        else
            $(this).parent().parent().addClass('opened');
    });
    $('body').on('click', '.offer-props-select li', function () {
        $(this).parent().parent().find('p').html($(this).text());
    });

    // Topmenu
    $('.topmenu').on('click', '.mainmenu-btn', function () {
        if ($('body').hasClass('mainmenu-show')) {
            $('body').removeClass('mainmenu-show');
        } else {
            $('body').addClass('mainmenu-show');
        }
            return false;
    });
    $('html').on('click', 'body.mainmenu-show', function () {
        $('body').removeClass('mainmenu-show');
    });
    $('body').on('click', '.mainmenu', function(event){
        event.stopPropagation();
    });

    // Topmenu (mobile)
    if ($(window).width() < 751) {
        $('.topmenu .mainmenu li a .fa').on('click', function () {
            if ($(this).parent().next('.sub-menu').hasClass('opened')) {
                $(this).parent().next('.sub-menu').removeClass('opened');
                $(this).parent().next('.sub-menu').slideUp();
            } else {
                $(this).parent().next('.sub-menu').addClass('opened');
                $(this).parent().next('.sub-menu').slideDown();
            }
            return false;
        });

        $('.topcatalog').on('click', '.topcatalog-btn', function () {
            if ($('body').hasClass('topcatalog-show')) {
                $('body').removeClass('topcatalog-show');
            } else {
                $('body').addClass('topcatalog-show');
            }
                return false;
        });
        $('html').on('click', 'body.topcatalog-show', function () {
            $('body').removeClass('topcatalog-show');
        });
        $('body').on('click', '.topcatalog-list', function(event){
            event.stopPropagation();
        });
        $('.topcatalog li .fa').on('click', function () {
            if ($(this).next('ul').hasClass('opened')) {
                $(this).next('ul').removeClass('opened');
                $(this).next('ul').slideUp();
            } else {
                $(this).next('ul').addClass('opened');
                $(this).next('ul').slideDown();
            }
            return false;
        });
    }

    // Search Button
    $('.topsearch').on('click', '#topsearch-btn', function () {
        if ($('body').hasClass('search-show')) {
            $('body').removeClass('search-show');
        } else {
            $('body').addClass('search-show');
        }
            return false;
    });

    // Search Close
    $('body.search-show').on('click', '#topsearch-btn', function () {
        if ($('body').hasClass('search-show')) {
            $('body').removeClass('search-show');
        }
        return false;
    });
    $('html').on('click', 'body.search-show', function () {
        $('body').removeClass('search-show');
    });
    $('body').on('click', '.topsearch', function(event){
        event.stopPropagation();
    });

    // Mainmenu "more" button
    if ($('.mainmenu').length > 0) {
        if ($(window).width() > 751) {
            var menu_sections = $('.mainmenu');
            var menu_width = menu_sections.width();
            var menu_items_width = 0;
            menu_sections.find('> li').each(function () {
                if (!$(this).hasClass('mainmenu-more')) {
                    menu_items_width = menu_items_width + $(this).outerWidth(true);
                    if (menu_width < menu_items_width) {
                        $(this).addClass('mainmenu-other');
                        $(this).appendTo('.mainmenu-sub');
                    } else if ($(this).hasClass('mainmenu-other')) {
                        $(this).removeClass('mainmenu-other');
                        $(this).prependTo('.mainmenu-sub');
                    }
                }
            });
            if (menu_width < menu_items_width) {
                $('.mainmenu-more').show();
            }
        }

        $('.mainmenu').addClass('sections-show');

        $(window).resize(function() {
            var menu_sections = $('.mainmenu');
            var menu_width = menu_sections.width();
            var menu_items_width = 0;
            if ($(window).width() > 751) {
                menu_sections.find('> li').each(function () {
                    menu_items_width = menu_items_width + ($(this).outerWidth(true) + 4);
                    if (!$(this).hasClass('mainmenu-more')) {
                        if (menu_width < menu_items_width) {
                            $(this).addClass('mainmenu-other');
                            $(this).appendTo('.mainmenu-sub');
                        } else if ($(this).hasClass('mainmenu-other')) {
                            $(this).removeClass('mainmenu-other');
                            $(this).prependTo('.mainmenu-sub');
                        }
                    }
                });
                if (menu_width < menu_items_width) {
                    $('.mainmenu-more').show();
                }
            } else {
                menu_sections.find('li.mainmenu-other').insertBefore('.mainmenu-more');
                menu_sections.find('li.mainmenu-other').removeClass('mainmenu-other');
            }
        });

    }

    // Popular Products "more" button
    if ($('.fr-pop-tabs').length > 0) {
        if ($(window).width() > 751) {
            var menu_sections = $('.fr-pop-tabs');
            var menu_width = menu_sections.width();
            var menu_items_width = 0;
            menu_sections.find('> li').each(function () {
                if (!$(this).hasClass('fr-pop-tabs-more')) {
                    menu_items_width = menu_items_width + $(this).outerWidth(true);
                    if (menu_width < menu_items_width) {
                        $(this).addClass('fr-pop-tabs-other');
                        $(this).appendTo('.fr-pop-tabs-sub');
                    } else if ($(this).hasClass('fr-pop-tabs-other')) {
                        $(this).removeClass('fr-pop-tabs-other');
                        $(this).prependTo('.fr-pop-tabs-sub');
                    }
                }
            });
            if (menu_width < menu_items_width) {
                $('.fr-pop-tabs-more').show();
            }
        }

        $('.fr-pop-tabs').addClass('sections-show');

        $(window).resize(function() {
            var menu_sections = $('.fr-pop-tabs');
            var menu_width = menu_sections.width();
            var menu_items_width = 0;
            if ($(window).width() > 751) {
                menu_sections.find('> li').each(function () {
                    menu_items_width = menu_items_width + ($(this).outerWidth(true) + 4);
                    if (!$(this).hasClass('fr-pop-tabs-more')) {
                        if (menu_width < menu_items_width) {
                            $(this).addClass('fr-pop-tabs-other');
                            $(this).appendTo('.fr-pop-tabs-sub');
                        } else if ($(this).hasClass('fr-pop-tabs-other')) {
                            $(this).removeClass('fr-pop-tabs-other');
                            $(this).prependTo('.fr-pop-tabs-sub');
                        }
                    }
                });
                if (menu_width < menu_items_width) {
                    $('.fr-pop-tabs-more').show();
                }
            } else {
                menu_sections.find('li.fr-pop-tabs-other').insertBefore('.fr-pop-tabs-more');
                menu_sections.find('li.fr-pop-tabs-other').removeClass('fr-pop-tabs-other');
            }
        });

    }

    // Reviews "Show Answer" button
    if ($('.reviews-i-showanswer').length > 0) {
        $('.reviews-i-showanswer').on('click', function () {
            if ($(this).hasClass('opened')) {
                $(this).removeClass('opened').find('span').text($(this).find('span').data('open'));
                $(this).parents('.reviews-i').find('.reviews-i-answer').slideUp();
            } else {
                $(this).addClass('opened').find('span').text($(this).find('span').data('close'));
                $(this).parents('.reviews-i').find('.reviews-i-answer').slideDown();
            }
            return false;
        });
    }

    // Catalog Gallery - Show Properties on hover
    if ($('.prod-items-galimg .prod-i-properties-label').length > 0) {
        $('.prod-items-galimg .prod-i-properties-label').on({
            mouseenter: function () {
                $(this).parents('.prod-i').find('.prod-i-properties').addClass('show');
                return false;
            },
            mouseleave: function () {
                $(this).parents('.prod-i').find('.prod-i-properties').removeClass('show');
                return false;
            }
        });
    }

    // Catalog Table - Show more info button
    if ($('.prodtb-i-toggle').length > 0) {
        $('.prodtb-i-toggle').on('click', function () {
            if ($(this).hasClass('opened')) {
                $(this).removeClass('opened').parents('.prodtb-i').find('.prodlist-i').hide();
            } else {
                $(this).addClass('opened').parents('.prodtb-i').find('.prodlist-i').show();
            }
            return false;
        });
    }
});




$(window).load(function () {

    // Quick View button
    $('.qview-btn').fancybox({
        content: $('.qview-modal'),
        padding: 0,
        helpers : {
            overlay : {
                locked  : false
            }
        }
    });

    // Product Images Slider
    if ($('.prod-slider-car').length > 0) {
        $('.prod-slider-car').each(function () {
            $(this).bxSlider({
                pagerCustom: $(this).parents('.prod-slider-wrap').find('.prod-thumbs-car'),
                adaptiveHeight: true,
                infiniteLoop: false,
            });
            $(this).parents('.prod-slider-wrap').find('.prod-thumbs-car').bxSlider({
                slideWidth: 5000,
                slideMargin: 8,
                moveSlides: 1,
                infiniteLoop: false,
                minSlides: 5,
                maxSlides: 5,
                pager: false,
            });
        });
    }

    // Filter
    if ($('.section-filter-ttl').length > 0) {
        $('.section-filter').on('click', '.section-filter-ttl', function () {
            if ($(this).parents('.section-filter-item').hasClass('opened')) {
                $(this).parents('.section-filter-item').removeClass('opened');

            } else {
                $(this).parents('.section-filter-item').addClass('opened');
            }
            return false;
        });
    }

    // Product Countdown
    if ($('.countdown').length > 0) {
        $('.countdown').each(function () {
            if (!$(this).data('date')) {
                return;
            }
            var countdown = $(this);
            var BigDay = new Date(countdown.data('date'));
            var msPerDay = 24 * 60 * 60 * 1000 ;
            window.setInterval(function(){
                var today = new Date();
                var timeLeft = (BigDay.getTime() - today.getTime());
                var e_daysLeft = timeLeft / msPerDay;
                var daysLeft = Math.floor(e_daysLeft);
                var e_hrsLeft = (e_daysLeft - daysLeft)*24;
                var hrsLeft = Math.floor(e_hrsLeft);
                var e_minsLeft = (e_hrsLeft - hrsLeft)*60;
                var minsLeft = Math.floor(e_minsLeft);
                var e_secsLeft = (e_minsLeft - minsLeft)*60;
                var secsLeft = Math.floor(e_secsLeft);
                var timeString = daysLeft + "d " + pad(hrsLeft) + ":" + pad(minsLeft) + ":" + pad(secsLeft);
                countdown.html(timeString);
                if (!countdown.hasClass('display')) {
                    countdown.addClass('display');
                }
            }, 1000);
        });
    }

});



/* PRODUCT V2 - start */
var fixed_obj = {};

function compareScrollStyles(st, newSt) {
    var obj1 = $.extend({}, st),
        obj2 = $.extend({}, newSt);
    $.each(obj1, function(i, k) {
        if (i !== 'position') {
            obj1[i] = Math.round(k);
        }
    });
    $.each(obj2, function(i, k) {
        if (i !== 'position') {
            obj2[i] = Math.round(k);
        }
    });
    return JSON.stringify(obj1) === JSON.stringify(obj2);
}

function setStyle(elem, name, value){
    elem = $(elem);
    if (!elem) return;
    if (typeof name == 'object') return $.each(name, function(k, v) { setStyle(elem,k,v); });
    elem.removeAttr('style');
    elem.css(name, value + 'px');
}

function fixed_on_scroll() {

    var
        thumbs = $('.prod2-thumbs-car'),
        content = $('.prod-cont-inner'),
        slider = $('.prod2-slider-wrap');

    var
        wh = $(window).height() || 0,
        st = $(window).scrollTop(),
        headH = 15,
        isFixed = content.css('position') == 'fixed',
        contentH = content.outerHeight(),
        sliderH = slider.outerHeight(),
        sliderPos = slider.offset().top,
        tooBig = contentH >= sliderH,
        contentBottom = st + wh - sliderH - sliderPos,
        contentPB = Math.max(0, contentBottom),
        contentPT = sliderPos - headH,
        contentPos = content.offset().top,
        thumbsH = (typeof thumbs !== "undefined" ? thumbs.outerHeight() : 0),
        thumbsPos = (typeof thumbs.offset() !== "undefined" ? thumbs.offset().top : 0),
        lastSt = fixed_obj.lastSt || 0,
        lastStyles = fixed_obj.lastStyles || {},
        styles,
        needFix = false,
        smallEnough = headH + contentH + contentPB <= wh,
        delta = 1;

    if (st - delta < contentPT && !(smallEnough && contentPos < headH) || tooBig) {
        thumbs.removeAttr('style');
        thumbs.removeClass('stick');
    } else if ((wh + st >= Math.max(contentPos + contentH, sliderPos + sliderH)) && (thumbsPos > sliderPos)) {
        thumbs.css('margin-top', (thumbsPos - sliderPos) + 'px');
        thumbs.removeClass('stick');
    } else if (wh + st < Math.max(contentPos + contentH, sliderPos + sliderH) && thumbsH < contentH) {
        thumbs.removeAttr('style');
        thumbs.addClass('stick');
    }

    if (st - delta < contentPT && !(smallEnough && contentPos < headH) || tooBig) {
        styles = {
            marginTop: 0
        };
    } else if (st - delta < Math.min(lastSt, contentPos - headH) || smallEnough) {
        styles = {
            top: headH
        };
        needFix = true;
    } else if (st + delta > Math.max(lastSt, contentPos + contentH - wh) && contentBottom < 0) {
        styles = {
            bottom: 0
        };
        needFix = true;
    } else {
        styles = {
            marginTop: (contentBottom >= 0) ? sliderH - contentH : Math.min(contentPos - sliderPos, sliderH - contentH + contentPT)
        };
    }

    if (!compareScrollStyles(styles, lastStyles)) {
        $.each (lastStyles, function(i, k) {
            lastStyles[i] = null;
        });
        setStyle(content, $.extend(lastStyles, styles));
        fixed_obj.lastStyles = styles;
    }
    if (needFix !== isFixed) {
        if (needFix) {
            $(content).addClass('fixed');
        } else {
            $(content).removeClass('fixed');
        }
    }
    fixed_obj.lastSt = st;

    if (content.width() !== content.parent().width() && needFix) {
        content.width(content.parent().width());
    }
}


$(window).load(function () {

    if ($('.prod2-slider-wrap').length > 0) {
        if ($(window).width() >= 975) {
            fixed_on_scroll();
        }
        $(window).scroll(function () {
            if ($(window).width() >= 975) {
                fixed_on_scroll();
            }
        });
    }

    if ($('.prod2-thumbs-car li a').length > 0) {

        // Scroll to
        $('.prod2-thumbs-car li').on('click', 'a', function () {
            if ($(window).width() >= 975) {
                var
                    el_index = $(this).attr('data-slide-index'),
                    slide = $('.prod2-slider-car li img').eq(el_index),
                    slide_h = slide.outerHeight(),
                    w_h = $(window).height(),
                    slide_pos = slide.offset().top + slide_h/2 - w_h/2;
                $('html, body').animate({scrollTop: slide_pos}, 700);
                return false;
            }
        });

        // Waypoints
        $('.prod2-slider-car li img').each(function (i) {
            var this_img = $(this);
            var inview = new Waypoint.Inview({
                element: this_img,
                entered: function(direction) {
                    $('.prod2-thumbs-car li img').removeClass('scroll_active');
                    $('.prod2-thumbs-car li img').eq(i).addClass('scroll_active');
                }
            });
        });
    }

    // Product Images Slider
    if ($('.prod2-slider-car').length > 0) {
        $('.prod2-slider-car').each(function () {

            var this_slider = $(this);
            var this_thumbs = $(this).parents('.prod2-slider-wrap').find('.prod2-thumbs-car');

            var slider_load = false;
            var slider;
            var thumbs;
            if ($(window).width() < 975) {
                slider_load = true;

                this_slider.parents('.prod2-slider-wrap').addClass('slider-load');

                slider = this_slider.bxSlider({
                    pagerCustom: this_thumbs,
                    adaptiveHeight: true,
                    infiniteLoop: false,
                });
                thumbs = this_thumbs.bxSlider({
                    slideWidth: 5000,
                    slideMargin: 8,
                    moveSlides: 1,
                    infiniteLoop: false,
                    minSlides: 5,
                    maxSlides: 5,
                    pager: false,
                });
            } else {

            }
            $(window).resize(function () {
                if (!slider_load && $(window).width() < 975) {
                    slider_load = true;

                    this_slider.parents('.prod2-slider-wrap').addClass('slider-load');

                    slider = this_slider.bxSlider({
                        pagerCustom: this_thumbs,
                        adaptiveHeight: true,
                        infiniteLoop: false,
                    });
                    thumbs = this_thumbs.bxSlider({
                        slideWidth: 5000,
                        slideMargin: 8,
                        moveSlides: 1,
                        infiniteLoop: false,
                        minSlides: 5,
                        maxSlides: 5,
                        pager: false
                    });
                } else if (slider_load && $(window).width() >= 975) {
                    slider_load = false;
                    this_slider.parents('.prod2-slider-wrap').removeClass('slider-load');
                    slider.destroySlider();
                    thumbs.destroySlider();
                }
            });
        });

    }



});
/* PRODUCT V2 - end */




// Compare List
(function($) {
    $.fn.setDraggable = function() {
        var compares = $(this),
            html = $('html');

        compares.each(function() {
            var compare = $(this),
                tables = compare.find('.wccm-table'),
                wrappers = compare.find('.wccm-table-wrapper'),
                dragging = false,
                maxshift = wrappers.width() - tables.width(),
                offset = 0,
                shift = 0;

            $(window).resize(function() {
                maxshift = wrappers.width() - tables.width();
                if (maxshift < 0) {
                    wrappers.css('cursor', 'move');
                } else {
                    wrappers.css('cursor', 'default');
                    tables.css('margin-left', '0');
                }
            });

            if (maxshift < 0) {
                wrappers.css('cursor', 'move');
                shift = parseInt(tables.css('margin-left'));
            }

            tables.mousedown(function(e) {
                var node = e.target.nodeName;

                if (maxshift < 0 && node != 'IMG' && node != 'A') {
                    dragging = true;
                    offset = e.screenX;
                    shift = parseInt(tables.css('margin-left'));
                    wrappers.css('cursor', 'default');
                }
            });

            html.mouseup(function() {
                dragging = false;
                if (maxshift < 0) {
                    wrappers.css('cursor', 'move');
                }
            });

            html.mousemove(function(e) {
                var move = shift - (offset - e.screenX);
                if (dragging && maxshift <= move && move <= 0) {
                    tables.css('margin-left', move + 'px');
                }
            });
        });
        return compares;
    };

    $(document).ready(function() {
        $('.wccm-compare-table').setDraggable();
        get_fat_catalogue();
        $("#tableview").click(function(){
          localStorage.setItem('cat_view', 'table');
        });
        $("#listview").click(function(){
          localStorage.setItem('cat_view', 'list');
        });
        $("#gridview").click(function(){
          localStorage.setItem('cat_view', 'grid');
        });

        var cat_view = localStorage.getItem('cat_view');
        setTimeout(function(){
          if(cat_view == 'grid'){
            $("#gridview").trigger('click');
          }else if(cat_view == 'list'){
            $("#listview").trigger('click');
          }else if(cat_view == 'table'){
            $("#tableview").trigger('click');
          }
        }, 100);
    });
})(jQuery);


// для аякс форм: {csrfmiddlewaretoken: getCookie('csrftoken')}
function getCookie(c_name) {
  if(document.cookie.length > 0) {
    var c_start = document.cookie.indexOf(c_name + "=");
    if(c_start != -1) {
      c_start = c_start + c_name.length + 1;
      var c_end = document.cookie.indexOf(";", c_start);
      if(c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start, c_end));
    }
  }
  return "";
}
function load_fat_catalogue_children(li){
  var ul = li.find('ul');

  if(li.hasClass('loaded')){

    ul.slideToggle();
    if (li.find('.section-sb-toggle').hasClass('opened'))
      li.find('.section-sb-toggle').removeClass("opened");
    else
      li.find('.section-sb-toggle').addClass('opened');

/*
    $(this).next('.section-filter-cont').slideToggle();
    if ($(this).hasClass('opened')) {
      $(this).removeClass("opened").find('span').text($(this).data("open"));
    }else {
      $(this).addClass('opened').find('span').text($(this).data("close"));
    }
*/
    return;
  }

  li.addClass('loaded');
  var params = {
    'csrfmiddlewaretoken': getCookie('csrftoken'),
    'filter__parents': li.attr('data-block_parents'),
  };
  var subli = '';
  $.ajax({
    type: 'POST',
    url: '/flatcontent/blocks/flatcat/api/',
    data: params,
    success: function(data) {
      var rows = data['data'];
      for(var i=0; i<rows.length; i++){
        subli = $('<li class="categ-2"><a href="' + rows[i]['link'] + '"><span class="categ-2-label">' + rows[i]['name'] + '</span></a></li>');
        ul.append(subli);
        subli.click(function(){
          window.location.href = $(this).find('a').attr('href');
          return false;
        });
      }
      ul.slideToggle();
      if (li.find('.section-sb-toggle').hasClass('opened'))
        li.find('.section-sb-toggle').removeClass("opened");
      else
        li.find('.section-sb-toggle').addClass('opened');
    }
  });
}

function get_fat_catalogue(){
  // Получить жирный каталог,
  // если каталог нашелся, заполняем все уровни
  var sidebar_catalogue = $("#section-sb-list");
  if(sidebar_catalogue.length > 0){
    // По каждой рубрике нужно запросить вложенные
    // Если они есть - отобразить плюсик
    var z = 1;
    $("#section-sb-list li.categ-1").each(function(){
      var cur_li = $(this);
      var params = {
        'csrfmiddlewaretoken': getCookie('csrftoken'),
        'filter__parents': $(this).attr('data-block_parents'),
        'only_fields': 'id',
      };
      $.ajax({
        type: 'POST',
        url: '/flatcontent/blocks/flatcat/api/',
        data: params,
        success: function(data) {
          if(parseInt(data['total_records']) > 0){
            cur_li.addClass('has_child');
            cur_li.find('.categ-1-label').after('<span class="section-sb-toggle" id="section-sb-toggle-' + z + '"><span class="section-sb-ico"></span></span>');
            cur_li.find('a').after('<ul></ul>');
            z += 1;

            cur_li.click(function(e){
              load_fat_catalogue_children($(this));
              return false;
            });
          }
        }
      });
    });
  }
}

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

var myMapContainer = "mapContainer";
var mapContainer_points = null;
var myPickupPoint = null;
function create_pickup_points_map(){
  var kwargs = {};
  kwargs['default_town'] = "Иркутск";
  create_new_map(myMapContainer);
  wait_for_result(myMapContainer, function(){
    var myMap = get_map(myMapContainer);
    disable_map_wheel(myMapContainer);
    myMap.kwargs = kwargs;
    var point;

    var pickup_points_menu = $("#map_pickup_points_menu");
    pickup_points_menu.html("");

    if(typeof(mapContainer_points) != null){
      for(var i=0; i<mapContainer_points.length; i++){
        point = mapContainer_points[i];

        myMap.myPoints.push({
          "type": "Feature",
          "id": point.id,
          "geometry": {
            "type": "Point",
            "coordinates": [point.latitude, point.longitude],
          },
          "properties": {
            "balloonContent": "<strong>" + point.addressLines + "</strong><br>" + point.place + "<br><a href='javascript:void(0);' onclick='set_pickup_point(" + point.id + ")'>Выбрать</a>",
            "clusterCaption": "Пункты выдачи",
            "hintContent": "Пункты выдачи",
          },
        });
        pickup_points_menu.append($("<li><a href='javascript:void(0);' id='pickup_point_" + point.id + "'>" + point.addressLines + " " + point.place + "</a></li>"));

        $("#pickup_point_" + point['id']).click(function(){
          scroll_to("#mapContainer");
          var pk = $(this).attr("id").replace("pickup_point_", "");
          var placemark = find_placemark_by_id(pk, myMap);
          console.log("placemark", placemark);
          if(placemark != null){
            var props = placemark['properties'];
            var coords = placemark['geometry']['coordinates'];
            if(myMap.balloon.isOpen()){
              myMap.balloon.close();
            }
            myMap.balloon.open(coords, props['balloonContent'], {});
            myMap.setCenter(coords, 16);
          }else{
            console.log("placemark is null", pk);
          }
        });
      }
      add_points_to_map(myMapContainer, myMap.myPoints);
      set_map_bounds(myMapContainer);
      $("#yandex_map_tab").click(function(){
        myMap.redraw();
      });
      if(myPickupPoint != null){
        $("#map_pickup_points_menu a").removeClass("selected");
        $("#pickup_point_" + myPickupPoint.id).addClass("selected");
      }
    }else{
      console.log("[ERROR]: mapContainer_points undefined");
    }
  }, ["map"]);
}
function set_pickup_point(point_id){
  scroll_to("#map_pickup_points_menu");
  $("#map_pickup_points_menu a").removeClass("selected");
  $("#pickup_point_" + point_id).addClass("selected");
  var params = {
    'point_id': point_id,
  };
  $.ajax({
    type: 'GET',
    url: '/simaland/set_pickup_point/',
    data: params,
    success: function(r) {
      console.log(r);
    }
  });
}
$(document).ready(function(){
  if($("#" + myMapContainer).length > 0){
    $.ajax({
      type: 'GET',
      url: '/simaland/get_pickup_point/',
      success: function(r) {
        if(r.address != undefined){
          myPickupPoint = r.address;
          if($("#pickup_point_" + myPickupPoint.id).length > 0){
            $("#map_pickup_points_menu a").removeClass("selected");
            $("#pickup_point_" + myPickupPoint.id).addClass("selected");
          }
        }
      }
    });
    var params = {
      'by': 100,
    }
    $.ajax({
      type: 'GET',
      url: '/addresses/addresses/api/',
      data: params,
      success: function(r) {
        mapContainer_points = r.data;
        load_yandex_maps_script(yandex_maps_api_key, create_pickup_points_map);
      }
    });
  }
});