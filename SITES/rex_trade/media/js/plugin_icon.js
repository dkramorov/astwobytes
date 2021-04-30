// SVG Animation
// <script src="/media/js/vivus.min.js"></script>
(function(theme,$){
  'use strict';
  theme=theme||{};
  var instanceName='__icon';
  var PluginIcon=function($el,opts){
    return this.initialize($el,opts);
  };
  PluginIcon.defaults={
    color:'#2388ED',
    animated:false,
    delay:300,
    onlySVG:false
  };
  PluginIcon.prototype={
    initialize:function($el,opts){
      if($el.data(instanceName)){return this;}
      this.$el=$el;this.setData().setOptions(opts).build();
      return this;
    },
    setData:function(){
      this.$el.data(instanceName,this);
      return this;
    },
    setOptions:function(opts){
      this.options=$.extend(true,{},PluginIcon.defaults,opts,{wrapper:this.$el});
      return this;
    },
    build:function(){
      var self=this,$el=this.options.wrapper,color=self.options.color,elTopDistance=$el.offset().top,windowTopDistance=$(window).scrollTop(),duration=(self.options.animated&&!self.options.strokeBased)?200:100;
      if(window.location.protocol==='file:'){
        $el.css({opacity:1,width:$el.attr('width')});
        if(self.options.extraClass){
          $el.addClass(self.options.extraClass);
        }
        if(self.options.extraClass.indexOf('-color-light')>0){
          $el.css({filter:'invert(1)'});
        }
        $(window).trigger('icon.rendered');return;
      }
      if(self.options.duration){duration=self.options.duration;}
      var SVGContent=$.get({
        url:$el.attr('src'),
        success:function(data,status,xhr){
          var iconWrapper=$('<div class="animated-icon animated fadeIn">'+xhr.responseText+'</div>'),uniqid='icon_'+Math.floor(Math.random()*26)+Date.now();iconWrapper.find('svg').attr('id',uniqid);
          if($el.attr('width')){
            iconWrapper.find('svg').attr('width',$el.attr('width')).attr('height',$el.attr('width'));
          }
          if($el.attr('height')){
            iconWrapper.find('svg').attr('height',$el.attr('height'));
          }
          if(self.options.svgViewBox){
            iconWrapper.find('svg').attr('viewBox',self.options.svgViewBox);
          }
          $el.replaceWith(iconWrapper);
          if(self.options.extraClass){
            iconWrapper.addClass(self.options.extraClass);
          }
          if(self.options.onlySVG){
            $(window).trigger('icon.rendered');
            return this;
          }
          $el=iconWrapper;
          var icon=new Vivus(uniqid,{
            start:'manual',
            type:'sync',
            selfDestroy:true,
            duration:duration,
            onReady:function(obj){
              var styleElement=document.createElementNS("http://www.w3.org/2000/svg","style"),animateStyle='';
              if(self.options.animated&&!self.options.strokeBased||!self.options.animated&&color&&!self.options.strokeBased){
                animateStyle='stroke-width: 0.1px; fill-opacity: 0; transition: ease fill-opacity 300ms;';
                styleElement.textContent='#'+uniqid+' path, #'+uniqid+' line, #'+uniqid+' rect, #'+uniqid+' circle, #'+uniqid+' polyline { fill: '+color+'; stroke: '+color+'; '+animateStyle+(self.options.svgStyle?self.options.svgStyle:"")+' } .finished path { fill-opacity: 1; }';
                obj.el.appendChild(styleElement);
              }
              if(self.options.animated&&self.options.strokeBased||!self.options.animated&&color&&self.options.strokeBased){
                styleElement.textContent='#'+uniqid+' path, #'+uniqid+' line, #'+uniqid+' rect, #'+uniqid+' circle, #'+uniqid+' polyline { stroke: '+color+'; '+(self.options.svgStyle?self.options.svgStyle:"")+'}';obj.el.appendChild(styleElement);
              }
              $.event.trigger('theme.plugin.icon.svg.ready');
            }
          });
          if(!self.options.animated){
            setTimeout(function(){icon.finish();},10);
            $el.css({opacity:1});
          }
          if(self.options.animated&&$(window).width()>767){
            if($el.visible(true)){
              self.startIconAnimation(icon,$el);
            }else if(elTopDistance<windowTopDistance){
              self.startIconAnimation(icon,$el);
            }
            $(window).on('scroll',function(){
              if($el.visible(true)){
                self.startIconAnimation(icon,$el);
              }
            });
          }else{
            $el.css({opacity:1});
            icon.finish();
            $(window).on('theme.plugin.icon.svg.ready',function(){
              setTimeout(function(){
                icon.el.setAttribute('class','finished');
                icon.finish();
              },300);
            });
          }
          $(window).trigger('icon.rendered');
        }
      });
      return this;
    },
    startIconAnimation:function(icon,$el){
      var self=this;
      $({to:0}).animate({to:1},((self.options.strokeBased)?self.options.delay:self.options.delay+300),function(){$el.css({opacity:1});});
      $({to:0}).animate({to:1},self.options.delay,function(){
        icon.play(1);
        setTimeout(function(){
          icon.el.setAttribute('class','finished');
        },icon.duration*5);
      });
    }
  };
  $.extend(theme,{PluginIcon:PluginIcon});
  $.fn.themePluginIcon=function(opts){
    return this.map(function(){
      var $this=$(this);
      if($this.data(instanceName)){
        return $this.data(instanceName);
      }else{
        return new PluginIcon($this,opts);
      }
    });
  };
}).apply(this,[window.theme,jQuery]);