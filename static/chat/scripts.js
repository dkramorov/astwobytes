// ----------------------------------------
// Класс для работы с чатом через websocket
// ----------------------------------------

// USAGE:
//var ws = new WebSocket("wss://207.154.244.145:8888/");
//var ws = new WebSocket("{{ ws_server }}");
//var TOKEN = '{{ token }}'; // {'token': 'hash'}
// Логин пользователя
//var USER = '{{ request.user.username }}';
//var contacts_container = $('#contacts'); // Контейнер пользователей
//var conversations_container = $('#discussions');
//var chats_container = $('#list-chat');
//var search_input = $('#people'); // Контейнер поиска пользователей
//var search_input_conversations = $('#conversations');
//var login_api = '{% url "login:api" "users" %}';
//var messages_api = '{% url "ws:messages_api" %}';
//var ws_chat = new WSChatClass(ws, TOKEN, USER, login_api, messages_api
//                              chats_container, contacts_container, conversations_container,
//                              search_input, search_input_conversations);

class WSChatClass{
    constructor(ws, token, user, login_api, messages_api,
                chats_container, contacts_container, conversations_container,
                search_input, search_input_conversations) {
        this.ws = ws; // websocket
        this.token = token; // Токен формируется на сервер и присылается в авторизации
        this.user = user; // Логин пользователя
        this.login_api = login_api; // Апи по пользователям
        this.messages_api = messages_api; // Апи по сообщениям
        this.page_get_contact_list = 0;
        this.mmr_interval = 4000; // mark messages read interval
        // Статусы сообщений
        this.STATUS_DANGER = 'danger';
        this.STATUS_WARNING = 'warning';
        this.STATUS_INFO = 'info';
        this.STATUS_SUCCESS = 'success';
        this.STATUS_I = 'i_am';
        // Аватар по умолчанию
        this.DEFAULT_AVATAR = '/static/admin/misc/avatar_small.png';
        this.DEFAULT_GROUP_AVATAR = '/static/admin/misc/avatar_group.png';
        // Хранилище
        this.USERS_LIST = {};
        this.BCAST_LIST = {}; // Очередь широковещательных сообщений (подкл/откл)
        this.ONLINE_USERS = [];
        this.QUEUED_LIST = {}; // Очередь сообщений пока чат не создан
        this.CONVERSATIONS = []; // Список бесед пользователя
        // Контейнеры для данных в DOM
        this.contacts_container = contacts_container;
        this.conversations_container = conversations_container;
        this.chats_container = chats_container;
        this.search_input = search_input;
        this.search_input_conversations = search_input_conversations;
        this.pk_contacts = this.contacts_container.attr('id');
        this.pk_conversations = this.conversations_container.attr('id');
        this.pk_chats = this.chats_container.attr('id');

        // Вспомогательные классы
        this.Message = new WSMessage();
        this.Chat = new WSChat();
        this.Conversation = new WSConversation(this);
        this.Contact = new WSContact(this);
        this.Notification = new WSNotification();
        // -----------------
        // События вебсокета
        // -----------------
        var self = this;
        this.ws.onopen = function() {
            //self.add_msg({'text': 'Соединение установлено', 'type': this.STATUS_SUCCESS}, true);
            self.send_msg({'action': 'auth'});
        };
        this.ws.onclose = function(event) {
            if (event.wasClean) {
                //self.add_msg({'text': 'Соединение закрыто', 'type': this.STATUS_DANGER}, true);
            } else {
                //self.add_msg({'text': 'Обрыв соединения', 'type': this.STATUS_DANGER}, true);
            }
            //self.add_msg({'text': 'Код: ' + event.code + ' причина: ' + event.reason, 'type': this.STATUS_DANGER}, true);
        };
        this.ws.onerror = function(error) {
            //self.add_msg({'text': error.message, 'type': STATUS_DANGER}, true);
        };
        this.ws.onmessage = function (event) {
            var json = JSON.parse(event.data);
            self.parse_msg(json);
        };
    }


    // -----------------------------------
    // Настраиваем ajax для отправки формы
    // -----------------------------------
    ajaxSetup() {
        var self = this;
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!self.csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        return csrftoken;
    }

