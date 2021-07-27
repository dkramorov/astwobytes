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
        //alert("Произошла ошибка");
        Notification("Произошла ошибка: " + result['error'], "error");
      }else{
        cart_details();
        result['success'] += "<br><a href='/shop/cart/'>Перейти в корзину</a>";
        Notification(result['success'], "success");
      }
    }
  });
  return 0;
}
function purchase_drop(purchase_id){
  /* Удаление покупки
     :param purchase_id: ид покупки
  */
  jQuery.ajax({
    type: "GET",
    url: "/shop/cart/drop/",
    data: "purchase_id=" + purchase_id,
    success: function(result){
      if(window.location.href.indexOf("/shop/cart/") > -1){
        // TODO: не перегружать страничку, просто делать товар блеклым
        window.location.reload();
      }else{
        cart_details();
        result['success'] += "<br><a href='/shop/cart/'>Перейти в корзину</a>";
        Notification(result['success'], "warning");
      }
    }
  });
  return 0;
}
function cart_details(cart){
  /* Выводит аяксовую корзинку в шаблон
     в ajax_cart.html
     для обновления цены и кол-ва
     <div class="hidden" id="ajax_cart_info"
          data-items="{% if cart.items %}{{ cart.items }}{% else %}0{% endif %}"
          data-total="{% if cart.total %}{{ cart.total|money_format }} ₽{% else %}0{% endif %}"
          data-items-selector="#sm_cartpro .cartpro-count"
          data-total-selector="#sm_cartpro .price">
     </div>
  */
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
      update_ajax_cart_info();
    }
  });
  return 0;
}
function update_ajax_cart_info(){
  /* Обновление информации в аякс корзинке (кол-во, сумма)
     #ajax_cart_info содержит всю нужную информацию,
     после удачного запроса, поэтому после запроса
     можно обновить кол-во и сумму выше аякс-корзинки
     в элементе #ajax_cart_info мы берем
     data-items и data-total и ложим значения в
     data-items-selector и data-total-selector
  */
  var ajax_cart_info = $("#ajax_cart_info");
  if(ajax_cart_info.length == 0){
    console.log("#ajax_cart_info not found");
    return;
  }
  var items = ajax_cart_info.attr("data-items");
  var total = ajax_cart_info.attr("data-total");
  var items_selector = ajax_cart_info.attr("data-items-selector");
  var total_selector = ajax_cart_info.attr("data-total-selector");
  $(items_selector).html(items);
  $(total_selector).html(total);
}



