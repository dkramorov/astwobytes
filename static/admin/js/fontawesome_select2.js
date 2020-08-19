function fontawesome_select2(select2_id){
  // --------------------------
  // Получение файла с иконками
  // и подстановка их в select2
  // :param select2_id: ид эл.,
  // например, icon_fontawesome
  // --------------------------
  var cur_value = $("#" + select2_id).val();
  $.getJSON( "/static/admin/misc/font-awesome.json", function(data){
    var items = [];
    var item = null;
    for(var i=0; i<data['results'].length; i++){
      item = data['results'][i];
      items.push("<option value='" + item['id'] + "'>" + item['text'] + "</option>");
    }
    $("#" + select2_id).html($(items.join("")));
    $("#" + select2_id).select2({
      placeholder: "Выберите иконку",
      width: "100%",
      allowClear: true,
      templateResult: function (data) {
        return "<i class='fa fa-" + data.id + "'></i> " + data.text;
      },
      templateSelection: function (data) {
        return "<i class='fa fa-" + data.id + "'></i> " + data.text;
      },
      escapeMarkup: function (m) { return m; },
    });
    // После заливки ставим старое значение

    if(typeof(cur_value) === "string"){
      $("#" + select2_id).val(cur_value).trigger("change");
    }
  });
}