    // --------------------------
    // Безопасные методы для csrf
    // --------------------------
    csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    // -----------------------------
    // Парсим сообщение от вебсокета
    // -----------------------------
    parse_msg(msg){
        var action = msg['action'];
        console.log(msg);
        switch (action) {
            case 'users_list':
                this.ONLINE_USERS = msg[action];
                this.update_users_statuses();
                break;
            case 'bcast_msg':
                this.add_msg({'text': msg[action],
                              'date': msg['date'],
                              'time': msg['time'],
                              'user': msg['from'],
                              'updated': msg['updated'],
                              'type': this.STATUS_WARNING}, true);
                break;
            case 'to_user':
                this.Notification.notifyMe(msg['from'], msg['msg']);
                this.add_msg({'text': msg['msg'],
                              'date': msg['date'],
                              'time': msg['time'],
                              'user': msg['from'],
                              'updated': msg['updated'],
                              'type': this.STATUS_I}, true);
                break;
            case 'to_group':
                this.Notification.notifyMe('Сообщение в группу', msg['msg']);
                this.add_group_msg({'text': msg['msg'],
                                    'date': msg['date'],
                                    'time': msg['time'],
                                    'user': msg['from'],
                                    'updated': msg['updated'],
                                    'is_group': true,
                                    'group_id': msg['group_id'],
                                    'type': this.STATUS_I}, true);
                break;
            case 'auth':
                this.Contact.activate_search(); // Поиск по контактам
                this.Conversation.search_conversations(); // Поиск по беседам
                this.get_conversations(); // Получаем беседы
                this.get_contact_list(); // Получаем список контактов
            default:
                this.add_msg({'text': JSON.stringify(msg), 'type': this.STATUS_DANGER}, true);
                break;
        }
    }


    // ---------------------------------
    // Отправка сообщения через вебсокет
    // с авторизацией (токен + логин)
    // ---------------------------------
    send_msg(json){
        json['token'] = this.token;
        json['user'] = this.user;
        this.ws.send(JSON.stringify(json));
    }


    // -------------------------------
    // Прокрутка активной области чата
    // 1) если активен чат и новое msg
    // 2) если переключаем/создаем чат
    // -------------------------------
    autoscroll(username){
        var cur_chat = $('#chat_' + username);
        if(cur_chat.length > 0){
            if(cur_chat.hasClass('hidden')){
                return;
            }
            var chat_messages = $('#content_' + username);
            var chat_messages_height = chat_messages[0].scrollHeight;
            chat_messages.animate({
                scrollTop: chat_messages_height
            }, 1000);
        }
    }


    // -------------------------------
    // Запросить статусы пользователей
    // -------------------------------
    ask_user_statuses(){
        this.send_msg({'action': 'users_list'});
    }


    // ----------------------------
    // Получить список контактов
    // и заполнить ими контакт-лист
    // ----------------------------
    get_contact_list(){
        var self = this;
        this.ajaxSetup();
        $.ajax({
            async : true,
            type: 'POST',
            url: self.login_api,
            data : 'page=' + self.page_get_contact_list,
            success : function (r) {
                if(r['last_page'] > self.page_get_contact_list){
                    // ----------------------
                    // Заполнить контакт лист
                    // ----------------------
                    self.fill_contact_list(r['data']);
                    self.page_get_contact_list += 1;
                    setTimeout(function(){
                        self.get_contact_list();
                    }, 1000);
                }else{
                    self.ask_user_statuses();
                    self.start_new_chat_listeners(); // Можно добавлять беседы
                }
            }
        });
    }


    // ---------------------
    // Получить список бесед
    // ---------------------
    get_conversations(){
        var self = this;
        this.ajaxSetup();
        $.ajax({
            async : true,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            url: self.messages_api,
            data : JSON.stringify({
                'token': self.token,
                'is_encoded': true,
                'msg': {
                    'action': 'get_conversations',
                },
            }),
            success : function (r) {
                // Заполнить беседы
                self.CONVERSATIONS = r;
                self.fill_conversation_list();
            }
        });
    }


    // ----------------------
    // Заполнить контакт лист
    // ----------------------
    fill_contact_list(data){
        var username;
        for(var i=0; i<data.length; i++){
            username = data[i]['username'];
            // -----------------------------------------
            // Только если пользователя еще нет в списке
            // -----------------------------------------
            if(this.USERS_LIST[username] !== undefined){
                continue;
            }
            this.USERS_LIST[username] = data[i];
            this.add_user2user_list(username);
        }
        // Заполнение бесед
        this.fill_conversation_list();
    }


