// -----------------
// EXAMPLE:
// cart_id = "#cart"
// -----------------
if(typeof(cart_id) == "undefined"){
  var cart_id = "#mini-cart";
}

function Notification(msg, type){
  var box = jQuery('<div class="' + type + '"><div class="close"></div><div class="icon"></div>' + msg + '</div>').hide();
  jQuery('#notification').prepend(box);
  if(type != 'warning'){
    box.fadeIn(500).delay(10000).fadeOut(500, function(){
      box.remove();
    });
  }else{
    box.fadeIn(500);
  }
  box.find('.close').on('click', function(){
    box.stop().fadeOut(500, function(){
      box.remove();
    });
  });
}
function add_to_cart(id, cost_type){
  // Добавление id товара в корзинку
  // :param id: ид товара
  // :param cost_type: тип цены
  var props_string = "";
  var props = find_selected_properties(id);
  for(var i=0; i<props.props.length; i++){
    props_string += "&prop_" + props.props[i]['id'] + "=" + props.props[i]['value'];
  }
  var params = "";
  var quantity = jQuery("input#quantity_" + id);
  if(quantity.length > 0){
    params += "&quantity=" + quantity.val();
  }
  if(typeof(cost_type) != "undefined"){
    params += "&cost_type_id=" + cost_type;
  }
  params += props_string;
  jQuery.ajax({
    type: "GET",
    url: "/shop/cart/add/",
    data: "product_id=" + id + params,
    success: function(result){
      if(result['error']){
        alert("Произошла ошибка");
      }else{
        cart_details();
        result['success'] += "<br><a href='/shop/cart/'>Перейти в корзину</a>";
        Notification(result['success'], "success");
      }
    }
  });
  return 0;
}
function purchase_drop(id){
  jQuery.ajax({
    type: "GET",
    url: "/shop/ajax_cart/remove/",
    data: "purchase_id=" + id,
    success: function(result){
      cart_details();
      result['success'] += "<br><a href='/shop/cart/'>Перейти в корзину</a>";
      Notification(result['success'], "warning");

      if(window.location.href.indexOf("/shop/cart/") > -1){
        window.location.reload();
      }else{
        cart_details();
      }
    }
  });
  return 0;
}
function cart_details(cart){
  jQuery.ajax({
    type: "GET",
    url: "/shop/cart/show/",
    data: "",
    success: function(result){
      if(cart){
        jQuery(cart).html(result)
      }else{
        jQuery(cart_id).html(result);
      }
    }
  });
  return 0;
}
function purchase_quantity(id, action){
  // Обновляем кол-во товара в корзине
  var purchase_pk = "#quantity_" + id;

  var count = parseInt(jQuery(purchase_pk).val());
  if(typeof(count) != "undefined" && typeof(action) != "undefined"){
    if(action == "+"){
      count += 1;
    }
    if(action == "-"){
      count -= 1;
    }
  }
  if(typeof(count) == "undefined"){
    count = 0;
  }
  jQuery.ajax({
    type: "GET",
    url: "/shop/ajax_cart/quantity/",
    data: "quantity=" + count + "&purchase_id=" + id,
    success: function(result){
      if(window.location.href.indexOf("/shop/cart/") > -1){
        window.location.reload();
      }else{
        cart_details();
        Notification(result['success'], "success");
      }
    }
  });
}
jQuery(document).ready(function($){
  if($("#notification").length){
    //console.log("notification id found");
  }else{
    $("body").prepend("<div id=\"notification\"></div>");
    //console.log("notification id NOT found");
  }
  if($(cart_id).length > 0){
    console.log("cart found");
  }else{
    console.log("[ERROR CART]: cart NOT found");
  }
  $(".add_to_cart_btn").click(function(){
    var product_id = $(this).attr("data-product_id");
    add_to_cart(product_id);
  });
});
// ---------------------------------------
// Найти все выбранные свойства для товара
// class="prop"
// data-prop-id=<prop_id>
// id=prop_<price_id>
// ---------------------------------------
function find_selected_properties(price_id){
  var selected_properties = Object();
  selected_properties.price_id = price_id;
  selected_properties.props = [];
  jQuery(".prop").each(function(){
    var prop_id = jQuery(this).attr("data-prop-id");
    var prop_value = jQuery(this).val();
    selected_properties.prop_id = prop_id;
    selected_properties.props.push({"id":prop_id, "value":prop_value});
  });
  return selected_properties;
}