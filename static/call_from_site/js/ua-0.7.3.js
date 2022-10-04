var elements = {
  configForm:      document.getElementById('config-form'),
  uaStatus:        document.getElementById('ua-status'),
  sessionList:     document.getElementById('session-list'),
  sessionTemplate: document.getElementById('session-template')
};

var config = window.sip_config !== undefined ? window.sip_config : {
  traceSip: false,
  register: false,
  userAgentString: 'sipjs',
  // без stun будет INCOMPATIBLE DESTINATION (candidates)
  stunServers: [],
};
console.log('---', config, '---');

var ua;
var sessionUIs = {};
var active_session = null;

var call_timer = 0;
var elapsed = setInterval(function(){
  if(active_session){
    call_timer += 1;
    update_call_timer();
  }
}, 1000);

var phone_prefix = null;
function set_phone_prefix(prefix){
  phone_prefix = prefix;
}

var call_controls = null;
function set_call_controls(cb, hb, ctimer){
  var hb_html = hb.html();
  call_controls = {
    "cb":cb,
    "hb":hb,
    "ctimer":ctimer
  }
  call_controls.start_call = function(){
    call_controls.cb.hide();
    call_controls.hb.show();
  }
  call_controls.end_call = function(){
    call_controls.cb.show();
    call_controls.hb.hide();
    call_timer = 0;
  }
  call_controls.update_call_timer = function(){
    var hours = parseInt(call_timer / 60);
    var seconds = call_timer - (hours*60);
    if(hours < 10){
      hours = "0" + hours;
    }
    if(seconds < 10){
      seconds = "0" + seconds;
    }
    ctimer.html(hours + ":" + seconds);
  }
  return call_controls;
}
function start_call(){
  if(call_controls != null){
    call_controls.start_call();
  }
}
function end_call(){
  if(call_controls != null){
    call_controls.end_call();
  }
}
function update_call_timer(){
  if(call_controls != null){
    call_controls.update_call_timer();
  }
}
function stopRingTone() {
  //try {ringtone.pause();}
  //catch (e) { }
  try {ringbacktone.pause();}
  catch (e) { }
}
function startRingTone() {
  try { ringbacktone.play(); }
  catch (e) { }
}

// ---------------------
// Подключение к серверу
// ---------------------
function connect_to_server(callback_function){
  var form, i, l, name, value;
  form = elements.configForm;

  for (i = 0, l = form.length; i < l; i++) {
    name = form[i].name;
    value = form[i].value;
    if (value !== '') {
      config[name] = value;
    }
  }
  elements.uaStatus.innerHTML = 'Connecting...';
  ua = new SIP.UA(config);
  ua.on('connected', function () {
    elements.uaStatus.innerHTML = 'Connected (Unregistered)';
    // --------------------------
    // вызываем callback_function
    // --------------------------
    if(typeof(callback_function) === "function"){
      callback_function();
    }
  });
  ua.on('registered', function () {
    elements.uaStatus.innerHTML = 'Connected (Registered)';
  });
  ua.on('unregistered', function () {
    elements.uaStatus.innerHTML = 'Connected (Unregistered)';
  });
  ua.on('invite', function (session) {
    createNewSessionUI(session.remoteIdentity.uri, session);
  });
  //if(typeof(connect_to_server_callback == "function")){
    //connect_to_server_callback();
  //}
}
// ----------------------
// Отключиться от сервера
// ----------------------
function unregister(){
  if (!ua) return;
  if (ua.isRegistered()) {
    ua.unregister();
  }
}
// -------------
// Набрать номер
// -------------
function make_call(phone_number) {
  if(active_session){
    console.log("ALREADY IN CALL");
    return "Сначала завершите текущий звонок";
  }
  // ---------------------------------
  // Телефон уже должен быть обработан
  // ---------------------------------
  var uri = "";
  for(var i=0; i<phone_number.length; i++){
    if("0123456789".indexOf(phone_number[i]) > -1){
      uri += phone_number[i];
    }
  }
  console.log("uri=>", uri);
  if (!uri) return "Неправильно набран номер";

  if (uri.length > 11){
    return "Максимум 11 цифр";
  }
  if (uri.length < 6){
    return "Минимум 6 цифр";
  }
  if (uri.length > 6 && uri.length < 10){
    return "Номер может быть только из 6,10 или 11 цифр";
  }

  if (uri.length == 6 && phone_prefix != null){
    uri = prefix + uri;
  }else if (uri.length == 10 && phone_prefix != null){
    uri = prefix.substring(0, 1) + uri;
  }

  // Send invite
  active_session = ua.invite(uri, {
    media: {
      constraints: {
        audio: true,
        video: false,
      }
    }
  });

  // Create new Session and append it to list
  var ui = createNewSessionUI(uri, active_session);
  start_call();
  startRingTone();
  return 1;
}
// ----------------
// Завершить звонок
// ----------------
function hangup_call(){
  end_call();
  if (!active_session) {
    console.log("session is null");
    return;
  } else if (active_session.startTime) { // Connected
    console.log("________________________session startTime " + active_session.startTime);
    active_session.bye();
  } else if (active_session.reject) { // Incoming
    console.log("________________________session incoming");
    active_session.reject();
  } else if (active_session.cancel) { // Outbound
    console.log("________________________session outbound");
    active_session.cancel();
  }
}
// --------------
// Отправить DTMF
// --------------
function send_dtmf(value){
  if (value === '' || !active_session) return;
  if (['0','1','2','3','4','5','6','7','8','9','*','#'].indexOf(value) > -1) {
    active_session.dtmf(value);
  }
}

