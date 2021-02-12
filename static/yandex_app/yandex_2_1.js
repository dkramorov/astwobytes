//  --------------------------------------
// Записываем все созданные карты в массив
// Затем будем работать по нему
// Например, функция search_by_geocoder
// ---------------------------------------
var myMaps = [];
var current_map_id = null;
var irkutsk_coords = [52.286387, 104.28066];

// --------------------------
// Демо функция как загрузить
// Яндекс.Карты на страничку
// --------------------------
function load_yandex_maps_script(api_key, callback){
  if(window.load_yandex_maps_script_status){
    if(typeof(callback) != "undefined"){
      console.log("Call callback function");
      callback();
    }
    return;
  }
  // Чтобы повторно не грузить
  window.load_yandex_maps_script_status = 1;
  $.getScript( "//api-maps.yandex.ru/2.1/?lang=ru_RU&apikey=" + api_key).done(function(script, textStatus) {
    console.log("Yandex maps loaded", textStatus);
    if(typeof(callback) != "undefined"){
      console.log("Call callback function");
      callback();
    }
  })
}

// --------------------------------------------
// Ищем карту в массиве - если не нашли, значит
// либо карта еще не успела создастся, либо она
// там и не появится - надо искать ошибку
// --------------------------------------------
function get_map(mapContainer){
  for(var i=0; i<myMaps.length; i++){
    if(myMaps[i].map_id == mapContainer){
      return myMaps[i];
    }
  }
  console.log("There is no mapContainer in myMaps " + mapContainer);
  return null;
}

// ---------------------------------------
// Иногда мы выполняем функции раньше,
// чем готова карта, поэтому надо обыграть
// перезапуск функции если такое произошло
// conds => набор условий, которые ждем
// ---------------------------------------
function wait_for_result(mapContainer, callback, conds){
  var myMap = get_map(mapContainer);
  if(myMap == null){
    console.log("MAP not ready yet, waiting 1sec");
    setTimeout(function(){
      wait_for_result(mapContainer, callback, conds);
    }, 1000);
    return;
  }
  if(conds.indexOf("search_by_geocoder") > -1){
    if(myMap.search_by_geocoder == null){
      console.log("GEOCODER not ready yet, waiting 1sec");
      setTimeout(function(){
        wait_for_result(mapContainer, callback, conds);
      }, 1000);
      return;
    }
  }
  //console.log(myMap);
  callback();
}

// --------------------
// Создание новой карты
// --------------------
function create_new_map(mapContainer){
  if($("#" + mapContainer).length > 0){
    current_map_id = mapContainer;
  }
  if(current_map_id == null){
    console.log("current_map_id is null");
    return;
  }else{
    ymaps.ready(init_new_map);
  }
}

// ---------------------------------------------
// Добавляем точки на карту через object_manager
// ---------------------------------------------
function add_points_to_map(mapContainer, points){
  var myMap = get_map(mapContainer);
  /* object_manager принимает данные json => */
  var demo_data = {
    "type": "FeatureCollection",
    "features": [
      //{"type": "Feature", "id": 0, "geometry": {"type": "Point", "coordinates": [55.831903, 37.411961]}, "properties": {"balloonContent": "Содержимое балуна", "clusterCaption": "Еще одна метка", "hintContent": "Текст подсказки"}},
      //{"type": "Feature", "id": 1, "geometry": {"type": "Point", "coordinates": [55.763338, 37.565466]}, "properties": {"balloonContent": "Содержимое балуна", "clusterCaption": "Еще одна метка", "hintContent": "Текст подсказки"}},
    ]
  }
  for(var i=0; i<points.length; i++){
    demo_data['features'].push(points[i]);
  }
  myMap.object_manager.add(demo_data);
}

