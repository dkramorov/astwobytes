var redactors = [];
var z = 0;
function create_editor(){
  var id;
  id = $(this).get(0).id;
  if(id == ""){
    z += 1;
    id = "e_"+z;
    $(this).attr("id", id);
  }
  destroy_all_editors(id);

  //alert($(this).get(0).tagName);
  var inArray = redactors.indexOf(id); // -1 or >=0
  if(inArray < 0){
    /* Без загрузки изображений */
    var buttons = ["html", "image", "link", "|", "fontcolor", "backcolor", "|", "horizontalrule", "|", "formatting", "|", "bold", "italic", "deleted", "underline"]
    if(upload_path == 0){
      $("#"+id).redactor({
        buttons:buttons,
        //iframe: true,
        //air: true,
        //airButtons: ["html", "formatting", "|", "bold", "italic", "deleted"]
      });
    /* С папкой для загрузки изображений */
    }else{
      $("#"+id).redactor({
        buttons:buttons,
        //iframe: true,
        //air: true,
        //airButtons: ["html", "formatting", "image", "|", "bold", "italic", "deleted"],
        imageUpload: "/main/editor/uploader/images/",
        uploadFields: {"dest": upload_path},
        imageGetJson: "/main/editor/images/"+upload_path+"/",
        fileUpload: "/main/editor/uploader/files/",
      });
    }
  }
  redactors.push(id);
}
function destroy_all_editors(except){
  for(var i=0; i<redactors.length; i++){
    if(except == "undefined"){
    }else{
      if(redactors[i] == except){
        continue;
      }
    }
    $("#"+redactors[i]).destroyEditor();
    $("#"+redactors[i]).removeAttr("id");
    delete redactors[i];
  }
}

