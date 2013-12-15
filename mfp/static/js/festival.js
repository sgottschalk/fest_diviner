$(document).ready(function(){
    $("#artistSearchBox").autocomplete({
      source: "/festivals/artists/search",
      minLength: 2,
      delay: 500,
      select: function( event, ui ) {
        event.preventDefault(); // stop from filling in search box
        $('#songkickId').val(ui.item.value); // fill in hidden input with value
        $('#artistSearchBox').val(ui.item.label); // fill in text input with value
        $.post($('#festivalHeader').data("festivalId") + '/add', $("#artistSearchForm").serialize(), function(data) {
            // TODO: do we reload here?
            console.log("added. data: " + data);
        });
        $("#artistSearchBox").val(''); // clear out search box text
      }
    });
});