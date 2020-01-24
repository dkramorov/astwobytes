var elements = {
  configForm:      document.getElementById('config-form'),
  uaStatus:        document.getElementById('ua-status'),
  //registerButton:  document.getElementById('ua-register'),
  registerCheckbox:  document.getElementById('ua_register'),
  newSessionForm:  document.getElementById('new-session-form'),
  inviteButton:    document.getElementById('ua-invite-submit'),
  uaVideo:         document.getElementById('ua-video'),
  uaURI:           document.getElementById('ua-uri'),
  sessionList:     document.getElementById('session-list'),
  sessionTemplate: document.getElementById('session-template'),
  messageTemplate: document.getElementById('message-template')
};
var z = 0;
var config = window.sip_config !== undefined ? window.sip_config : {
  traceSip: false,
  register: true,
  userAgentString: 'sipjs',
};
console.log('---', config, '---');

var mediaConstraints = {
  audio: true,
  video: false
};

var ua;
var sessionUIs = {};

function startRingTone() {
  try {
    ringtone.play();
    Notification.requestPermission( function(status) {
      console.log(status);
      var n = new Notification("Звонок!", {body: "Возьмите трубку"});
    });
  }
  catch (e) { }
}
function stopRingTone() {
  try {ringtone.pause();}
  catch (e) { }
  try {ringbacktone.pause();}
  catch (e) { }
}
function startRingbackTone() {
  try { ringbacktone.play(); }
  catch (e) { }
}

if(window.set_status === undefined){
  console.log("[ERROR]: you not define set_status function ---");
  window.set_status = function(state){
    /* DEMO:
    $.ajax({
      url: "/oper/freeswitch/",
      type: "GET",
      //dataType: "json",
      data: "action=set_status&state=" + state,
      success: function(response) {
        console.log('[SET STATUS]:', response);
      }
    });
    */
    console.log('dummy set status', state);
  }
}

function connect_to_server(callback_function){
  var form, i, l, name, value;
  elements.registerCheckbox.checked = false;

  form = elements.configForm;

  for (i = 0, l = form.length; i < l; i++) {
    name = form[i].name;
    value = form[i].value;
    if (name !== 'configSubmit' && value !== '') {
      config[name] = value;
    }
  }

  ua = new SIP.UA(config);

  ua.on("connected", function () {
    elements.uaStatus.className = "btn--color-red";
    elements.registerCheckbox.checked = false;
    // --------------------------
    // вызываем callback_function
    // --------------------------
    if(typeof(callback_function) === "function"){
      callback_function();
    }
  });

  // ---------
  //state_vars = {1:"'Logged Out'", 2:"'Available'", 3:"'Available (On Demand)'", 4:"'On Break'"}
  // ---------
  ua.on("registered", function () {
    elements.uaStatus.className = "btn--color-green";
    //elements.uaStatus.innerHTML = "Активен";
    elements.registerCheckbox.checked = true;
    set_status(2);
  });

  ua.on("unregistered", function () {
    elements.uaStatus.className = "btn--color-red";
    //elements.uaStatus.innerHTML = "Подключено (не активен)";
    elements.registerCheckbox.checked = false;
    set_status(1);
  });

  ua.on("invite", function (session) {
    createNewSessionUI(session.remoteIdentity.uri, session);
  });

  ua.on("message", function (message) {
    if (!sessionUIs[message.remoteIdentity.uri]) {
      createNewSessionUI(message.remoteIdentity.uri, null, message);
    }
  });

  document.body.className = "started";
}

var calls_log = 1;
elements.uaStatus.addEventListener("click", function () {
  if(calls_log == 1){
    elements.sessionList.style.height = "auto";
    elements.sessionList.style.width = "auto";
    calls_log = 100;
  }else{
    elements.sessionList.style.height = "54px";
    elements.sessionList.style.width = "500px";
    calls_log = 1;
  }
});

elements.registerCheckbox.addEventListener("click", function () {
  if (!ua) return;

  if (ua.isRegistered()) {
    ua.unregister();
  } else {
    ua.register();
  }
}, false);

function inviteSubmit(e) {
  e.preventDefault();
  e.stopPropagation();

  // Parse config options
  var video = elements.uaVideo.checked;
  var uri = elements.uaURI.value;
  //elements.uaURI.value = '';

  if (!uri) return;

  // Send invite
  var session = ua.invite(uri, {
    media: {
      constraints: mediaConstraints
    }
  });

  // Create new Session and append it to list
  var ui = createNewSessionUI(uri, session);
  startRingbackTone();
}
elements.inviteButton.addEventListener('click', inviteSubmit, false);
elements.newSessionForm.addEventListener('submit', inviteSubmit, false);

