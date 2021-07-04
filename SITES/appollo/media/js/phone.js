window.sip_config = {
  traceSip: false,
  register: false,
  userAgentString: window.personal_user_id ? window.personal_user_id : 'sipjs',
  stunServers: ['stun:91.185.46.56:3478'],
};

function load_free_calls(){
  if(typeof(DetectRTC) == "undefined"){
    var head_el = document.getElementsByTagName("head")[0];
    var rtc_script = document.createElement("script");
    rtc_script.type = "text/javascript";
    rtc_script.src = "/static/call_from_site/js/DetectRTC.js";
    rtc_script.onload = function(){
      var is_webrtc_supported = false;
      DetectRTC.load(function(){
        is_webrtc_supported = DetectRTC.isWebRTCSupported;
        if(is_webrtc_supported){
          load_sipjs();
        }else{
          $("#call_error").html("К сожалению, ваш браузер не поддерживает технологию звонков, пожалуйста, воспользуйтесь другим браузером");
          $("#call_error").show();
        }
      });
    };
    head_el.appendChild(rtc_script);
  }else{
    console.log("DetectRTC already loaded");
  }
}
function connected_to_server(){
  $(".make_call").show();
}
function load_sipjs(callback){
  if(typeof(SIP) == "undefined"){
    var head_el = document.getElementsByTagName("head")[0];
    var sip_script = document.createElement("script");
    sip_script.type = "text/javascript";
    sip_script.src = "/static/call_from_site/js/sip-0.7.8.js";
    sip_script.onload = function(){
      var not_registered_error = $(".not_registered_error").length;
      var not_confirmed_phone_error = $(".not_confirmed_phone_error").length;

      var sipua_script = document.createElement("script");
      sipua_script.type = "text/javascript";
      sipua_script.src = "/static/call_from_site/js/ua-0.7.3.js?v=2";
      sipua_script.onload = function(){
        connect_to_server(connected_to_server);
        set_call_controls($(".make_call"), $(".hangup"), $(".call_timer"));
        set_phone_mask();
        set_phone_prefix("8800");
        $(".make_call").click(function(){
          if($(this).attr('data-phone') != undefined){
            $("#phone_number").val($(this).attr('data-phone'));
          }
          $(".not_registered_error").addClass("hidden");
          $(".not_confirmed_phone_error").addClass("hidden");
          // -------------------
          // Событие для метрики
          // -------------------
          /*
          var ym = search_yandex_counter_number();
          if(ym !== null){
            ym.reachGoal('call_from_browser');
          }
          */
          $("#ext_dial").val("");
          var phone_value = $("#phone_number").val();
          var digits = "";
          for(var i=0; i<phone_value.length; i++){
            if("0123456789".indexOf(phone_value[i]) > -1){
              digits += phone_value[i];
            }
          }

          if(not_registered_error == 0){
            if(not_confirmed_phone_error == 0){
              var new_call = make_call(digits);
              if(new_call !== 1){
                show_error(new_call);
              }
            }else{
              if(digits === "88000000000"){
                var new_call = make_call(phone_value);
                if(new_call !== 1){
                  show_error(new_call);
                }
              }else{
                $(".not_confirmed_phone_error").removeClass("hidden");
              }
            }
          }else {
            if(digits === "88000000000"){
              var new_call = make_call(phone_value);
              if(new_call !== 1){
                show_error(new_call);
              }
            }else{
              $(".not_registered_error").removeClass("hidden");
            }
          }

        });
        $(".hangup").click(function(){
          hangup_call();
        });
        $(".keypad-toggle-link").click(function(){
          $("div.digits").toggleClass("visible");
          $(this).toggleClass("active");
        });
        $(".js-call_phone_btn").click(function(){
          var key = $(this).find("span").html();
          if(active_session){
            var dtmf_value = $("#ext_dial").val();
            $("#ext_dial").val(dtmf_value + key);
          }else{
            var phone = $("#phone_number").val();
            $("#phone_number").val(phone + key);
          }
        });
        $(".clear_phone").click(function(){
          if(active_session){
            $("#ext_dial").val("");
          }else{
            $("#phone_number").val("");
          }
        });
        $(".ext_dial_button").click(function(){
          var dtmf = $("#ext_dial").val();
          $(".dtmf input[type=\"text\"]").val(dtmf);
          console.log("sending dtmf "+dtmf);
          send_dtmf(dtmf);
          $("#ext_dial").val("");
        });
      };
      head_el.appendChild(sipua_script);
    };
    head_el.appendChild(sip_script);
  }else{
    console.log("SIP already loaded");
  }
}

