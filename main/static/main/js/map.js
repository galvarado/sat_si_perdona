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
  $('.area').click(function() {
    // Obtain name of state dependind his id and put it in the info div
    var id= $(this).attr('id');
    var state = $.inArray(id,states);
    $('#info').html(state_names[state]);
    $.ajax({
      url: "/get_graph_by_state",
      type: 'post',
      dataType: 'json',
      data: {
        state:state_names[state],
      },
      success: function(data) {
        $("#graph-tabs").tabs().show();
        if (data.response) {
            var pie = new RGraph.Pie('cvs1', [data.total_moral,data.total_physic]);
            pie.Set('chart.origin', 0);
            pie.Set('chart.tooltips', [data.total_moral,data.total_physic]);
            pie.Set('chart.labels', ['Fisicas','Morales']);
            pie.Set('chart.shadow', true);            
            pie.Set('chart.background.piecolor1', 'white');
            pie.Set('chart.background.piecolor2', 'white');
            pie.Set('chart.background.grid', true);
            pie.Set('chart.colors', ['orange', 'white']);
            pie.Set('chart.text.color', 'white');
            pie.Set('chart.variant', '3d');
            pie.Draw();
            var bar = new RGraph.Bar('cvs2', [5,4,1,6,8,5,3]);
            bar.Set('chart.labels', ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']);
            bar.Draw();
            bar.Set('chart.background.barcolor1', 'white');
            bar.Set('chart.background.barcolor2', 'white');
            bar.Set('chart.background.grid', true);
            bar.Set('chart.colors', ['orange', 'white']);
            bar.Set('chart.text.color', 'white');
            bar.Set('chart.variant', '3d');
            bar.Draw();
            var hbar = new RGraph.HBar('cvs3', [5,8,6,4,3,2,1,6,8]);
            hbar.Set('chart.labels', ['Venus','Felicity','Cynthia','Frederick','Hoolio','Peter','Jennifer','Richard','Joathan']);
            hbar.Draw();
        }
      }
    });
  });
});