/**=========================================================
 * Module: classy-loader.js
 * Enable use of classyloader directly from data attributes
 =========================================================*/

(function($, window, document){
  'use strict';

  var Selector        = '[data-toggle="classyloader"]',
      $scroller       = $(window),
      inViewFlagClass = 'js-is-in-view'; // a classname to detect when a chart has been triggered after scroll

  $(Selector).each(function (e) {

      var $element = $(this),
          options  = $element.data();

      // At lease we need a data-percentage attribute
      if(options) {
        if( options.triggerInView ) {

          $scroller.scroll(function() {
            var offset = 0;
            if( ! $element.hasClass(inViewFlagClass) &&
                $.Utils.isInView($element, {topoffset: offset}) ) {
              $element.ClassyLoader(options).addClass(inViewFlagClass);
            }
          });

        }
        else
          $element.ClassyLoader(options);
      }

  });

}(jQuery, window, document));

/**=========================================================
 * Module: clear-storage.js
 * Removes a key from the browser storage via element click
 =========================================================*/

(function($, window, document){
  'use strict';

  if( !store || !store.enabled ) return;

  var Selector = '[data-toggle="reset"]';

  $(document).on('click', Selector, function (e) {
      e.preventDefault();
      var key = $(this).data('key');

      if(key) {
        store.remove(key);
      }
      else {
        var shouldClear = confirm("This action will restore the current app state.");
        if (shouldClear == true) {
          store.clear();
        }
      }

      // at last, reload the page
      window.location.reload();

  });

}(jQuery, window, document));

/**=========================================================
 * Module: jquery.maskedinput.js
 =========================================================*/
(function($, window, document){
  'use strict';

  var Selector = 'input.phone';

  $(Selector).each(function() {
    $(this).mask("8(999)9 999-999");
  });

}(jQuery, window, document));

/**=========================================================
 * Module: dropdown-animate.js
 * Animated transition for dropdown open state
 * Animation name placed in [data-play="animationName"]  (http://daneden.github.io/animate.css/)
 * Optionally add [data-duration=seconds]
 *
 * Requires animo.js
 =========================================================*/

(function($, window, document){
  'use strict';

  $(function() {
    var Selector = '.dropdown-toggle[data-play]',
        parent = $(Selector).parent(); /* From BS-Doc: All dropdown events are fired at the .dropdown-menu's parent element. */

    parent.on('show.bs.dropdown', function () {
      //e.preventDefault();

      var $this     = $(this),
          toggle    = $this.children('.dropdown-toggle'),
          animation = toggle.data('play'),
          duration  = toggle.data('duration') || 0.5,
          target    = $this.children('.dropdown-menu');

      if(!target || !target.length)
        $.error('No target for play-animation');
      else
        if( $.fn.animo && animation)
          target.animo( { animation: animation,  duration: duration} );

    });
  });

}(jQuery, window, document));

/**=========================================================
 * Module: filter-tag.js
 * Basic items filter
 =========================================================*/

(function($, window, document){
  'use strict';

  var selectorFilterTag   = '[data-filter-tag]',    // the trigger button
      selectorFilterGroup = '[data-filter-group]',  // items to be filtered
      itemAnimation       = 'fadeIn';               // supported by animo.js

  $(function() {

      $(selectorFilterGroup).first().closest('.row').eq(0).css('overflow','hidden');

      $(document).on('click', selectorFilterTag, function() {

        var $this = $(this),
            targetGroup = $this.data('filterTag');


        if(targetGroup) {

          var allItems     = $(selectorFilterGroup),
              visibleItems = allItems.filter(function() {
                              var group = $(this).data('filterGroup');
                              return ('all' == targetGroup || group == targetGroup);
                            });

          allItems.parent() // select the col- element
                  .hide()   // Hide them
                  //.removeClass('elementHasBeenFiltered')
                  ;
          visibleItems.parent()   // select the col- element
                      .show()     // display and run the animation
                      .animo( { animation: itemAnimation, duration: 0.5} )
                      //.addClass('elementHasBeenFiltered')
                      ;

          // active by default de current trigger
          $this.addClass('active');
          // try to active the parent when in ul.nav element
          var res = $this.parents('ul').eq(0).children('li').removeClass('active');
          if(res.length) $this.parent().addClass('active');
        }
      });

  });

}(jQuery, window, document));

/**=========================================================
 * Module: form-wizard.js
 * Handles form wizard plugin and validation
 * [data-toggle="wizard"] to activate wizard plugin
 * [data-validate-step] to enable step validation via parsley
 =========================================================*/

(function($, window, document){
  'use strict';

  if(!$.fn.bwizard) return;

  var Selector = '[data-toggle="wizard"]';

  $(Selector).each(function() {

    var wizard = $(this),
        validate = wizard.data('validateStep'); // allow to set options via data-* attributes
    if(validate) {
      wizard.bwizard({
        clickableSteps: false,
        validating: function(e, ui) {

          var $this = $(this),
              form = $this.parent(),
              group = form.find('.bwizard-activated');

          if (false === form.parsley().validate( group[0].id )) {
            e.preventDefault();
            return;
          }
        }
      });
    }
    else {
      wizard.bwizard();
    }

  });

}(jQuery, window, document));


