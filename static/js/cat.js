function rebuild_query_path_with_param(new_param, new_value){
  /* Перестройка ссылки в соответствии с новым параметром
     Берем ссылку, и достаем все параметры
     впихиваем наш параметр и возвращаем что получилось
     Используется для странички каталога
     :param new_param: новый параметр
     :param new_value: значение нового параметра
     :return: строка с новым и старыми параметрами
  */
  var new_params = [];
  var params = decodeURIComponent(location.search.substr(1)).split("&");
  var new_param_in_url = false;
  for(var i=0; i<params.length; i++){
    var param = params[i].split("=");
    if(param[0] === new_param){
      new_param_in_url = true;
      if(new_value !== ""){
        new_params.push(new_param + "=" + new_value);
      }
    }else{
      new_params.push(param[0] + "=" + param[1]);
    }
  }
  if(!new_param_in_url){
    if(new_value !== ""){
      new_params.push(new_param + "=" + new_value);
    }
  }
  return new_params.join("&");
}