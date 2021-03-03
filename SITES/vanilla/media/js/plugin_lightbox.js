(function(theme,$){
  theme=theme||{};
  var instanceName='__lightbox';
  var PluginLightbox=function($el,opts){
    return this.initialize($el,opts);
  };
  PluginLightbox.defaults={
    tClose:'Close (Esc)',
    tLoading:'Loading...',
    gallery:{tPrev:'Previous (Left arrow key)',
    tNext:'Next (Right arrow key)',
    tCounter:'%curr% of %total%'},
    image:{tError:'<a href="%url%">The image</a> could not be loaded.'},
    ajax:{tError:'<a href="%url%">The content</a> could not be loaded.'},
    callbacks:{
      open:function(){
        $('html').addClass('lightbox-opened');
      },
      close:function(){
        $('html').removeClass('lightbox-opened');
      }
    }
  };
  PluginLightbox.prototype={
    initialize:function($el,opts){
      if($el.data(instanceName)){return this;}
      this.$el=$el;
      this.setData().setOptions(opts).build();
      return this;
    },
    setData:function(){
      this.$el.data(instanceName,this);
      return this;
    },
    setOptions:function(opts){
      this.options=$.extend(true,{},PluginLightbox.defaults,opts,{wrapper:this.$el});
      return this;
    },
    build:function(){
      if(!($.isFunction($.fn.magnificPopup))){return this;}
      this.options.wrapper.magnificPopup(this.options);
      return this;
    }
  };
  $.extend(theme,{PluginLightbox:PluginLightbox});
  $.fn.themePluginLightbox=function(opts){
    return this.map(function(){
      var $this=$(this);
      if($this.data(instanceName)){
        return $this.data(instanceName);
      }else{
        return new PluginLightbox($this,opts);
      }
    });
  }
}).apply(this,[window.theme,jQuery]);
(function($){
  'use strict';
  if($.isFunction($.fn['themePluginLightbox'])&&($('[data-plugin-lightbox]').length||$('.lightbox').length)){
    theme.fn.execOnceTroughEvent('[data-plugin-lightbox]:not(.manual), .lightbox:not(.manual)','mouseover.trigger.lightbox',function(){
      var $this=$(this),opts;
      var pluginOptions=theme.fn.getOptions($this.data('plugin-options'));
      if(pluginOptions)
        opts=pluginOptions;
      $this.themePluginLightbox(opts);
    });
  }
}).apply(this,[jQuery]);