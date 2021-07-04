function add_functions2jabber(jabber_vars){

  /* Отправка на сервер ping
  */
  jabber_vars.ping = function(){
    if(!jabber_vars.connected){
      console.log("not connected");
      return false; // удалить handler
    }
    // .getUserFromJid(“darcy@pemberley.lit/library”);     // darcy
    // .getDomainFromJid(“darcy@pemberley.lit/library”);   // pemberley.lit
    // .getResourceFromJid(“darcy@pemberley.lit/library”); // library
    // .getBareJidFromJid(“darcy@pemberley.lit/library”);  // darcy@pemberley.lit
    var to = Strophe.getDomainFromJid(jabber_vars.conn.jid);
    var ping = $iq({
      to: to,
      type: "get",
      id: "ping1",
    }).c("ping", {xmlns: "urn:xmpp:ping"});
    jabber_vars.ping_started = (new Date()).getTime();
    console.log("ping", ping);
    jabber_vars.conn.send(ping);
  };

  /* Ответ от сервера на ping
  */
  jabber_vars.pong = function(iq){
    console.log("ping-pong:", (new Date()).getTime() - jabber_vars.ping_started);
    jabber_vars.ping();
    return true;  // не удалять handler
  };

  /* Логирование
  */
  jabber_vars.log = function(msg){
    $("#" + jabber_vars.ejabberd_id).append($("<p>" + msg + "</p>"));
  };

  /* Преобразование текста в xml
  */
  jabber_vars.text2xml = function(text){
    var parser = new DOMParser();
    var doc = parser.parseFromString(text, "text/xml");
    var el = doc.documentElement;
    if($(el).filter("parsererror").length > 0){
      return null;
    }
    return el;
  };

  /* Преобразование jabber_id в #id
  */
  jabber_vars.jid2id = function(jabber_id){
    return Strophe.getBareJidFromJid(jabber_id)
           .replaceAll("@", "-")
           .replaceAll(".", "-");
  }

  /* Получение ростера
  */
  jabber_vars.get_roster = function(){
    var iq = $iq({
      type: 'get',
    }).c("query", {xmlns: Strophe.NS.ROSTER}); // "jabber:iq:roster"
    // http://strophe.im/strophejs/doc/1.1.3/files/strophe-js.html#Strophe.Connection.sendIQ
    jabber_vars.conn.sendIQ(iq, jabber_vars.handle_roster);
  };

  /* Обработка ростера, добавление контактов
  */
  jabber_vars.handle_roster = function(iq){
    $(iq).find("item").each(function(){
      var jabber_id = $(this).attr("jid");
      var jabber_login = jabber_vars.jid2id(jabber_id);
      var name = $(this).attr("name") || jabber_id;
      var status = "roster-contact offline";
      var contact_html = jabber_vars.roster_contact_el(jabber_id, name, status);
      jabber_vars.add_contact(contact_html);
    });
  };

  /* Вес элемента для сортировки контакта ростера
  */
  jabber_vars.presence_value = function(el){
    if(el.hasClass("online")){
      return 2;
    }else if(el.hasClass("away")){
      return 1;
    }
    return 0;
  };

  /* Добавление контакта ростера
  */
  jabber_vars.add_contact = function(el){
    var jabber_id = el.find('.roster-jid').text();
    var presence = jabber_vars.presence_value(el.find('.roster-contact'));
    var contacts = $("#" + jabber_vars.roster_container_id + " li");
    if(contacts.length > 0){
      var inserted = false;
      contacts.each(function(){
        var cmp_presence = jabber_vars.presence_value(
          $(this).find('.roster-contact')
        );
        var cmp_jabber_id = $(this).find('.roster-jid').text();
        if(presence > cmp_presence){
          $(this).before(el);
          inserted = true;
        }else{
          if(jabber_id < cmp_jabber_id){
            $(this).before(el);
            inserted = true;
          }
        }
        if(!inserted){
          $("#" + jabber_vars.roster_container_id).append(el);
        }
      });
    }else{
      $("#" + jabber_vars.roster_container_id).append(el);
    }
    jabber_vars.contacts_listeners();
  };


  /* Обновление списка контактов
  */
  jabber_vars.on_presence = function(presence){
    var pel = $(presence);
    var ptype = pel.attr('type');
    var jabber_id = jabber_vars.jid2id(pel.attr('from'));
    if(ptype === "subscribe"){
      jabber_vars.penging_subscriber = jabber_id;
      $("#" + jabber_vars.ejabberd_id).trigger("pending_subscriber");
    } else if(ptype !== 'error'){
      var contact = $("#" + jabber_vars.roster_container_id + " li#" + jabber_id)
                    .removeClass("touched")
                    .removeClass("online")
                    .removeClass("away")
                    .removeClass("offline");
      if(ptype === "unavailable"){
        contact.addClass("offline");
      }else{
        var show = pel.find("show").text();
        if(show === "" || show === "chat"){
          contact.addClass("online");
        }else{
          contact.addClass("away");
        }
      }
      contact.remove();
      contact.find(".remove").removeClass("touched");
      jabber_vars.add_contact(contact);
    }
    return true;
  };


  jabber_vars.on_roster_changed = function(iq){
    $(iq).find("item").each(function(){
      var sub = $(this).attr("subscription");
      var jabber_id = $(this).attr("jid");
      var name = $(this).attr("name") || jabber_id;
      var jabber_login = jabber_vars.jid2id(jabber_id);
      if(sub === "remove"){
        // remove contact
        $("#" + jabber_login).remove();
      }else{
        // added or modified
        var status = "roster-contact offline";
        if($("#" + jabber_login).length > 0){
          $("#" + jabber_login).removeClass("touched");
          status = $("#" + jabber_login).attr("class");
        }
        var contact_html = jabber_vars.roster_contact_el(jabber_id, name, status);

        if($("#" + jabber_login).length > 0){
          $("#" + jabber_login).replaceWith(contact_html);
        }else{
          jabber_vars.add_contact(contact_html);
        }
      }
    });
    jabber_vars.contacts_listeners();
    return true;
  };

  /* Создание $ хтмл элемента контакта для ростера
  */
  jabber_vars.roster_contact_el = function(jabber_id, name, status){
    var jabber_login = jabber_vars.jid2id(jabber_id);
    return $("<li id='" + jabber_login + "'>" +
             "  <div class='" + status + "'>" +
             "    <div class='roster-name'>" + name + "</div>" +
             "    <div class='roster-jid'>" + jabber_id + "</div>" +
             "  </div>" +
             "  <div class='remove'><i class='fa fa-trash'></i></div>" +
             "</li>");
  };

  /* Добавление события на удаление контактов ростера
  */
  jabber_vars.drop_contact_listeners = function(){
    $("#" + jabber_vars.roster_container_id + " li .remove").each(function(){
      if($(this).hasClass("touched")){
        return;
      }
      $(this).addClass("touched");
      $(this).click(function(e){
        var jabber_id = $(this).parent().find(".roster-jid").text();
        jabber_vars.roster_unsubscribe(jabber_id);
        e.preventDefault();
      });
    });
  };

  /* Добавление события на выбор контакта ростера
  */
  jabber_vars.select_contact_listeners = function(){
    $("#" + jabber_vars.roster_container_id + " li").each(function(){
      if($(this).hasClass("touched")){
        return;
      }
      $(this).addClass("touched");
      $(this).click(function(){
        var jabber_id = $(this).find(".roster-jid").text();
        var jabber_login = jabber_vars.jid2id(jabber_id);
        var name = $(this).find(".roster-name").text();
        jabber_vars.receiver = jabber_id;
        jabber_vars.create_chat_window(jabber_id, name);
        $("#" + jabber_vars.dialogs_container_id + " > .panel").addClass("hidden");
        $("#chat-" + jabber_login).removeClass("hidden");
      });
    });
  };

  jabber_vars.create_chat_window = function(jabber_id, name){
    var jabber_login = jabber_vars.jid2id(jabber_id);
    if($("#chat-" + jabber_login).length > 0){
      return;
    }
    $("#" + jabber_vars.dialogs_container_id).append($(
      "<div class='panel panel-default hidden' id='chat-" + jabber_login + "'>" +
      "<div class='panel-heading'>" + name + "</div>" +
      "<div class='panel-body'>" +
      "</div>" +
      "</div>"
    ));
    $("#chat-" + jabber_login).data("jabber_id", jabber_id);
  };

  jabber_vars.contacts_listeners = function(){
    jabber_vars.select_contact_listeners();
    jabber_vars.drop_contact_listeners();
  };

  jabber_vars.on_message = function(msg){
    var copied = $(msg);
    var jabber_id = copied.attr("from"); // .match(/^who@domain.ru/)
    var jabber_login = jabber_vars.jid2id(jabber_id);
    var name = copied.attr("name") || jabber_login;
    jabber_vars.create_chat_window(jabber_id, name);

    var body = copied.find("html > body");
    if (body.length === 0){
      body = copied.find("body");
      if(body.length > 0){
        body = body.text();
      }else{
        body = null;
      }
    }else{
      body = body.contents();
      var span = $("<span></span>");
      body.each(function(){
        if(document.importNode){
          $(document.importNode(this, true)).appendTo(span);
        }else{
          span.append(this.xml);
        }
      });
      body = span;
    }
    if(body){
      var msg_el = jabber_vars.new_message_el(jabber_id, name);
      $("#chat-" + jabber_login + " .panel-body").append(msg_el);
      $("#chat-" + jabber_login + " .chat-message:last .chat-text pre").append(body);
      jabber_vars.scroll_chat(jabber_id);
    }
    return true;
  };

  jabber_vars.scroll_chat = function(jabber_id){
    var jabber_login = jabber_vars.jid2id(jabber_id);
    var div = $("#chat-" + jabber_login + " .panel-body").get(0);
    div.scrollTop = div.scrollHeight;
  };


  /* Отправка сообщения */
  jabber_vars.send_message = function(msg){
    if(!jabber_vars.connected){
      jabber_vars.log('not connected');
      return;
    }

    var jabber_id = jabber_vars.receiver;
    if(!jabber_id){
      jabber_vars.log('receiver not selected');
      return;
    }

    msg = $.trim(msg);
    if(msg.length < 1){
      console.log("empty message");
      return;
    }

    var xml = $msg({
      to: jabber_id,
      type: "chat",
    }).c("body").t(msg);

    jabber_vars.conn.send(xml);

    var jabber_login = jabber_vars.jid2id(jabber_id);
    var name = "Я";
    var msg_el = jabber_vars.new_message_el(jabber_id, name);
    $("#chat-" + jabber_login + " .panel-body").append(msg_el);
    $("#chat-" + jabber_login + " .chat-message:last .chat-text pre").append(msg);
    jabber_vars.scroll_chat(jabber_id);

  };

  /* Создание элемента для сообщения
  */
  jabber_vars.new_message_el = function(jabber_id, name){
    var jabber_login = jabber_vars.jid2id(jabber_id);
    return $("<div class='chat-message'>" +
             "&lt;<span class='chat-name'>" +
             name +
             "</span>&gt;" +
             "<span class='chat-text'>" +
             "<pre></pre>" +
             "</span>" +
             "</div>"
    );
  };

  /* Запрос на добавление нового контакта в ростер
  */
  jabber_vars.roster_create_contact = function(jabber_id, name){
    var data = {
      jid: jabber_id,
      name: name || "",
    };
    var iq = $iq({
      type: "set"
    }).c("query", {xmlns: Strophe.NS.ROSTER})
      .c("item", data);
    jabber_vars.conn.sendIQ(iq);
  };

  /* Добавить контакт и подписаться на его обновления
  */
  jabber_vars.roster_subscribe = function(jabber_id, name){
    jabber_vars.roster_create_contact(jabber_id, name);
    var presence = $pres({
      to: jabber_id,
      type: "subscribe",
    });
    jabber_vars.conn.send(presence);
  }

  /* Запрос на удаление контакта из ростера
  */
  jabber_vars.roster_drop_contact = function(jabber_id){
    var data = {
      jid: jabber_id,
      subscription: "remove",
    };
    var iq = $iq({
      type: "set"
    }).c("query", {xmlns: Strophe.NS.ROSTER})
      .c("item", data);
    jabber_vars.conn.sendIQ(iq);
  };

  /* Отписаться от обновлений контакта и удалить его
  */
  jabber_vars.roster_unsubscribe = function(jabber_id){
    var presence = $pres({
      to: jabber_id,
      type: "unsubscribe",
    });
    jabber_vars.conn.send(presence);
    jabber_vars.roster_drop_contact(jabber_id);
  }


};