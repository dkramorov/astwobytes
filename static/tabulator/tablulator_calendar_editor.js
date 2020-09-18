var conclusionDateEditor = function(cell, onRendered, success, cancel, editorParams){
  var cellValue = cell.getValue(),
  input = document.createElement("input");
  input.setAttribute("type", "text");
  input.value = typeof cellValue !== "undefined" ? cellValue : "";
  onRendered(function(){
    input.style.height = "100%";
    $(input).datepicker({
      onClose: onChange,
      onSelect: function (fd, d, calendar) {
        calendar.hide();
        onChange(fd);
      },
      todayButton: new Date(),
    });
    input.focus();
  });
  function onChange(e){
    if(((cellValue === null || typeof cellValue === "undefined") && input.value !== "") || input.value != cellValue){
      success(input.value);
    }else{
      cancel();
    }
  }
  //submit new value on enter
  $(input).on("keydown", function(e){
    if(e.keyCode == 13){
      success($(input).val());
    }
    if(e.keyCode == 27){
      cancel();
    }
  });
  return input;
}
