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
    pageLength: 100,
    "lengthMenu": [[10, 25, 50, 100, 200, -1], [10, 25, 50, 100, 200, "All"]],
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