/**=========================================================
 * Module: navbar-search.js
 * Navbar search toggler
 * To open search add a buton with [data-toggle="navbar-search"]
 * To close search add an element with [data-toggle="navbar-search-dismiss"]
 *
 * Auto dismiss on ESC key
 =========================================================*/

(function($, window, document){
  'use strict';
  $(function() {
    var openSelector    = '[data-toggle="navbar-search"]',
        dismissSelector = '[data-toggle="navbar-search-dismiss"]',
        inputSelector   = '.navbar-form input[type="text"]',
        navbarForm      = $('form.navbar-form');
    var NavSearch = {
      toggle: function() {
        navbarForm.toggleClass('open');
        var isOpen = navbarForm.hasClass('open');
        navbarForm.find('input')[isOpen ? 'focus' : 'blur']();
      },
      dismiss: function() {
        navbarForm
          .removeClass('open')      // Close control
          .find('input[type="text"]').blur() // remove focus
          //.val('')                    // Empty input
          ;
      }
    };
    $(document)
        .on('click', NavSearch.dismiss)
        .on('click', openSelector +', '+ inputSelector +', '+ dismissSelector, function (e) {
          e.stopPropagation();
        })
        .on('click', dismissSelector, NavSearch.dismiss)
        .on('click', openSelector, NavSearch.toggle)
        .keyup(function(e) {
          if (e.keyCode == 27) // ESC
            NavSearch.dismiss();
        });
  });
}(jQuery, window, document));

/**=========================================================
 * Module: notify.js
 * Create toggleable notifications that fade out automatically.
 * Based on Notify addon from UIKit (http://getuikit.com/docs/addons_notify.html)
 * [data-toggle="notify"]
 * [data-options="options in json format" ]
 =========================================================*/

(function($, window, document){
  'use strict';

  var Selector = '[data-toggle="notify"]',
      autoloadSelector = '[data-onload]',
      doc = $(document);


  $(function() {

    $(Selector).each(function(){

      var $this  = $(this),
          onload = $this.data('onload');

      if(onload !== undefined) {
        setTimeout(function(){
          notifyNow($this);
        }, 1000);
      }

      $this.on('click', function (e) {
        e.preventDefault();
        notifyNow($this);
      });

    });

  });

  function notifyNow($element) {
      var message = $element.data('message'),
          options = $element.data('options');

      if(!message)
        $.error('Notify: No message specified');
      $.notify(message, options || {});
  }


}(jQuery, window, document));


/**
 * Notify Addon definition as jQuery plugin
 * Adapted version to work with Bootstrap classes
 * More information http://getuikit.com/docs/addons_notify.html
 */

(function($, window, document){

    var containers = {},
        messages   = {},

        notify     =  function(options){

            if ($.type(options) == 'string') {
                options = { message: options };
            }

            if (arguments[1]) {
                options = $.extend(options, $.type(arguments[1]) == 'string' ? {status:arguments[1]} : arguments[1]);
            }

            return (new Message(options)).show();
        },
        closeAll  = function(group, instantly){
            if(group) {
                for(var id in messages) { if(group===messages[id].group) messages[id].close(instantly); }
            } else {
                for(var id in messages) { messages[id].close(instantly); }
            }
        };

    var Message = function(options){

        var $this = this;

        this.options = $.extend({}, Message.defaults, options);

        this.uuid    = "ID"+(new Date().getTime())+"RAND"+(Math.ceil(Math.random() * 100000));
        this.element = $([
            // @geedmo: alert-dismissable enables bs close icon
            '<div class="uk-notify-message alert-dismissable">',
                '<a class="close">&times;</a>',
                '<div>'+this.options.message+'</div>',
            '</div>'

        ].join('')).data("notifyMessage", this);

        // status
        if (this.options.status) {
            this.element.addClass('alert alert-'+this.options.status);
            this.currentstatus = this.options.status;
        }

        this.group = this.options.group;

        messages[this.uuid] = this;

        if(!containers[this.options.pos]) {
            containers[this.options.pos] = $('<div class="uk-notify uk-notify-'+this.options.pos+'"></div>').appendTo('body').on("click", ".uk-notify-message", function(){
                $(this).data("notifyMessage").close();
            });
        }
    };


    $.extend(Message.prototype, {

        uuid: false,
        element: false,
        timout: false,
        currentstatus: "",
        group: false,

        show: function() {

            if (this.element.is(":visible")) return;

            var $this = this;

            containers[this.options.pos].show().prepend(this.element);

            var marginbottom = parseInt(this.element.css("margin-bottom"), 10);

            this.element.css({"opacity":0, "margin-top": -1*this.element.outerHeight(), "margin-bottom":0}).animate({"opacity":1, "margin-top": 0, "margin-bottom":marginbottom}, function(){

                if ($this.options.timeout) {

                    var closefn = function(){ $this.close(); };

                    $this.timeout = setTimeout(closefn, $this.options.timeout);

                    $this.element.hover(
                        function() { clearTimeout($this.timeout); },
                        function() { $this.timeout = setTimeout(closefn, $this.options.timeout);  }
                    );
                }

            });

            return this;
        },

        close: function(instantly) {

            var $this    = this,
                finalize = function(){
                    $this.element.remove();

                    if(!containers[$this.options.pos].children().length) {
                        containers[$this.options.pos].hide();
                    }

                    delete messages[$this.uuid];
                };

            if(this.timeout) clearTimeout(this.timeout);

            if(instantly) {
                finalize();
            } else {
                this.element.animate({"opacity":0, "margin-top": -1* this.element.outerHeight(), "margin-bottom":0}, function(){
                    finalize();
                });
            }
        },

        content: function(html){

            var container = this.element.find(">div");

            if(!html) {
                return container.html();
            }

            container.html(html);

            return this;
        },

        status: function(status) {

            if(!status) {
                return this.currentstatus;
            }

            this.element.removeClass('alert alert-'+this.currentstatus).addClass('alert alert-'+status);

            this.currentstatus = status;

            return this;
        }
    });

    Message.defaults = {
        message: "",
        status: "normal",
        timeout: 5000,
        group: null,
        pos: 'top-center'
    };


    $["notify"]          = notify;
    $["notify"].message  = Message;
    $["notify"].closeAll = closeAll;

    return notify;

}(jQuery, window, document));

