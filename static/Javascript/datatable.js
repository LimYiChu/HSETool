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