// -------------------------------------------------
// Создание новой карты в элементе id=current_map_id
// -------------------------------------------------
function init_new_map(){
  var myMap = new ymaps.Map(current_map_id, {
    //center: [55.76, 37.64], // Москва
    center: irkutsk_coords,
    controls: ['zoomControl'],
    zoom: 10
  }, {
    suppressMapOpenBlock: true,
    // -------------------------
    // Отключение точек интереса
    // -------------------------
    // http://dimik.github.io/ymaps/examples/group-menu/menu03.html
    yandexMapDisablePoiInteractivity: true
    //searchControlProvider: 'yandex#search'
  });
  // ----------------------------------------
  // Управление объектами через ObjectManager
  // ----------------------------------------
  object_manager = new ymaps.ObjectManager({
    // Чтобы метки начали кластеризоваться, выставляем опцию.
    clusterize: true,
    // ObjectManager принимает те же опции, что и кластеризатор.
    gridSize: 32
  });
  // https://yandex.ru/dev/maps/jsapi/doc/2.1/ref/reference/map.GeoObjects.html
  myMap.geoObjects.add(object_manager);
  myMap.object_manager = object_manager;

  // Создаем экземпляр класса ymaps.control.SearchControl
  var mySearchControl = new ymaps.control.SearchControl({
    options: {
      // Заменяем стандартный провайдер данных (геокодер) нашим собственным.
      provider: new CustomSearchProvider(current_map_id),
      // Не будем показывать еще одну метку при выборе результата поиска,
      // т.к. метки коллекции myCollection уже добавлены на карту.
      noPlacemark: true,
      resultsPerPage: 5
    }
  });
  // Добавляем контрол в верхний правый угол,
  myMap.controls.add(mySearchControl, { float: 'right' });

  // ----------------------------------------------
  // Обработка события, возникающего при щелчке
  // левой кнопкой мыши в любой точке карты
  // При возникновении такого события откроем балун
  // ----------------------------------------------
  myMap.search_by_address_placemark = null;
  myMap.events.add("click", function (e) {
    var coords = e.get("coords");
    if(myMap.kwargs['search_address_by_click'] != null){
      // ----------------------------------------------
      // Если метка уже создана – просто передвигаем ее
      // Если нет – создаем
      // ----------------------------------------------
      if (myMap.search_by_address_placemark != null) {
        myMap.search_by_address_placemark.geometry.setCoordinates(coords);
      }else {
        // --------------
        // Создание метки
        // --------------
        myMap.search_by_address_placemark = new ymaps.Placemark(coords, {
            iconCaption: "Поиск..."
        }, {
            preset: "islands#violetDotIconWithCaption",
            draggable: true
        });

        myMap.geoObjects.add(myMap.search_by_address_placemark);
        // -------------------------------------------------
        // Слушаем событие окончания перетаскивания на метке
        // -------------------------------------------------
        myMap.search_by_address_placemark.events.add("dragend", function () {
          search_by_coords(myMap.map_id, myMap.search_by_address_placemark.geometry.getCoordinates());
        });
      }
      search_by_coords(myMap.map_id, coords);
    }

    if (!myMap.balloon.isOpen()) {
      console.log("[CLICK COORDS]: " + coords[0] + ", " + coords[1]);
/*
      myMap.balloon.open(coords, {
        contentHeader:'Событие!',
        contentBody:'<p>Кто-то щелкнул по карте.</p>' +
          '<p>Координаты щелчка: ' + [
          coords[0].toPrecision(6),
          coords[1].toPrecision(6)
        ].join(', ') + '</p>',
        contentFooter:'<sup>Щелкните еще раз</sup>'
      });
*/
    }else {
      //myMap.balloon.close();
    }
    e.stopPropagation();
  });


  // ---------------------
  // Кнопка удаления карты
  // ---------------------
  var drop_map_button = $("#" + current_map_id + "_remove_map");
  if(drop_map_button.length > 0){
    $(drop_map_button).click(function () {
      myMap.destroy();
    });
  }else{
    console.log("drop button is not found for " + current_map_id);
  }
  // ---------------------------------------------
  // Заполняем переменными, добавляем в массив
  // Обнуляем, чтобы не создавать второй раз карту
  // ---------------------------------------------
  myMap.map_id = current_map_id;
  myMap.search_by_geocoder = null;
  myMap.myPoints = [];
  myMap.search_results = [];
  // ----------------------
  // Дополнительные функции
  // ----------------------
  myMap.kwargs = {
    // ---------------------------
    // Добавляется в строку поиска
    // ---------------------------
    "default_town": "",
    // ------------------------------
    // Поиск адреса по клику на карте
    // ------------------------------
    "search_address_by_click": null,
    // ----------------------------------
    // Действие, когда поиск был завершен
    // и были получены результаты поиска
    // ----------------------------------
    "after_search": null,
    // -------------------------------
    // Действие для заполнения формы
    // результатом поиска (по нажатию)
    // -------------------------------
    "search_result_to_form": null,
    "search_result_to_form_by_click": null,
  };

  myMaps.push(myMap);
  current_map_id = null;
}
// -------------------------------------------
// Вспомогательная функция, которая вызывается
// если kwargs['search_result_to_form'] задан
// -------------------------------------------
function search_result_to_form_callback(mapContainer, ind, coords){
  var myMap = get_map(mapContainer);
  myMap.kwargs['click_coords'] = coords.split(",");
  if(myMap.kwargs['search_result_to_form'] != null){
    myMap.kwargs['search_result_to_form'](ind);
  }
}