/**=========================================================
 * Module: panel-perform.js
 * Dismiss panels
 * [data-perform="panel-dismiss"]
 *
 * Requires animo.js
 =========================================================*/
(function($, window, document){
  'use strict';
  var panelSelector = '[data-perform="panel-dismiss"]',
      removeEvent   = 'panel-remove',
      removedEvent  = 'panel-removed';

  $(document).on('click', panelSelector, function () {
    // find the first parent panel
    var parent = $(this).closest('.panel');

    if($.support.animation) {
      parent.animo({animation: 'bounceOut'}, removeElement);
    }
    else removeElement();

    function removeElement() {
      // Trigger the event and finally remove the element
      $.when(parent.trigger(removeEvent, [parent]))
       .done(destroyPanel);
    }

    function destroyPanel() {
      var col = parent.parent();
      parent.remove();
      // remove the parent if it is a row and is empty and not a sortable (portlet)
      col
        .trigger(removedEvent) // An event to catch when the panel has been removed from DOM
        .filter(function() {
        var el = $(this);
        return (el.is('[class*="col-"]:not(.sortable)') && el.children('*').length === 0);
      }).remove();

    }

  });

}(jQuery, window, document));


/**
 * Collapse panels
 * [data-perform="panel-collapse"]
 *
 * Also uses browser storage to keep track
 * of panels collapsed state
 */
(function($, window, document) {
  'use strict';
  var panelSelector = '[data-perform="panel-collapse"]',
      storageKeyName = 'panelState';

  // Prepare the panel to be collapsable and its events
  $(panelSelector).each(function() {
    // find the first parent panel
    var $this        = $(this),
        parent       = $this.closest('.panel'),
        wrapper      = parent.find('.panel-wrapper'),
        collapseOpts = {toggle: false},
        iconElement  = $this.children('em'),
        panelId      = parent.attr('id');
    // if wrapper not added, add it
    // we need a wrapper to avoid jumping due to the paddings
    if( ! wrapper.length) {
      wrapper =
        parent.children('.panel-heading').nextAll() //find('.panel-body, .panel-footer')
          .wrapAll('<div/>')
          .parent()
          .addClass('panel-wrapper');
      collapseOpts = {};
    }

    // Init collapse and bind events to switch icons
    wrapper
      .collapse(collapseOpts)
      .on('hide.bs.collapse', function() {
        setIconHide( iconElement );
        savePanelState( panelId, 'hide' );
      })
      .on('show.bs.collapse', function() {
        setIconShow( iconElement );
        savePanelState( panelId, 'show' );
      });

    // Load the saved state if exists
    var currentState = loadPanelState( panelId );
    if(currentState) {
      setTimeout(function() { wrapper.collapse( currentState ); }, 0);
      savePanelState( panelId, currentState );
    }

  });

  // finally catch clicks to toggle panel collapse
  $(document).on('click', panelSelector, function () {
    var parent = $(this).closest('.panel');
    var wrapper = parent.find('.panel-wrapper');

    wrapper.collapse('toggle');

  });

  /////////////////////////////////////////////
  // Common use functions for panel collapse //
  /////////////////////////////////////////////
  function setIconShow(iconEl) {
    iconEl.removeClass('fa-plus').addClass('fa-minus');
  }

  function setIconHide(iconEl) {
    iconEl.removeClass('fa-minus').addClass('fa-plus');
  }

  function savePanelState(id, state) {
    if(!id || !store || !store.enabled) return false;
    var data = store.get(storageKeyName);
    if(!data) { data = {}; }
    data[id] = state;
    store.set(storageKeyName, data);
  }

  function loadPanelState(id) {
    if(!id || !store || !store.enabled) return false;
    var data = store.get(storageKeyName);
    if(data) {
      return data[id] || false;
    }
  }


}(jQuery, window, document));


/**
 * Refresh panels
 * [data-perform="panel-refresh"]
 * [data-spinner="standard"]
 */
