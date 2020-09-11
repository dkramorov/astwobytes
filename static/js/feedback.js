// ---------------------------------------
// Класс для отправки формы обратной связи
// requirements:
// jquery.form.min.js
// jquery.validate.min.js
// в input data-msg="Введите вашу почту"
// ---------------------------------------
class FeedBack {
    constructor(form_id, custom_fm) {
        // :param form_id: id формы
        // :param fm: feedback_messages сообщени по состоянию
        var $ = jQuery;
        var instance = this;

        this.form_id = form_id;
        var fid = "#" + this.form_id;

        var form = $(fid);
        if(form.length < 1){
            console.log("form not found", fid);
        }
        var default_fm = {
            "wait": "Ждите...",
            //"send": "Отправить",
            "success": "Сообщение отправлено. Спасибо!",
            "progress": "Пожалуйста, ждите...",
            "error": "Произошла ошибка, сообщите нам по телефону",
            "error_captcha": "Не пройдена проверка на работа",
            "callback_success": "",
            "callback_error": "",
            "dont_reset_on_submit": "", // or 1
            //"errorClass": "invalid",
        }
        var fm = custom_fm;
        if(custom_fm === undefined){
            fm = default_fm;
        }
        var fb_close = "<button class='close' type='button'>×</button>";
        var fb_success = "<div style='display:none;' class='successMessage alert alert-success'>" + fb_close + fm['success'] + "</div>";
        var fb_error = "<div style='display:none;' class='errorMessage alert alert-danger'>" + fb_close + fm['error'] + "</div>";
        var fb_progress = "<div style='display:none;' class='notifyMessage alert alert-warning'>" + fb_close + fm['progress'] + "</div><div class='clear clearfix'></div>";

        var alerts = "";
        alerts += fb_success + fb_error + fb_progress;

        var fb_alerts = $(fid + " .feedback_alerts");
        if(fb_alerts.length < 1){
            console.log(fid, "zero-length .feedback_alerts");
        }else{
            fb_alerts.html(alerts);
        }
        var input_submit = $(fid + " [type='submit']:not(.freeze)");
        instance.close_listener(fid);
        // ---------------------------
        // Запоминаем названия кнопок,
        // чтобы вернуть их обратно
        // ---------------------------
        input_submit.each(function(){
          $(this).attr("data-original-name", $(this).val());
        });
        input_submit.attr("disabled", false);

        $(fid).validate({
            // ---------------------------------
            // Сделать свои сообщения об ошибках
            // ---------------------------------
            //errorClass: "invalid"
            //http://jqueryvalidation.org/validate/#toptions
        });
        $(fid).ajaxForm({
            beforeSubmit: function(){
                var is_valid = $(fid).valid();
                if(is_valid){
                    $(fid + " .notifyMessage").show();
                    input_submit.attr("disabled", "disabled").val(fm['wait']);
                }
                return is_valid;
            },
            error: function(responseText, statusText, xhr, $form){
                $(fid + " .errorMessage").show();
                $(fid + " .successMessage").hide();
                $(fid + " .notifyMessage").hide();
                $(fid + " .errorCaptcha").hide();
            },
            success: function(responseText, statusText, xhr, $form){
                $(fid + " .errorMessage").hide();
                $(fid + " .successMessage").hide();
                $(fid + " .notifyMessage").hide();
                $(fid + " .errorCaptcha").hide();
                input_submit.attr("disabled", false);

                // --------------------------
                // Возвращаем названия кнопок
                // --------------------------
                input_submit.each(function(){
                    $(this).val($(this).attr("data-original-name"));
                });
                // Выводим либо стандартную ошибку,
                // либо ошибки responseText['errors']
                if(responseText['error'] || responseText['errors']){
                    $(fid + " .notifyMessage").hide();
                    if(responseText['error_captcha']){
                        $(fid + " .errorCaptcha").show();
                        return;
                    }
                    if(responseText['errors']){
                        $(fid + " .errorMessage").html(fb_close + responseText['errors'].join('<br>'));
                        instance.close_listener(fid);
                    }
                    $(fid + " .errorMessage").show();
                    if(fm['callback_error']){
                        fm['callback_error'](responseText);
                    }
                }else{
                    $(fid + " .successMessage").show();
                    $(fid + " .notifyMessage").hide();
                    if(fm['callback_success']){
                        fm['callback_success'](responseText);
                    }
                }
                if(fm['dont_reset_on_submit'] !== 1){
                    $(fid)[0].reset();
                }
            }
        });
    }
    close_listener(fid){
        $(fid + " .close").on("click", function(){
            $(this).parent().hide();
/*
            $(fid + " .errorMessage").hide();
            $(fid + " .successMessage").hide();
            $(fid + " .notifyMessage").hide();
            $(fid + " .errorCaptcha").hide();
*/
        });
    }
}