    // ----------------------
    // Заполнить список бесед
    // ----------------------
    fill_conversation_list(){
        var users_list = {};
        var user_id;
        var item;
        var self = this;
        Object.keys(this.USERS_LIST).forEach(function(key) {
            users_list[self.USERS_LIST[key]['id']] = self.USERS_LIST[key];
        });

        for(var i=0; i<this.CONVERSATIONS.length; i++){
            item = this.CONVERSATIONS[i];
            if(item['filled'] !== undefined){
                continue;
            }
            if(item['is_group']){
                item.users = {};
                item['filled'] = true;
                for(var j=0; j<item['contacts'].length; j++){
                    user_id = item['contacts'][j];
                    if(users_list[user_id] === undefined){
                        item['filled'] = undefined;
                        break;
                    }else{
                      item.users[user_id] = users_list[user_id];
                    }
                }
                if(item['filled'] !== undefined){
                    this.add_group_conversation(item);
                }
            }else if(users_list[item['from_user']] !== undefined){
                item.user = users_list[item['from_user']];
                item['filled'] = true;
                this.add_conversation(item);
            }
        }
    }


    // ------------------------------
    // Вспомогательная функция
    // Добавление беседы в DOM-дерево
    // ------------------------------
    add_conversation_helper(username, new_messages, name,
                            time, date, text, avatar, is_first){
        var new_conversation_block = this.Conversation.new_conversation(username, new_messages, name, time, date, text, avatar, is_first);
        // В случае, если беседа новая, надо ее вставить сверху
        if(is_first !== undefined){
            $('#' + this.pk_conversations +' #chats').prepend(new_conversation_block);
        }else{
            $('#' + this.pk_conversations +' #chats').append(new_conversation_block);
        }
    }


    // ------------------------------------------
    // Добавление групповой беседы в список бесед
    // ------------------------------------------
    add_group_conversation(conversation){
        var group_id = conversation.from_user;
        var avatar = this.DEFAULT_GROUP_AVATAR;
        this.add_conversation_helper(group_id, conversation.new_messages,
                                     conversation.group_name,
                                     conversation.time, conversation.date,
                                     conversation.text, avatar, conversation.first);

        var self = this;
        $('#conversation_' + group_id).click(function(){
            $('#list-chat .chat').addClass('hidden');
            if($('#chat_' + group_id).length === 0){
                self.create_group_chat(group_id);
            }else{
                $('#chat_' + group_id).removeClass('hidden');
                self.autoscroll(group_id);
                var conversation = self.get_conversation(group_id);
                setTimeout(function(){
                    self.mark_messages_read(group_id, conversation.updated, true);
                }, self.mmr_interval);
            }
        });
    }


    // --------------------------------------
    // Добавление новой беседы в список бесед
    // --------------------------------------
    add_conversation(conversation){
        var username = conversation.user.username;
        this.add_conversation_helper(username, conversation.new_messages,
                                     conversation.user.name,
                                     conversation.time, conversation.date,
                                     conversation.text, conversation.user.avatar,
                                     conversation.first);

        var self = this;
        $('#conversation_' + username).click(function(){
            $('#list-chat .chat').addClass('hidden');
            if($('#chat_' + username).length === 0){
                self.create_chat(username);
            }else{
                $('#chat_' + username).removeClass('hidden');
                self.autoscroll(username);
                var conversation = self.get_conversation(username);
                setTimeout(function(){
                    self.mark_messages_read(username, conversation.updated, false);
                }, self.mmr_interval);
            }
        });
    }

    // --------------------------------------
    // Добавление пользователя в контакт лист
    // --------------------------------------
    add_user2user_list(username){
        var user = this.USERS_LIST[username];
        // Самого себя не добавляем в контакт-лист

        var name = user['name'];
        var email = user['email'];
        var first_name = user['first_name'].toLowerCase();
        var last_name = user['last_name'].toLowerCase();
        var avatar = user['thumb'];
        if(avatar === ''){
            avatar = this.DEFAULT_AVATAR;
        }
        this.USERS_LIST[username]['avatar'] = avatar;
        var data_search = username + ' ' + email + ' ' + first_name + ' ' + last_name;
        this.USERS_LIST[username]['search'] = data_search;

        // Самого себя не надо добавлять
        if(username == this.user){
            return;
        }
        var new_user = this.Contact.new_contact(username, avatar, name, email);
        this.contacts_container.append($(new_user));
        var self = this;
        $('#contact_' + username).click(function(){
            $('#list-chat .chat').addClass('hidden');
            if($('#chat_' + username).length === 0){
                self.create_chat(username);
            }else{
                $('#chat_' + username).removeClass('hidden');
                self.autoscroll(username);
                var conversation = self.get_conversation(username);
                setTimeout(function(){
                    self.mark_messages_read(username, conversation.updated, false);
                }, self.mmr_interval);
            }
        });
    }