(function($, window, document){
  'use strict';
  var panelSelector  = '[data-perform="panel-refresh"]',
      refreshEvent   = 'panel-refresh',
      csspinnerClass = 'csspinner',
      defaultSpinner = 'standard';

  // method to clear the spinner when done
  function removeSpinner(){
    this.removeClass(csspinnerClass);
  }

  // catch clicks to toggle panel refresh
  $(document).on('click', panelSelector, function () {
      var $this   = $(this),
          panel   = $this.parents('.panel').eq(0),
          spinner = $this.data('spinner') || defaultSpinner
          ;

      // start showing the spinner
      panel.addClass(csspinnerClass + ' ' + spinner);

      // attach as public method
      panel.removeSpinner = removeSpinner;

      // Trigger the event and send the panel object
      $this.trigger(refreshEvent, [panel]);

  });


  /**
   * This function is only to show a demonstration
   * of how to use the panel refresh system via
   * custom event.
   * IMPORTANT: see how to remove the spinner.
   */

  $('.panel.panel-demo').on('panel-refresh', function(e, panel){

    // perform any action when a .panel triggers a the refresh event
    setTimeout(function(){

      // when the action is done, just remove the spinner class
      panel.removeSpinner();

    }, 3000);

  });

}(jQuery, window, document));

/**=========================================================
 * Module: play-animation.js
 * Provides a simple way to run animation with a trigger
 * Targeted elements must have
 *   [data-toggle="play-animation"]
 *   [data-target="Target element affected by the animation"]
 *   [data-play="Animation name (http://daneden.github.io/animate.css/)"]
 *
 * Requires animo.js
 =========================================================*/

(function($, window, document){
  'use strict';

  var Selector = '[data-toggle="play-animation"]';

  $(function() {
    var $scroller = $(window).add('body, .wrapper');

    // Parse animations params and attach trigger to scroll
    $(Selector).each(function() {
      var $this     = $(this),
          offset    = $this.data('offset'),
          delay     = $this.data('delay')     || 100, // milliseconds
          animation = $this.data('play')      || 'bounce';

      if(typeof offset !== 'undefined') {
        // test if the element starts visible
        testAnimation($this);
        // test on scroll
        $scroller.scroll(function(){
          testAnimation($this);
        });

      }

      // Test an element visibilty and trigger the given animation
      function testAnimation(element) {
          if ( !element.hasClass('anim-running') &&
              $.Utils.isInView(element, {topoffset: offset})) {
          element
            .addClass('anim-running');

          setTimeout(function() {
            element
              .addClass('anim-done')
              .animo( { animation: animation, duration: 0.7} );
          }, delay);

        }
      }

    });

    // Run click triggered animations
    $(document).on('click', Selector, function() {

      var $this     = $(this),
          targetSel = $this.data('target'),
          animation = $this.data('play') || 'bounce',
          target    = $(targetSel);

      if(target && target) {
        target.animo( { animation: animation } );
      }
    });

  });

}(jQuery, window, document));

/**=========================================================
 * Module: portlet.js
 * Drag and drop any panel to change its position
 * The Selector should could be applied to any object that contains
 * panel, so .col-* element are ideal.
 =========================================================*/

(function($, window, document){
  'use strict';

  // Component is required
  if(!$.fn.sortable) return;

  var Selector = '[data-toggle="portlet"]',
      storageKeyName = 'portletState';

  $(function(){

    $( Selector ).sortable({
      connectWith:          Selector,
      items:                'div.panel',
      handle:               '.portlet-handler',
      opacity:              0.7,
      placeholder:          'portlet box-placeholder',
      cancel:               '.portlet-cancel',
      forcePlaceholderSize: true,
      iframeFix:            false,
      tolerance:            'pointer',
      helper:               'original',
      revert:               200,
      forceHelperSize:      true,
      start:                saveListSize,
      update:               savePortletOrder,
      create:               loadPortletOrder
    })
    // optionally disables mouse selection
    //.disableSelection()
    ;

  });

  function savePortletOrder(event, ui) {
    var data = store.get(storageKeyName);
    if(!data) { data = {}; }

    data[this.id] = $(this).sortable('toArray');

    if(data) {
      store.set(storageKeyName, data);
    }
    // save portlet size to avoid jumps
    saveListSize.apply(this);
  }

  function loadPortletOrder() {
    var data = store.get(storageKeyName);

    if(data) {
      var porletId = this.id,
          panels   = data[porletId];

      if(panels) {
        var portlet = $('#'+porletId);
        $.each(panels, function(index, value) {
           $('#'+value).appendTo(portlet);
        });
      }

    }

    // save portlet size to avoid jumps
    saveListSize.apply(this);
  }

  // Keeps a consistent size in all portlet lists
  function saveListSize() {
    var $this = $(this);
    $this.css('min-height', $this.height());
  }

  /*function resetListSize() {
    $(this).css('min-height', "");
  }*/

}(jQuery, window, document));


/**=========================================================
 * Module: sidebar-menu.js
 * Provides a simple way to implement bootstrap collapse plugin using a target 
 * next to the current element (sibling)
 * Targeted elements must have [data-toggle="collapse-next"]
 =========================================================*/
(function($, window, document){
  'use strict';

  var collapseSelector = '[data-toggle="collapse-next"]',
      colllapsibles    = $('.sidebar .collapse').collapse({toggle: false}),
      toggledClass     = 'aside-collapsed',
      $body            = $('body'),
      phone_mq         = 768; // media querie

  $(function() {

    $(document)
      .on('click', collapseSelector, function (e) {
          e.preventDefault();
          if ($(window).width() > phone_mq &&
              $body.hasClass(toggledClass)) return;

          // Try to close all of the collapse areas first
          colllapsibles.collapse('hide');
          // ...then open just the one we want
          var $target = $(this).siblings('ul');
          $target.collapse('show');

      })
      // Submenu when aside is toggled
      .on('click', '.sidebar > .nav > li', function() {

        if ($body.hasClass(toggledClass) &&
          $(window).width() > phone_mq) {

            $('.sidebar > .nav > li')
              .not(this)
              .removeClass('open')
              .end()
              .filter(this)
              .toggleClass('open');
        }

      });

  });


}(jQuery, window, document));

