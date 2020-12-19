// --------------------------------------------------------
// Поиск счетчика Яндекс Метрики
// /?_ym_debug=1 для отладки
// https://yandex.ru/support/metrika/objects/reachgoal.html
// Цели reachGoal:
// TARGET_NAME - название цели
// USAGE:
//  var ym = search_yandex_counter_number();
//  if(ym !== null){
//    ym.reachGoal(TARGET_NAME);
//  }
// --------------------------------------------------------
function search_yandex_counter_number(){
  for(var key in window){
    if(window.hasOwnProperty(key)){
      if(key.indexOf("yaCounter") > -1){
        var number = key.replace("yaCounter", "");
        if(!isNaN(parseInt(number))){
          return window[key];
        }
      }
    }
  }
  return null;
}