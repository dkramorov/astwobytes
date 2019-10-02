// ---------------------------
// Класс для покупки контракта
// ---------------------------
class WebSocketShopperClass{
  constructor(app_id, token) {
    this.app_id = app_id;
    this.ws = null;
    this.ws_instance = null;
    this.authorized = false;
    this.ws_token = token;
    this.label = 'WebSocketShopperClass';
    this.deals_data = {}; // сделки по контрактам
    this.stats_data = {}; // статистика по контрактам
  }
  // -------------
  // Инициализация
  // -------------
  init_websocket(){
    var this_class = this;
    this.ws_instance = new WebSocket(`wss://ws.binaryws.com/websockets/v3?app_id=${this.app_id}&l=RU`);
    this.ws_instance.onopen = function(evt) {
      log(this_class.label, "ws opened");
      this_class.ws = this;
    };
    this.ws_instance.onmessage = function(msg) {
      var data = JSON.parse(msg.data);
      switch(data.msg_type){
        case 'ping':
          return;
        case 'authorize':
          this_class.authorized = data.authorize;
          this_class.show_account();
          return;
        // ------------------------------------------
        // Заключен контракт и мы на него подписались
        // ------------------------------------------
        case 'proposal_open_contract':
          this_class.save_new_deal(data.proposal_open_contract);
          break;
        // -----------------
        // Покупка контракта
        // -----------------
        case 'buy':
          this_class.update_account(data.buy);
          break;
        default:
          break;
      }
      log(`${this_class.label}.onmessage`, data);
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
  // ----------------------------------------
  // Делаем ставку, т/к условия удовлетворены
  // symbol - контракт, type = PUT|POST
  // ----------------------------------------
  buy_from_playboy(symbol, type){
    if(!(symbol in this.deals_data)){
      this.deals_data[symbol] = Array();
      // ------------------------------
      // Записываем статистику в массив
      // ------------------------------
      this.stats_data[symbol] = {
        "started": Date.now(),
        "max_loose_in_sequence": 0,
      };
    }

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
    $(`#analytics_${this.app_id}`).append($("<p>" + " " + now + " " + symbol + " " + type + " ставка " + deal_params['amount'] + "</p>"));
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
        // ------------------------------------
        // Если какая то сделка без информации,
        // пропускаем ее
        // ------------------------------------
        if(deal.status === "open"){
          continue;
        }
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
  // ---------------------------------
  // Показываем информацию об аккаунте
  // после того как авторизовались
  // ---------------------------------
  show_account(){
    var container = $(`#authorized_${this.app_id}`);
    if(container.length == 0){
      $("body").append($(`<div id='authorized_${this.app_id}'></div>`));
      container = $(`#authorized_${this.app_id}`);
    }
    container.html(`
      <p class='balance' data-balance='${this.authorized.balance}'>Баланс: ${this.authorized.balance}</p>
      <p>email: ${this.authorized.email}</p>
      <p>is_virtual: ${this.authorized.is_virtual}</p>
      <p>scopes: ${this.authorized.scopes.join(", ")}</p>
    `);
    var container_analytics = $(`#analytics_${this.app_id}`);
    if(container_analytics.length == 0){
      $("body").append($(`<div id='analytics_${this.app_id}' class='col-md-6 analytics'></div>`));
      container_analytics = $(`#authorized_${this.app_id}`);
    }
    container_analytics.append($(`<p>Начинаем, баланс ${this.authorized.email} : ${this.authorized.balance}</p>`));
  }
  // --------------------------------
  // Обновляем информацию об аккаунте
  // data = {'balance_after':1000.00}
  // --------------------------------
  update_account(data){
    var container_name = `#authorized_${this.app_id}`;
    $(`${container_name} .balance`).html(`Баланс: ${data.balance_after}`);
    $(`${container_name} .balance`).attr("data-balance", data.balance_after);
    $(`#analytics_${this.app_id}`).append($(`<p>Баланс: ${data.balance_after}</p>`));
  }
  // ----------
  // Пингуем ws
  // ----------
  ping(){
    if(this.ws !== null){
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
      "authorize": this.ws_token,
    });
  }
  // ------------------
  // Отправка сообщения
  // ------------------
  send(msg){
    this.ws.send(JSON.stringify(msg)); // {ticks:'R_100'}
  }
  // ------------------------------
  // Покупка
  // params - параметры для сделки:
  // ------------------------------
  buy(contract, params){
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
    this.send(deal);
  }
}