// -------------------------------------
// Поиск координат по текстовому запросу
// mapContainer - по какой карте ищем
// -------------------------------------
function search_by_geocoder(mapContainer, text){
  var myMap = get_map(mapContainer);
  if(myMap == null){
    return;
  }

  ymaps.geocode(text, {
    /**
    * Опции запроса
    * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/geocode.xml
    */
    // Сортировка результатов от центра окна карты.
    // boundedBy: myMap.getBounds(),
    // strictBounds: true,
    // Вместе с опцией boundedBy будет искать строго внутри области, указанной в boundedBy.
    // Если нужен только один результат, экономим трафик пользователей.
    results: 1
  }).then(function (res) {
    // Выбираем первый результат геокодирования
    var firstGeoObject = res.geoObjects.get(0)//,

    // Координаты геообъекта
    //coords = firstGeoObject.geometry.getCoordinates(),
    // Область видимости геообъекта
    //bounds = firstGeoObject.properties.get('boundedBy');

    // -------------------------------------------
    // Просто записываем результат поиска в объект
    // -------------------------------------------
    myMap.search_by_geocoder = firstGeoObject;

    // Добавляем первый найденный геообъект на карту.
    // myMap.geoObjects.add(firstGeoObject);
    // Масштабируем карту на область видимости геообъекта.
    // myMap.setBounds(bounds, {
    // Проверяем наличие тайлов на данном масштабе.
      //checkZoomRange: true
    //});

    //console.log('Все данные геообъекта: ', firstGeoObject.properties.getAll());
    //console.log('Метаданные ответа геокодера: ', res.metaData);
    //console.log('Метаданные геокодера: ', firstGeoObject.properties.get('metaDataProperty.GeocoderMetaData'));
    //console.log('precision', firstGeoObject.properties.get('metaDataProperty.GeocoderMetaData.precision'));
    //console.log("Тип геообъекта: %s", firstGeoObject.properties.get('metaDataProperty.GeocoderMetaData.kind'));
    //console.log("Координаты объекта: %s %s", coords[0], coords[1]);
    //console.log("Название объекта: %s", firstGeoObject.properties.get('name'));
    //console.log("Описание объекта: %s", firstGeoObject.properties.get('description'));
    //console.log("Полное описание объекта: %s", firstGeoObject.properties.get('text'));
    /**
    * Если нужно добавить по найденным геокодером координатам метку со своими стилями и контентом балуна, создаем новую метку по координатам найденной и добавляем ее на карту вместо найденной.
    */
    /**
    var myPlacemark = new ymaps.Placemark(coords, {
      iconContent: 'моя метка',
      balloonContent: 'Содержимое балуна <strong>моей метки</strong>'
    }, {
      preset: 'islands#violetStretchyIcon'
    });
    myMap.geoObjects.add(myPlacemark);
    */
  });
}
// -------------------------------------------------
// Показываем все точки на карте с отступом от краев
// -------------------------------------------------
function set_map_bounds(mapContainer){
  var myMap = get_map(mapContainer);
  myMap.setBounds(myMap.geoObjects.getBounds(), {checkZoomRange:true, zoomMargin:100});
//.then(function(){ if(myMap.getZoom() > 10) myMap.setZoom(10);});
}

// --------------------------------
// Отключает колесико мыши для зума
// --------------------------------
function disable_map_wheel(mapContainer){
  var myMap = get_map(mapContainer);
  myMap.behaviors.disable("scrollZoom");
}
// ----------------
// Центрируем карту
// ----------------
function set_map_center (mapContainer, coords, zoom) {
  var myMap = get_map(mapContainer);
  if(typeof(zoom) == "undefined"){
    zoom = 16;
  }
  myMap.setCenter(coords, zoom);
}

