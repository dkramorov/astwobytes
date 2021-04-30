var myMapContainer = "mapContainer";

// ----------------------
// Скролл к нужной секции
// ----------------------
function scroll_to(section, offset){
  if(typeof(offset) == "undefined"){
    offset = 0;
  }
  $("html, body").animate({
    scrollTop: $(section).offset().top + offset
  }, 500);
  console.log("scrolling to " + section + " " + $(section).offset().top);
}

function search_dealers_listener(search_arr){
  var search_field = $("#search_dealer_field");
  search_field.keyup(function(){
    var queries = search_field.val().split(" ");
    var q_arr = Array();
    var q;
    var cities = Array();
    for(var i=0; i<queries.length; i++){
      q = queries[i].toLowerCase();
      q = $.trim(q);
      if(q.length > 0){
        q_arr.push(q);
      }
    }

    var item;
    var is_visible = true;
    for(var i=0; i<search_arr.length; i++){
      is_visible = true;
      item = search_arr[i];
      for(var j=0; j<q_arr.length; j++){
        if(item['terms'].indexOf(q_arr[j]) < 0){
          $("#dealer_row_" + item['id']).hide();
          is_visible = false;
          break;
        }
      }
      if(is_visible){
        if(cities.indexOf(item['city_id']) < 0){
          cities.push(item['city_id']);
        }
        $("#dealer_row_" + item['id']).show();
      }
    }
    $(".city_row").hide();
    for(var i=0; i<cities.length; i++){
      $("#city_row_" + cities[i]).show();
    }
  })
}

function create_dealers_map(){
  var kwargs = {};
  kwargs['default_town'] = "Иркутск";

  create_new_map(myMapContainer);
  wait_for_result(myMapContainer, function(){
    var myMap = get_map(myMapContainer);
    disable_map_wheel(myMapContainer);
    myMap.kwargs = kwargs;
    var point;

    var search_arr = [];

    if(typeof(mapContainer_points) != "undefined"){
      for(var i=0; i<mapContainer_points.length; i++){
        point = mapContainer_points[i];
        myMap.myPoints.push(point);

        search_arr.push({
          'id': point['id'],
          'terms': point['terms'],
          'city_id': point['city_id'],
        });

        $("#dealer_address_" + point['id']).click(function(){
          scroll_to("#dealers_title");
          var pk = $(this).attr("id").replace("dealer_address_", "");
          var placemark = find_placemark_by_id(pk, myMap);
          console.log("placemark", placemark);
          if(placemark != null){
            var props = placemark['properties'];
            var coords = placemark['geometry']['coordinates'];
            if(myMap.balloon.isOpen()){
              myMap.balloon.close();
            }
            myMap.balloon.open(coords, props['balloonContent'], {});
            myMap.setCenter(coords, 16);
          }else{
            console.log("placemark is null", pk);
          }
        });
      }
      add_points_to_map(myMapContainer, mapContainer_points);
      set_map_bounds(myMapContainer)

      search_dealers_listener(search_arr);
    }else{
      console.log("[ERROR]: mapContainer_points undefined");
    }

  }, ["map"]);
}
$(document).ready(function(){
  if($("#" + myMapContainer).length > 0){
    //create_dealers_map();
    load_yandex_maps_script(yandex_maps_api_key, create_dealers_map);
  }
  $(".nav-item").click(function(){
    if($("#product_props").length > 0){
      scroll_to("#product_props", -100);
    }
  });
});

