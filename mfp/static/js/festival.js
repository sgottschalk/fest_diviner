$(document).ready(function(){
    $('#artistTable').dataTable({
        "bJQueryUI": true,
        "bPaginate": false,
        "bInfo": false,
        "bLengthChange": false,
        "bSortClasses": false
    });

    // Set up the search box
    // TODO: trim whitespace
    $("#artistSearchBox").autocomplete({
      source: "/planner/festivals/artists/search",
      minLength: 2,
      delay: 500,
      search: function( event, ui ) {
        $("#noArtistFoundMsg").hide();
        $("#artistSearchSpinner").show();
      },
      response: function( event, ui ) {
        $("#artistSearchSpinner").hide();
        if (ui.content.length === 0) {
            $("#noArtistFoundMsg").show();
        }
      },
      select: function( event, ui ) {
        event.preventDefault(); // stop from filling in search box
        $('#songkickId').val(ui.item.value); // fill in hidden input with value
        $('#artistSearchBox').val(ui.item.label); // fill in text input with value
        $.post($('#festivalHeader').data("festivalId") + '/add', $("#artistSearchForm").serialize(), function(data) {
            // TODO: don't reload the whole page
            window.location.reload();
        });
        $("#artistSearchBox").val(''); // clear out search box text
      }
    });
});