/* Editable settings
   https://vitalets.github.io/x-editable/docs.html
*/
var translate_mode = getCookie("translate_mode");
function get_translatable_labels(){
  /* Собираем все метки, которые хотим дать возможность перевести,
     делаем динамически потому что есть пункты меню, выпадашки и др.
  */
  var labels_for_translate = [];
  $(".label_for_translate").each(function(){
    var label_for_translate = $(this).attr("attr-class_name");
    if(label_for_translate != "undefined"){
      labels_for_translate.push(label_for_translate);
    }
  });

  return labels_for_translate;
}

function destroy_xeditable_for_translations(){
  /* Убираем редактируемые метки для перевода
  */
  var class_names = get_translatable_labels();
  for(var i=0; i<class_names.length; i++){
    $("." + class_names[i]).editable("destroy");
  }
}
function create_xeditable_for_translations(){
  /* Добавляем редактируемые метки для перевода
  */
  var csrf = getCookie('csrftoken');
  var class_names = get_translatable_labels();
  for(var i=0; i<class_names.length; i++){
    var edit_mode = "inline"; // or popup
    if($("." + class_names[i]).attr("attr-edit_mode") === "popup"){
      edit_mode = "popup"
    }
    $("." + class_names[i]).editable({
      //type: "text",
      type: "textarea",
      url: "/languages/translate_mode/",
      pk: class_names[i],
      mode: edit_mode,
      params: function(params) {
        params.csrfmiddlewaretoken = csrf;
        return params;
      },
      success: function(response, newValue){
        //console.log(response, newValue);
      }
    });
  }
}

function get_translations(){
  /* Получение переводов
  */
  var class_names = get_translatable_labels();
  /* Может и не быть в некоторых случаях
  if(class_names < 1){
    return;
  }
  */
  $.ajax({
    async : true,
    type: "POST",
    data: {
      "class_names": class_names.join(),
      "csrfmiddlewaretoken": getCookie('csrftoken')
    },
    url: "/languages/get_translations/",
    success : function (r) {
      for(var i=0; i<r['translations'].length; i++){
        if(translate_mode === "on"){
          $("." + r['translations'][i]['class_name']).editable("setValue", r['translations'][i]['value']);
        }else{
          $("." + r['translations'][i]['class_name']).html(r['translations'][i]['value']);
        }
      }
      for(var i=0; i<r['left_menu_translations'].length; i++){
        var menu = r['left_menu_translations'][i];
        var pk = menu['class_name'].replace('_label', '')
        $("#" + pk + " span").html(menu['value']);
      }
    }
  });
}

function create_translatable_left_menu(){
  /* Создает дубль меню для перевода
  */
  if($("#left_menu_apps").length < 1 || $("#left_menu_apps_translations").length < 1){
    return;
  }
  $(".translations_for_menu").removeClass("hidden");
  var container = $("#left_menu_apps_translations");
  $("#left_menu_apps>li").each(function(){
    var icon = $(this).find("em").attr('class');
    var pk = $(this).attr("id");
    if(typeof(pk) == "undefined"){
      return;
    }

    var menu = '<li class="translations">';
    menu += '<a>';
    menu += '<em class="' + icon + '"></em>\n';
    menu += '<span class="item-text label_for_translate ' + pk + '_label" attr-class_name="' + pk + '_label">';
    menu += $(this).find('span').html();
    menu += '</span>';
    menu += '</a>';
    /* Подменю */
    if($(this).find("ul").length > 0){
      var submenus = $("#" + pk + " ul>li");
      menu += '<ul class="nav">';
      submenus.each(function(){
        var pk_sub = $(this).attr('id');
        menu += '<li class="translations">';
        menu += '<a>';
        menu += '<span class="item-text label_for_translate ' + pk_sub + '_label" attr-class_name="' + pk_sub + '_label">';
        menu += $(this).find('span').html();
        menu += '</span>';
        menu += '</a>';
        menu += '</li>';
      });
      menu += '</ul>';
    }

    menu += '</li>';
    container.append($(menu));
  });
}
function remove_translatable_left_menu(){
  /* Удаляет дубль меню для перевода */
  $(".translations_for_menu").addClass("hidden");
  if($("#left_menu_apps_translations").length > 0){
    $("#left_menu_apps_translations").html("");
  }
}

function turn_on_translatable_labels(){
  /* Включить режим перевода
  */
  create_translatable_left_menu();
  create_xeditable_for_translations();
  $(".translate_mode").prop("checked", "checked");
  get_translations();
}

function turn_off_translatable_labels(){
  /* Отключить режим перевода
  */
  remove_translatable_left_menu();
  destroy_xeditable_for_translations();
  $(".translate_mode").prop("checked", "");
  get_translations();
}

$(document).ready(function(){
  /* Собираем список элементов, которые можно перевести
     в классе должно стоять label_for_translate и
     класс элемента, а также attr-class_name должен
     содержать название класса из класса, например,
         class="label_for_translate translate_mode_label"
         attr-class_name="translate_mode_label"
  */

  if (translate_mode === "on"){
    turn_on_translatable_labels();
  }else{
    turn_off_translatable_labels();
  }

  $(".translate_mode").click(function(){
    if($(this).prop("checked")){
      turn_on_translatable_labels();
      document.cookie = "translate_mode=on; path=/; max-age=3600";
    }else{
      turn_off_translatable_labels();
      document.cookie = "translate_mode=off; path=/; max-age=3600";
    }
  });

});