    // -------------------------------
    // Обновляем статусы пользователей
    // в списке контактов/бесед
    // -------------------------------
    update_users_statuses(){
        var status;
        var user;
        $('#' + this.pk_contacts + ' a.contact .status i').removeClass('online').addClass('offline');
        $('#' + this.pk_conversations + ' a.conversation .status i').removeClass('online').addClass('offline');

        $('#list-chat .chat .inside .status i').removeClass('online').addClass('offline');
        $('#list-chat .chat .inside .data span').html('Не на связи');
        for(var i=0; i<this.ONLINE_USERS.length; i++){
            user = this.ONLINE_USERS[i];
            status = $('#contact_' + user + ' .status i');
            status.removeClass('offline').addClass('online');
            status = $('#chat_' + user + ' .status i');
            status.removeClass('offline').addClass('online');
            $('#chat_' + user + ' .data span').html('На связи');
            status = $('#conversation_' + user + ' .status i');
            status.removeClass('offline').addClass('online');
        }
    }


    // -------------------------------------------------
    // Если мы отправляем сообщение новому пользователю,
    // если пользователь получает сообщение от другого
    // пользователя, которого нет в списке бесед,
    // тогда нужно вставить такую беседу
    // -------------------------------------------------
    add_conversation_if_not_exist(username, msg, is_incoming){
        // Если контакт есть, значит и беседа уже должна быть
        if(this.USERS_LIST[username] !== undefined){
            if($('#conversation_' + username).length == 0){
                // Содаем беседу
                var conversation = {
                    'user': this.USERS_LIST[username],
                    'text': msg.text,
                    'new_messages': 0, // доплюсуется в update_conversation_info
                    'time': msg.time,
                    'date': msg.date,
                    'updated': msg.updated,
                    'filled': true,
                    'first': true, // чтобы добавить в начало списка
                };
                this.CONVERSATIONS.push(conversation);
                this.add_conversation(conversation);
                this.update_users_statuses();
            }
        }
    }


    // ---------------------------
    // Добавление групповой беседы
    // ---------------------------
    add_group_conversation_if_not_exist(group_id, msg, is_incoming){
        var group = this.get_conversation(group_id);
        if(group !== undefined){
        }else{
            // Ее надо получить с сервера, а затем добавить
            var self = this;
            this.ajaxSetup();
            $.ajax({
                async : true,
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                url: self.messages_api,
                data : JSON.stringify({
                    'token': self.token,
                    'is_encoded': true,
                    'msg': {
                        'action': 'get_group',
                        'group_id': group_id,
                    },
                }),
                success : function (r) {
                    var ids_users = {};
                    Object.keys(self.USERS_LIST).forEach(function(key) {
                        ids_users[self.USERS_LIST[key].id] = self.USERS_LIST[key];
                    });
                    if($('#conversation_' + r['from_user']).length == 0){
                        // Содаем беседу
                        r['first'] = true
                        self.CONVERSATIONS.push(r);
                        self.fill_conversation_list();
                    }
                }
            });
        }
    }


    // --------------------------
    // Добавление сообщения в чат
    // scroll = true/false,
    // если много - то false
    // --------------------------
    add_msg(msg, scroll){
        // msg = {'text': '...', 'user': user, 'date': 'H:M:S d/m/y', 'type': 'STATUS_...'}
        if(!msg.user){
            msg.user = '';
        }else{
            var new_msg;
            if(msg.time === undefined){
                msg.time = this.strftime(new Date());
            }
            if(msg.user === this.user){
                new_msg = this.Message.new_msg('from_me', msg, this.DEFAULT_AVATAR);
                $('#content_' + msg.to_user + ' .messages').append($(new_msg));
                if(scroll){
                    this.add_conversation_if_not_exist(msg.to_user, msg, false);
                    this.autoscroll(msg.to_user);
                    this.update_conversation_info(msg.to_user, msg, false);
                }
            }else{
                if(scroll){
                    this.add_conversation_if_not_exist(msg.user, msg, true);
                    this.update_conversation_info(msg.user, msg, true);
                }
                // Если чата нихера нету еще,
                // то пишем в историю, когда чат
                // будет создан - запишем
                if($('#content_' + msg.user + ' .messages').length == 0){
                    this.msg2queue(msg);
                    return;
                }
                var from_user = this.USERS_LIST[msg.user];
                new_msg = this.Message.new_msg('to_me', msg, from_user.avatar);
                $('#content_' + msg.user + ' .messages').append($(new_msg));
                if(scroll){
                    this.autoscroll(msg.user);
                }
            }
        }
    }


