(function($) {

    $.organicTabs = function(el, options) {
    
        var base = this;
        base.$el = $(el);
        base.$nav = base.$el.find(".tea14-settings-nav");
                
        base.init = function() {
        
            base.options = $.extend({},$.organicTabs.defaultOptions, options);
            
            // Accessible hiding fix
            base.$el.find('> div > ul').filter(function(index) {
				return index > 0;
			}).hide();
            
            base.$nav.delegate("li > a", "click", function() {
            
                // Figure out current list via CSS class
                var curList = base.$el.find("a.tea14-settings-nav-current").attr("href").substring(1),
                
                // List moving to
                    $newList = $(this),
                    
                // Figure out ID of new list
                    listID = $newList.attr("href").substring(1);
                
                if ((listID != curList) && ( base.$el.find(":animated").length == 0)) {
                                            
                    // Fade out current list
                    base.$el.find("#"+curList).fadeOut(base.options.speed, function() {
                        
                        // Fade in new list on callback
                        base.$el.find("#"+listID).fadeIn(base.options.speed);
                        
                        // Remove highlighting - Add to just-clicked tab
                        base.$el.find(".tea14-settings-nav li a").removeClass("tea14-settings-nav-current");
                        $newList.addClass("tea14-settings-nav-current");
                            
                    });
                    
                }   
                
                // Don't behave like a regular link
                // Stop propegation and bubbling
                return false;
            });
            
        };
        base.init();
    };
    
    $.organicTabs.defaultOptions = {
        "speed": 300
    };
    
    $.fn.organicTabs = function(options) {
        return this.each(function() {
            (new $.organicTabs(this, options));
        });
    };
    
})(jQuery);