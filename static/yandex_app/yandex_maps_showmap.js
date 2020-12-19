// Создание стиля
var styleExample = new YMaps.Style();
styleExample.iconStyle = new YMaps.IconStyle();
styleExample.iconStyle.href = "/static/maps/ballons/dot.png"; // Ссылка на значок
styleExample.iconStyle.size = new YMaps.Point(26, 46); // Размер значка
styleExample.iconStyle.offset = new YMaps.Point(-22, -46); // Смещение значка (для визуального выравнивания)
YMaps.Styles.add("default#dota", styleExample);

  var map={ // Словарь Карта
    coords:{ x:"104.27563", y:"52.313021", zoom:"10" },
    towns:[],
    bounds:"",

    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Создаем карту, центруем
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    init: function(div){
      this.map = new YMaps.Map(YMaps.jQuery(div)[0]);
      this.map.setCenter(new YMaps.GeoPoint(this.coords.x, this.coords.y), this.coords.zoom);
      this.bounds = this.map.getBounds();
      this.map.addControl(new YMaps.Zoom());
      this.map.addControl(new YMaps.ToolBar());
      this.map.addControl(new YMaps.ScaleLine());
      //this.map.enableScrollZoom({smooth:true});
      this.map.enableHotKeys();
      this.map.addControl(new YMaps.Traffic.Control()); // Пробки
      //(new YMaps.SearchControl({
         //useMapBounds:true,
         //noCentering:false,
         //noPlacemark:true,
         //resultsPerPage:5,
         //width:400
         //})).onAddToMap(this.map, new YMaps.ControlPosition(YMaps.ControlPosition.TOP_RIGHT, new YMaps.Point(0, 0)));
    },

    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Поиск координат по названиям (адресам)
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    multiSearch: function(){
      map.bounds = new YMaps.GeoCollectionBounds();
      var geocoder = new MultiplyGeocoder(map.towns);
      this.map.addOverlay(geocoder);
      YMaps.Events.observe(geocoder, "Load", function (geocoder) {
        //alert("Геокодирование завершено"+map.bounds);
        map.map.setBounds(map.bounds);
      });
    },
    // predifined placemarks styles
    predefinedStyles : [
        {"style":"default#dota","url":"/static/maps/ballons/dot.png"},
        {"style":"default#whitePoint","url":"/static/maps/ballons/pmwts.png"},
        {"style":"default#greenPoint","url":"/static/maps/ballons/pmgns.png"},
        {"style":"default#redPoint","url":"/static/maps/ballons/pmrds.png"},
        {"style":"default#yellowPoint","url":"/static/maps/ballons/pmyws.png"},
        {"style":"default#darkbluePoint","url":"/static/maps/ballons/pmdbs.png"},
        {"style":"default#nightPoint","url":"/static/maps/ballons/pmnts.png"},
        {"style":"default#greyPoint","url":"/static/maps/ballons/pmgrs.png"},
        {"style":"default#bluePoint","url":"/static/maps/ballons/pmbls.png"},
        {"style":"default#orangePoint","url":"/static/maps/ballons/pmors.png"},
        {"style":"default#darkorangePoint","url":"/static/maps/ballons/pmdos.png"},
        {"style":"default#pinkPoint","url":"/static/maps/ballons/pmpns.png"},
        {"style":"default#violetPoint","url":"/static/maps/ballons/pmvvs.png"},
    ],
    data : [],// list of maps overlays
    layerName : "jocker#" + new Date().getTime(),// prefix for polyline/polygon styles

    // setup {name, description} for DescriptionControl & apply description to current overlay
    setDescription : function(description) {
        if (description) {
            this.overlayName.val(description.name);
            this.overlayDescription.val(description.description);
        }
        if (this.currentObject) {
            this.currentObject.name = this.overlayName.val();
            this.currentObject.description = this.overlayDescription.val();
            this.currentObject.update();
        }
    },
    // setup PlacemarkStyle for PlacemarkSelectorControl & apply style for current overlay
    setPlacemarkStyle : function(style) {
        if (style) {
            if (this.currentPlacemarkStyleElm) {
                this.currentPlacemarkStyleElm.className = "placemarkStyle";
            }
            var marks = YMaps.jQuery("#tools .placemark .placemarkStyle");
            for (i = 0; i < marks.length; i++) {
                if (marks[i].id == style) {
                    this.currentPlacemarkStyleElm = marks[i];
                    break;
                }
            }
            this.currentPlacemarkStyleElm.className = "placemarkStyle selectedPlacemarkStyle";
            this.placemarkStyle = style;
        }
        if (this.currentObject instanceof YMaps.Placemark) {
            var options = this.currentObject.getOptions();
            options.style = this.placemarkStyle;
            this.currentObject.setOptions(options);
            this.currentObject.update();
        }
    },
    // setup Style for LineStyleControl & apply style for current overlay
    // style may be YMaps.LineStyle, YMaps.PolygonStyle or null;
    // in last case will be apply current style from LineStyleControl 
    setLineStyle : function(style) {
        var alpha, color;
        if (style) {
            alpha = style.fillColor ? style.fillColor.substr(6, 2) : style.strokeColor.substr(6, 2);
            color = style.strokeColor.substr(0, 6);
            this.lineSample.css("backgroundColor", '#' + color);
            this.lineSample.css("height", style.strokeWidth);
            this.colorSelector.val(color);
            this.withSelector.val(style.strokeWidth);
            this.alphaSelector.val(alpha);
            this.lineStyle = style;
        } else {
            alpha = this.lineStyle.fillColor ? this.lineStyle.fillColor.substr(6, 2) : this.lineStyle.strokeColor.substr(6, 2);
            color = this.lineStyle.strokeColor.substr(0, 6);
        }
        if (this.currentObject instanceof YMaps.Polyline) {
            var s = YMaps.Styles.get(this.currentObject.getStyle());
            if (!s.lineStyle) {
                s.lineStyle = new YMaps.LineStyle();
            }
            s.lineStyle.strokeColor = this.lineStyle.strokeColor;
            s.lineStyle.strokeWidth = this.lineStyle.strokeWidth;
            this.currentObject.update();
        } else if (this.currentObject instanceof YMaps.Polygon) {
            var s = YMaps.Styles.get(this.currentObject.getStyle());
            if (!s.polygonStyle) {
                s.polygonStyle = new YMaps.PolygonStyle();
            }
            s.polygonStyle.strokeColor = color + "ff";
            s.polygonStyle.fillColor = color + alpha;
            s.polygonStyle.outline = true;
            s.polygonStyle.strokeWidth = this.lineStyle.strokeWidth;
            this.currentObject.update();
        }
    },
    // creates new named style for YMaps.Polyline or YMaps.Polygon
    createStyle : function() {
        var key = this.layerName + "#" + this.data.length;
        YMaps.Styles.add(key, new YMaps.Style());
        return key;
    },
    // returns array of StyleDescription for exportLayer function
    getStyleDescriptions:function() {
        var styles = [];
        for (var i = 0; i < this.data.length; i++)
            if (this.data[i]) {
                var s = YMaps.Styles.get(this.data[i].getStyle());
                if (this.data[i] instanceof YMaps.Polyline) {
                    styles[styles.length] = {
                        name:this.data[i].getStyle(),
                        style:{lineStyle : {
                            strokeColor:s.lineStyle.strokeColor,
                            strokeWidth:s.lineStyle.strokeWidth
                        }}
                    }
                } else if (this.data[i] instanceof YMaps.Polygon) {
                    styles[styles.length] = {
                        name:this.data[i].getStyle(),
                        style:{polygonStyle : {
                            strokeColor:s.polygonStyle.strokeColor,
                            strokeWidth:s.polygonStyle.strokeWidth,
                            fillColor:s.polygonStyle.fillColor,
                            fill:true,
                            outline:true
                        }}
                    }
                }
            }
        return styles;
    },
    // returns arry of ObjectDescription for exportLayer function
    getObjectDescriptions : function() {
        function convertPoint(point) {
            return {
                lng:point.getX(),
                lat:point.getY()
            };
        }

        function convertPoints(points) {
            var r = [];
            for (var i = 0; i < points.length; i++)
                r[r.length] = convertPoint(points[i]);
            return r;
        }

        var objects = [];
        for (var i = 0; i < this.data.length; i++)
            if (this.data[i] != null) {
                var o = {
                    style:this.data[i].getStyle(),
                    name:this.data[i].name,
                    description:this.data[i].description
                };
                if (this.data[i] instanceof YMaps.Polyline) {
                    o.type = "Polyline";
                    o.points = convertPoints(this.data[i].getPoints());
                } else if (this.data[i] instanceof YMaps.Polygon) {
                    o.type = "Polygon";
                    o.points = convertPoints(this.data[i].getPoints());
                } else if (this.data[i] instanceof YMaps.Placemark) {
                    o.type = "Placemark";
                    o.points = convertPoint(this.data[i].getGeoPoint());
                }
                objects[objects.length] = o;
            }
        return objects;
    },

    // import layer in LayerDescription format into the Editor
    importLayer : function(layer, active) {
        // creates overlay from ObjectDescription
        function createMapOverlay(objectDesc, map, active) {
            var points = objectDesc.points;
            if (points.length > 0) {
                for (var i = 0; i < points.length; i++) {
                    points[i] = new YMaps.GeoPoint(points[i].lng, points[i].lat);
                }
            } else {
                points = new YMaps.GeoPoint(points.lng, points.lat);
            }
            if (points.length == 0)
                return false;
            var allowObjects = ["Placemark", "Polyline", "Polygon"],
                    index = YMaps.jQuery.inArray(objectDesc.type, allowObjects),
                    constructor = allowObjects[(index == -1) ? 0 : index];
            var description = objectDesc.description || "";
            var object = new YMaps[constructor](points, {style: objectDesc.style });
            object.description = description;
            object.name = objectDesc.name;

            // Проверяем - если это метка и если указано, что надо открыть балун
            if(active == 1){
              map.openBalloon(points, object.name+"<br />"+object.description, {hasCloseButton: true, mapAutoPan: 1});
            }
            return object;
        }

        // import styles
        for (var i = 0; i < layer.styles.length; i++) {
            YMaps.Styles.add(layer.styles[i].name, layer.styles[i].style);
        }
        // import objects
        for (var i = 0; i < layer.objects.length; i++) {
            // В createMapOverlay даем ссылку на карту где будем делать openBalloon
            var o = createMapOverlay(layer.objects[i], this.map, active);
            if (o) {
                this.data[this.data.length] = o;
                this.map.addOverlay(o);
//map.openBalloon(new YMaps.GeoPoint(37.616485,55.751635), 'Москва', {hasCloseButton: false, mapAutoPan: 0});
            }
        }
    },

        // gets layer with name
        get : function(name) {
            for (var i = 0; i < this.data.length; i++)
                if (this.data[i].name == name)
                    return this.data[i];
        },
        // show layer with name
        show : function(name) {
            var layer = this.get(name);
            if (layer.show) return;
            for (var i = 0; i < layer.content.length; i++)
                this.map.addOverlay(layer.content[i]);
            layer.show = true;
            var point = new YMaps.GeoPoint(layer.center.lng, layer.center.lat);
            this.map.setZoom(layer.center.zoom, {smooth:true,position:point, centering:true});
        },
        // hide layer with name
        hide : function(name) {
            var layer = this.get(name);
            if (!layer.show) return;
            for (var i = 0; i < layer.content.length; i++)
                this.map.removeOverlay(layer.content[i]);
            layer.show = false;
        }

  }// END Словарь Карта

  // Реализует наследование прототипа без исполнения конструктора родителя
  // Подробнее о наследовании: http://javascript.ru/tutorial/object/inheritance
  function extend (child, parent) {
    var c = function () {};
    c.prototype = parent.prototype;
    c.prototype.constructor = parent;
    return child.prototype = new c;
  };
  // Множественный геокодер
  // requests - массив адресов
  function MultiplyGeocoder (requests) {
    // Вызов родительского конструктора
    YMaps.GeoObjectCollection.call(this);
    var _this = this,
    // Количество вызовов геокодера
    geocodeCallCount = 0,
    // Обработчики событий
    listeners = [];
    // Последовательно геокодируем все переданные адреса
    for (var i = 0, l = requests.length; i < l; i++) {
      geocode(requests[i]);
    }
    // Функция, отвечающая за геокодировании одного адреса
    function geocode (request) {
      // Геокодируем
      var geocoder = new YMaps.Geocoder(request.address, { results:1, boundedBy: map.bounds } );
      // Счетчик вызовов геокодирования увеличиваем
      geocodeCallCount++;
      // Сохраняем ссылки на обработчики событий
      listeners = listeners.concat(
      // Обработка событий Load и Fault
      YMaps.Events.observe(geocoder, [geocoder.Events.Load, geocoder.Events.Fault], function (geocoder) {
        if (geocoder.length()) {
          var placemark = new YMaps.Placemark(new YMaps.GeoPoint(geocoder.get(0).getGeoPoint().getX(),geocoder.get(0).getGeoPoint().getY()), {style: "default#lightbluePoint"});
          placemark.name=request.desc;
          //placemark.description = map.placemark['description'];
          _this.add(placemark);
          //_this.add(geocoder.get(0));
          map.bounds.add(geocoder.get(0).getGeoPoint());
        }
        geocodeCallCount--;
        isFinish();
      })
      );
    }
    // Функция для проверки окончания процесса геокодирования
    function isFinish () {
      // Если все объекты сгеокодированы, то генерируем событие завершения
      if (!geocodeCallCount) {
        // Событие о завершении геокодирования
        YMaps.Events.notify(_this, "Load", _this);
        // Удаление обработчиков событий
        for (var i = 0, l = listeners.length; i < l; i++) {
          listeners[i].cleanup();
        }
      }
    }
  }
var ptp = extend(MultiplyGeocoder, YMaps.GeoObjectCollection);

var georesult;
function StrToCoord(value){
  map.map.removeOverlay(georesult);
  var geocoder = new YMaps.Geocoder(value, {results:1, boundedBy: map.map.bounds});
  YMaps.Events.observe(geocoder, geocoder.Events.Load, function(){
    if(this.length()){
      georesult = this.get(0);
      map.map.addOverlay(georesult);
      map.map.setBounds(georesult.getBounds());
    }else{
      //alert("Ничего не найдено");
    }
  });
  YMaps.Events.observe(geocoder, geocoder.Events.Fault, function(geocoder, error){
    alert("Извините, пожалуйста, произошла ошибка, если вы сообщите нам о ней, мы устраним ее: "+error);
  })
} 