    // --------------------------
    // Добавление сообщения в чат
    // scroll = true/false,
    // если много - то false
    // --------------------------
    add_group_msg(msg, scroll){
        var new_msg;
        if(msg.time === undefined){
            msg.time = this.strftime(new Date());
        }
        if(msg.user === this.user){
            new_msg = this.Message.new_msg('from_me', msg, this.DEFAULT_AVATAR);
            $('#content_' + msg.to_user + ' .messages').append($(new_msg));
            if(scroll){
                this.add_group_conversation_if_not_exist(msg.group_id, msg, false);
                this.autoscroll(msg.group_id);
                this.update_conversation_info(msg.group_id, msg, false);
            }
        }else{
            if(scroll){
                this.add_group_conversation_if_not_exist(msg.group_id, msg, true);
                this.update_conversation_info(msg.group_id, msg, true);
            }
            // Если чата нихера нету еще,
            // то пишем в историю, когда чат
            // будет создан - запишем
            if($('#content_' + msg.group_id + ' .messages').length == 0){
                this.msg2queue(msg);
                return;
            }
            var from_user = this.USERS_LIST[msg.user];
            new_msg = this.Message.new_msg('to_me', msg, from_user.avatar);
            $('#content_' + msg.group_id + ' .messages').append($(new_msg));
            if(scroll){
                this.autoscroll(msg.group_id);
            }
        }
    }


    // -------------------------------------
    // Обновляем время/текст беседы
    // Обновление количества новых сообщений
    // -------------------------------------
    update_conversation_info(username, msg, is_incoming){
        var conversation;
        var is_group = msg.is_group === undefined ? false : true;
        // Помечаем все сообщения как прочитанные
        for(var i=0; i<this.CONVERSATIONS.length; i++){
            conversation = this.CONVERSATIONS[i];
            if(is_group && conversation.is_group === undefined){
                continue
            }
            if(!is_group && conversation.is_group !== undefined){
                continue
            }
            if((!is_group && conversation['user']['username'] === username) ||
               (is_group  && conversation['from_user'] === username)){
                if(conversation['filled']){
                    $('#conversation_' + username + ' .data span').html(this.strftime(new Date()));
                    var short_msg = msg.text;
                    if(short_msg.length > 20){
                        short_msg = short_msg.slice(0, 20) + '...';
                    }
                    $('#conversation_' + username + ' .data p').html(short_msg);
                }
                // Вхоядщее сообщение
                if(is_incoming){
                    var new_messages_container = $('#conversation_' + username + ' .new');
                    // Сообщение считаем прочитанным
                    var cur_chat = $('#chat_' + username);
                    if(cur_chat.length > 0){
                        if(!cur_chat.hasClass('hidden')){
                            var self = this;
                            setTimeout(function(){
                                self.mark_messages_read(username, msg.updated, is_group);
                            }, self.mmr_interval);
                        }else{
                            this.CONVERSATIONS[i]['new_messages'] += 1;
                            this.CONVERSATIONS[i]['updated'] = msg.updated;
                            new_messages_container.removeClass('hidden');
                            new_messages_container.find('span').html(this.CONVERSATIONS[i]['new_messages']);
                        }
                    }else{
                        this.CONVERSATIONS[i]['new_messages'] += 1;
                        this.CONVERSATIONS[i]['updated'] = msg.updated;
                        new_messages_container.removeClass('hidden');
                        new_messages_container.find('span').html(this.CONVERSATIONS[i]['new_messages']);
                    }
                }
                break;
            }
        }
    }


    // -----------------------------
    // Добавить сообщение в очередь,
    // если чат еще не создан
    // -----------------------------
    msg2queue(msg){
        // Если такого чата еще нет, значит,
        // сообщения будут получены при нажатии на него,
        // очередь в этом случае не нужна
        if($('#chat_' + msg.user).length == 0){
            //console.log('chat does not exists, do not queue this');
            return;
        }
        console.log('[QUEUED]', msg);
        if(this.QUEUED_LIST[msg.user] === undefined){
            this.QUEUED_LIST[msg.user] = Array();
        }
        this.QUEUED_LIST[msg.user].push(msg);
    }


