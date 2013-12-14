$(document).ready(function(){
    $("#artistSearchBox").autocomplete({
      source: "/festivals/artists/search",
      minLength: 2,
      delay: 500,
      select: function( event, ui ) {
        event.preventDefault(); // stop from filling in search box
        $("#artistSearchBox").val(''); // clear out search box text
        $('#songkickId').val(ui.item.value); // fill in hidden input with value
        $.post($('#festivalHeader').data("festivalId") + '/add', $("#artistSearchForm").serialize(), function(data) {
            // TODO: do we reload here?
            alert('yes!');
        });
      }
    });
});