function purchase_quantity(id){
  /* Обновляем кол-во товара в корзине
     :param id: purchase_id
  */
  var inp = $("#quantity_" + id);
  if(inp.length == 0){
    console.log("[ERROR]: quantity_ input not found for " + purchase_id);
    return;
  }
  jQuery.ajax({
    type: "GET",
    url: "/shop/cart/quantity/",
    data: "quantity=" + inp.val() + "&purchase_id=" + id,
    success: function(result){
      if(result['error']){
        Notification(result['error'], "error");
        return;
      }
      if(window.location.href.indexOf("/shop/cart/") > -1){
        window.location.reload();
      }else{
        cart_details();
        Notification(result['success'], "success");
      }
    }
  });
}
function purchase_drop_listener(purchase_id, drop_btn){
  /* Слушалка на кнопочку удаления
     :param purchase_id: ид покупки
     :param drop_btn: Кнопка удаления (jquery элемент)
  */
  if(drop_btn.hasClass("touched")){
    console.log("[WARNING]: drop_btn already touched for " + purchase_id);
    return;
  }
  drop_btn.click(function(){
    purchase_drop(purchase_id);
  });
}
function promocode_activate(inp){
  /* Активация промокода
     :param inp: поле ввода промокода
  */
  jQuery.ajax({
    type: "GET",
    url: "/shop/cart/promocode/",
    data: "promocode=" + inp.val(),
    success: function(result){
      if(result['error']){
        Notification(result['error'], "error");
        return;
      }
      if(window.location.href.indexOf("/shop/cart/") > -1){
        window.location.reload();
      }else{
        cart_details();
        Notification(result['success'], "success");
      }
    }
  });
}
function promocode_activate_listener(promocode_inp, promocode_btn){
  /* Слушалка на активацию промокода
     :param promocode_inp: Поле ввода промокода
     :param promocode_btn: Кнопка активации промокода
  */
  if(promocode_btn.hasClass("touched")){
    console.log("[WARNING]: promocode_btn already touched");
    return;
  }
  promocode_btn.click(function(){
    promocode_activate(promocode_inp);
  });
}
function quantity_listener(purchase_id, plus, minus, send_event){
  /* Слушалка для кнопочек больше/меньше для изменения кол-ва товара
     На инпут должен висеть purchase_id
     Без send_event можно вешать на product_id
     :param purchase_id: ид покупки
     :param plus: Кнопка плюс (jquery элемент)
     :param minus: Кнопка минус (jquery элемент)
     :param send_event: Отправлять событие на сервер (на страничке корзинки)
     USAGE:
     quantity_listener(1, $("#plus_1"), $("#minus_1"));
  */
  var inp = jQuery("#quantity_" + purchase_id);
  if (inp.length == 0){
    console.log("[ERROR]: quantity_ input not found for " + purchase_id);
    return;
  }
  if(inp.hasClass("touched")){
    console.log("[WARNING]: qunatity_ input already listening for " + purchase_id);
    return;
  }
  inp.addClass("touched");
  inp.change(function(){
    var count = parseInt(inp.val());
    if(isNaN(count)){
      count = 1;
    }
    if(count <= 0){
      count = 1
    }
    inp.val(count);
    if(send_event !== undefined){
      purchase_quantity(purchase_id);
    }
  });
  plus.click(function(){
    var count = parseInt(inp.val());
    inp.val(count + 1);
    if(send_event !== undefined){
      purchase_quantity(purchase_id);
    }
    return false;
  });
  minus.click(function(){
    var count = parseInt(inp.val());
    count = count - 1;
    if(count <= 0){
      count = 1;
    }
    inp.val(count);
    if(send_event !== undefined){
      purchase_quantity(purchase_id);
    }
    return false;
  });
}
function add_to_compare(id){
  // Добавление id товара в сравнение товаров
  // :param id: ид товара

  jQuery.ajax({
    type: "GET",
    url: "/shop/compare/add/",
    data: "product_id=" + id,
    success: function(result){
      if(result['error']){
        //alert("Произошла ошибка");
        Notification("Произошла ошибка: " + result['error'], "error");
      }else{
        //compare_details();
        result['success'] += "<br><a href='/shop/compare/'>Перейти к сравнению товаров</a>";
        Notification(result['success'], "success");
      }
    }
  });
  return 0;
}
function drop_from_compare(id){
  // Удаление id товара из сравнения товаров
  // :param id: ид товара
  jQuery.ajax({
    type: "GET",
    url: "/shop/compare/drop/",
    data: "product_id=" + id,
    success: function(result){
      if(result['error']){
        //alert("Произошла ошибка");
        Notification("Произошла ошибка: " + result['error'], "error");
      }else{
        //compare_details();
        result['success'] += "<br><a href='/shop/compare/'>Перейти к сравнению товаров</a>";
        Notification(result['success'], "success");
      }
      setTimeout(function(){
        window.location.reload();
      }, 1000);
    }
  });
  return 0;
}

function show_compare_count(callback){
  // Сколько товаров находится в сравнении товаров
  // :param callback: функция,
  // которую надо выполнить после получения результатов
  if (callback == undefined){
    return;
  }
  jQuery.ajax({
    type: "GET",
    url: "/shop/compare/show/",
    success: function(result){
      callback(result['count']);
    }
  });
  return 0;
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
    var cost_type_id = $(".cost-type-radio_" + product_id + ":checked").attr("data-cost_type_id");
    add_to_cart(product_id, cost_type_id);
  });
  // Обновление аякс корзинки (кол-во и сумма)
  update_ajax_cart_info();

  $(".add_to_compare_btn").click(function(){
    var product_id = $(this).attr("data-product_id");
    add_to_compare(product_id);
  });
  $(".drop_from_compare_btn").click(function(){
    var product_id = $(this).attr("data-product_id");
    drop_from_compare(product_id);
  });
});
function demo_fill_order(){
  $("#confirm_order input[name='name']").val("господин Денис");
  $("#confirm_order input[name='first_name']").val("Денис");
  $("#confirm_order input[name='last_name']").val("Краморов");
  $("#confirm_order input[name='middle_name']").val("Геннадьевич");
  $("#confirm_order input[name='phone']").val("83952959223");
  $("#confirm_order input[name='email']").val("dk@223-223.ru");
  $("#confirm_order input[name='address']").val("Иркутск, ");
}
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