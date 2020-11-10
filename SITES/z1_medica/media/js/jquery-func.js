$(document).ready(function(){
    
    
    $('.form-holder .txtfiled').focus(function(){
        if($(this).val()=="Имя пользователя")
            $(this).val("");    
    });
    
    $('.form-holder .txtfiled').blur(function(){
        if($(this).val()=="")
            $(this).val("Имя пользователя");           
    });
    
    

});

function fun_select(){$('#select').submit();}
(function($){  
      
        /* использование: <a class='scrollTop' href='#' style='display:none;'></a> 
        ------------------------------------------------- */  
        $(function(){  
            
            var speed = 500;  
      
             $(".scrollTop").click(function(){  
                $("html:not(:animated)" +( !$.browser.opera ? ",body:not(:animated)" : "")).animate({ scrollTop: 0}, 500 );  
                return false; //важно!  
            });  
            //появление  
            function show_scrollTop(){  
                if ( $(window).scrollTop() > 200 ) {
				$(".scrollTop").fadeIn(600); 
				$("#favicon").show().animate({marginTop:"5px"},1000);
				$("#toppanel").addClass("shadow");
				
				}
				else { 
				$(".scrollTop").hide();
				$("#favicon").stop(true);
				$("#favicon").css("margin-Top","-85px").hide();
				$("#toppanel").removeClass("shadow");
				}  
			}		
            
			$(window).scroll( function(){show_scrollTop()} ); show_scrollTop();  
        });  
      
 })(jQuery)  
