function check_ip_range_from_form(start_ip_selector, end_ip_selector) {
  /* Проверка формы для ввода диапазона
     Проверку следует выполнять в submit формы
  */
  var start_ip = $("input.ip[name='start_ip']").val();
  if (start_ip_selector != undefined) {
    start_ip = $(start_ip_selector).val();
  }
  var start_ip_parts = start_ip.split('.');

  var end_ip = $("input.ip[name='end_ip']").val();
  if (end_ip_selector != undefined) {
    end_ip = $(end_ip_selector).val();
  }
  var end_ip_parts = end_ip.split('.');

  var isRangeError = false;
  if (parseInt(start_ip_parts[0]) > parseInt(end_ip_parts[0])) {
    isRangeError = true;
  } else if (parseInt(start_ip_parts[0]) == parseInt(end_ip_parts[0])) {
    if (parseInt(start_ip_parts[1]) > parseInt(end_ip_parts[1])) {
      isRangeError = true;
    } else if (parseInt(start_ip_parts[1]) == parseInt(end_ip_parts[1])) {
      if (parseInt(start_ip_parts[2]) > parseInt(end_ip_parts[2])) {
        isRangeError = true;
      } else if (parseInt(start_ip_parts[2]) == parseInt(end_ip_parts[2])) {
        if (parseInt(start_ip_parts[3]) > parseInt(end_ip_parts[3])) {
          isRangeError = true;
        }
      }
    }
  }
  return isRangeError;
}
function check_triptix(arr) {
  /* Вспомогательная функция для проверки,
     что массив из частей айпи адреса валиден (0<x<255)
  */
  var iptext = arr.join('');
  var parts = iptext.split('.');
  if (parts.length > 4) {
    parts = parts.slice(0, 4);
  }
  var part;
  var new_parts = [];
  for (var i=0; i<parts.length; i++) {
    part = parts[i];
    if (part.length > 3) {
      part = part.substr(0,3);
    }
    var digit = parseInt(part);
    if (isNaN(digit)) {
      digit = 0;
    } else if (digit > 255) {
      digit = 255;
    } else if (digit < 0) {
      digit = 0;
    }
    new_parts.push('' + digit);
  }
  return new_parts.join('.')
}
function listen_input_for_ip_address(input_selector, error_selector) {
  /* Функция добавляет слушатели для валидации
     на input куда вводят ip адрес
     input_selector куда вешаем обработчики событий
     error_selector нужен, чтобы убрать предыдущии сообщения об ошибках
  */
  if (input_selector == undefined) {
    input_selector = "input.ip";
  }
  if (error_selector == undefined) {
    error_selector = ".ip_error";
  }
  $(input_selector).keyup(function() {
    var value = $(this).val();
    if (!value) {
      return;
    }
    var allowed = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'];
    var digit;
    var arr = [];
    for (var i=0; i<value.length; i++) {
      digit = value[i];
      if (allowed.indexOf(digit) > -1) {
        arr.push(digit);
      }
    }
    $(this).val(check_triptix(arr));
    $(error_selector).html("");
  });
  $(input_selector).blur(function () {
    var value = $(this).val();
    var parts = value.split('.');
    if (parts.length < 4) {
      $(this).val('');
    }
    if (isNaN(parseInt(parts[0])) || parseInt(parts[0]) <= 0) {
      $(this).val('');
    }
  });
}