    // ------------------------------
    // Вспомогательная функция
    // подготавливает сообщение,
    // полученное по истории для чата
    // ------------------------------
    load_history_msg_helper(r){
        var scroll = false;
        var is_group = r['is_group'];
        var messages_count = r['messages'].length;
        if(messages_count > 0){
            for(var i=0; i<messages_count; i++){
                var msg = r['messages'][i];
                if(msg['bcast_message'] !== undefined){
                    msg['type'] = this.STATUS_WARNING;
                }else if(msg['from_user'] == this.user){
                    msg['type'] = this.STATUS_I;
                    msg['user'] = this.user;
                }else{
                    msg['type'] = this.STATUS_INFO;
                    msg['user'] = msg['from_user'];
                }
                if(messages_count === i + 1){
                    scroll = true;
                }
                if(is_group){
                    this.add_group_msg(msg, scroll);
                }else{
                    this.add_msg(msg, scroll);
                }
            }
        }
    }


    // --------------------------
    // Загрузка истории сообщений
    // Будем грузить по 50 штук,
    // останавливаться по айди
    // --------------------------
    load_history(username){
        var last_pk = 0;
        var by = 50;
        if(this.USERS_LIST[username]['history'] === undefined){
            this.USERS_LIST[username]['history'] = {'last_pk': 0, 'by': 50}
        }else{
            last_pk = this.USERS_LIST[username]['history']['last_pk'];
            by = this.USERS_LIST[username]['history']['by']
        }
        var self = this;
        this.ajaxSetup();
        $.ajax({
            async : true,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            url: self.messages_api,
            data : JSON.stringify({
                'token': self.token,
                'is_encoded': true,
                'msg': {
                    'with_user': username,
                    'action': 'get_messages',
                    'last_pk': last_pk,
                    'by': by,
                },
            }),
            success : function (r) {
                self.load_history_msg_helper(r);
            }
        });
    }


    // --------------------------
    // Загрузка истории сообщений
    // по групповому чату
    // Будем грузить по 50 штук,
    // останавливаться по айди
    // --------------------------
    load_group_history(group_id){
        var last_pk = 0;
        var by = 50;

        var group = this.get_conversation(group_id);
        if(group === undefined){
            return;
        }

        if(group['history'] === undefined){
            group['history'] = {'last_pk': 0, 'by': 50}
        }else{
            last_pk = group['history']['last_pk'];
            by = group['history']['by']
        }
        var self = this;
        this.ajaxSetup();
        $.ajax({
            async : true,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            url: self.messages_api,
            data : JSON.stringify({
                'token': self.token,
                'is_encoded': true,
                'msg': {
                    'group': group_id,
                    'action': 'get_group_messages',
                    'last_pk': last_pk,
                    'by': by,
                },
            }),
            success : function (r) {
                self.load_history_msg_helper(r);
            }
        });
    }


    // -----------------------
    // Вспомогательная функция
    // Добавление чата в DOM
    // -----------------------
    create_chat_helper(username, name, avatar){
        var status_class = $('#contact_' + username + ' .status i').hasClass('online') ? 'online' : 'offline';
        var status_str = status_class === 'online' ? 'На связи' : 'Не на связи';
        var new_chat = this.Chat.new_chat(username, avatar, status_class, status_str, name);
        $('#' + this.pk_chats).append($(new_chat));
    }


    // ----------------------------
    // Добавление чата на страничку
    // ----------------------------
    create_chat(username){
        var user = this.USERS_LIST[username];
        if(user === undefined){
            return;
        }

        this.create_chat_helper(username, user.name, user.avatar);

        this.load_history(username);
        if(this.QUEUED_LIST[username] !== undefined){
            var scroll = false;
            var list_len = this.QUEUED_LIST[username].length;
            for(var i=0; i<list_len; i++){
                if(list_len === i + 1){
                    scroll = true;
                }
                this.add_msg(this.QUEUED_LIST[username][i], scroll);
            }
            this.QUEUED_LIST[username] = Array();
        }
        this.create_chat_listeners(username, false);
    }


    // ---------------------------------------
    // Добавление группового чата на страничку
    // ---------------------------------------
    create_group_chat(group_id){
        var group = this.get_conversation(group_id);
        if(group === undefined){
            return;
        }
        var avatar = this.DEFAULT_GROUP_AVATAR;
        this.create_chat_helper(group_id, group.group_name, avatar);

        this.load_group_history(group_id);
/* МОГУТ ЛИ БЫТЬ У НАС в ОЧЕРЕДИ сообщения по групповым беседам?
        if(this.QUEUED_LIST[username] !== undefined){
            var scroll = false;
            var list_len = this.QUEUED_LIST[username].length;
            for(var i=0; i<list_len; i++){
                if(list_len === i + 1){
                    scroll = true;
                }
                this.add_msg(this.QUEUED_LIST[username][i], scroll);
            }
            this.QUEUED_LIST[username] = Array();
        }
*/
        this.create_chat_listeners(group_id, true);
    }


