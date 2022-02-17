$(document).ready(function() {
  // Setup - add a text input to each footer cell
  $('table.fixedtable').each(function () {
  var datatableid = '#' + $(this).attr('id');
  $(datatableid + ' thead tr').clone(true).appendTo(datatableid + ' thead'); //clone headers
  $(datatableid + ' thead tr:eq(1) th').each(function (i) {

  var title = $(this).text();
  $(this).html( '<input type="text" placeholder="Search" class="column_search" />' );
  } );
  // DataTable
  var table = $(datatableid).DataTable({
    orderCellsTop: true,
    "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
  });
// Apply the search
  $( datatableid +' thead'  ).on( 'keyup', ".column_search",function () {
      table
          .column( $(this).parent().index() )
          .search( this.value )
          .draw();

          
  } );
  
} );
})

function launchtable(that, event, tablepopup) {
  fadein(that);
  ajaxcall(event,tablepopup);
}

function fadein(that) {    
var $x = $($(that).closest('div .divclick'));
var $y = $($(that).closest('div .divclick').siblings('.popup'));  
$x.css("animaton", "mymoveout .5s ease");
$y.css("animation", "slide-in .5s ease");
$y.css("display", "block");

}

function ajaxcall(event, tablepopup) {
var data = event.currentTarget.firstElementChild.innerText  
var title = event.currentTarget.firstElementChild.innerText  
$('.caption').html(title);
  
$.ajax({   
  url: "/" + tablepopup,   
  type : 'GET',   
  data : {   
  "data": data   
  },   
  success: function (response){  
    dtable(response); donutchart(response); 
  }
})
}

function dtable(response) {
              
var dflist = response.dflist   
var nestedheader = response.nestedheader    
var dynamicheaders = []; 
for (var i=0; i < nestedheader.length; i++ ) { 
  dynamicheaders.push({ 
            "sTitle": nestedheader[i], 
    }); 
}; 

$('table.nestedtable').each(function () {
  var datatableid = '#' + $(this).attr('id');
  
  if ( $.fn.dataTable.isDataTable(datatableid) ) {
    $(datatableid).DataTable().destroy();
    $(datatableid).empty();
  }
  
  var table = $(datatableid).DataTable( {  
      data: dflist,      
                      
    "aoColumns": dynamicheaders, 
    "columnDefs": [  
      { "targets" : [0],  
          "mRender": function ( data,row,column) {  
            return '<a href="/pmtrepviewall'+ '/' + column[5]+'/view'+'">'+ data + '</a>';  
          }},  
    ],
    "bDestroy":true, 
    orderCellsTop: true,
    "lengthMenu": [[-1, 10, 25, 50, 200], ["All", 10, 25, 50, 200]],
    "createdRow": function( row, data, dataIndex,column ) {

      if ( data[6] == 'Red'){
        return $(column[4]).addClass( 'table-danger' )}

      else if ( data[6] == 'Yellow'){
        return $(column[4]).addClass( 'table-warning' )}

      else if ( data[6] == 'Green'){
        return $(column[4]).addClass( 'table-success' );
      
  
  }
  },
  });  
  
  $(datatableid + ' thead tr').clone(false).appendTo(datatableid + ' thead'); //clone headers
  $(datatableid + ' thead tr:eq(1) th').each(function (i) {
  $(this).html( '<input type="text" placeholder="Search" class="column_search" />' );
  $(this).removeClass( "sorting sorting_asc sorting_desc" )
  } ); 
  
  $( datatableid +' thead'  ).on( 'keyup', ".column_search",function () {
    table
        .column( $(this).parent().index() )
        .search( this.value )
        .draw(); 
  } );
});  
}

function donutchart(response) {
google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
  
    var donutclose = response.donutclose
    var donutopen = response.donutopen

    var data = google.visualization.arrayToDataTable([
      ['Status', 'Number'],
      donutclose,
      donutopen,
    ]);

    var options = {
      width: 500,
      height: 200,
      backgroundColor: '#f3f2f2',
      pieHole: 0.4,
      pieSliceText: 'value',
      tooltip: {text: 'value'},
      chartArea : { width:'100%',height:'90%', left: '50%'},
      legend : {position:'left'}
    };
    // var div = document.getElementsByClassName('donutchart');
    // var g = document.createElement('div');
    // g.id = 'chart1';
    // div.append(g);
    // var $div = $('.donutchart')
    
    // var $div = $('.donutchart').html('')
    // $("<div/>").attr('id','chart1').appendTo($div);

    // $('.donutchart').each(function () {
    //   var donutchart = '#' + $(this).attr('id');
    // var div = document.getElementById(donutchart)

    var chart = new google.visualization.PieChart(document.getElementById('chart1'));
    var chart2 = new google.visualization.PieChart(document.getElementById('chart2'));
    chart.draw(data, options);
    chart2.draw(data, options);
    // })
  }
}

function fadeout(that) {

  var $x = $($(that).closest('div .popup').siblings('.divclick'));
  var $y = $($(that).closest('div .popup'))
  $x.css("animaton", "mymovein 2.5s ease")
  $y.css("animation", "slide-out .5s ease");
  setTimeout(() => {
    $y.css("display", "none");
  }, 500);
}

$( document ).ready(function() {
  $( '.tablinks' ).each(function() {
    $(this).on("click", function(){   
    var $x = $('.divclick');
    var $y = $('.popup');
    if($y.css('display') !== 'none')
    { 
      $x.css("animaton", "mymovein 2.5s ease")
      $y.css("animation", "slide-out .5s ease");
      setTimeout(() => {
        $y.css("display", "none");
      }, 500);
    }
    });
  });
});