jQuery(function(a){
  a(function(){
    Progress.init();
    Progress.show();
    var d=Timer("Загрузка...");
    var c=new Array();
    var g=a("#tea14-src");
    var e=a("#tea14-preview");
    var f=a("#tea14-module-list");
    var b=false;
    Progress.log("1 из 2: Грузим тему");

    g.attr("src", g.attr("data-src"));

    g.load(function(){
      var i=g.contents();
      Progress.log("2 из 2: Загрузка редактора");
      i.find("[data-templateapp]").each(function(o){
        c.push({
          index:o,name:this.getAttribute("data-templateapp"),value:this.outerHTML}
        )}
      );
      var j="";
      i.find("style").each(function(o){
        j+=a(this).text();
      });
      a(document).find("head").append('<style type="text/css">'+j+"</style>");
      i.find("link").each(function(o){
        a(document).find("head").append(this)
      });
      a.each(c,function(o){
        f.append('<li title="Перетащите блок в конструктор">'+c[o].name+"</li>")
      });
      e.sortable({
        axis:"y",
        revert:200,
        forceHelperSize:true,
        forcePlaceholderSize:true,
        zIndex:9999,
        cancel:":input,button,.redactor_toolbar li,[contenteditable]",
        stop:function(o,p){
          var q=Timer("Sortable stop event");
          if(p.item.hasClass("ui-draggable-handle")){
            a.each(c,function(r){
              if(c[r].name==p.item.html()){
                p.item.html(c[r].value);a(".spectrum.tea14dc-opt").each(function(t,s){
                  $this=a(s);
                  Paint.optional($this,$this.spectrum("get"),p.item.find("*"),true)
                });
                Paint.all(m,n,p.item.find("*"));
                p.item.children().css("background-color",h);
                return
              }
            });
            p.item.removeClass("ui-draggable-handle")
          }
          e.find(".tea14-sortable-close").remove();
          e.find(".tea14-sortable-hover").removeClass("tea14-sortable-hover");q.stop()
        }
      }).on("mouseenter","li",function(o){
        if(a(this).parent().hasClass("redactor_toolbar")){
          return false;
        }
        a(this).addClass("tea14-sortable-hover").prepend('<span class="tea14-sortable-close">&times;</span>')
      }).on("mouseleave","li",function(o){
        a(this).removeClass("tea14-sortable-hover").find(".tea14-sortable-close:first").remove()
      }).on("click",".tea14-sortable-close",function(o){
        a(this).parent().hide("slow",function(){
          a(this).remove()
        })
      }).on("click","a",function(o){
        o.preventDefault();o.stopImmediatePropagation()
      }).disableSelection();
      f.children().draggable({
        revertDuration:200,
        revert:"invalid",
        addClasses:false,
        appendTo:e,
        connectToSortable:e,
        scroll:false,
        start:function(){
          e.parent().css("overflow","hidden")
        },stop:function(){
          e.parent().css("overflow","auto")
        },helper:function(p){
          var q=a(p.target).text();
          var o="";
          a.each(c,function(r){
            if(c[r].name==q){
              o=a('<div id="tea14-drag-helper" class="Email">'+c[r].value+"</div>");
              return
            }
          });
          return o
        }
      }).disableSelection();a(".spectrum.background").spectrum({
        showInitial:true,
        showInput:true,
        preferredFormat:"hex6",
        clickoutFiresChange:true,
        change:function(o){
          h=o.toHexString();
          e.css("background-color",h);
          e.find("> li").children().css("background-color",h);
          b=true
        }
      });
      a(".spectrum.main").spectrum({
        showInitial:true,
        showInput:true,
        preferredFormat:"hex6",
        clickoutFiresChange:true,change:function(o){
          Paint.all(n,o,e.find("*"));
          n=a(".spectrum.main").spectrum("get");
          b=true
        }
      });
      var h="";
      var n=a(".spectrum.main").spectrum("get");
      var m=n;a(".spectrum.tea14dc-opt").spectrum({
        showInitial:true,
        showInput:true,
        preferredFormat:"hex6",
        clickoutFiresChange:true,
        change:function(o){
          Paint.optional(a(this),o,e.find("*"));b=true
        }
      });
      function l(o){
        a("#tea14-tools-advanced-mode").val(o).change()
      }
      function k(p){
        a(this).off();var o=Timer("Загрузка всех модулей");
        if(b){
          Progress.show()
        }
        e.html("");
        l(0);
        a.each(c,function(r){
          if(b){
            var q=a(c[r].value);
            e.css("background-color",h);
            q.css("background-color",h);
            Paint.all(m,n,q.find("*"));
            a(".spectrum.tea14dc-opt").each(function(t,s){
              $this=a(s);
              Paint.optional($this,$this.spectrum("get"),q.find("*"),true)
            });
            c[r].value=q.prop("outerHTML")
          }
          e.append("<li>"+c[r].value+"</li>")
        });
        l(1);
        if(b){
          a(".spectrum.tea14dc-opt").each(function(r,q){
            $origin=a(q);$origin.attr("data-tea14dc-backup",$origin.attr("data-tea14dc-old"))
          });
          Progress.hide()
        }
        b=false;
        o.stop();
        a(this).on("click",k)
      }
      a("#tea14-tools-advanced-all").on("click",k);
      a("#tea14-tools-advanced-clean").click(function(o){
        e.html("");l(0)
      });
      a("#tea14-tools-advanced-mode").change(function(){
        if(parseInt(this.value)){
          e.enableSelection();
          //e.find("img").parent().prop("contenteditable",true).addClass("tea14-content-editable");
          //$(".tea14-content-editable").on("mouseover", create_editor);
          $(".editable").on("click", create_editor);
        }else{
          //destroy_all_editors();
          //a(".tea14-content-editable").prop("contenteditable",false).removeClass("tea14-content-editable");
          e.disableSelection();
        }
      });
      a("#tea14-tools-switch").click(function(o){
        a(".tea14-left, .tea14-right").toggleClass("tea14-hide");
        setTimeout(function(){
          a(".tea14-main").toggleClass("tea14-hide")
        },500)
      });
      a("#tea14-tools-refresh").click(function(){
        destroy_all_editors();
      });
      a("#tea14-tools-download").click(function(p){
        p.preventDefault();
        p.stopImmediatePropagation();
        /*alert($("ul#tea14-preview").html());*/
        /*Progress.show();
        */
        destroy_all_editors();
        l(0);

        var q="";
        e.find("> li").each(function(){
          q+=this.innerHTML
        });

        $("#template").val(q);
        $("#template_form").submit();



        /*
        var o="";
        if(h){
          o='style="background-color:'+h+';"'
        }

        alert(o);
        a.ajax({
          url:DOWNLOAD,
          type:"post",
          cache:false,
          data:{
            src:q,
            bgcolor:o
          },success:function(r){
            l(1);
            Progress.hide();
            window.location.href=r
          }
        })
        */
      });
      a("#tea14-tools-advanced-all").click();
      a(".tea14-left").organicTabs();
      l(1);
      Progress.hide(function(){
        Progress.log();
        a(".tea14-main").show();
        d.stop()
      })
    })
  })
});
