// ---------------------------------------------
// Класс для работы с несколькими сокетами сразу
// только один экземпляр класса должен писать
// данные, такие как контракты, тики, остальные
// классы просто ждут время для ставки
// ---------------------------------------------
// Предназначено для использования комбинации
// демо-аккаунт + реальный счет
// ---------------------------------------------
// Все хтмл блоки располагаем в app_id
// зависимом контейнере, например, ws + app_id
// ---------------------------------------------
class WebSocketClass{
  constructor(app_id) {
    this.is_parent = true; // true если этот экземпляр пишет данные

    this.app_id = app_id;
    this.ws = null;
    this.ws_instance = null;

    this.authorized = false;
    this.active_symbols = null;
    this.subscribed_tick_ids = Array(); // по каким контрактам подписаны на тики
    this.ticks_data = {}; // тики по контрактам
    this.deals_data = {}; // сделки по контрактам

    this.delay_before_deal = {}; // замок - задержка перед следующей ставкой по контрактам
    this.charts_data = {}; // графики по контрактам
    this.stats_data = {}; // статистика по контрактам
    // ---------------------
    // Настройки Болленджера
    // ---------------------
    this.MAX_TICKS = 1000;
    this.BOLLINGER_BANDS_STEPS = 20;
    this.STANDARD_DEVIATIONS = 2;
  }
  // -------------
  // Инициализация
  // -------------
  init_websocket(){
    this.ws_instance = new WebSocket(`wss://ws.binaryws.com/websockets/v3?app_id=${app_id}&l=RU`);
    this.ws_instance.onopen = function(evt) {
      log("ws_instance.onopen", "ws opened");
      this.ws = this.ws_instance;
    };
    this.ws_instance.onmessage = function(msg) {
      var data = JSON.parse(msg.data);
      switch(data.msg_type){
        case 'ping':
          return;
        case 'authorize':
          this.authorized = data.authorize;
          this.show_account();
          return;
        case 'forget':
          log("ws_instance.onmessage", "forget subscribe");
          return;
        case 'active_symbols':
          this.active_symbols = data.active_symbols;
          this.show_active_symbols();
          break;
        case 'tick':
          this.check_subscribed_ticks(data.tick, data.subscription.id);
          // ---------------------------------------------------
          // save_new_tick(data.tick); => check_subscribed_ticks
          // Иначе тики придут и нарушат сортировку в истории
          // ---------------------------------------------------
          return;
        case 'history':
          this.save_new_ticks(data.echo_req.ticks_history, data.history);
          break;
        // ------------------------------------------
        // Заключен контракт и мы на него подписались
        // ------------------------------------------
        case 'proposal_open_contract':
          this.save_new_deal(data.proposal_open_contract);
          break;
        // -----------------
        // Покупка контракта
        // -----------------
        case 'buy':
          this.update_account(data.buy);
          break;
        default:
          break;
      }
      log("ws_instance.onmessage", data);
    };
  }
  // -------------------------------------
  // Запоминаем полученную сделку в потоке
  // -------------------------------------
  save_new_deal(data){
    // ----------------------------
    // Добавляем контракт в сделки,
    // если его там еще нет
    // ----------------------------
    var tick_symbol = data.underlying;
    if(!(tick_symbol in this.deals_data)){
      this.deals_data[tick_symbol] = Array();
    }

    for(var i=0; i<data.tick_stream.length; i++){
      var tick = data.tick_stream[i];
      data.tick_stream[i] = [local_timestamp(tick.epoch), parseFloat(tick.tick)];
    }
    // ----------------------------------------
    // Если мы выигрываем/проигрываем контракт,
    // контракт подменяется на результат ставки
    // ----------------------------------------
    //var tick_contract = data.id;
    var tick_contract = data.contract_id;
    var cur_contract = false;
    for(var i=0; i<this.deals_data[tick_symbol].length; i++){
      if(this.deals_data[tick_symbol][i].contract_id === tick_contract){
        cur_contract = true;
        this.deals_data[tick_symbol][i] = data;
      }
    }
    // ----------------------------------
    // Если это новый контракт, добавляем
    // ----------------------------------
    if(!cur_contract){
      this.deals_data[tick_symbol].push(data);
    }
  }
  // -----------------------------------
  // Запоминаем полученные тики в потоке
  // -----------------------------------
  save_new_tick(tick){
    if(!(tick.symbol in this.ticks_data)){
      this.ticks_data[tick.symbol] = Array();
    }
    var new_tick = [local_timestamp(tick.epoch), parseFloat(tick.quote)];

    this.ticks_data[tick.symbol].push(new_tick);
    if(this.ticks_data[tick.symbol].length > this.MAX_TICKS){
      this.ticks_data[tick.symbol].shift();
    }
    // ----------------------------
    // Докидываем боллинджера в тик
    // третий элемент массива в
    // каждом тике со словарем
    // ----------------------------
    var prices = Array();
    for(var i=0; i<this.ticks_data[tick.symbol].length; i++){
      prices.push(this.ticks_data[tick.symbol][i][1]);
    }
    for(var i=0; i<this.ticks_data[tick.symbol].length; i++){
      var cur_tick = this.ticks_data[tick.symbol][i];
      if(cur_tick.length < 3){
        // -------------------
        // Линии болленджера
        // top, middle, bottom
        // -------------------
        var bb = bollinger_bands(prices, i, this.BOLLINGER_BANDS_STEPS, this.STANDARD_DEVIATIONS);
        this.ticks_data[tick.symbol][i].push(bb);
      }
    }
  }
  // ----------------------------------------
  // Делаем ставку, т/к условия удовлетворены
  // symbol - контракт, type = PUT|POST
  // ----------------------------------------
  buy_from_playboy(symbol, type){
    // -----------------------
    // Делаем ставку,
    // что там по мартингейлу?
    // -----------------------
    var deal_params = {
      "contract_type": type,
      "amount": this.calc_rates(symbol),
    }
    this.buy(symbol, deal_params);
    var date = new Date();
    var now = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds() + " " + date.getDate() + "/" + date.getMonth() + "/" + date.getFullYear();
    $("#analytics").append($("<p>" + " " + now + " " + symbol + " " + type + " ставка " + deal_params['amount'] + "</p>"));
  }
  // ----------------------------------
  // Покупка =>
  // Цена пересекает среднюю линию
  // канала Боллинджера или касается ее
  // После этого касается крайней
  // линии канала Боллинджера
  // Покупка делается противоположно
  // ----------------------------------
  playboy(symbol){
    // -----------------------------------
    // Ищем по контракту последнюю сделку,
    // от нее считать будем
    // -----------------------------------
    var epoch = 0;
    var last_deal = null;
    var last_deal_len = this.deals_data[symbol].length;
    if(last_deal_len !== 0){
      // --------------------------------
      // Если последняя сделка еще
      // не завершена, тогда пока ожидаем
      // --------------------------------
      last_deal = this.deals_data[symbol][last_deal_len - 1];
      if(last_deal.status === "open"){
        return;
      }
      epoch = local_timestamp(this.deals_data[symbol][last_deal_len - 1].date_expiry);
    }
    // ---------------------------------
    // Проверяем последний тик,
    // должно быть касание верхней линии
    // ---------------------------------
    var ticks_len = this.ticks_data[symbol].length;
    if(ticks_len < 10){
      return;
    }
    var last_tick = this.ticks_data[symbol][ticks_len-1];

    var bb = last_tick[2];
    if(last_tick[1] > bb[0]){
      // ---------------------------------------------------
      // Если после предыдущей сделки не был касание центра,
      // то защищаемся от тренда и не делаем ставку
      // ---------------------------------------------------
      if(last_deal !== null){
        // ---------------------------
        // Идем в обратном направлении
        // Ищем пересечение центра
        // ---------------------------
        for(var i=(ticks_len-1); i>=0; i--){
          var tick = this.ticks_data[symbol][i];
          bb = tick[2];
          // -------------------
          // Пересечения не было
          // -------------------
          if(epoch > tick[0]){
            break;
          }
          // ----------------
          // Пересечение было
          // ----------------
          if(tick[1] <= bb[1]){
            this.buy_from_playboy(symbol, "PUT");
            break;
          }
        }
      }else{
        this.buy_from_playboy(symbol, "PUT");
      }
    }else if(last_tick[1] < bb[2]){
      // ----------------------------------------------------
      // Если после предыдущей сделки не было касание центра,
      // то защищаемся от тренда и не делаем ставку
      // ----------------------------------------------------
      if(last_deal !== null){
        // ---------------------------
        // Идем в обратном направлении
        // Ищем пересечение центра
        // ---------------------------
        for(var i=(ticks_len-1); i>=0; i--){
          var tick = this.ticks_data[symbol][i];
          bb = tick[2];
          // -------------------
          // Пересечения не было
          // -------------------
          if(epoch > tick[0]){
            break;
          }
          // ----------------
          // Пересечение было
          // ----------------
          if(tick[1] >= bb[1]){
            this.buy_from_playboy(symbol, "CALL");
            break;
          }
        }
      }else{
        this.buy_from_playboy(symbol, "CALL");
      }
    }
  }
  // ----------------------------------------
  // Рассчитываем сколько раз мы уже серанули
  // ----------------------------------------
  get_loose_count(symbol){
    var loose_count = 1;
    for(var i=(this.deals_data[symbol].length-1); i>=0; i--){
      var deal = this.deals_data[symbol][i];
      if(deal.status === "lost"){
        loose_count += 1;
      }else{
        // -----------------------------------
        // Тут непонятка - если мы в сделке,
        // то будет всегда digit возвращаться,
        // но лучше так
        // -----------------------------------
        break;
      }
    }
    return loose_count;
  }
  // ----------------------------------
  // Высчитываем с помощью мартингейла
  // сколько мы должны сейчас поставить
  // ----------------------------------
  calc_rates(symbol){
    var digit = 0.35;
    var max_loose_count = 5;
    var multiply = 2; // Множитель
    var loose_count = this.get_loose_count(symbol);
    // -------------------------------------
    // Если умудрились max раз подряд всрать
    // пишем в статистику
    // -------------------------------------
    if(loose_count > this.stats_data[symbol].max_loose_in_sequence){
      this.stats_data[symbol].max_loose_in_sequence = loose_count;
    }
    while(loose_count > max_loose_count){
      loose_count = loose_count - max_loose_count;
    }
    return martingail(digit, loose_count, multiply);
  }
  // -------------------------------------
  // Запоминаем полученные тики по истории
  // -------------------------------------
  save_new_ticks(symbol, history){
    // ----------------
    // Обнуляем массивы
    // ----------------
    this.ticks_data[symbol] = Array();
    this.deals_data[symbol] = Array();
    // ---------------------
    // Подготавливаем массив
    // ---------------------
    for(var i=0; i<history.prices.length; i++){
      var tick = {
        symbol: symbol,
        quote: history.prices[i],
        epoch: history.times[i],
      };
      this.save_new_tick(tick);
    }
    // -----------------
    // Создаем диаграмму
    // -----------------
    if($("#chart_" + tick.symbol).length < 1){
      this.create_chart(tick.symbol);
    }
  }
  // ----------------------------------
  // Если приходят какие то тики,
  // то добавляем айди потоков в массив
  // Сохраняем по 1 тику здесь, чтобы
  // не сохранять их раньше чем зайдет
  // вся история и сортировка нарушится
  // ----------------------------------
  check_subscribed_ticks(tick, id){
    for(var i=0; i<this.subscribed_tick_ids.length; i++){
      if(this.subscribed_tick_ids[i][0] === tick.symbol && this.subscribed_tick_ids[i][1] === id){
        this.save_new_tick(tick);
        // ------------
        // И ... играем
        // ------------
        this.playboy(tick.symbol);
        return;
      }
    }
    this.subscribed_tick_ids.push([tick.symbol, id]);
    // ------------------------------------------
    // Запрашиваем историю по тикам для контракта
    // ------------------------------------------
    this.get_ticks_history(tick.symbol);
  }
  // ----------------------------
  // Запрашиваем историю по тикам
  // ----------------------------
  get_ticks_history(symbol){
    this.send({
      "ticks_history": symbol,
      "end": "latest",
      "start": 1,
      "style": "ticks",
      "adjust_start_time": 1,
      "count": this.MAX_TICKS,
    })
  }
  // ---------------------------------
  // Показываем информацию об аккаунте
  // после того как авторизовались
  // ---------------------------------
  show_account(){
    var container = $(`#authorized_${app_id}`);
    if(container.length == 0){
      $("body").append($(`<div id='authorized_${app_id}'></div>`));
      container = $("#authorized_" + app_id);
    }
    container.html(`
      <p class='balance' data-balance='${this.authorized.balance}'>Баланс: ${this.authorized.balance}</p>
      <p>email: ${this.authorized.email}</p>
      <p>is_virtual: ${this.authorized.is_virtual}</p>
      <p>scopes: ${this.authorized.scopes.join(", ")}</p>
    `);
    var container_analytics = $(`#analytics_${app_id}`);
    if(container_analytics.length == 0){
      $("body").append($(`<div id='analytics_${app_id}'></div>`));
      container_analytics = $("#authorized_" + app_id);
    }
    container_analytics.append($(`<p>Начинаем, баланс ${this.authorized.email} : ${this.authorized.balance}</p>`));
  }
  // --------------------------------
  // Обновляем информацию об аккаунте
  // data = {'balance_after':1000.00}
  // --------------------------------
  update_account(data){
    var container_name = `#authorized_${app_id}`;
    $(`${container_name} .balance`).html(`Баланс: ${data.balance_after}`);
    $(`${container_name} .balance`).attr("data-balance", data.balance_after);
    $(`#analytics_${app_id}`).append($(`<p>Баланс: ${data.balance_after}</p>`));
  }
  // ---------------------------------
  // Сгруппировать возможные контракты
  // Вывести возможные контракты
  // ---------------------------------
  show_active_symbols(){
    var result = {};
    var container = $("#active_symbols");
    for(var i=0; i<this.active_symbols.length; i++){
      var active_symbol = this.active_symbols[i];
      // ------
      // Маркет
      // ------
      var market = active_symbol.market;
      var market_container = container.find("#market_" + market);
      if((market_container).length < 1){
        container.append($(
          `<div class='market' id='market_${market}'>
            <h2>${active_symbol.market_display_name}</h2>
          </div>`)
        );
      }
      // ---------
      // Субмаркет
      // ---------
      var submarket = active_symbol.submarket;
      market_container = container.find("#market_" + market);
      var submarket_container = market_container.find("#submarket_" + submarket);
      if((submarket_container).length < 1){
        market_container.append($(
          `<div class='submarket' id='submarket_${submarket}'>
            <h3>${active_symbol.submarket_display_name}</h3>
          </div>`)
        );
      }
      // ------
      // Индекс
      // ------
      var symbol = active_symbol.symbol;
      submarket_container = market_container.find("#submarket_" + submarket);
      var symbol_container = submarket_container.find("#symbol_" + symbol);
      if((symbol_container).length < 1){
        submarket_container.append($(
          `<div class='symbol' id='symbol_${symbol}'>
            <label for='symbol_${symbol}_checkbox'>
              <input type='checkbox' name='symbol_${symbol}' class='checkbox_symbol' id='symbol_${symbol}_checkbox' data-symbol='${symbol}' id='subscribe_ticks_stream_${symbol}' >
              ${active_symbol.display_name}
            </label>
          </div>`)
        );
        $(`#subscribe_ticks_stream_${symbol}`).change(function(){
          this.subscribe_ticks_stream();
        });
      }
    }
    $("#symbol_R_50_checkbox").click();
    return result;
  }
  // ----------
  // Пингуем ws
  // ----------
  ping(){
    if(this.ws !== null){
      if(this.active_symbols === null){
        this.get_active_symbols();
        return;
      }
      if(!this.authorized){
        this.authorize();
        return;
      }
      this.send({ping: 1});
    }
  }
  // -----------
  // Авторизация
  // -----------
  authorize(){
    this.send({
      "authorize": ws_tokens[0],
    });
  }
  // ------------------
  // Отправка сообщения
  // ------------------
  send(msg){
    this.ws.send(JSON.stringify(msg)); // {ticks:'R_100'}
  }
  // -----------------------------------------
  // Проверить все тиковые потоки и на нужные
  // подписаться (где стоит галка), а от
  // ненужных - отписаться
  // TODO повешать на класс???
  // -----------------------------------------
  subscribe_ticks_stream(){
    $(".symbol .checkbox_symbol").each(function(){
      var symbol = $(this).attr("data-symbol");
      var subscribe = 0;
      if($(this).prop("checked")){
        // ------------------------------------
        // Не подписываемся, если уже подписаны
        // ------------------------------------
        var already_subscribed = false;
        for(var i=0; i<this.subscribed_tick_ids.length; i++){
          if(this.subscribed_tick_ids[i][0] === symbol){
            already_subscribed = true;
          }
        }
        if(!already_subscribed){
          log("subscribe_ticks_stream", "RUN=>" + symbol);
          this.send({
            ticks: symbol,
            subscribe: 1,
          });
        }
      }else{
        for(var i=0; i<this.subscribed_tick_ids.length; i++){
          if(this.subscribed_tick_ids[i][0] === symbol){
            this.send({
              "forget": this.subscribed_tick_ids[i][1],
            });
            this.subscribed_tick_ids.splice(i, 1);
            break;
          }
        }
      }
    });
  }
  // ----------------------------
  // Получаем возможные контракты
  // ----------------------------
  get_active_symbols(){
    this.send({
      active_symbols: "brief",
      product_type: "basic",
    });
  }
  // -----------------
  // Создаем диаграмму
  // -----------------
  create_chart(symbol){
    $("#charts").append($(`<div id="chart_${symbol}"></div>`));
    var data = [{ // 0
        id: "series_" + symbol,
        name: symbol,
        data: [],
      }, { // 1
        name: 'Bollinger',
        data: [],
        color: Highcharts.getOptions().colors[0],
        marker: {
          enabled: false
        }
      }, { // 2
        name: 'BollingerBands',
        data: [],
        type: 'arearange',
        lineWidth: 0,
        linkedTo: ':previous',
        color: Highcharts.getOptions().colors[0],
        fillOpacity: 0.15,
        zIndex: 0,
        marker: {
          enabled: false
        }
      }, { // 3
        type: 'flags',
        name: 'Сделки',
        data: [],
        onSeries: "series_" + symbol,
        width: 32,
      }];
    var tick = null;
    for(var i=0; i<this.ticks_data[symbol].length; i++){
      tick = this.ticks_data[symbol][i];
      data[0].data.push([tick[0], tick[1]]);
      var bb = tick[2];
      data[1].data.push([tick[0], bb[1]]);
      data[2].data.push([tick[0], bb[0], bb[2]]);
    }
    var myChart = Highcharts.chart('chart_' + symbol, {
      chart: {
        height:600,
      },
      tooltip: {
        crosshairs: true,
        shared: true,
      },
      title: {
        text: symbol,
      },
      navigator: {
        enabled: true,
      },
      scrollbar: {
        enabled: true,
      },
      rangeSelector: {
        enabled: true,
      },
      xAxis: {
        type: 'datetime',
        range: 60 * 1000 // 60 sec
      },
      series: data,
      plotOptions: {
        series: {
          allowPointSelect: true,
        }
      },
    });
    // --------------------------
    // Записываем график в массив
    // --------------------------
    if(this.charts_data[symbol] === undefined){
      this.charts_data[symbol] = myChart;
    }
    // ------------------------------
    // Записываем статистику в массив
    // ------------------------------
    if(this.stats_data[symbol] === undefined){
      this.stats_data[symbol] = {
        "started": Date.now(),
        "max_loose_in_sequence": 0,
      };
    }
    var interval = setInterval(function() {
      var cur_tick = null;
      var shift = false;
      var redraw = false;

      for(var i=0; i<this.ticks_data[symbol].length; i++){
        cur_tick = this.ticks_data[symbol][i];
        if(cur_tick[0] > tick[0]){
          tick = cur_tick;
          myChart.series[0].addPoint([tick[0], tick[1]], redraw, shift);
          var bb = tick[2];
          myChart.series[1].addPoint([tick[0], bb[1]], redraw, shift);
          myChart.series[2].addPoint([tick[0], bb[0], bb[2]], redraw, shift);
        }
      };
      // ----------------
      // Флаги для сделок
      // ----------------
      var deals_data_len = this.deals_data[symbol].length;
      for(var i=0; i<deals_data_len; i++){
        var deal = this.deals_data[symbol][i];
        // ------------------------
        // Если сделка завершена
        // и обработана, пропускаем
        // ------------------------
        if(deal.processed === 1){
          continue;
        }
        // ---------------------------
        // Название флага (вверх/вниз)
        // ---------------------------
        var title = "↓";
        if(deal.contract_type == "CALL"){
          title = "↑";
        }
        // ---------------------
        // Выбираем цвет флага
        // Выбираем исход сделки
        // ---------------------
        var color = "#000000";
        var status = ""
        switch(deal.status){
          case "won":
            color = "#00FF00";
            status = "+"
            break;
          case "lost":
            color = "#FF0000";
            status = "-"
            break;
          default:
            break;
        }
        title += " " + status;
        if(deal.tick_stream.length > 0){
          var dd = deal.tick_stream[0];
          // ----------------------------------------
          // Проверка на то, что точка уже на графике
          // ----------------------------------------
          var index = myChart.series[3].xData.indexOf(dd[0]);
          if(index === -1){
            myChart.series[3].addPoint({
              x: dd[0],
              title: title,
              color: color,
              text: 'Цена: ' + deal.buy_price + '<br />Статус: Сделка открыта' + '<br />Значение:' + dd[1],
            }, redraw, shift);
          }
        }
        // ----------------------------------
        // Если сделка закрыта,
        // тогда отмечаем ее как обработанную
        // ----------------------------------
        if(deal.status !== "open"){
          deal.processed = 1;
          // ---------------------------
          // Показываем результат сделки
          // ---------------------------
          var tick_stream_len = deal.tick_stream.length;
          if(tick_stream_len > 0){
            var dd = deal.tick_stream[tick_stream_len-1];
            myChart.series[3].addPoint({
              x: dd[0],
              title: title,
              color: color,
              text: 'Цена: ' + deal.buy_price + '<br />Статус: ' + status + '<br />Значение:' + dd[1],
            }, redraw, shift);
          }
          // -----------------------------------
          // Обновить баланс при успешной сделке
          // -----------------------------------
          if(deal.status === "won"){
            var balance = $("#authorized .balance").attr("data-balance");
            var balance_after = parseFloat(balance) + deal.payout;
            this.update_account({'balance_after':balance_after.toFixed(2)});
            $("#analytics").append($("<p>Выигрыш</p><p>---</p>"));
          }else{
            $("#analytics").append($("<p>Проигрыш</p><p>---</p>"));
          }
        }
      };
      // -------------------------
      // Перерисовка по завершению
      // -------------------------
      myChart.redraw();
    }, 1000);
  }
  // ------------------------------
  // Покупка
  // params - параметры для сделки:
  // ------------------------------
  buy(contract, params){
    // ---------------------------------
    // Задержка перед следующей покупкой
    // ---------------------------------
    if(this.delay_before_deal[contract] === undefined){
      this.delay_before_deal[contract] = 0;
    }else{
      var now = Date.now();
      if(now <= this.delay_before_deal[contract]){
        console.log("[WARN]: delay before deal");
        return;
      }
    }
    console.log(params);
    var deal_params = {
      "symbol": contract,
      "duration_unit": "t", // m
      "duration": 5, // 1
      "contract_type": "CALL", // PUT
      "basis": "stake", // payout
      "currency": "USD",
      "amount": "0.35",
      // "date_start":date_start, # Отложенные контракты должны начинаться позднее, чем через 5 минут от настоящего момента.
    }
    // -------------------------------------
    // Переопределение параметров для сделки
    // -------------------------------------
    if(params !== undefined){
      if(params['contract_type']){
        deal_params['contract_type'] = params['contract_type'];
      }
      if(params['amount']){
        deal_params['amount'] = params['amount'];
      }
    }

    var deal = {"parameters": deal_params};
    deal['price'] = deal_params['amount'];
    deal['buy'] = 1;
    deal['subscribe'] = 1;
    console.log("[DEAL]:", deal);
    this.delay_before_deal[contract] = Date.now() + 5000; // 5 сек задержка
    this.send(deal);
  }
}