function createNewSessionUI(uri, session, message) {
  z += 1;
  var tpl = elements.sessionTemplate;
  var node = tpl.cloneNode(true);
  node.setAttribute("id", "session-"+z);
  var sessionUI = {};
  var messageNode;

  uri = session ?
    session.remoteIdentity.uri :
    SIP.Utils.normalizeTarget(uri, ua.configuration.hostport_params);
  var displayName = (session && session.remoteIdentity.displayName) || uri.user;
  //alert(uri); //sip:959223@10.1.250.6
  if (!uri) { return; }

  // Save a bunch of data on the sessionUI for later access
  sessionUI.session        = session;
  sessionUI.node           = node;
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
  //sessionUI.messageForm    = node.querySelector('.message-form');
  //sessionUI.messageInput   = node.querySelector('.message-form input[type="text"]');
  sessionUI.renderHint     = {
    remote: sessionUI.video
  };

  //sessionUI.renderHint     = {
    //remote: {
      //video: sessionUI.video
    //}
  //};

  sessionUIs[uri] = sessionUI;

  // Update template
  node.classList.remove('template');
  sessionUI.displayName.textContent = displayName || uri.user;
  var phone = "";
  var prefix = "";
  phone = uri.toString();
  phone = phone.replace("sip:", "");
  phone = phone.split("@")[0];

  // Контекст определен, запускаем функцию, которую желательно override
  extension_is(sessionUI.displayName.textContent, phone);

  //sessionUI.uri.textContent = '<' + uri + '>';
  sessionUI.uri.textContent = phone;

  // DOM event listeners
  sessionUI.green.addEventListener("click", function () {
    var video = elements.uaVideo.checked;
    var options = {
      media: {
        constraints: mediaConstraints
      }
    };

    var session = sessionUI.session;
    if (!session) {
      /* TODO - Invite new session */
      /* Don't forget to enable buttons */
      session = sessionUI.session = ua.invite(uri, options);
      setUpListeners(session);
    } else if (session.accept && !session.startTime) { // Incoming, not connected
      session.accept(options);
    }
  }, false);

  sessionUI.red.addEventListener('click', function () {
    var session = sessionUI.session;
    if (!session) {
      return;
    } else if (session.startTime) { // Connected
      session.bye();
    } else if (session.reject) { // Incoming
      session.reject();
    } else if (session.cancel) { // Outbound
      session.cancel();
    }
  }, false);


  ////////////////////////
  // BLIND transfer
  ////////////////////////
  sessionUI.gray.addEventListener("click", function () {
    var session = sessionUI.session;
    var new_phone = sessionUI.gray_transfer;
    if (session) {
      var new_phone = prompt("Куда переадресовать?");
      if(new_phone){

        var pstn_phone = new_phone.replace(/[^0-9]/gi, "");
        pstn_phone = pstn_phone.trim();
        var pstn_phone_len = pstn_phone.length;

        if( (pstn_phone_len == 6) || (pstn_phone_len == 10) || (pstn_phone_len == 11) ){
          pstn_phone = "oper_" + pstn_phone;
          console.log(" +++++++++++++++++++++++++++++++++++++++++++++++++++");
          console.log("CHANGING new_phone from " + new_phone + " to " + pstn_phone);
          console.log(" +++++++++++++++++++++++++++++++++++++++++++++++++++");
          session.refer(pstn_phone);
        }else{
          new_phone = new_phone.trim();
          var new_phone_len = new_phone.length;
          if((new_phone_len < 2) || (new_phone_len > 11)){
            alert("Невозможно переадресовать на такой номер");
          }else{
            session.refer(new_phone);
          }
        }
      }
    }
  }, false);

  sessionUI.dtmf.addEventListener("submit", function (e) {
    e.preventDefault();

    var value = sessionUI.dtmfInput.value;
    if (value === "" || !session) return;
    //value = parseInt(value);

    sessionUI.dtmfInput.value = "";

    //if (['0','1','2','3','4','5','6','7','8','9','*','#'].indexOf(value) > -1) {
      session.dtmf(value);
    //}

  });
  sessionUI.gray.style.display = "none";
  sessionUI.dtmf.style.display = "none";
  // Initial DOM state
  if (session && !session.accept) {
    sessionUI.green.disabled = true;
    sessionUI.green.innerHTML = "x";
    sessionUI.red.innerHTML = "<i class=\"icon-thumbs-down\"></i>";
  } else if (!session) {
    sessionUI.red.disabled = true;
    sessionUI.green.innerHTML = "<i class=\"icon-phone\"></i>";
    sessionUI.red.innerHTML = "x";
  } else {
    sessionUI.green.innerHTML = "<i class=\"icon-thumbs-up\"></i>";
    sessionUI.red.innerHTML = "<i class=\"icon-thumbs-down\"></i>";
  }
  sessionUI.dtmfInput.disabled = true;

  // SIP.js event listeners
  function setUpListeners(session) {
    sessionUI.red.disabled = false;

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

    session.on("accepted", function () {
      sessionUI.green.disabled = true;
      sessionUI.green.innerHTML = "x";
      sessionUI.red.innerHTML = "<i class=\"icon-thumbs-down\"></i>";
      sessionUI.dtmfInput.disabled = false;
      sessionUI.video.className = "on";
      session.mediaHandler.render(sessionUI.renderHint);
      sessionUI.gray.style.display = "inline";
      sessionUI.dtmf.style.display = "inline";
      // Дилинь-дилинь
      stopRingTone();
      // Звонок отвечен, нужно подождать 1-2 секунды, чтобы убедиться,
      // что бридж создан, затем выполнять функцию, которая нужна
      console.log("-------------------------talking-------------------------");
      call_is();
    });

    session.mediaHandler.on("addStream", function () {
      session.mediaHandler.render(sessionUI.renderHint);
    });

    session.on("rejected", function () {
      //elements.sessionList.innerHTML = "";
      delete sessionUI.session;
      sessionUI.gray.style.display = "none";
      sessionUI.dtmf.style.display = "none";
      // Дилинь-дилинь
      stopRingTone();
    });

    // Отмена исходящего звонка
    session.on("cancel", function () {
      sessionUI.red.disabled = true;
      sessionUI.gray.style.display = "none";
      sessionUI.dtmf.style.display = "none";
      stopRingTone();
    });

    session.on("bye", function () {
      //sessionUI.green.disabled = false;
      sessionUI.red.disabled = true;
      sessionUI.dtmfInput.disable = true;
      //sessionUI.green.innerHTML = "Набрать";
      sessionUI.red.innerHTML = "x";
      sessionUI.video.className = "";
      delete sessionUI.session;
      sessionUI.gray.style.display = "none";
      sessionUI.dtmf.style.display = "none";
      // Дилинь-дилинь
      stopRingTone();
    });

    session.on("failed", function () {
      sessionUI.green.disabled = true;
      sessionUI.red.disabled = true;
      sessionUI.dtmfInput.disable = true;
      sessionUI.green.innerHTML = "x";
      sessionUI.red.innerHTML = "x";
      sessionUI.video.className = "";
      delete sessionUI.session;
      sessionUI.gray.style.display = "none";
      sessionUI.dtmf.style.display = "none";
      // Дилинь-дилинь
      stopRingTone();
    });

    session.on("refer", function handleRefer (request) {
      var target = request.parseHeader("refer-to").uri;
      session.bye();

      createNewSessionUI(target, ua.invite(target, {
        media: {
          constraints: mediaConstraints
        }
      }));
    });
  }

  if (session) {
    setUpListeners(session);
  }

  // Messages
  function appendMessage(body, className) {
    messageNode = document.createElement("li");
    messageNode.className = className;
    messageNode.textContent = body;
    sessionUI.messages.appendChild(messageNode);
    //sessionUI.messages.scrollTop = sessionUI.messages.scrollHeight;
  }

  // Add node to live session list
  /*elements.sessionList.appendChild(node);*/
  /* Добавляем в начало запись о сессии */
  elements.sessionList.insertBefore(node, elements.sessionList.firstChild);
  /* Заменяем в сессии последнюю запись */
  //elements.sessionList.innerHTML = "";
  //elements.sessionList.appendChild(node);
}

// -------------------------------------------------------------------
// Функция, которая запускается, когда поймано имя (телефон) звонящего
// обычно этот телефон - это эксенжон (ext) и можно дальше производить
// маршрутизацию
// -------------------------------------------------------------------
function extension_is(ext, phone){
  console.log("+++++++++++++++++++++++++++++++++++++++++++");
  console.log("+ Ext is: " + ext);
  console.log("+ Phone is: " + phone);
  console.log("+++++++++++++++++++++++++++++++++++++++++++");
  return 1;
}
// ------------------------------------------------------------
// Фунцкия, которая запускается, когда соединение установлено,
// (оператор ответил), дальше можно запросить у АТС uuid звонка
// ------------------------------------------------------------
function call_is(){
  console.log("+++++++++++++++++++++++++++++++++++++++++++");
  console.log("+ CALL IN PROGRESS");
  console.log("+++++++++++++++++++++++++++++++++++++++++++");
  return 1;
}