/**=========================================================
 * Module: table-checkall.js
 * Tables check all checkbox
 =========================================================*/

(function($, window, document){
  'use strict';

  var Selector = 'th.check-all';

  $(Selector).on('change', function() {
    var $this = $(this),
        index= $this.index() + 1,
        checkbox = $this.find('input[type="checkbox"]'),
        table = $this.parents('table');
    // Make sure to affect only the correct checkbox column
    table.find('tbody > tr > td:nth-child('+index+') input[type="checkbox"]')
      .prop('checked', checkbox[0].checked);
  });
}(jQuery, window, document));

/**=========================================================
 * Module: toggle-state.js
 * Toggle a classname from the BODY. Useful to change a state that
 * affects globally the entire layout or more than one item
 * Targeted elements must have [data-toggle="CLASS-NAME-TO-TOGGLE"]
 * Optionally save and restore state [data-persists="true"]
 =========================================================*/

(function($, window, document){
  'use strict';

  var SelectorToggle  = '[data-toggle-state]',
      $body           = $('body'),
      storageKeyName  = 'toggleState';


  $(document)
    .ready(function() {
      restoreState($body);
    })
    .on('click', SelectorToggle, function (e) {
      e.preventDefault();
      var classname = $(this).data('toggleState'),
          persists  = $(this).data('persists');

      if(classname) {
        if( $body.hasClass(classname) ) {
          $body.removeClass(classname);
          if(persists) removeState(classname);
        }
        else {
          $body.addClass(classname);
          if(persists) addState(classname);
        }

      }

  });

  // Add a state to the browser storage to be restored later
  function addState(classname){
    var data = store.get(storageKeyName);

    if(!data)  {
      data = classname;
    }
    else {
      data = WordChecker.addWord(data, classname);
    }

    store.set(storageKeyName, data);
  }

  // Remove a state from the browser storage
  function removeState(classname){
    var data = store.get(storageKeyName);
    // nothing to remove
    if(!data) return;

    data = WordChecker.removeWord(data, classname);

    store.set(storageKeyName, data);
  }

  // Load the state string and restore the classlist
  function restoreState($elem) {
    var data = store.get(storageKeyName);
    // nothing to restore
    if(!data) return;
    $elem.addClass(data);
  }


  //////////////////////////////////////////////////
  // Helper object to check for words in a phrase //
  //////////////////////////////////////////////////
  var WordChecker = {
    hasWord: function (phrase, word) {
      return new RegExp('(^|\\s)' + word + '(\\s|$)').test(phrase);
    },
    addWord: function (phrase, word) {
      if (!this.hasWord(phrase, word)) {
        return (phrase + (phrase ? ' ' : '') + word);
      }
    },
    removeWord: function (phrase, word) {
      if (this.hasWord(phrase, word)) {
        return phrase.replace(new RegExp('(^|\\s)*' + word + '(\\s|$)*', 'g'), '');
      }
    }
  };


}(jQuery, window, document));

/**=========================================================
 * Module: tooltips.js
 * Initialize Bootstrap tooltip with auto placement
 =========================================================*/

(function($, window, document){
  'use strict';

  $(function(){

    $('[data-toggle="tooltip"]').tooltip({
      container: 'body',
      placement: function (context, source) {
                    //return (predictTooltipTop(source) < 0) ?  "bottom": "top";
                    var pos = 'top';
                    if(predictTooltipTop(source) < 0)
                      pos = 'bottom';
                    if(predictTooltipLeft(source) < 0)
                      pos = 'right';
                    return pos;
                }
    });

  });

  // Predicts tooltip top position
  // based on the trigger element
  function predictTooltipTop(el) {
    var top = el.offsetTop;
    var height = 40; // asumes ~40px tooltip height

    while(el.offsetParent) {
      el = el.offsetParent;
      top += el.offsetTop;
    }
    return (top - height) - (window.pageYOffset);
  }

  // Predicts tooltip top position
  // based on the trigger element
  function predictTooltipLeft(el) {
    var left = el.offsetLeft;
    var width = el.offsetWidth;

    while(el.offsetParent) {
      el = el.offsetParent;
      left += el.offsetLeft;
    }
    return (left - width) - (window.pageXOffset);
  }

}(jQuery, window, document));

/**=========================================================
 * Module: upload.js
 * Allow users to upload files through a file input form element or a placeholder area.
 * Based on addon from UIKit (http://getuikit.com/docs/addons_upload.html)
 *
 * Adapted version to work with Bootstrap classes
 =========================================================*/

