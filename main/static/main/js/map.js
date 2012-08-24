// State IDS
var states = [
  'AGU','BCN','BCS','CAM','CHH',
  'CHP','COA','COL','DIF','DUR',
  'GRO','GUA','HID','JAL','MEX',
  'MIC','MOR','NAY','NLE','OAX',
  'PUE','QUE','ROO','SIN','SLP',
  'SON','TAB','TAM','TLA','VER',
  'YUC','ZAC'
];
// State Names
var state_names = [
  'Aguascalientes', 'Baja California Norte', 'Baja California Sur', 'Campeche',
  'Chihuahua','Chiapas','Coahuila','Colima','Distrito Federal','Durango','Guerrero',
  'Guanajuato','Hidalgo','Jalisco','Edo. Mexico','Michoacán','Morelos','Nayarit',
  'Nuevo León','Oaxaca','Puebla','Queretaro','Quintana Roo','Sinaloa','San Luis Potosí',
  'Sonora','Tabasco','Tamaulipas','Tlaxcala','Veracruz','Yucatán','Zacatecas'
];
$(function() {
  // Initialize table
  datatable = $('#deputies-datatable').dataTable({
    "sDom": "<'row'<'span6'l><'span6'f>r>t<'row'<'span6'i><'span6'p>>",
    "sPaginationType": "bootstrap",
    "bProcessing": true,
    "sAjaxSource": "map/get_deputies",
    "bServerSide": true,
    "oLanguage": {
      "sUrl": STATIC_URL + "main/js/libs/dataTables.spanish.txt"
    },
    "aoColumns": [
        { "sWidth": "60%" },
        { "sWidth": "15%" },
        { "sWidth": "10%" },
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
  // Activate map highlight funcionality
  $('#map').maphilight();
  // When user is over an state
  $('.area').hover(function() {
    // Obtain name of state dependind his id and put it in the info div
    var id= $(this).attr('id');
    var state = $.inArray(id,states);
    $('#info').html(state_names[state]);
    datatable.fnFilter(state_names[state]);
    // Show table results
    $('#deputies-table').show();
  }, function(){
      $('#info').html('');
  });
});