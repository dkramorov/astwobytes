class FastChat{
    constructor() {
        // Со странички чата не надо делать запросы
        this.interval = 3000;
        this.DEFAULT_AVATAR = '/static/admin/misc/avatar_small.png';
        this.received = Array();
        this.messages = Array();
        this.url = $('#fast_chat_form_action').attr('data-url');
        this.chat_page_url = $('#fast_chat_form_action').attr('data-chat-url');
        this.id_name = 'identifier_name';
        this.id_value = '' + (new Date()).getTime();
        // Замок на потрахон сервачка
        this.master_lock = true;
        this.is_storage = false;

        // Проверяем поддержку оповещений
        this.with_notify = true;
        if (!("Notification" in window)) {
            this.with_notify = false;
        }
        this.mark_all_read_listener();
        this.live_notifications = true;
        if(window.location.pathname === this.chat_page_url){
            this.live_notifications = false;
        }else{
            this.is_storage = this.check_storage();
        }

        var self = this;
        if(this.is_storage){
            setInterval(function(){
                self.check_master_lock();
            }, this.interval);
        }
        setTimeout(function(){
            self.check_unread_messages_helper();
        }, 2000);
        console.log('--- FastChat initialization ---', this.id_value);
    }
    // -------------------------------------
    // Задать замок на потрахивание сервера,
    // если есть поддержка хранилища
    // -------------------------------------
    set_master_lock(new_id_value){
        this.master_lock = true;
        // Задаем замочек на наш экземпляр
        window.localStorage.setItem(this.id_name, this.id_value);
        // Задаем дату обновления
        window.localStorage.setItem(this.id_value, new_id_value);
    }
    // ---------------------------------------------
    // Проверяем монополию на потрахивание сервачка,
    // если есть поддержка хранилища
    // ---------------------------------------------
    check_master_lock(){
        var id_value = window.localStorage.getItem(this.id_name);
        var new_id_value = '' + (new Date()).getTime();
        // Забираем замок на себя
        if(id_value === null){
            this.set_master_lock(new_id_value);
            console.log('Иницализирован замок');
            return;
        }
        // Замок наш - обновляемся
        if(id_value === this.id_value){
            this.set_master_lock(new_id_value);
            console.log('Замок наш');
        }else{
            this.master_lock = false;
            // Но если того, кто ставил замок съели динозавры
            // надо нам перехватить инициативу
            var old_id_value = window.localStorage.getItem(id_value);
            if( (parseInt(new_id_value) - parseInt(old_id_value)) > this.interval*2){
                this.set_master_lock(new_id_value);
                console.log('Замок перехвачен нами');
            }else{
                console.log('Управление с другой вкладки');
                var received = localStorage.getItem('fast_chat_received');
                if(received !== null && received !== JSON.stringify(this.received)){
                    var messages = localStorage.getItem('fast_chat_messages');
                    messages = JSON.parse(messages);
                    this.messages = Array();
                    this.received = Array();
                    for(var i=0; i<messages.length; i++){
                        for(var j=0; j<messages[i]['messages'].length; j++){
                            this.received.push(messages[i]['messages'][j].id);
                        }
                        this.messages.push(messages[i]);
                    }
                    var container = $('#fast_chat_unread_messages .scroll-content');
                    container.html('');
                    this.fill_unread_messages(this.messages);
                }else{
                    console.log('собщения не изменились');
                }
            }
        }
    }
    // -------------------
    // Проверить хранилище
    // -------------------
    check_storage(){
        var test = 'test_localStorage';
        try{
            window.localStorage.setItem(test, test);
            window.localStorage.getItem(test);
            window.localStorage.removeItem(test);
        }catch(e){
            return false;
        }
        var self = this;
        this.master_lock = false;
        // Задаем в хранилище свой идентификатор,
        // если вдруг другое окно захочет подписаться на события,
        // то надо проверить идентификатор - если он не обновлялся
        /*
        window.addEventListener('storage', function(e) {
            console.log("ВНИМАНИЕ БЛЯДЬ: НЕ РЕАГИРУЕТ НА ТОЙ ЖЕ СТРАНИЧКЕ", e);
        });
        */

        this.check_master_lock();
        //console.log('Замок на потрахон сервачка:', this.master_lock);
        return true;
    }

    // ----------------------------------------------
    // Заполнить непрочитанные сообщения из хранилища
    // ----------------------------------------------
    fill_unread_messages(){
        var obj;
        var avatar;
        var msg;
        var new_msg;
        var messages_count = this.received.length;

        $('#fast_chat_uread_messages_counter div.label').html(messages_count);
        var container = $('#fast_chat_unread_messages .scroll-content');
        //container.html('');
        if(messages_count === 0){
            $('#fast_chat_unread_messages div.scroll-viewport').addClass('hidden');
            $('#fast_chat_unread_messages li.mark_all_read').addClass('hidden');
            $('#fast_chat_unread_messages .dropdown-menu-header').html('Нет новых сообщений');
        }else{
            $('#fast_chat_unread_messages div.scroll-viewport').removeClass('hidden');
            $('#fast_chat_unread_messages li.mark_all_read').removeClass('hidden');
            $('#fast_chat_unread_messages .dropdown-menu-header').html('Новые сообщения');
            for(var i=0; i<this.messages.length; i++){
                obj = this.messages[i];
                avatar = this.DEFAULT_AVATAR;
                for(var j=0; j<obj['messages'].length; j++){
                    msg = obj['messages'][j];
                    // Пропускаем, если уже выведено
                    if(msg.filled !== undefined){
                        continue;
                    }
                    msg.filled = true;
                    new_msg = `
<a class="list-group-item" href="${this.chat_page_url}?contact=${obj.user.id}" target="_blank">
  <div class="media">
    <div class="pull-left">
      <img class="media-object img-circle thumb48" src="${avatar}"/>
    </div>
    <div class="media-body clearfix">
      <small class="pull-right">${msg.time}</small>
      <strong class="media-heading text-primary">
        <span class="point point-info point-md"></span>
        ${obj.user.last_name} ${obj.user.first_name} ${obj.user.username}
      </strong>
      <p class="mb-sm">
        <small>${msg.text}</small>
      </p>
    </div>
  </div>
</a>`;
                    container.append($(new_msg));
                }
            }
        }
    }
    // -------------------------------
    // Проверка новых сообщений в базе
    // -------------------------------
    check_unread_messages(){
        var self = this;
        if(!this.live_notifications){
            return;
        }
        setTimeout(function(){
            //console.log('--- check unread messages ---');
            self.check_unread_messages_helper();
        }, self.interval);
    }
    // --------------------------------
    // Добавить в прочитанные сообщения
    // --------------------------------
    add_to_received(messages){
        for(var i=0; i<messages.length; i++){
            this.messages.push(messages[i]);
            for(var j=0; j<messages[i]['messages'].length; j++){
                this.received.push(messages[i]['messages'][j].id);
            }
        }
        // Записать сообщения в хранилище
        if(this.is_storage){
            window.localStorage.setItem('fast_chat_messages', JSON.stringify(this.messages));
            window.localStorage.setItem('fast_chat_received', JSON.stringify(this.received));
        }
    }
    check_unread_messages_helper(){
        if(!this.master_lock){
            this.check_unread_messages();
            return;
        }
        var self = this;
        var messages = Array();
        $.ajax({
            async : true,
            type: 'POST',
            data: 'action=get_new_messages&exclude=' + self.received,
            url: self.url,
            success : function (r) {
                // Это первый запрос, поэтому переинициализация
                if(self.received.length === 0){
                    window.localStorage.removeItem('fast_chat_messages');
                    window.localStorage.removeItem('fast_chat_received');
                }
                if(r.length > 0){
                    self.add_to_received(r);
                    self.fill_unread_messages();
                    self.notifyMe('У вас есть новые сообщения', 'Новых сообщений: ' + r.length);
                }
                self.check_unread_messages();
            }
        });
    }
    mark_all_read_listener(){
        var self = this;
        $('.mark_all_read').click(function(){
            $.ajax({
                async : true,
                type: 'POST',
                data: 'action=mark_messages_read&ids=' + self.received,
                url: self.url,
                success : function (r) {
                    // скрывать нет нужды
                    self.notifyMe('Сообщения отмечены прочитанными', '');
                }
            });
        });
    }
    // https://developer.mozilla.org/en-US/docs/Web/API/notification#Browser_compatibility
    notifyMe(title, text) {
        if(!this.with_notify){
            return;
        }
        var options = {
            body: text,
        }
        if (Notification.permission === "granted") {
            var notification = new Notification(title, options);
            return;
        }else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(function (permission) {
                if (permission === "granted") {
                    var notification = new Notification(title, options);
                    return;
                }
            });
        }
        // Не беспокоим повторно
        this.with_notify = false;
    }
}

$(document).ready(function(){
    var fast_chat = new FastChat();
});