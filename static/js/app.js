(function( $ ) {

  $.fn.clickThrough = function() {
    var $select = this,
        sel_length = $select.children('option').length-1;
    $select.hide().after("<span class='option'></span>");
    var $span = $select.next();

    $span.mousedown(function() {
      var current_idx = $select.val();
      if(current_idx == sel_length) { current_idx = 0 } else { current_idx++; }
      $select.val( current_idx );
      $span.text( $select.find('option:selected').text() );
    });

    $select.val( Math.floor(Math.random() * sel_length) );
    $span.text( $select.find('option:selected').text() );
    return this;
  };
}( jQuery ));


$('#id_address').focus();

$('#id_theme').clickThrough();
$('#id_color').clickThrough();
$('#id_price').clickThrough();
$('#id_curator').clickThrough();
