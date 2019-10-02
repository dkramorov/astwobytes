var Timer=function(a){
  var b=new Date();
  return{
    stop:function(){
      var c=new Date();
      var d=c.getTime()-b.getTime();
      console.log(a,":",d,"ms");
      return d
    }
  }
};
var Progress=(function(e){
  var d,b,c;
  var a=function(g){
    var f="";
    f+='<div id="'+g+'" class="reveal-modal">';
    f+='<a class="close-reveal-modal">&#215;</a>';
    f+='<p style="text-align: center;"><i class="fa fa-refresh fa-3x fa-spin"></i></p>';
    f+='<div class="tea14-loading-log"></div>';
    f+="</div>";
    e("body").append(f);
    d=e("#"+g);b=e("#"+g+" .close-reveal-modal");
    c=e("#"+g+" .tea14-loading-log")
  };
  return{
    init:function(){
      a("tea14-loading")
    },show:function(){
      d.reveal({closeonbackgroundclick:false,})
    },hide:function(f){
      b.click();
      c.text("");
      if(typeof f=="function"){f()}
    },log:function(f){
      if(typeof f=="undefined"){c.text("")}else{c.append("<p>"+f+"</p>")}
    }
  }
})(jQuery);
var Paint=(function(b){
  var a=function(f,d,e,c){
    c.filter(function(){
      return b(this).css(f)==d.toRgbString()
    }).css(f,e.toHexString())
  };
  return{
    background:function(d,e,c){
      c.filter(function(){
        var g=b(this).css("background-color")==d.toRgbString();
        var f=b(this).attr("bgcolor")==d.toHexString();
        return g||f
      }).css("background-color",e.toHexString())
    },text:function(d,e,c){
      a("color",d,e,c)
    },border:function(e,f,d){
      var c=["border-top-color","border-right-color","border-bottom-color","border-left-color"];
      b.each(c,function(h,g){
        a(g,e,f,d)
      })
    },all:function(d,e,c){
      this.background(d,e,c);
      this.border(d,e,c);
      this.text(d,e,c)
    },optional:function(d,g,f,c){
      var e;
      if(c){
        e=tinycolor(d.attr("data-tea14dc-backup"))
      }else{
        e=tinycolor(d.attr("data-tea14dc-old"))
      }
      if(d.hasClass("tea14dc-opt-text")){
        this.text(e,g,f)
      }else{
        if(d.hasClass("tea14dc-opt-background")){
          this.background(e,g,f)
        }else{
          if(d.hasClass("tea14dc-opt-border")){
            this.border(e,g,f)
          }
        }
      }
      d.attr("data-tea14dc-old",g.toHexString())
    }
  }
})(jQuery);
function getTextNodesIn(d,a){
  var c=[],e=/\S/;
  function b(h){
    if(h.nodeType==3){
      if(a||e.test(h.nodeValue)){c.push(h)}
    }else{
      for(var g=0,f=h.childNodes.length;g<f;++g){
        b(h.childNodes[g])
      }
    }
  }
  b(d);
  return c
}
function wrapTextNodesIn(d,a){
  var c=[],e=/\S/;
  function b(j){
    if(j.nodeType==3){
      if(a||e.test(j.nodeValue)){
        var h=document.createElement("span");
        h.innerHTML=j.nodeValue;
        j.parentNode.replaceChild(h,j);
        c.push(j)
      }
    }else{
      for(var g=0,f=j.childNodes.length;g<f;++g){
        b(j.childNodes[g])
      }
    }
  }
  b(d);
  return c
}
