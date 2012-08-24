$(function() {
  // Initialize table
  datatable = $('#credits-search-datatable').dataTable({
    "bJQueryUI": true,
    "sPaginationType": "full_numbers",
    "bProcessing": true,
    "sAjaxSource": "search/get_credits",
    "bServerSide": true,
    "oLanguage": {
      "sUrl": STATIC_URL + "main/js/libs/dataTables.spanish.txt"
    },
    "aoColumns": [
        { "sWidth": "25%" },
        { "sWidth": "25%" },
        { "sWidth": "15%" },
        { "sWidth": "15%" },
        { "sWidth": "15%" },
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
});