function createNewSessionUI(uri, session) {
  var tpl = elements.sessionTemplate;
  var node = tpl.cloneNode(true);
  var sessionUI = {};

  uri = session ?
    session.remoteIdentity.uri :
    SIP.Utils.normalizeTarget(uri, ua.configuration.hostport_params);

  if (!uri) { return; }

  // Save a bunch of data on the sessionUI for later access
  sessionUI.session        = session;
  sessionUI.node           = node;
  sessionUI.video          = node.querySelector('video');

  sessionUI.displayName    = node.querySelector('.display-name');
  sessionUI.uri            = node.querySelector('.uri');
  sessionUI.green          = node.querySelector('.green');
  sessionUI.red            = node.querySelector('.red');
  sessionUI.gray           = node.querySelector('.gray');
  sessionUI.gray_transfer  = node.querySelector('.gray_transfer');
  sessionUI.dtmf           = node.querySelector('.dtmf');
  sessionUI.dtmfInput      = node.querySelector('.dtmf input[type="text"]');
  sessionUI.video          = node.querySelector('video');
  sessionUI.messages       = node.querySelector('.messages');

  sessionUI.renderHint     = {
    remote: sessionUI.video
  };
  sessionUIs[uri] = sessionUI;
  // Update template
  node.classList.remove('template');

  // SIP.js event listeners
  function setUpListeners(session) {

    if (session.accept) {
      sessionUI.green.disabled = false;
      sessionUI.green.innerHTML = "<i class=\"icon-thumbs-up\"></i>";
      sessionUI.red.innerHTML = "<i class=\"icon-thumbs-down\"></i>";
      // Дилинь-дилинь
      startRingTone();
    } else {
      sessionUI.green.innerHMTL = "x";
      sessionUI.red.innerHTML = "<i class=\"icon-thumbs-down\"></i>";
      // Дилинь-дилинь
      stopRingTone();
    }

    session.on('accepted', function () {
      session.mediaHandler.render(sessionUI.renderHint);
      stopRingTone();
    });

    session.mediaHandler.on('addStream', function () {
      session.mediaHandler.render(sessionUI.renderHint);
    });

    session.on('bye', function () {
      delete sessionUI.session;
      active_session = null;
      end_call();
      stopRingTone();
    });
    session.on('failed', function () {
      delete sessionUI.session;
      active_session = null;
      end_call();
      stopRingTone();
    });
    session.on("rejected", function () {
      delete sessionUI.session;
      active_session = null;
      end_call();
      stopRingTone();
    });
    // Отмена исходящего звонка
    session.on("cancel", function () {
      delete sessionUI.session;
      active_session = null;
      end_call();
      stopRingTone();
    });


    session.on('refer', function handleRefer (request) {
      var target = request.parseHeader('refer-to').uri;
      session.bye();

      createNewSessionUI(target, ua.invite(target, {
        media: {
          constraints: {
            audio: true,
            video: false
          }
        }
      }));
    });
  }

  if (session) {
    setUpListeners(session);
  }
  // Add node to live session list
  elements.sessionList.appendChild(node);
}