(function($, window, document){
    'use strict';
    var UploadSelect = function(element, options) {
        var $this    = this,
            $element = $(element),
            options  = $.extend({}, xhrupload.defaults, UploadSelect.defaults, options);

        if ($element.data("uploadSelect")) return;
        this.element = $element.on("change", function() {
            xhrupload($this.element[0].files, options);
        });

        $element.data("uploadSelect", this);
    };

    UploadSelect.defaults = {};

    var UploadDrop = function(element, options) {
        var $this      = this,
            $element   = $(element),
            options    = $.extend({}, xhrupload.defaults, UploadDrop.defaults, options),
            hasdragCls = false;

        if ($element.data("uploadDrop")) return;
        $element.on("drop", function(e){
            if (e.dataTransfer && e.dataTransfer.files) {
                e.stopPropagation();
                e.preventDefault();
                $element.removeClass(options.dragoverClass);
                xhrupload(e.dataTransfer.files, options);
            }
        }).on("dragenter", function(e){
            e.stopPropagation();
            e.preventDefault();
        }).on("dragover", function(e){
            e.stopPropagation();
            e.preventDefault();

            if (!hasdragCls) {
                $element.addClass(options.dragoverClass);
                hasdragCls = true;
            }
        }).on("dragleave", function(e){
            e.stopPropagation();
            e.preventDefault();
            $element.removeClass(options.dragoverClass);
            hasdragCls = false;
        });

        $element.data("uploadDrop", this);
    };

    UploadDrop.defaults = {
        'dragoverClass': 'dragover'
    };

    $.upload = { "select" : UploadSelect, "drop" : UploadDrop };
    $.support.ajaxupload = (function() {
        function supportFileAPI() {
            var fi = document.createElement('INPUT'); fi.type = 'file'; return 'files' in fi;
        }
        function supportAjaxUploadProgressEvents() {
            var xhr = new XMLHttpRequest(); return !! (xhr && ('upload' in xhr) && ('onprogress' in xhr.upload));
        }
        function supportFormData() {
            return !! window.FormData;
        }
        return supportFileAPI() && supportAjaxUploadProgressEvents() && supportFormData();
    })();

    if ($.support.ajaxupload){
        $.event.props.push("dataTransfer");
    }

    function xhrupload(files, settings) {
        if (!$.support.ajaxupload){
            return this;
        }
        settings = $.extend({}, xhrupload.defaults, settings);
        if (!files.length){
            return;
        }

        if (settings.allow !== '*.*') {
            for(var i=0,file;file=files[i];i++) {
                if(!matchName(settings.allow, file.name)) {
                    if(typeof(settings.notallowed) == 'string') {
                       alert(settings.notallowed);
                    } else {
                       settings.notallowed(file, settings);
                    }
                    return;
                }
            }
        }
        var complete = settings.complete;
        if (settings.single){
            var count    = files.length,
                uploaded = 0;
                settings.complete = function(response, xhr){
                    uploaded = uploaded+1;
                    complete(response, xhr);
                    if (uploaded<count){
                        upload([files[uploaded]], settings);
                    } else {
                        settings.allcomplete(response, xhr);
                    }
                };
                upload([files[0]], settings);
        } else {
            settings.complete = function(response, xhr){
                complete(response, xhr);
                settings.allcomplete(response, xhr);
            };
            upload(files, settings);
        }

        function upload(files, settings){
            // upload all at once
            var formData = new FormData(), xhr = new XMLHttpRequest();
            if (settings.before(settings, files)===false) return;
            for (var i = 0, f; f = files[i]; i++) { formData.append(settings.param, f); }
            for (var p in settings.params) { formData.append(p, settings.params[p]); }
            // Add any event handlers here...
            xhr.upload.addEventListener("progress", function(e){
                var percent = (e.loaded / e.total)*100;
                settings.progress(percent, e);
            }, false);

            xhr.addEventListener("loadstart", function(e){ settings.loadstart(e); }, false);
            xhr.addEventListener("load",      function(e){ settings.load(e);      }, false);
            xhr.addEventListener("loadend",   function(e){ settings.loadend(e);   }, false);
            xhr.addEventListener("error",     function(e){ settings.error(e);     }, false);
            xhr.addEventListener("abort",     function(e){ settings.abort(e);     }, false);

            xhr.open(settings.method, settings.action, true);
            xhr.onreadystatechange = function() {
                settings.readystatechange(xhr);
                if (xhr.readyState==4){
                    var response = xhr.responseText;
                    if (settings.type=="json") {
                        try {
                            response = $.parseJSON(response);
                        } catch(e) {
                            response = false;
                        }
                    }
                    settings.complete(response, xhr);
                }
            };
            xhr.send(formData);
        }
    }

    xhrupload.defaults = {
        'action': '',
        'single': true,
        'method': 'POST',
        'param' : 'files[]',
        'params': {},
        'allow' : '*.*',
        'type'  : 'text',

        // events
        'before'          : function(o){},
        'loadstart'       : function(){},
        'load'            : function(){},
        'loadend'         : function(){},
        'error'           : function(){},
        'abort'           : function(){},
        'progress'        : function(){},
        'complete'        : function(){},
        'allcomplete'     : function(){},
        'readystatechange': function(){},
        'notallowed'      : function(file, settings){ alert('Only the following file types are allowed: '+settings.allow); }
    };

    function matchName(pattern, path) {
        var parsedPattern = '^' + pattern.replace(/\//g, '\\/').
            replace(/\*\*/g, '(\\/[^\\/]+)*').
            replace(/\*/g, '[^\\/]+').
            replace(/((?!\\))\?/g, '$1.') + '$';
        parsedPattern = '^' + parsedPattern + '$';
        return (path.match(new RegExp(parsedPattern)) !== null);
    }
    $.xhrupload = xhrupload;
    return xhrupload;
}(jQuery, window, document));

/**=========================================================
 * Module: utils.js
 * jQuery Utility functions library
 * adapted from the core of UIKit
 =========================================================*/

(function($, window, doc){
    'use strict';
    var $html = $("html"), $win = $(window);

    $.support.transition = (function() {

        var transitionEnd = (function() {

            var element = doc.body || doc.documentElement,
                transEndEventNames = {
                    WebkitTransition: 'webkitTransitionEnd',
                    MozTransition: 'transitionend',
                    OTransition: 'oTransitionEnd otransitionend',
                    transition: 'transitionend'
                }, name;

            for (name in transEndEventNames) {
                if (element.style[name] !== undefined) return transEndEventNames[name];
            }
        }());

        return transitionEnd && { end: transitionEnd };
    })();

    $.support.animation = (function() {

        var animationEnd = (function() {

            var element = doc.body || doc.documentElement,
                animEndEventNames = {
                    WebkitAnimation: 'webkitAnimationEnd',
                    MozAnimation: 'animationend',
                    OAnimation: 'oAnimationEnd oanimationend',
                    animation: 'animationend'
                }, name;

            for (name in animEndEventNames) {
                if (element.style[name] !== undefined) return animEndEventNames[name];
            }
        }());

        return animationEnd && { end: animationEnd };
    })();

    $.support.requestAnimationFrame = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.msRequestAnimationFrame || window.oRequestAnimationFrame || function(callback){ window.setTimeout(callback, 1000/60); };
    $.support.touch                 = (
        ('ontouchstart' in window && navigator.userAgent.toLowerCase().match(/mobile|tablet/)) ||
        (window.DocumentTouch && document instanceof window.DocumentTouch)  ||
        (window.navigator['msPointerEnabled'] && window.navigator['msMaxTouchPoints'] > 0) || //IE 10
        (window.navigator['pointerEnabled'] && window.navigator['maxTouchPoints'] > 0) || //IE >=11
        false
    );
    $.support.mutationobserver      = (window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver || null);

    $.Utils = {};

    $.Utils.debounce = function(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    };

    $.Utils.removeCssRules = function(selectorRegEx) {
        var idx, idxs, stylesheet, _i, _j, _k, _len, _len1, _len2, _ref;

        if(!selectorRegEx) return;

        setTimeout(function(){
            try {
              _ref = document.styleSheets;
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                stylesheet = _ref[_i];
                idxs = [];
                stylesheet.cssRules = stylesheet.cssRules;
                for (idx = _j = 0, _len1 = stylesheet.cssRules.length; _j < _len1; idx = ++_j) {
                  if (stylesheet.cssRules[idx].type === CSSRule.STYLE_RULE && selectorRegEx.test(stylesheet.cssRules[idx].selectorText)) {
                    idxs.unshift(idx);
                  }
                }
                for (_k = 0, _len2 = idxs.length; _k < _len2; _k++) {
                  stylesheet.deleteRule(idxs[_k]);
                }
              }
            } catch (_error) {}
        }, 0);
    };

    $.Utils.isInView = function(element, options) {

        var $element = $(element);

        if (!$element.is(':visible')) {
            return false;
        }

        var window_left = $win.scrollLeft(),
            window_top  = $win.scrollTop(),
            offset      = $element.offset(),
            left        = offset.left,
            top         = offset.top;

        options = $.extend({topoffset:0, leftoffset:0}, options);

        if (top + $element.height() >= window_top && top - options.topoffset <= window_top + $win.height() &&
            left + $element.width() >= window_left && left - options.leftoffset <= window_left + $win.width()) {
          return true;
        } else {
          return false;
        }
    };

    $.Utils.options = function(string) {

        if ($.isPlainObject(string)) return string;

        var start = (string ? string.indexOf("{") : -1), options = {};

        if (start != -1) {
            try {
                options = (new Function("", "var json = " + string.substr(start) + "; return JSON.parse(JSON.stringify(json));"))();
            } catch (e) {}
        }

        return options;
    };

    $.Utils.events       = {};
    $.Utils.events.click = $.support.touch ? 'tap' : 'click';

    $.langdirection = $html.attr("dir") == "rtl" ? "right" : "left";

    $(function(){

        // Check for dom modifications
        if(!$.support.mutationobserver) return;

        // Install an observer for custom needs of dom changes
        var observer = new $.support.mutationobserver($.Utils.debounce(function(mutations) {
            $(doc).trigger("domready");
        }, 300));

        // pass in the target node, as well as the observer options
        observer.observe(document.body, { childList: true, subtree: true });

    });

    // add touch identifier class
    $html.addClass($.support.touch ? "touch" : "no-touch");

}(jQuery, window, document));