function set_phone_mask(){
  var head_el = document.getElementsByTagName("head")[0];
  var phone_mask_script = document.createElement("script");
  phone_mask_script.type = "text/javascript";
  phone_mask_script.src = "/static/js/jquery.maskedinput.min.js";
  phone_mask_script.onload = function(){
    $("input[type='text'].phone").mask("8(800) 999-9999");
    //$("input[type='text'].phone").mask("8(9999) 999-999");
  };
  head_el.appendChild(phone_mask_script);
}

function show_error(error){
  $("#call_error").html(error);
  $("#call_error").show();
  setTimeout(function(){
  $("#call_error").fadeOut("slow", function(){
    $("#call_error").hide();
  });
  }, 1500);
}
$(document).ready(function(){

  /* Современный номеронабиратель */
  if($("#modern_phone").length > 0){
    load_free_calls();
  }

  /* Ретро номеронабиратель */
  if($("#retro_phone").length < 1){
    return;
  }
	const wheelElm = document.querySelector('#wheel');
	const numberElm = document.querySelector('#number');

	var isDragging = false;
	var isRewinding = false;

	var wheelAngle = 0;
	var wheelCenter = null;
	var dragStartAngle = null;

	// -----------------------------------------------
	// Dragging

	function startDrag(e) {
		e.preventDefault();
		if (isRewinding) {
			return;
		}

		isDragging = true;
		wheelCenter = getCenterPoint(wheelElm.getBoundingClientRect());
		dragStartAngle = getAngle({ x: e.clientX, y: e.clientY }, wheelCenter);
		document.body.addEventListener('mouseup', endDrag);
		document.body.addEventListener('mousemove', drag);
	}

	function endDrag(e) {
		document.body.removeEventListener('mouseup', endDrag);
		document.body.removeEventListener('mousemove', drag);
		isDragging = false;
		startRewind();
	}

	function drag(e) {
		const angle = getAngle({ x: e.clientX, y: e.clientY }, wheelCenter);
		var angleDiff = angle - dragStartAngle;

		// Convert the angle range from (-180 to 180) to (0 to 360).
		angleDiff = angleDiff < 0 ? 360 - (-angleDiff) : angleDiff;
		setWheelRotation(angleDiff);
	}

	// -----------------------------------------------
	// Rewinding

	function startRewind() {
		if (wheelAngle <= 0) {
			return;
		}

		isRewinding = true;
		const num = getNumberFromAngle(wheelAngle);
		const rewindTime = (wheelAngle * 4.5) << 0
		wheelElm.style.transition = `transform ${rewindTime}ms linear`;
		setWheelRotation(0);

		setTimeout(() => endRewind(num), rewindTime);
	}

	function endRewind(number) {
		wheelElm.style.transition = 'none';
		isRewinding = false;
		appendNumber(number);
	}

	// -----------------------------------------------
	// Functions

	function setWheelRotation(angle) {
		if (angle > 295) {
			angle = angle < 315 ? 295 : 0;
		}

		wheelAngle = angle;
		wheelElm.style.transform = `rotate(${angle}deg)`;
	}

	function appendNumber(num) {
		if (Number.isNaN(num) || num === null) {
			return;
		}

		numberElm.innerHTML += num;
	}

	function getNumberFromAngle(angle) {
		var number = Math.floor((angle + 6) / 24) - 2;
		if (number < 1) {
			return null;
		} else if (number > 9) {
			return 0;
		}

		return number;
	}

	function getCenterPoint(rect) {
		return {
			x: rect.left + (rect.width / 2),
			y: rect.top + (rect.height / 2)
		};
	}

	function getAngle(p1, p2) {
		const deltaX = p2.x - p1.x;
		const deltaY = p2.y - p1.y;
		return Math.atan2(deltaY, deltaX) * 180 / Math.PI;
	}

	// -----------------------------------------------
	// Events

	wheel.addEventListener('mousedown', startDrag);

});