    // -------------------------------------------
    // Создаем обработчики событий для нового чата
    // -------------------------------------------
    create_chat_listeners(username, is_group){
        var textarea = $('#chat_' + username + ' textarea');
        autosize(textarea);
        // не отправять форму
        $('#chat_' + username + ' form').submit(function(){
            return false;
        });

        var self = this;
        if(is_group){
            $('#chat_' + username + ' .conversation_information').click(function(){
                var group = self.get_conversation(username);
                $('#participant_select2').val('');
                var usernames = [];
                Object.keys(group.users).forEach(function(key) {
                     usernames.push(group.users[key].username);
                });
                $('#participant_select2').val(usernames);
                $('#participant_select2').trigger("change");
                $('#startnewchat h1').html('Информация');
                $('#new_chat_topic').val(group.group_name);
                $('#startnewchat button[type="submit"]').html('Изменить');
                $('#new_chat_form').attr('conversation_id', group.from_user);
            });
        }
        $('#chat_' + username + ' .bottom button[type=submit]').click(function(){
            self.send_msg_helper(username, $('#chat_' + username + ' textarea'), is_group);
        });
        textarea.keydown(function(e){
            var code = e.keyCode ? e.keyCode : e.which;
            if (code == 13 && !e.shiftKey){
                self.send_msg_helper(username, $(this), is_group);
            }
        });
        $('#drop_chat_' + username).click(function(){
            if(confirm('Вы действительно хотите удалить чат "' + $(this).attr('data-name') + '"?')){
                self.drop_chat(username, is_group);
            }
        });
    }


    // ---------------------------------------------
    // Помечаем сообщения на сервере как прочитанные
    // ---------------------------------------------
    mark_messages_read(username, updated, is_group){
        var self = this;
        this.ajaxSetup();
        $.ajax({
            async : true,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            url: self.messages_api,
            data : JSON.stringify({
                'token': self.token,
                'is_encoded': true,
                'msg': {
                    'is_group': is_group,
                    'with_user': username,
                    'action': 'mark_messages_read',
                    'updated': updated,
                },
            }),
            success : function (r) {
                var conversation;
                var new_messages_container = $('#conversation_' + username + ' .new');
                if(is_group){
                    conversation = self.get_conversation(username);
                    conversation['new_messages'] = 0;
                    new_messages_container.addClass('hidden');
                    new_messages_container.find('span').html(conversation['new_messages']);
                }else{
                    for(var i=0; i<self.CONVERSATIONS.length; i++){
                        conversation = self.CONVERSATIONS[i];
                        if(conversation['filled'] === undefined){
                            continue;
                        }
                        if(conversation['user']['username'] === username){
                            self.CONVERSATIONS[i]['new_messages'] = 0;
                            new_messages_container.addClass('hidden');
                            new_messages_container.find('span').html(self.CONVERSATIONS[i]['new_messages']);
                            break;
                        }
                    }
                }
            }
        });
    }


    // ----------------------------------------------
    // Вспомогательная функция для отправки сообщения
    // ----------------------------------------------
    send_msg_helper(to_username, textarea, is_group){
        var msg = textarea.val();
        var group;
        var conversation;
        textarea.val('');
        autosize.update(textarea);
        msg = $.trim(msg);
        if(msg.length > 0){
            // Отправка сообщения в группу
            // to_username = id группы
            if(is_group){
                group = this.get_conversation(to_username);
                if(group !== null){
                    var usernames = [];
                    Object.keys(group.users).forEach(function(key) {
                         usernames.push(group.users[key].username);
                    });
                    this.send_msg({'to_group': usernames, 'action': 'to_group', 'msg': msg, 'group_id': to_username});
                    this.add_msg({'is_group': true, 'to_user': to_username, 'user': this.user, 'text': msg, 'type': this.STATUS_INFO}, true);
                }
                return;
            }
            // Отправка сообщения тет-а-тет
            this.send_msg({'to_user': to_username, 'action': 'to_user', 'msg': msg});
            this.add_msg({'to_user': to_username, 'user': this.user, 'text': msg, 'type': this.STATUS_INFO}, true);
        }
    }