/**
 * Provides a start point to run plugins and other scripts
 */
(function($, window, document){
  'use strict';

  if (typeof $ === 'undefined') { throw new Error('This application\'s JavaScript requires jQuery'); }

  $(window).load(function() {
    $('.scroll-content').slimScroll({
        height: '250px'
    });
    adjustLayout();
  }).resize(adjustLayout);


  $(function() {

    // Init Fast click for mobiles
    FastClick.attach(document.body);

    // inhibits null links
    $('a[href="#"]').each(function(){
      this.href = 'javascript:void(0);';
    });

    // popover init
    $('[data-toggle=popover]').popover();

    // Bootstrap slider
    $('.slider').slider();

    // Chosen
    //$('.chosen-select').chosen();

    // Filestyle
    $('.filestyle').filestyle();

    // Masked inputs initialization
    $.fn.inputmask && $('[data-toggle="masked"]').inputmask();

  });

  // keeps the wrapper covering always the entire body
  // necessary when main content doesn't fill the viewport
  function adjustLayout() {
    $('.wrapper > section').css('min-height', $(window).height());
  }

  // ----------------
  // Удаление объекта
  // ----------------
  $('#ajax_drop_obj_button').click(function(){
    var pk = $('#ajax_drop_obj_id').html();
    var row_index = parseInt($('#ajax_drop_obj_ind').html());
    var $form = $('#current_drop_form');
    var msg = 'Произошла ошибка, сообщите администратору';
    var status = 'danger';

    $.ajax({
      type: $form.attr('method'),
      url: $form.attr('action'),
      data: $form.serialize()
    }).done(function(r) {
      if(r.error){
        msg = r.error;
      }else if(r.success){
        msg =  r.success;
        status = 'success';
        // Удаляем строчку из таблицы
        main_table.deleteRow(row_index);
      }
      $.notify({
        message: msg,
      },{
        status: status,
      });
    }).fail(function() {
      $.notify({
        message: msg,
      },{
        status: status,
      });
    });
  });

  autosize(document.querySelectorAll("textarea"));

  $(".bg-color-for-img").keyup(function(){
    var value = $(this).val();
    if(value.length == 4 || value.length == 7){
      $(this).parent().parent().find('.img_block').css('background-color', value);
    }
  });

  $(document).on("keypress", function(e) {
    if(e.which == 13) {
      if($("#ajax_drop_obj").hasClass("in")){
        $("#ajax_drop_obj").modal('hide');
        $("#ajax_drop_obj_button").click();
      }
    }
  });

}(jQuery, window, document));

