// ---------------------------------
// Настройки видимости полей таблицы
// ---------------------------------
$(document).ready(function(){
  if(window['main_table'] === undefined){
    console.log('main_table not found');
    return;
  }
  if(window['main_table_columns'] === undefined){
    console.log('main_table_columns not found');
    return;
  }
  // Текущий статус видимости столбцов
  var current_status_columns = {};
  $(".tabulator-col").each(function(){
    current_status_columns[$(this).attr("tabulator-field")] = $(this).is(":visible");
  });
  // Вывод настроек
  var tabulator_visible_columns = $("#tabulator_visible_columns");
  for(var i=0; i<main_table_columns.length; i++){
    var column = main_table_columns[i];
    var field = column['field'];
    if(!field){
      continue;
    }
    var html = '';
    var checked = 'checked';
    if(!current_status_columns[field]){
      checked = '';
    }
    html += '<div class="col-masonry">';
    html += '<div class="box-placeholder m0">';
    html += '<p>' + column['title'] + '</p>';
    html += '<label class="switch">';
    html += '<input type="checkbox" id="tabulator_visible_columns_' + field + '" ' + checked + '>';
    html += '<span></span>';
    html += '</label>';
    html += '</div>';
    html += '</div>';
    tabulator_visible_columns.append($(html));
    tabulator_toggle_column(field);
  }
  // Переключение видимости
  function tabulator_toggle_column(field){
    $('#tabulator_visible_columns_' + field).click(function(){
      main_table.toggleColumn(field);
      //main_table.hideColumn("position");
      //main_table.showColumn("position");
    });
  }
});