// ----------------------------------------
// Провайдер данных для элемента управления
// ymaps.control.SearchControl
// Осуществляет поиск геообъектов
// по массиву points
// Реализует интерфейс IGeocodeProvider
// ----------------------------------------
function CustomSearchProvider(mapContainer){
  this.map_id = mapContainer;
}
// ---------------------------------
// Проверяет есть ли точка в массиве
// с переданными координатами
// coords = [xxx, yyy]
// arr (p.geometry.getCoordinates())
// ---------------------------------
function coords_in_map(coords, mapContainer){
  var myMap = get_map(mapContainer);
  for(var i=0; i<myMap.search_results.length; i++){
    var point = myMap.search_results[i];
    var p_coords = point.geometry.getCoordinates();
    if((coords[0] == p_coords[0]) && (coords[1] == p_coords[1])){
      console.log("point already exists");
      return true;
    }
  }
  for(var i=0; i<myMap.myPoints.length; i++){
    var point = myMap.myPoints[i];
    var p_coords = point.geometry.coordinates;
    if((coords[0] == p_coords[0]) && (coords[1] == p_coords[1])){
      console.log("point already exists");
      return true;
    }
  }
  return false;
}

// ---------------------------
// Находим placemark в массиве
// myMap.myPoints, например,
// чтобы открыть балун
// ---------------------------
function find_placemark_by_id(point_id, myMap){
  var point;
  for(var i=0; i<myMap.myPoints.length; i++){
    point = myMap.myPoints[i];
    if(point_id == point['id']){
      return point;
    }
  }
  return null;
}

// ---------------------------------------
// Провайдер ищет по полю text стандартным
// методом String.ptototype.indexOf
// ---------------------------------------
CustomSearchProvider.prototype.geocode = function (request, options) {
  var mapContainer = this.map_id;
  var myMap = get_map(mapContainer);

  if(request.indexOf(myMap.kwargs['default_town']) > -1){
  }else{
    request = myMap.kwargs['default_town'] + " " + request
  }
  console.log("Search: " + request + " by map_id => " + this.map_id);

  var deferred = new ymaps.vow.defer(),
  geoObjects = new ymaps.GeoObjectCollection(),
  // Сколько результатов нужно пропустить.
  offset = options.skip || 0,
  // Количество возвращаемых результатов.
  limit = options.results || 20;

  wait_for_result(mapContainer, function(){
    // --------------
    // Обнуляем поиск
    // --------------
    myMap.search_by_geocoder = null;
    search_by_geocoder(mapContainer, request);
  }, ["map"]);
  wait_for_result(mapContainer, function(){
    // --------------------------
    // Результаты поиска получены
    // --------------------------
    var point = myMap.search_by_geocoder,
    coords = point.geometry.getCoordinates();
    //console.log(coords);
    // -------------------------------------------
    // Добавляем точку в результаты поиска, но
    // надо проверить - может уже есть такая точка
    // -------------------------------------------
    var already_exists = coords_in_map(coords, mapContainer);

    if(!already_exists){
      myMap.search_results.push(point);
      var search_result_to_form = "";

      // -------------------------------
      // Сразу отправляем данные в форму
      // -------------------------------
      var coords_str = coords[0] + "," + coords[1];
      if(myMap.kwargs['search_result_to_form_by_click'] != null){
        search_result_to_form_callback(mapContainer, myMap.search_results.length - 1, coords_str);
      }

      if(myMap.kwargs['search_result_to_form'] != null){
        search_result_to_form += "<p><a href='javascript:void(0);' onclick='search_result_to_form_callback(\""+mapContainer+"\", " + (myMap.search_results.length - 1) + ",\"" + coords_str + "\")'>Подставить кооридинаты этой точки в адрес</a></p>";
      }

      // --------------------------------------
      // Вручную добавляем в object_manager
      // нашей карты точку с результатом поиска
      // --------------------------------------
      var myPoint = {
        "type": "Feature",
        "id": myMap.search_results.length,
        "geometry": {
          "type": "Point",
          "coordinates": coords
        },
        "properties": {
          "balloonContent": "<p>" + point.properties.get("text") + "</p>" + search_result_to_form,
          "clusterCaption": "Результаты поиска", "hintContent": "<p>" + point.properties.get("text") + "</p>" + search_result_to_form,
        },
      };
      add_points_to_map(mapContainer, [myPoint]);

    }
    geoObjects.add(new ymaps.Placemark(coords, {
      name: point.properties.get("name"),
      description: point.properties.get("description"),
      balloonContentBody: "<p>" + point.properties.get("text") + "</p>" + search_result_to_form,

      boundedBy: [coords, coords]
    }));

    deferred.resolve({
      // Геообъекты поисковой выдачи.
      geoObjects: geoObjects,
      // Метаинформация ответа.
      metaData: {
        geocoder: {
          // Строка обработанного запроса.
          request: request,
          // Количество найденных результатов.
          found: geoObjects.getLength(),
          // Количество возвращенных результатов.
          results: limit,
          // Количество пропущенных результатов.
          skip: offset
        }
      }
    });
    if(myMap.kwargs['after_search'] != null){
      myMap.kwargs['after_search']();
    }
  }, ["search_by_geocoder"]);

  return deferred.promise();
};
// -------------------------------
// Определяем адрес по координатам
// -------------------------------
function search_by_coords(mapContainer, coords) {

  var myMap = get_map(mapContainer);
  var placemark = myMap.search_by_address_placemark;

  placemark.properties.set("iconCaption", "Поиск...");
  ymaps.geocode(coords).then(function (res) {
    var firstGeoObject = res.geoObjects.get(0);

    // ----------------------------------------------
    // Если включено заполнение формы по координатам,
    // тогда выводим возможность выполнить функцию
    // ----------------------------------------------
    var search_result_to_form = "";
    if(myMap.kwargs['search_result_to_form'] != null){

      // -----------------------------------
      // Добавляем точку в результаты поиска
      // -----------------------------------
      myMap.search_results.push(firstGeoObject);

      // -------------------------------
      // Сразу отправляем данные в форму
      // -------------------------------
      var coords_str = coords[0] + "," + coords[1];
      if(myMap.kwargs['search_result_to_form_by_click'] != null){
        search_result_to_form_callback(mapContainer, myMap.search_results.length - 1, coords_str);
      }

      search_result_to_form += "<p><a href='javascript:void(0);' onclick='search_result_to_form_callback(\""+mapContainer+"\", " + (myMap.search_results.length - 1) + ",\"" + coords_str + "\")'>Подставить кооридинаты этой точки в адрес</a></p>";
    }

    placemark.properties.set({
      balloonContentBody: "<p>" + firstGeoObject.properties.get("text") + "</p>" + search_result_to_form,
      iconCaption: firstGeoObject.properties.get('name'),
      balloonContent: firstGeoObject.properties.get('text')
    });
  });
}




