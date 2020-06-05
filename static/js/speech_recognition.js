// ---------------------------------------
// Класс для отправки формы обратной связи
// ---------------------------------------
function _parseTranscript(e) {
    return Array.from(e.results).map(function (result) {
        return result[0];
    }).map(function (result) {
        return result.transcript;
    }).join('');
}
class MySpeechRecognition {
    constructor(input_id, lang) {
        // :param input_id: ид элемента input
        // :param lang: язык (ru-RU)
        if(lang == undefined){
            lang = 'ru-RU';
        }
        var $ = jQuery;
        window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if(!window.SpeechRecognition){
            console.log('[ERROR]: SpeechRecognition is not supported!');
            return;
        }
        var input = $('#' + input_id);
        var sp_class = 'speech_recognition_touched';
        if(input.hasClass(sp_class)){
            return;
        }
        input.addClass(sp_class);
        // надо добавить иконку-микрофон на input
        var voice_trigger_html = '<span id="voice-trigger-' + input_id + '" class="voice-trigger hidden"><i class="fa fa-microphone"></i></span>';
        $('#' + input_id).after($(voice_trigger_html));
        var voice_trigger = $("#voice-trigger-" + input_id);

        var recognition = new window.SpeechRecognition();
        recognition.interimResults = true;
        recognition.lang = lang;
        recognition.addEventListener('result', function(e){
            var speechOutput = _parseTranscript(e);
            input.val(speechOutput);
            if (e.results[0].isFinal) {
                // we can here _form.submit();
            }
        });

        var is_recognizing = false;
        recognition.onstart = function () {
            is_recognizing = true;
            voice_trigger.addClass('active');
        };
        recognition.onend = function () {
            is_recognizing = false;
            voice_trigger.removeClass('active');
        };
        recognition.onerror = function(event) {
            is_recognizing = false;
            console.log('[ERROR]: ', event.error);
            if(event.error == 'no-speech'){
                voice_trigger.removeClass('active');
            }
            voice_trigger.removeClass('active');
        }
        voice_trigger.removeClass('hidden');

        voice_trigger.on('click touch', function(e){
            e.preventDefault();
            if(!is_recognizing){
                recognition.start();
            }
        });
    }
}
