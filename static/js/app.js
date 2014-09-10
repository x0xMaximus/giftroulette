$('select').mousedown(function(evt) {
  var $el = $(this),
      current_idx = $el.val();
  if(current_idx == $el.children('option').length-1) { current_idx = 0 } else { current_idx++; }
  $el.val( current_idx )
});
$('#id_address').focus();
