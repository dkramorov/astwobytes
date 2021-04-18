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
  if(class_names < 1){
    return;
  }
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
    }
  });
}

function create_translatable_left_menu(){
  /* Создает дубль меню для перевода
  */
  if($("#left_menu_apps").length < 1){
    return;
  }
  if($("#left_menu_apps .translations").length < 1){
    var container = $("#left_menu_apps");
    container.append($('<li class="nav-heading translations">Translate menu:</li>'));
    $("#left_menu_apps>li").each(function(){
      var icon = $(this).find("em").attr('class');

      var menu = '<li class="translations">';
      menu += '<a>';
      menu += '<em class="' + icon + '"></em>\n';
      menu += '<span class="item-text">';
      menu += $(this).find('span').html();
      menu += '</span>';
      menu += '</a>';
      menu += '</li>';
      container.append($(menu));
    });
  };
}
function remove_translatable_left_menu(){
  /* Удаляет дубль меню для перевода */
console.log($("#left_menu_apps .translations"));
  if($("#left_menu_apps .translations").length > 0){
    $("#left_menu_apps .translations").remove();
  }
}

function turn_on_translatable_labels(){
  /* Включить режим перевода
  */
  create_translatable_left_menu();
  create_xeditable_for_translations();
  $(".translate_mode").prop("checked", "checked");
}

function turn_off_translatable_labels(){
  /* Отключить режим перевода
  */
  remove_translatable_left_menu();
  destroy_xeditable_for_translations();
  $(".translate_mode").prop("checked", "");
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

  get_translations();

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