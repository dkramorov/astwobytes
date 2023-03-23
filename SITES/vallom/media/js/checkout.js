$(document).ready(function(){
  $(document).on('click','.md-modal .close', function(e){
    e.preventDefault();
    $('.md-modal').removeClass('md-show');
  });
});