    // ----------------
    // Окно нового чата
    // ----------------
    start_new_chat_listeners(){
        var self = this;
        var option;
        // Создание новой беседы
        $('.start_new_chat').click(function(){
            $('#participant_select2').val('');
            var usernames = [];
            $('#participant_select2').trigger("change");
            $('#startnewchat h1').html('Новый чат');
            $('#new_chat_topic').val('');
            $('#startnewchat button[type="submit"]').html('Создать новый чат');
            $('#new_chat_form').attr('conversation_id', '0');
        });

        $('#new_chat_form').submit(function(){
            var action = 'new_conversation';
            var conversation_id = $('#new_chat_form').attr('conversation_id');
            if(parseInt(conversation_id) > 0){
                action = 'edit_conversation';
            }
            var users = $('#participant_select2').val();
            if(users.length == 0){
                return;
            }
            var name = $('#new_chat_topic').val();
            // Закрываем нахер создание чата
            // а то накнопают, блеать
            $('#startnewchat').modal('toggle');
            $('#new_chat_topic').val('');
            $('#participant_select2').val('').trigger("change");
            self.ajaxSetup();
            $.ajax({
                async : true,
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                url: self.messages_api,
                data : JSON.stringify({
                    'token': self.token,
                    'is_encoded': true,
                    'msg': {
                        'name': name,
                        'users': users,
                        'action': action,
                        'conversation_id': conversation_id,
                    },
                }),
                success : function (r) {
                    if(action === 'edit_conversation'){
                        // После редактирования надо подправить беседу
                        var group = self.get_conversation(conversation_id);
                        group['group_name'] = r['group_name'];
                        group['contacts'] = r['contacts'];
                        group['filled'] = undefined;
                        group['users'] = [];
                        group['first'] = true;
                        $('#conversation_' + conversation_id).remove();
                    }else{
                        self.CONVERSATIONS.push(r);
                    }
                    self.fill_conversation_list();
                }
            });
            return false;
        });
        Object.keys(this.USERS_LIST).forEach(function(key) {
            option = $('<option value="' + key + '">' + key + '</option>');
            $('#participant_select2').append(option);
        });
        $('#participant_select2').select2({
            // Внутри модалки правильное функционирование только так
            dropdownParent: $('#startnewchat'),
            matcher: function(params, data) {
                if ($.trim(params.term) === '') {
                    return data;
                }
                // Do not display the item if there is no 'text' property
                if (typeof data.text === 'undefined') {
                    return null;
                }

                var found = true;
                var data_search = self.USERS_LIST[data.id]['search'];
                var value = params.term.split(' ');
                for(var i=0; i<value.length; i++){
                    if(data_search.indexOf(value[i]) === -1){
                        found = false;
                    }
                }

                // params.term should be the term that is used for searching
                // data.text is the text that is displayed for the data object
                if (found) {
                    //var modifiedData = $.extend({}, data, true);
                    //modifiedData.text += '';
                    //return modifiedData;
                    return data;
                }

                // Return null if the term should not be displayed
                return null;
            }
        });
    }

    // -------------------------------------
    // Поиск нужной беседы в нашем хранилище
    // -------------------------------------
    get_conversation(from){
        var conversation;
        for(var i=0; i<this.CONVERSATIONS.length; i++){
            conversation = this.CONVERSATIONS[i];
            if(conversation['is_group'] !== undefined){
                if(conversation['from_user'] == from){
                    return this.CONVERSATIONS[i];
                }
            }else{
                if(conversation['user'] !== undefined){
                    if(conversation['user']['username'] == from){
                        return this.CONVERSATIONS[i];
                    }
                }
            }
        }
        return undefined;
    }

    // ------------------------------
    // Вывод даты в привычном формате
    // ------------------------------
    strftime(d){
        var hours = d.getHours() + '';
        var minutes = d.getMinutes() + '';
        if(hours.length < 2){
            hours = '0' + hours;
        }
        if(minutes.length < 2){
            minutes = '0' + minutes;
        }
        return hours + ':' + minutes;
    }


    // -------------
    // Удаление чата
    // -------------
    drop_chat(username, is_group){
        var self = this;
        var conversation;
        this.ajaxSetup();
        $.ajax({
            async : true,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            url: self.messages_api,
            data : JSON.stringify({
                'token': self.token,
                'is_encoded': true,
                'msg': {
                    'with_user': username,
                    'action': 'drop_chat',
                },
            }),
            success : function (r) {
                if(r['success']){
                    if(is_group){
                        // Удаление группого чата
                        for(var i=0; i<self.CONVERSATIONS.length; i++){
                            conversation = self.CONVERSATIONS[i];
                            if(conversation['is_group'] === undefined){
                                continue
                            }
                            if(conversation['from_user'] === username){
                                $('#conversation_' + username).remove();
                                $('#chat_' + username).remove();
                                self.CONVERSATIONS.splice(i, 1);
                                break
                            }
                        }
                    }
                }else if(r['error']){
                    alert(r['error']);
                }
            }
        });
    }


}