// для аякс форм: {csrfmiddlewaretoken: getCookie('csrftoken')}
function getCookie(c_name) {
  if(document.cookie.length > 0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if(c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";", c_start);
      if(c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start,c_end));
    }
  }
  return "";
}

function set_ajax_form(form_id, callback_success, callback_fail, is_file){
  // Настраиваем форму на аякс отправку
  // :param form_id: ид формы #current_edit_form
  // :param callback_success: функция после успешного получения данных
  // :param callback_fail: функция после НЕуспешного получения данных
  // :param is_file: отправка файла через форму
  if(typeof(parsley) === "undefined"){
    console.log('[ERROR]: parsley not imported');
    console.log('/static/admin/js/parsley.min.js not found');
    return;
  }
  $(form_id).parsley();
  $(form_id).submit(function(e) {
    var $form = $(this);
    var msg = 'Произошла ошибка, обновите страничку';
    var status = 'danger'; // success, warning, info, danger
    var params = {
      type: $form.attr('method'),
      url: $form.attr('action'),
      data: $form.serialize(),
    };
    if(is_file){
      // Отправка файла через аякс-форму
      var formData = new FormData($form[0]);
      params.processData = false;
      params.contentType = false;
      params.data = formData;
    }
    $.ajax(params).done(function(r) {
      if(r.error){
        msg = r.error;
      } else if(r.success) {
        msg =  r.success;
        status = 'success';
      }
      $.notify({
        message: msg,
      },{
        status: status,
      });
      if(callback_success !== undefined){
        callback_success(r);
      }
    }).fail(function() {
      $.notify({
        message: msg,
      },{
        status: status,
      });
      if(callback_fail !== undefined){
        callback_fail(r);
      }
    });
    //отмена действия по умолчанию для кнопки submit
    e.preventDefault();
  });
}
function set_ajax_form_save_xlsx(button_id, excel_table, callback_success, callback_fail, operation){
  // Настраиваем форму на аякс отправку данных, полученных с xlsx файла
  // Кнопке button_id даем data-save-action и туда засылаем xlsx данные
  // :param button_id: ид кнопки сохранения #save_excel_table
  // :param excel_table: таблица с данными эксельки
  // :param callback_success: функция после успешного получения данных
  // :param callback_fail: функция после НЕуспешного получения данных
  // :param action: действие (по умолчанию save)
  if(operation === undefined){
    operation = 'save';
  }
  $(button_id).click(function(){
    var msg = "Произошла ошибка, обновите страничку";
    var status = "danger"; // success, warning, info, danger
    var rows = excel_table.getData();
    var action = $(button_id).attr('data-save-action');
    if(rows.length < 1 || !action){
      console.log("[ERROR]: empty data or action for save from xlsx");
      return;
    }
    $.ajax({
      type: "POST",
      url: action,
      data: {
        csrfmiddlewaretoken: getCookie('csrftoken'),
        action: operation,
        count: rows.length,
        data: rows,
      },
    }).done(function(r) {
      if(r.error){
        msg = r.error;
      } else if(r.success) {
        msg =  r.success;
        status = 'success';
      }
      $.notify({
        message: msg,
      },{
        status: status,
      });
      if(callback_success !== undefined){
        callback_success(r);
      }
    }).fail(function() {
      $.notify({
        message: msg,
      },{
        status: status,
      });
      if(callback_fail !== undefined){
        callback_fail(r);
      }
    });
  });
}