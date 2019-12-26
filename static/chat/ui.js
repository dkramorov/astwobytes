// -----------------------------
// Класс для работы с сообщением
// -----------------------------
class WSMessage{
    constructor() {
        console.log('--- WSMessage initialization ---');
    }
    // ---------------
    // Новое сообщение
    // ---------------
    new_msg(direction, msg, avatar){
        if(direction === 'from_me'){
             return `
<div class="message me">
  <div class="text-main">
    <div class="text-group me">
      <div class="text me">
        <pre>${msg.text}</pre>
      </div>
    </div>
    <span>${msg.time}</span>
  </div>
</div>`;
        }
        if(direction === 'to_me'){
            return `
<div class="message">
  <img class="avatar-md" src="${avatar}">
  <div class="text-main">
    <div class="text-group">
      <div class="text">
        <pre>${msg.text}</pre>
      </div>
    </div>
    <span>${msg.time}</span>
  </div>
</div>`;
        }
        return '';
    }
}

// ------------------------
// Класс для работы с чатом
// ------------------------
class WSChat{
    constructor() {
        console.log('--- WSChat initialization ---');
    }
    // ---------
    // Новый чат
    // ---------
    new_chat(username, avatar, status_class, status_str, name){
        return `
<div class="chat" id="chat_${username}">
  <div class="top">
    <div class="col-md-12">
      <div class="inside">
        <a href="#">
          <img class="avatar-md" src="${avatar}">
        </a>
        <div class="status">
          <i class="fa fa-circle material-icons ${status_class}"></i>
        </div>
        <div class="data">
          <h5><a href="#">${name}</a></h5>
          <span>${status_str}</span>
        </div>
        <button class="btn connect d-md-block d-none" name="1">
          <i class="fa fa-phone material-icons md-30"></i>
        </button>
        <button class="btn connect d-md-block d-none" name="1">
          <i class="fa fa-video-camera material-icons md-36"></i>
        </button>
        <button class="btn d-md-block d-none conversation_information" data-toggle="modal" data-target="#startnewchat">
          <i class="fa fa-info-circle material-icons md-30"></i>
        </button>
        <div class="dropdown">
          <button class="btn" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="fa fa-ellipsis-v material-icons md-30"></i>
          </button>
          <div class="dropdown-menu dropdown-menu-right">
            <button class="dropdown-item connect" name="1">
              <i class="fa fa-phone material-icons"></i>Голосовой вызов
            </button>
            <button class="dropdown-item connect" name="1">
              <i class="fa fa-video-camera material-icons"></i>Видео вызов
            </button>
            <hr>
            <button class="dropdown-item" id="drop_chat_${username}" data-name="${name}">
              <i class="fa fa-trash material-icons"></i>Удалить чат
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="clearfix"></div>
  </div>
  <div class="content" id="content_${username}">
    <div class="col-md-12 messages">
    </div>
    <div class="clearfix"></div>
  </div>
  <div class="col-md-12">
    <div class="bottom">
      <form class="position-relative w-100">
        <textarea class="form-control" placeholder="Ваше сообщение..." rows="1"></textarea>
        <button class="btn emoticons"><i class="fa fa-smile-o material-icons"></i></button>
        <button type="submit" class="btn send"><i class="fa fa-location-arrow material-icons"></i></button>
      </form>
    </div>
    <div class="clearfix"></div>
  </div>
  <div class="clearfix"></div>
</div><div class="clearfix"></div>`;
    }
}

// --------------------------
// Класс для работы с беседой
// --------------------------
class WSConversations{
    constructor(parent) {
        console.log('--- WSConversation initialization ---');
        this.parent = parent;
    }
    new_conversation(username, new_messages, name,
                     time, date, text, avatar, is_first){
        var conversation_time = `<span>${time} ${date}</span>`;
        var new_msg_class = '';
        if(new_messages == 0){
            new_msg_class = ' hidden';
        }
        var new_messages_block = `
<div class="new bg-blue${new_msg_class}">
  <span>${new_messages}</span>
</div>`;
        return `
<a href="javascript:void(0);" id="conversation_${username}" class="single conversation">
  <img class="avatar-md" src="${avatar}">
  <div class="status">
    <i class="fa fa-circle offline material-icons"></i>
  </div>
  ${new_messages_block}
  <div class="data">
    <h5>${name}</h5>
    ${conversation_time}
    <p>${text}</p>
  </div>
</a>`;
    }
    // -----------
    // Поиск бесед
    // -----------
    search_conversations(){
        var self = this;
        var pk_conversations = self.parent.pk_conversations;
        this.parent.search_input_conversations.keyup(function(event) {
            var CONVERSATIONS = self.parent.CONVERSATIONS;
            var value = $.trim($(this).val()).toLowerCase();
            if(value === ''){
                $('#' + pk_conversations + ' .conversation').removeClass('hidden');
                return;
            }
            var found = true;
            var data_search = '';
            var is_group;
            value = value.split(' ');
            // TODO: групповые беседы
            for(var i=0; i<CONVERSATIONS.length; i++){
                found = true;
                is_group = CONVERSATIONS[i]['is_group'] !== undefined;
                if(is_group){
                    data_search = CONVERSATIONS[i]['group_name'].toLowerCase();
                }else{
                    data_search = CONVERSATIONS[i]['user']['search'];
                }
                for(var j=0; j<value.length; j++){
                    if(data_search.indexOf(value[j]) === -1){
                        found = false;
                    }
                }
                if(found){
                    is_group ? $('#conversation_' + CONVERSATIONS[i]['from_user']).removeClass('hidden') : $('#conversation_' + CONVERSATIONS[i]['user']['username']).removeClass('hidden');
                }else{
                    is_group ? $('#conversation_' + CONVERSATIONS[i]['from_user']).addClass('hidden') : $('#conversation_' + CONVERSATIONS[i]['user']['username']).addClass('hidden');
                }
            }
        });
    }
}

// -----------------------------
// Класс для работы с контактами
// -----------------------------
class WSContacts{
    constructor(parent) {
        console.log('--- WSContacts initialization ---');
        this.parent = parent;
    }
    new_contact(username, avatar, name, email){
        return `
<a href="#" class="contact" id="contact_${username}">
  <img class="avatar-md" src="${avatar}">
  <div class="status">
    <i class="fa fa-circle offline material-icons"></i>
  </div>
  <div class="data">
    <h5>${name}</h5>
    <p>${email}</p>
  </div>
  <div class="person-add">
    <i class="fa fa-user material-icons"></i>
  </div>
</a>)`;
    }
    // ---------------
    // Поиск контактов
    // ---------------
    activate_search(){
        var self = this;
        var pk_contacts = self.parent.pk_contacts;
        var USERS_LIST;
        this.parent.search_input.keyup(function(event) {
            USERS_LIST = self.parent.USERS_LIST;
            var value = $.trim($(this).val()).toLowerCase();
            if(value === ''){
                $('#' + pk_contacts + ' .contact').removeClass('hidden');
                return;
            }
            var found = true;
            var data_search = '';
            value = value.split(' ');

            Object.keys(USERS_LIST).forEach(function(key) {
                found = true;
                data_search = USERS_LIST[key]['search'];
                for(var i=0; i<value.length; i++){
                    if(data_search.indexOf(value[i]) === -1){
                        found = false;
                    }
                }
                if(found){
                    $('#contact_' + USERS_LIST[key]['username']).removeClass('hidden');
                }else{
                    $('#contact_' + USERS_LIST[key]['username']).addClass('hidden');
                }
            });
        });
    }
}