// UNUSED
/*
function onObjectEvent (e) {
        var objectId = e.get('objectId');
        if (e.get('type') == 'mouseenter') {
            objectManager.objects.setObjectOptions(objectId, {
                preset: 'islands#yellowIcon'
            });
        } else {
            objectManager.objects.setObjectOptions(objectId, {
                preset: 'islands#blueIcon'
            });
        }
    }
    function onClusterEvent (e) {
        var objectId = e.get('objectId');
        if (e.get('type') == 'mouseenter') {
            objectManager.clusters.setClusterOptions(objectId, {
                preset: 'islands#yellowClusterIcons'
            });
        } else {
            objectManager.clusters.setClusterOptions(objectId, {
                preset: 'islands#blueClusterIcons'
            });
        }
    }
    myMap.object_manager.objects.events.add(['mouseenter', 'mouseleave'], onObjectEvent);
    myMap.object_manager.clusters.events.add(['mouseenter', 'mouseleave'], onClusterEvent);


// -------------------------------------------
// Устанавливаем тип карты и передвигаем центр
// -------------------------------------------
function setTypeAndPan () {
  // Меняем тип карты на "Гибрид".
  myMap.setType("yandex#hybrid");
  // Плавное перемещение центра карты в точку с новыми координатами.
  myMap.panTo([62.915, 34.461], {
    // Задержка между перемещениями.
    delay: 1500
  });
}
function toggle () {
  bigMap = !bigMap;
  // Добавляем/убираем CSS-класс, определяющий размеры контейнера карты,
  // заданные в абсолютных единицах (300x200 px).
  if (bigMap) {
    $('#map').removeClass('smallMap');
  } else {
    $('#map').addClass('smallMap');
  }
  // Если выставлен флаг, сообщаем карте, что ей следует
  // привести свои размеры к размерам контейнера.
  if ($('#checkbox').prop('checked')) {
    myMap.container.fitToViewport();
  }
}
*/
