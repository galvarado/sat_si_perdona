$(function() {
  // Initialize table
  datatable = $('#credits-search-datatable').dataTable({
    "bJQueryUI": true,
    "sPaginationType": "full_numbers",
    "bProcessing": true,
    "sAjaxSource": "get_credits_search",
    "bServerSide": true,
    "oLanguage": {
      "sUrl": STATIC_URL + "main/js/libs/dataTables.spanish.txt"
    },
    "aoColumns": [
        { "sWidth": "10%" },
        { "sWidth": "10%" },
        { "sWidth": "30%" },
        { "sWidth": "10%" },
        { "sWidth": "20%" },
    ],
    // Fill the table with ajax source
    "fnServerData": function ( sSource, aoData, fnCallback ) {
      $.ajax({
        "dataType": 'json',
        "type": "POST",
        "url": sSource,
        "data": aoData,
        "success": fnCallback
      });
    }
  });
  $('#specific-search').keyup(function(){
    datatable.fnFilter($(this).val());
  });
});